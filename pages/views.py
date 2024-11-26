
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from monitors.models import MonitorProfile
from clients.models import ClientProfile,Controle
from django.db.models import Count,Sum 
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

# Create your views here.
 
def custom_404(request, exception):
    return render(request, 'pages/404.html', status=404)
def custom_501(request, exception):
    return render(request, 'pages/501.html', status=501)

@login_required(login_url='signin')
def index(request):
    context={}
    clients = ClientProfile.objects.all()

    if now().month.__ge__(1) and now().month.__le__(3):
        date__range=["2024-01-01", "2024-03-31"]
    elif now().month.__ge__(4) and now().month.__le__(6):
        date__range=["2024-04-01", "2024-06-30"]
    elif now().month.__ge__(7) and now().month.__le__(9):
        date__range=["2024-07-01", "2024-09-30"]
    elif now().month.__gt__(9):
        date__range=["2024-10-01", "2024-12-31"]
    tax = Controle.objects.filter(exam_t1_date__range=date__range).all() 
    monitors = MonitorProfile.objects.all()
    mnts_count = []
    list_mnt = []

    if tax.exists():
        for m in range(len(monitors)):
            for c in range(len(tax)):
                if monitors[m].cnie == tax[c].client.monitor.cnie:
                    mnts_count.append(f'{monitors[m].fnameAR} {monitors[m].lnameAR}')

        mnts = list(dict.fromkeys(mnts_count))
        if len(mnts) > 0:
            for ct in range(len(mnts)):
                c = mnts_count.count(mnts[ct])
                list_mnt.append({'name' : f'{mnts[ct]}','count' : c,'tax': c *450 })
        else:
            c = mnts_count.count(mnts[0])
            list_mnt.append({'name' : f'{mnts[0]}', 'count' : c, 'tax': c *450})

        context = {
            'isTax':True,
            'monitors':list_mnt,
        }

    context['clients'] = clients
    return render(request,'pages/resume.html',context)



def signin(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['user']
        password = request.POST['pass']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if 'memberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
           
            return redirect('signin')

        else:
            messages.error(request,'اسم المستخدم أو كلمة المرور غير صحيحة.')
            return redirect('signin')
    else:
        return render(request, 'pages/signin.html')

@login_required(login_url='signin')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

@login_required(login_url='signin')
def search(request):
    if request.user is not None and request.user.id != None:
        monitors = MonitorProfile.objects.all()
        if(monitors.exists()):
            return render(request, 'pages/search.html',{'monitors':monitors})
        else:
            return redirect('addmonitor')
    else:
        return redirect('signin')


def about(request):
    return render(request, 'pages/about.html')
