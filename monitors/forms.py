from django import forms
from .models import Vehicule,Societe

class CarForm(forms.ModelForm):
    expired_date = forms.DateField(label="تاريخ إنتهاء العمل", required=False,widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Vehicule
        fields = (
            'vehicule_name',
            'vehicule_registration',
            'expired_date',
            'vehicule_photo',
        )
        labels = {
            'vehicule_name' :'إسم العربة',
            'vehicule_registration' :'رقم التعريفي للعربة',
            'vehicule_photo' :'صورة العربة'
        }




class SteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = (
            'societe_name',
            'ceo_fname',
            'ceo_lname',
            'ceo_cnie',
            'ceo_mail',
            'city',
            'address',
            'fix',
            'phone',
            'license_number',
            'reg_num_in_cms',
            'reg_num_pro_tax',
        )
        labels = {
            'societe_name' :"إسم المؤسسة",
            'ceo_fname':  "إسم الشخصي للمدير"  ,
            'ceo_lname':  "إسم العائلي للمدير"  ,
            'ceo_cnie':   "رقم ب.ت.و"  ,
            'ceo_mail':  "البريد الإلكتروني"   ,
            'city':  "مقر المؤسسة"   ,
            'address':  "عنوان المؤسسة",
            'fix':  "رقم الهاتف الثابت",
            'phone':   "رقم الهاتف" ,
            'license_number':  "رقم الرخصة" ,
            'reg_num_in_cms':  "رقم القيد في السجل التجاري" ,
            'reg_num_pro_tax':  "رقم القيد في سجل الضريبة المهنية",
        }
