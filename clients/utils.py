import sys
import django
import pandas as pd

if sys.version_info >= (3, ):
    from django.utils.encoding import force_str as force_text
else:
    from django.utils.encoding import force_text
from django.db.models import Field
from django.core.cache import cache


FieldDoesNotExist = (
    django.db.models.fields.FieldDoesNotExist
    if django.VERSION < (1, 8)
    else django.core.exceptions.FieldDoesNotExist
)

def to_fields(qs, fieldnames):
    for fieldname in fieldnames:
        model = qs.model
        for fieldname_part in fieldname.split('__'):
            try:
                field = model._meta.get_field(fieldname_part)
            except FieldDoesNotExist:
                try:
                    rels = model._meta.get_all_related_objects_with_model()
                except AttributeError:
                    field = fieldname
                else:
                    for relobj, _ in rels:
                        if relobj.get_accessor_name() == fieldname_part:
                            field = relobj.field
                            model = field.model
                            break
            else:
                model = get_related_model(field)
        yield field



def queryset_to_dataframe(qs, fieldnames=(), index_col=None, coerce_float=False,
               verbose=True, datetime_index=False, column_names=None):
    if fieldnames:
        fieldnames = pd.unique(fieldnames)
        if index_col is not None and index_col not in fieldnames:
            # Add it to the field names if not already there
            fieldnames = tuple(fieldnames) + (index_col,)
            if column_names:
                column_names = tuple(column_names) + (index_col,)
        fields = to_fields(qs, fieldnames)

    elif is_values_queryset(qs):
        if django.VERSION < (1, 9):  # pragma: no cover
            annotation_field_names = list(qs.query.annotation_select)

            if annotation_field_names is None:
                annotation_field_names = []

            extra_field_names = qs.extra_names
            if extra_field_names is None:
                extra_field_names = []

            select_field_names = qs.field_names

        else:  # pragma: no cover
            annotation_field_names = list(qs.query.annotation_select)
            extra_field_names = list(qs.query.extra_select)
            select_field_names = list(qs.query.values_select)

        fieldnames = select_field_names + annotation_field_names + \
            extra_field_names
        fields = [None if '__' in f else qs.model._meta.get_field(f)
                  for f in select_field_names] + \
            [None] * (len(annotation_field_names) + len(extra_field_names))

        uniq_fields = set()
        fieldnames, fields = zip(
            *(f for f in zip(fieldnames, fields)
              if f[0] not in uniq_fields and not uniq_fields.add(f[0])))
    else:
        fields = qs.model._meta.fields
        fieldnames = [f.name for f in fields]
        fieldnames += list(qs.query.annotation_select.keys())

    if is_values_queryset(qs):
        recs = list(qs)
    else:
        recs = list(qs.values_list(*fieldnames))

    df = pd.DataFrame.from_records(
        recs,
        columns=column_names if column_names else fieldnames,
        coerce_float=coerce_float
    )

    if verbose:
        update_with_verbose(df, fieldnames, fields)

    if index_col is not None:
        df.set_index(index_col, inplace=True)

    if datetime_index:
        df.index = pd.to_datetime(df.index, errors="ignore")
    return df


def is_values_queryset(qs):
    if django.VERSION < (1, 9):  # pragma: no cover
        return isinstance(qs, django.db.models.query.ValuesQuerySet)
    else:
        return qs._iterable_class == django.db.models.query.ValuesIterable

def update_with_verbose(df, fieldnames, fields):
    for fieldname, function in build_update_functions(fieldnames, fields):
        if function is not None:
            df[fieldname] = function(df[fieldname])

def get_model_name(model):
    """
    Returns the name of the model
    """
    return model._meta.model_name

def get_base_cache_key(model):
    return 'pandas_%s_%s_%%s_rendering' % (
        model._meta.app_label, get_model_name(model))
def replace_from_choices(choices):
    def inner(values):
        return [choices.get(v, v) for v in values]
    return inner

def replace_pk(model):
    base_cache_key = get_base_cache_key(model)

    def get_cache_key_from_pk(pk):
        return None if pk is None else base_cache_key % str(pk)

    def inner(pk_series):
        pk_series = pk_series.astype(object).where(pk_series.notnull(), None)
        # cache_keys = pk_series.apply(
        #     get_cache_key_from_pk,   convert_dtype=False)
        
        cache_keys = pk_series.astype(object).apply(get_cache_key_from_pk)

        unique_cache_keys = list(filter(None, cache_keys.unique()))

        if not unique_cache_keys:
            return pk_series

        out_dict = cache.get_many(unique_cache_keys)

        if len(out_dict) < len(unique_cache_keys):
            out_dict = dict([(base_cache_key % obj.pk, force_text(obj))
                            for obj in model.objects.filter(
                            pk__in=list(filter(None, pk_series.unique())))])
            cache.set_many(out_dict)

        return list(map(out_dict.get, cache_keys))

    return inner


def get_related_model(field):
    """Gets the related model from a related field"""
    model = None

    if hasattr(field, 'related_model') and field.related_model:   #  pragma: no cover
        model = field.related_model
    # Django<1.8 doesn't have the related_model API, so we need to use rel,
    # which was removed in Django 2.0
    elif hasattr(field, 'rel') and field.rel:  # pragma: no cover
        model = field.rel.to

    return model

def build_update_functions(fieldnames, fields):
    for fieldname, field in zip(fieldnames, fields):
        if not isinstance(field, Field):
            yield fieldname, None
        else:
            if field and field.choices:
                choices = dict([(k, force_text(v))
                                for k, v in field.flatchoices])
                yield fieldname, replace_from_choices(choices)

            elif field and field.get_internal_type() == 'ForeignKey':
                yield fieldname, replace_pk(get_related_model(field))
