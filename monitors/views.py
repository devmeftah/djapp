from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import CarForm,SteForm
import re
#from .forms import MonitorForm,UserForm
from monitors.models import MonitorProfile, Vehicule,Societe
from django.utils.timezone import now
# Create your views here.
 
def addsociete(request):
    if request.user is not None and request.user.id != None:
        if Societe.objects.all().count() > 0:
            return redirect('monitors')
        if request.method == 'POST'and 'savesociete' in request.POST:
            societe_name=None
            ceo_fname=None
            ceo_lname=None
            ceo_cnie=None
            ceo_mail=None
            city=None
            address=None
            fix=None 
            phone=None
            license_number=None
            reg_num_in_cms=None
            reg_num_pro_tax=None

            if 'societe_name' in request.POST: societe_name = request.POST['societe_name']
            if 'ceo_fname' in request.POST: ceo_fname = request.POST['ceo_fname']
            if 'ceo_lname' in request.POST: ceo_lname = request.POST['ceo_lname']
            if 'ceo_cnie' in request.POST: ceo_cnie = request.POST['ceo_cnie']
            if 'ceo_mail' in request.POST: ceo_mail = request.POST['ceo_mail']
            if 'city' in request.POST: city = request.POST['city']
            if 'address' in request.POST: address = request.POST['address']
            if 'fix' in request.POST: fix = request.POST['fix']
            if 'phone' in request.POST: phone = request.POST['phone']
            if 'license_number' in request.POST: license_number = request.POST['license_number']
            if 'reg_num_in_cms' in request.POST: reg_num_in_cms = request.POST['reg_num_in_cms']
            if 'reg_num_pro_tax' in request.POST: reg_num_pro_tax = request.POST['reg_num_pro_tax']


            if societe_name and ceo_fname and ceo_lname and ceo_cnie and ceo_mail and city and\
                address and fix and phone and license_number and reg_num_in_cms and reg_num_pro_tax:
                if not Societe.objects.filter(license_number=license_number).exists():
                    societe = Societe(
                        societe_name    =  societe_name ,
                        ceo_fname   =  ceo_fname ,
                        ceo_lname   =  ceo_lname ,
                        ceo_cnie    =  ceo_cnie ,
                        ceo_mail    =   ceo_mail,
                        city    =  city ,
                        address =  address ,
                        fix =  fix ,
                        phone   =  phone ,
                        license_number  = license_number  ,
                        reg_num_in_cms  =   reg_num_in_cms,
                        reg_num_pro_tax =  reg_num_pro_tax ,
                    )
                    societe.save()
                    messages.success(request, 'لقد تم تسجيل المؤسسة بنجاح')
                    return redirect('addcar')
            return redirect('addcar')
        
        else :
            steform = SteForm()
            context = {
                'steform':steform,
            }
            return render(request,'monitors/societe.html', context)
    else:
        return redirect('signin')


def addcar(request):
    if request.user is not None and request.user.id != None:
        if Societe.objects.all().count() <= 0:
            return redirect('addsociete')
        if request.method == 'POST'and 'savecar' in request.POST:
            vehicule_registration=None
            vehicule_name=None
            expired_date=None
            vehicule_photo=None
            if 'vehicule_registration' in request.POST: vehicule_registration = request.POST['vehicule_registration']
            else : messages.error(request, 'Error request vehicule_registration')
            if 'vehicule_name' in request.POST: vehicule_name = request.POST['vehicule_name']
            else : messages.error(request, 'Error request vehicule_name')
            
            if 'expired_date' in request.POST: 
                expired_date = request.POST['expired_date']
                if not expired_date:
                    expired_date = None
            else : expired_date = None

            if 'vehicule_photo' in request.POST and 'vehicule_photo' in request.FILES:
                vehicule_photo = request.FILES['vehicule_photo']
            else : vehicule_photo = None

            if vehicule_registration and  vehicule_name:
                if not Vehicule.objects.filter(vehicule_registration=vehicule_registration).exists():
                    vehicule = Vehicule(
                        vehicule_registration=vehicule_registration,
                        vehicule_name=vehicule_name,
                        expired_date=expired_date,
                        vehicule_photo=vehicule_photo,
                    )
                    vehicule.save()

                    messages.success(request, 'لقد تم تسجيل العربة بنجاح')
                    return render(request,'monitors/addcar.html', {'is_added':True})
                else:
                    messages.error(request, 'الرقم التعريفي للعربة سبق إستخدامه')
            return redirect('addcar')
        
        else :
            carform = CarForm()
            context = {
                'carform':carform,
            }
            return render(request,'monitors/addcar.html', context)
    else:
        return redirect('signin')


