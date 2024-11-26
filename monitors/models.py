from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Vehicule(models.Model):
    class Meta:
        verbose_name_plural = "قائمة العربات"
    vehicule_registration= models.CharField(verbose_name="رقم التعريفي للعربة", max_length=20,null=True,unique=True)
    vehicule_name= models.CharField(verbose_name="إسم العربة", max_length=20)
    expired_date = models.DateField(null=True,blank=True,verbose_name="تاريخ إنتهاء العمل")
    vehicule_photo = models.ImageField(upload_to='photos/vehicules/%Y/%m/%d/',verbose_name="الصورة العربة" ,blank=True, null=True)
    def __str__(self):
        return self.vehicule_name
     
class MonitorProfile(models.Model): 
    class Meta:
        verbose_name_plural = "قائمة المدربون"
    #user = models.OneToOneField(User, verbose_name="المدرب", on_delete=models.CASCADE)

    vehicule = models.ForeignKey(Vehicule,verbose_name="العربة",on_delete=models.DO_NOTHING)
 
    monitor_authorization_number =models.CharField(unique=True, verbose_name="الرقم الوطني للمدرب", max_length=8)
    fnameAR = models.CharField(max_length=15,verbose_name="الإسم الشخصي")
    lnameAR = models.CharField(max_length=15,verbose_name="الإسم العائلي")
    fnameLA = models.CharField(max_length=15,verbose_name="First name")
    lnameLA = models.CharField(max_length=15,verbose_name="Last name")
    phone = models.CharField(max_length=14,verbose_name="رقم الهاتف") 
    cnie = models.CharField(unique=True, max_length=15,verbose_name="رقم بطاقة التعريف الوطنية")

    photo_mnt = models.ImageField(blank=True, null=True,upload_to='photos/monitors/%Y/%m/%d/',verbose_name="الصورة الشخصية" )
    GENDER_CHOICES = ( 
        (1, "ذكر"), 
        (2, "أنثى"), 
    ) 
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES,verbose_name="الجنس", default=1,serialize=True)
    CATY_CHOICES = ( 
        (1, "A"), 
        (2, "A1"), 
        (3, "B"), 
    ) 
    category = models.PositiveSmallIntegerField(choices=CATY_CHOICES ,verbose_name="الصنف", default=3,serialize=True)
    nationality = models.CharField(default="MAROCAINE", max_length=15,verbose_name="الجنسية")
    joined_date = models.DateField(verbose_name="تاريخ التسجيل",auto_now_add=True,editable=True)

    def __str__(self):
        return f'{self.fnameAR} {self.lnameAR}'
    

    def get_clients(self):
        return self.clientprofile_set.all()
    @property
    def tmalepermnt(self):
        male = 0
        for i in self.get_clients():
            if i.gender == 1:
                male += 1
        return male
    @property
    def tfemalepermnt(self):
        female = 0
        for i in self.get_clients():
            if i.gender == 2:
                female += 1
        return female

    def save(self, *args, **kwargs):
        if not self.photo_mnt:
            if self.gender == 1:
                self.photo_mnt = '/photos/random/m.svg'
            else:
                self.photo_mnt = '/photos/random/f.svg'
        return super(MonitorProfile, self).save(*args, **kwargs) 
 
class Societe(models.Model):
    class Meta:
        verbose_name_plural = "قائمة خاصة بالمؤسسة"
    societe_name = models.CharField(max_length=30 ,verbose_name="إسم المؤسسة")
    ceo_fname = models.CharField(max_length=20 ,verbose_name="إسم الشخصي للمدير")
    ceo_lname = models.CharField(max_length=20 ,verbose_name="إسم اعائلي للمدير")
    ceo_cnie = models.CharField( max_length=10,verbose_name="رقم ب.ت.و")
    ceo_mail = models.CharField( max_length=30,verbose_name="البريد الإلكتروني")
    city = models.CharField(max_length=15,verbose_name="مقر المؤسسة")
    address = models.CharField(max_length=40,verbose_name="عنوان المؤسسة")
    fix = models.CharField(max_length=10, verbose_name="رقم الهاتف الثابت")
    phone = models.CharField(max_length=10,verbose_name="رقم الهاتف")
    license_number = models.SmallIntegerField(verbose_name="رقم الرخصة")
    reg_num_in_cms = models.SmallIntegerField(verbose_name="رقم القيد في السجل التجاري")
    reg_num_pro_tax = models.SmallIntegerField(verbose_name="رقم القيد في سجل الضريبة المهنية ")
    def __str__(self):
        return f'إسم المؤسسة : {self.societe_name} رقم الرخصة {self.license_number}'