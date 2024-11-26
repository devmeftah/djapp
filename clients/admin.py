from django.contrib import admin
from .models import ClientProfile, Finance,Controle
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin
from django.contrib import admin

# Register your models here.

class ClientProfileResource(resources.ModelResource):
    user =  Field(attribute='user', column_name='المرشح')
    cnie =  Field(attribute='cnie', column_name='رقم ب.ت.و')
    addressAR = Field(attribute='addressAR', column_name='العنوان الشخصي')
    nclient = Field(attribute='nclient', column_name='الرقم الترتيبي')
    phone =  Field(attribute='phone', column_name='رقم الهاتف')
    gender =  Field(attribute='get_gender_display', column_name='جنس المرشح')
    class Meta:
        model = ClientProfile
        fields = ('user','nclient','cnie','gender', 'addressAR','phone')
        export_order = ('user','nclient', 'cnie','gender', 'addressAR', 'phone')
    def dehydrate_user(self,obj):
        return "{0} {1}".format(obj.fnameAR,obj.lnameAR)

class ClientProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class = ClientProfileResource

    list_filter = [
         "date_joined",
         "monitor",
         "gender"
    ]
    search_fields = (
        "cnie",
        "lnameLA",
    )

class FinanceAdmin(admin.ModelAdmin):
    list_filter = [
        "payement_date",
        "client",
        "client__date_joined",

    ]
    search_fields = (
        "paid",
        "client__lnameLA",
    )

class ControleResource(resources.ModelResource):
    client =  Field(attribute='client', column_name='المرشح')
    cnie =  Field(attribute='client', column_name='رقم ب.ت.و')
    result = Field(attribute='get_result_display', column_name='النتيجة النهائية')
    theoretic = Field(attribute='theoretic', column_name='الحصص النظرية')
    practical =  Field(attribute='practical', column_name='الحصص التطبيقية')
    class Meta:
        model = Controle
        fields = ('client','cnie','theoretic', 'practical','result')
        export_order = ('client','cnie', 'theoretic', 'practical', 'result')
    def dehydrate_client(self,obj):
        return "{0} {1}".format(obj.client.fnameAR,obj.client.lnameAR)
    def dehydrate_cnie(self,obj):
        return obj.client.cnie

class ControleAdmin(ExportActionMixin,admin.ModelAdmin):
    resource_class = ControleResource
    list_filter = [
        "client",
        "result",
        "result_date",
        "result_date",
        "client__date_joined",
    ]
    search_fields = (
        "result",
        "client__lnameLA",
    )

admin.site.register(ClientProfile,ClientProfileAdmin)
admin.site.register(Finance,FinanceAdmin) 
admin.site.register(Controle,ControleAdmin) 