def updatemonitor(request,mnt_id):
    if request.user is not None and request.user.id != None:
        monitorprofile = MonitorProfile.objects.filter(pk=mnt_id)
        if monitorprofile.exists():
            if request.method == 'POST' and 'btnedit' in request.POST :

                gender = int(request.POST['gender'])
                if request.POST['cnie'] and request.POST['vehicule'] and request.POST['fnameLA'] and request.POST['lnameLA'] and request.POST['fnameAR'] \
                    and request.POST['lnameAR'] and gender and request.POST['monitor_authorization_number']  and request.POST['category']  and request.POST['phone']:
                    monitorprofile = MonitorProfile.objects.get(pk=mnt_id)

                    arabic = '^[ء-ي0-9]+$'
                    if not re.match(arabic,request.POST['lnameLA']):fnameAR=None
                    if not re.match(arabic,request.POST['lnameLA']):lnameAR=None
                    monitorprofile.cnie = request.POST['cnie']
                    monitorprofile.vehicule_id = request.POST['vehicule']
                    monitorprofile.monitor_authorization_number = request.POST['monitor_authorization_number']
                    monitorprofile.fnameLA = request.POST['fnameLA']
                    monitorprofile.lnameLA = request.POST['lnameLA']
                    monitorprofile.fnameAR = request.POST['fnameAR']
                    monitorprofile.lnameAR = request.POST['lnameAR']
                    if 'photo_mnt' in request.FILES:
                        photo_mnt = request.FILES['photo_mnt']
                        monitorprofile.photo_mnt = photo_mnt
                    monitorprofile.gender = gender
                    monitorprofile.nationality = request.POST['nationality']
                    monitorprofile.category = request.POST['category']
                    monitorprofile.phone = request.POST['phone']
                    monitorprofile.save()

                    messages.success(request,'لقد تم تعديل البيانات بنجاح.')
                    auth.login(request,request.user)
                else: 
                    messages.error(request, 'Check your values and elements!')
                    return redirect("updatemonitor",str(mnt_id))
                return redirect("updatemonitor",str(mnt_id))
            elif request.method == 'GET': 
                context = None
                vehicules = Vehicule.objects.all()

                if vehicules.exists():
                    monitorprofile = MonitorProfile.objects.get(pk=mnt_id)                   
                    context= {
                        'vehicules' :vehicules,
                        'vehicule':monitorprofile.vehicule_id,
                        'monitor_authorization_number':monitorprofile.monitor_authorization_number,
                        'fnameLA':monitorprofile.fnameLA,
                        'lnameLA':monitorprofile.lnameLA,
                        'fnameAR':monitorprofile.fnameAR,
                        'lnameAR':monitorprofile.lnameAR,
                        'phone':monitorprofile.phone,
                        'cnie':monitorprofile.cnie,
                        'gender' :monitorprofile.gender,
                        'nationality' :monitorprofile.nationality,
                        'category' :monitorprofile.category,
                        'is_editpage':True
                    }


                    return render(request, 'monitors/addmonitor.html', context)

            else: 
                return redirect('addmonitor')
            
            #return render(request, 'accounts/profile.html')
        else:
            context={
                'monitor':get_object_or_404(MonitorProfile,pk=mnt_id),
                'is_editpage':True

            }
            return render(request,'monitors/addmonitor.html',context)
    else:
        return redirect('signin')
    

