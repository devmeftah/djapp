from django import forms
from .models import Controle

class Eduform(forms.ModelForm):
    theoretic = forms.IntegerField(label="التعليم النظري", widget=forms.NumberInput(attrs={'class':'text-center'}))
    practical = forms.IntegerField(label="التعليم التطبيقي", widget=forms.NumberInput(attrs={'class':'text-center'}))

    class Meta:
        model = Controle
        fields = (
            'theoretic',
            'practical',
        )
        labels = {
            'theoretic' :'التعليم النظري',
            'practical' :'التعليم التطبيقي',
        }
class MedForm(forms.ModelForm):
    doctor_date = forms.DateField(label="تاريخ الفحص", widget=forms.DateInput(attrs={'type':'date','class':'text-center'}))
    doctor_name = forms.CharField(label="إسم الطبيب", widget=forms.TextInput(attrs={'class':'text-center'}))

    class Meta:
        model = Controle
        fields = (
            'doctor_name',
            'doctor_date',
        )
        labels = {
            'doctor_date' :'إسم الطبيب',
        }
class TvaForm(forms.ModelForm):
    TVA_date = forms.DateField(label="تاريخ آداء الضريبة", widget=forms.DateInput(attrs={'type':'date','class':'text-center'}))
    TVA_price = forms.IntegerField(label="ثمن الضريبة TVA", widget=forms.NumberInput(attrs={'class':'text-center'}))
    class Meta:
        model = Controle
        fields = (
            'TVA_price',
            'TVA_date',
        )
        labels = {
            'TVA_price' :'ثمن الضريبة TVA',
        }
class CtlForm(forms.ModelForm):
    exam_t1_date = forms.DateField(label="تاريخ إمتحان النظري الأول", widget=forms.DateInput(attrs={'type':'date','class':'text-center'}))
    exam_p1_date = forms.DateField(label="تاريخ إمتحان التطبيقي الأول", widget=forms.DateInput(attrs={'type':'date','class':'text-center'}))
    result_date = forms.DateField(label="تاريخ إعلان النتيجة", widget=forms.DateInput(attrs={'type':'date','class':'text-center'}))
    class Meta:
        model = Controle
        fields = (
            'exam_t1_date',
            'exam_p1_date',
            'result',
            'result_date',
        )
        labels = {
            'result' :'النتيجة النهائية',
        }
