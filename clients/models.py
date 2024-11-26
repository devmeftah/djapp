from django.db import models
from monitors.models import MonitorProfile
from django.db.models import Count,Sum
from django.utils.timezone import now

# Create your models here.
    
class ClientProfile(models.Model):
    class Meta:
        verbose_name_plural = "قائمة الزبناء"
    monitor = models.ForeignKey(MonitorProfile, verbose_name=("المدرب"), on_delete=models.DO_NOTHING)
    fnameAR = models.CharField(max_length=15,verbose_name="الإسم الشخصي")
    lnameAR = models.CharField(max_length=15,verbose_name="الإسم العائلي")
    fnameLA = models.CharField(max_length=15,verbose_name="First name")
    lnameLA = models.CharField(max_length=15,verbose_name="Last name")
    cnie = models.CharField(unique=True, max_length=15,verbose_name="رقم بطاقة التعريف الوطنية")
    phone = models.CharField(max_length=14,verbose_name="رقم الهاتف") 
    ncreation = models.CharField(max_length=100,verbose_name="رقم التسجيل")
    addressAR = models.CharField(max_length=255,verbose_name="العنوان")

    photo_clt = models.ImageField(blank=True, null=True,upload_to='photos/clients/%Y/%m/%d/',verbose_name="الصورة الشخصية" )
    GENDER_CHOICES = ( 
        (1, "ذكر"), 
        (2, "أنثى"), 
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES,verbose_name="الجنس", default=1)
    CATY_CHOICES = ( 
        (1, "A"), 
        (2, "A1"), 
        (3, "B"),  
    ) 
    category = models.PositiveSmallIntegerField(choices=CATY_CHOICES ,verbose_name="الصنف", default=3)
    
    nationality = models.CharField(default="MAROCAINE", max_length=15,verbose_name="الجنسية")
    nclient = models.CharField(max_length=10,verbose_name="رقم الزبون",null=True,blank=True)
    date_joined = models.DateField(verbose_name="تاريخ التسجيل", auto_now_add=True )
    is_payed = models.BooleanField(verbose_name="خالص",default=False)
    price = models.PositiveIntegerField(verbose_name="الثمن الإجمالي",default=3000)
    placeofbirthAR = models.CharField(verbose_name='مكان الإزدياد',max_length=50)
    dateofbirth = models.DateField(verbose_name='تاريح الإزدياد')
    def get_finance(self):
        return self.finance_set.all()
    def get_controle(self):
        return self.controle_set.all()
    @property
    def totalpaid(self):
        total=0
        for i in self.get_finance():
            total += i.paid
        return total
    @property
    def rest(self):
        rest = self.price - self.totalpaid
        return rest
    @property
    def totalgender(self):
        return ClientProfile.objects.values('gender').annotate(Count('gender'))

    def save(self, *args, **kwargs):
        if not self.photo_clt:
            if self.gender == 1:
                self.photo_clt = '/photos/random/m.svg'
            else:
                self.photo_clt = '/photos/random/f.svg'
        clients = ClientProfile.objects
        usercreation = clients.all() \
            .extra({'created': "strftime('%Y',date_joined)"}) \
            .values('created').order_by('-created')
        if usercreation.exists():
            #lastId = clients.latest('id').id # auto increment max count of client
            lastId = int(clients.latest('id').nclient.split("/")[1])
        else:
            lastId = 0
        if lastId > 1:
            if 'created' in usercreation[0]:
                date_joined = usercreation[0]['created']
                usermaxcount = lastId+1
                self.nclient = f'{date_joined}/{usermaxcount}'
                self.ncreation =f'1114-{self.cnie}-{usermaxcount}'
        else: 
            lastId = lastId+1
            self.nclient = f'{now().year}/{lastId}'
            self.ncreation =f'1114-{self.cnie}-{lastId}'
        return super(ClientProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.fnameAR +' '+ self.lnameAR

class Finance(models.Model):
    class Meta:
        verbose_name_plural = "قائمة الموارد المالية"
    client = models.ForeignKey(ClientProfile, verbose_name="المالية", on_delete=models.CASCADE)
    paid = models.PositiveIntegerField(verbose_name="قيمة الدفعة",default=0)
    payement_date = models.DateField(verbose_name="تاريخ الدفعة", auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.client.fnameAR} {self.client.lnameAR} | {self.paid} درهم | {self.payement_date}'
    @property
    def sumpaidprefer(self):
        return Finance.objects.values('paid').annotate(Count('paid'))
    @property
    def sumpaidclient(self):
        return Finance.objects.values('client').annotate(Sum('paid'))
    @property
    def countpaidclient(self):
        return Finance.objects.values('client').annotate(Count('paid'))
    
class Controle(models.Model):
    class Meta:
        verbose_name_plural = "قائمة تدبير مصالح الزبون"
    client = models.ForeignKey(ClientProfile, verbose_name="الزبون", on_delete=models.CASCADE)
 
    theoretic = models.PositiveIntegerField(default=0,verbose_name="التعليم النظري")
    practical = models.PositiveIntegerField(default=0,verbose_name="التعليم التطبيقي")
    exam_t1_date = models.DateField(null=True, blank=True, verbose_name="تاريخ إمتحان النظري الأول")
    exam_p1_date = models.DateField(null=True, blank=True,verbose_name="تاريخ إمتحان التطبيقي الأول")
    exam_t2_date = models.DateField(null=True, blank=True,verbose_name="تاريخ إمتحان النظري التاني")
    exam_p2_date = models.DateField(null=True, blank=True,verbose_name="تاريخ إمتحان التطبيقي التاني")
    RESULT_CHOICES = ( 
        (0, "ليس بعد"),
        (1, "ناجح"),
        (2, "راسب"), 
    )
    result = models.PositiveIntegerField(choices=RESULT_CHOICES,verbose_name="النتيجة النهائية", default=0)
    result_date = models.DateField(null=True,blank=True,verbose_name="تاريخ النتيجة النهائية")
    def __str__(self):
        return f'{self.client.fnameAR} {self.client.lnameAR} | النتيجة : {self.get_result_display()}'