def addmonitor(request):
    if request.user is not None and request.user.id != None:
        vehicules = Vehicule.objects.all()
        if vehicules.exists():
            if request.method == 'POST'and 'btnsave' in request.POST:
                #variable
                cnie=None
                fnameLA =None
                lnameLA =None
                vehicule =None
                is_added =None
                fnameAR =None
                lnameAR =None

                phone =None
                cnie =None
                gender =None
                nationality =None
                category =None
                monitor_authorization_number =None
                photo_mnt=None

                if 'vehicule' in request.POST: vehicule = request.POST['vehicule']
                else : messages.error(request, 'Error in vehicule')

                if 'cnie' in request.POST: cnie = request.POST['cnie']
                else : messages.error(request, 'Error in cnie')

                if 'fnameLA' in request.POST: fnameLA = request.POST['fnameLA']
                else : messages.error(request, 'Error in first name')

                if 'lnameLA' in request.POST: lnameLA = request.POST['lnameLA']
                else : messages.error(request, 'Error in last name')
                
                if 'fnameAR' in request.POST: fnameAR = request.POST['fnameAR']
                else : messages.error(request, 'Error in phone')   

                if 'lnameAR' in request.POST: lnameAR = request.POST['lnameAR']
                else : messages.error(request, 'Error in lnameAR')   

                if 'monitor_authorization_number' in request.POST: monitor_authorization_number = request.POST['monitor_authorization_number']
                else : messages.error(request, 'Error in email monitor_authorization_number')

                if 'phone' in request.POST: phone = request.POST['phone']
                else : messages.error(request, 'Error in phone')
                                
                if 'gender' in request.POST: 
                    gender = request.POST['gender']
                    gender = int(gender)
                else : messages.error(request, 'Error in gender')

                if 'nationality' in request.POST:
                    nationality = request.POST['nationality']
                    if not nationality:
                        nationality = 'MAROCAINE'
                else : nationality = 'MAROCAINE'

                if 'category' in request.POST: category = request.POST['category']
                
                if 'photo_mnt' in request.FILES: 
                    photo_mnt = request.FILES['photo_mnt']
                    if not photo_mnt:
                        if gender == 2:
                            photo_mnt = '/photos/random/f.svg'
                        else :                  
                            photo_mnt = '/photos/random/m.svg'

                arabic = '^[ء-ي0-9\،\.\s]+$'
                if not re.match(arabic,fnameAR):fnameAR=None
                if not re.match(arabic,lnameAR):lnameAR=None
                if fnameLA and  lnameLA and fnameAR and lnameAR and vehicule and phone and gender and phone and cnie\
                         and monitor_authorization_number:
                    # username is taken?
                    if MonitorProfile.objects.filter(cnie=cnie).exists():
                        messages.error(request,'لقد ثم تسجيل هذا المدرب من قبل')
                    else:
                        # Email is taken?
                        if MonitorProfile.objects.filter(monitor_authorization_number=monitor_authorization_number).exists():
                            messages.error(request,'رقم المدرب سبق إستعماله')
                        else:
                            monitorprofile = MonitorProfile(
                                #user = user,
                                photo_mnt=photo_mnt,
                                monitor_authorization_number=monitor_authorization_number,
                                fnameLA=fnameLA,
                                lnameLA=lnameLA,
                                phone = phone,
                                cnie = cnie,
                                fnameAR = fnameAR,
                                lnameAR = lnameAR,
                                gender = gender,
                                nationality = nationality,
                                category = category,
                                vehicule_id = vehicule
                            )
                            monitorprofile.save()

                            messages.success(request,f'لقد تم المدرب {fnameAR} {lnameAR} بنجاح.')
                            vehicule=None;cnie=None;fnameLA =None; lnameLA =None
                            fnameAR =None; lnameAR =None
                            phone =None;gender =None; nationality =None; category =None
                            is_added = True  ;monitor_authorization_number=None
                            return render(request, 'monitors/addmonitor.html',{'is_added':is_added})
                            # reset input
                            
                    return redirect('addmonitor')            
                else:
                    messages.error(request, 'المرجو ملء البيانات المطلوبة.')
                    return render(request, 'monitors/addmonitor.html',{
                        'vehicules' :vehicules,
                        'vehicule':vehicule,#vehicule_id
                        'monitor_authorization_number':monitor_authorization_number,
                        'fnameLA':fnameLA,
                        'lnameLA':lnameLA,
                        'fnameAR':fnameAR,
                        'lnameAR':lnameAR,
                        'phone':phone,
                        'cnie':cnie,
                        'is_added':is_added,
                        'gender' :gender,
                        'nationality' :nationality,
                        'category' :category,
                        'is_editpage':False
                    })
            else:
                context = {
                    'vehicules' :vehicules,
                    'is_editpage':False
                }
                return render(request, 'monitors/addmonitor.html',context)
        else:
            context = {
                'vehicules' :vehicules,
                'is_editpage':False
            }
            return render(request, 'monitors/addmonitor.html',context)
        return redirect('index')
    else:  
        return redirect('signin')


def monitors(request):
    if request.user is not None and not request.user.is_anonymous:
        context=None
        monitors = MonitorProfile.objects.all()
        context = {
            'monitors':monitors
        }
        return render(request,'monitors/monitors.html',context)
    else:
        return redirect('signin')
