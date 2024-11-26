from django.contrib import admin

from .models import MonitorProfile, Societe, Vehicule
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin
# Register your models here.

class MonitorProfileResource(resources.ModelResource):
    monitor_name =  Field(attribute='fnameAR', column_name='المدرب')
    cnie =  Field(attribute='cnie', column_name='بطاقة التعريف الوطنية')
    category =  Field(attribute='category', column_name='الصنف')
    addressAR = Field(attribute='addressAR', column_name='العنوان')
    class Meta:
        model = MonitorProfile
        fields = ('monitor_name','category','cnie', 'addressAR')
        export_order = ('monitor_name', 'cnie', 'addressAR', 'category')
    def dehydrate_monitor_name(self,obj):
        return f'{obj.fnameAR} obj.lnameAR'

    def dehydrate_category(self,obj):
        if obj.category == 1:
            return "A"
        elif obj.category == 2:
            return "A1"
        else :
            return "B"


class MonitorProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class = MonitorProfileResource
    list_filter = [
        "joined_date",
        "monitor_authorization_number",
        "gender",
        "cnie",

    ]
    search_fields = (
        "monitor_authorization_number",
        "cnie",
    )

class SocieteResource(resources.ModelResource):
    societe_name =  Field(attribute='societe_name', column_name="إسم المؤسسة")
    ceo_name =  Field(attribute='ceo_name', column_name="إسم المدير")
    ceo_cnie =  Field(attribute='ceo_cnie', column_name="رقم ب.ت.و")
    license_number =  Field(attribute='license_number', column_name="رقم الرخصة")
    phone = Field(attribute='phone', column_name="رقم الهاتف")
    
    class Meta:
        model = Societe
        fields = ('societe_name','ceo_name','ceo_cnie','license_number', 'phone')
        export_order = ('societe_name', 'ceo_name','ceo_cnie', 'license_number', 'phone')

class SocieteAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class = SocieteResource

admin.site.register(Vehicule)
admin.site.register(MonitorProfile,MonitorProfileAdmin)
admin.site.register(Societe,SocieteAdmin)

