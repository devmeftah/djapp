
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import pandas as pd
from django.http import JsonResponse
from .forms import Eduform,MedForm,TvaForm,CtlForm
from .models import ClientProfile,Finance, Controle 
from monitors.models import MonitorProfile, Societe
from django.utils.timezone import now
import re
from weasyprint import HTML
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import plotly.express as px
from .utils import queryset_to_dataframe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.




def clients(request):
    if request.user is not None and not request.user.is_anonymous:
        scnie = None; sfname = None; slname = None; sphone = None
        scs = None; smnt=None; spfrom=None; spto=None
        mng=None
        context={}        
        clients = ClientProfile.objects.filter(controle__result=0).all()
        if 'scs' in request.GET:
            scs = request.GET['scs']
            if not scs:
                scs = 'off'

        if 'scnie' in request.GET:
            scnie = request.GET['scnie'] 
            if scnie:
                if scs == 'on':
                    clients = clients.filter(cnie__contains = scnie)
                else:
                    clients = clients.filter(cnie__icontains = scnie)

        if 'sfnameAR' in request.GET:
            sfnameAR = request.GET['sfnameAR'] 
            if sfnameAR:
                clients = clients.filter(fnameAR__contains = sfnameAR)
        if 'slnameAR' in request.GET:
            slnameAR = request.GET['slnameAR'] 
            if slnameAR:
                clients = clients.filter(lnameAR__contains = slnameAR)

        if 'sfnameLA' in request.GET:
            sfnameLA = request.GET['sfnameLA'] 
            if sfnameLA:
                    clients = clients.filter(lnameLA__contains = sfnameLA)
        if 'slnameLA' in request.GET:
            slnameLA = request.GET['slnameLA'] 
            if slnameLA:
                    clients = clients.filter(lnameAR__contains = slnameLA)

        if 'sphone' in request.GET:
            sphone = request.GET['sphone'] 
            if sphone:
                if scs == 'on':
                    clients = clients.filter(phone__contains = sphone)
                else:
                    clients = clients.filter(phone__icontains = sphone)
        if 'smnt' in request.GET:
            smnt = request.GET['smnt'] 
            if smnt:
                if scs == 'on':
                    clients = clients.filter(monitor__pk__contains = smnt)
                else:
                    clients = clients.filter(monitor__pk__icontains = smnt)

        if 'spfrom' in request.GET and 'spto' in request.GET:
            spfrom = request.GET['spfrom']
            spto = request.GET['spto']
            if spfrom and spto:
                if spfrom.isdigit() and spto.isdigit():
                    clients = clients.filter(price__gte = spfrom, price__lte = spto)        

        if 'sgender' in request.GET:
            sgender = request.GET['sgender'] 
            if sgender:
                if sgender == '1' or sgender == '2':
                    clients = clients.filter(gender__contains = int(sgender))
       
        if 'mng' in request.GET:
            mng = request.GET['mng'] 
            if mng:
                context['mng']=  True
           
        paginator = Paginator(clients,24)
        page = request.GET.get('page')
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        index = clients.number -1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index -5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        context['clients'] = clients
        context['page_range'] = page_range
        return render(request,'clients/clients.html',context)
    else:
        return redirect('signin')


def addclient(request):
    if request.user is not None and request.user.id != None:
        monitors = MonitorProfile.objects.all()
        if(monitors.exists()):
            if request.method == 'POST'and 'btnsave' in request.POST:
                #variable
                cnie=None;fnameLA =None; lnameLA =None;monitor =None;is_added =None
                fnameAR =None
                lnameAR =None
                phone =None
                cnie =None
                gender =None
                nationality =None
                category =None
                nclient =None
                ncreation =None
                photo_clt = None
                refweb=None
                placeofbirthAR=None
                addressAR=None
                dateofbirth=None
                if 'monitor' in request.POST: monitor = request.POST['monitor']
                else : messages.error(request, 'Error in monitor')

                if 'cnie' in request.POST: cnie = request.POST['cnie']
                else : messages.error(request, 'Error in cnie')

                if 'fnameLA' in request.POST: fnameLA = request.POST['fnameLA'] 
                else : messages.error(request, 'Error in first name')

                if 'lnameLA' in request.POST: lnameLA = request.POST['lnameLA']
                else : messages.error(request, 'Error in last name')
                
                if 'fnameAR' in request.POST: fnameAR = request.POST['fnameAR']
                else : messages.error(request, 'Error in phone')   

                if 'lnameAR' in request.POST: lnameAR = request.POST['lnameAR']


                if 'addressAR' in request.POST: addressAR = request.POST['addressAR']
                else : messages.error(request, 'Error in address')                     
                
                if 'refweb' in request.POST: refweb = request.POST['refweb']

                if 'placeofbirthAR' in request.POST: placeofbirthAR = request.POST['placeofbirthAR']

                if 'dateofbirth' in request.POST: dateofbirth = request.POST['dateofbirth']
                else : messages.error(request, 'Error in dateofbirth')
                

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
                else : messages.error(request, 'Error in category')


                if 'photo_clt' in request.FILES:
                    photo_clt = request.FILES['photo_clt'] 
                    if not photo_clt:
                        if gender == 2:
                            photo_clt = '/photos/random/f.svg' 
                        else :                  
                            photo_clt = '/photos/random/m.svg'
                
                arabic = r'^[ء-ي0-9\.\،\s]+$'
                if not re.match(arabic,fnameAR):fnameAR=None
                if not re.match(arabic,lnameAR):lnameAR=None
                if placeofbirthAR:
                    if not re.match(arabic,placeofbirthAR):
                        placeofbirthAR=None
                if fnameLA and  lnameLA and fnameAR and lnameAR and monitor and addressAR \
                and placeofbirthAR and dateofbirth  and phone and category and gender  and  cnie:

                    if ClientProfile.objects.filter(cnie=cnie).exists():
                        messages.error(request,'لقد ثم تسجيل هذا الزبون من قبل')
                        return redirect('addclient')
                    else:
                        ##SQLITE
                        if not refweb:
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
                                    nclient = f'{date_joined}/{usermaxcount}'
                                    ncreation =f'1114-{cnie}-{usermaxcount}'
                            else: 
                                lastId = lastId+1
                                nclient = f'{now().year}/{lastId}'
                                ncreation =f'1114-{cnie}-{lastId}'
                        else:
                            ncreation = refweb
                        #add user profile
                        clientprofile = ClientProfile(
                            addressAR=addressAR,
                            fnameLA=fnameLA,
                            lnameLA=lnameLA,
                            phone = phone,
                            cnie = cnie,
                            fnameAR = fnameAR,
                            lnameAR = lnameAR,
                            placeofbirthAR = placeofbirthAR,
                            dateofbirth = dateofbirth,
                            gender = gender,
                            photo_clt = photo_clt,
                            nationality = nationality,
                            category = category,
                            nclient = nclient,
                            ncreation = ncreation,
                            monitor_id =monitor
                        )

                        clientprofile.save()
                        controle = Controle.objects.filter(client=clientprofile)
                        if not controle.exists():
                            controle = Controle(
                                client = clientprofile,
                                theoretic = 0,
                                practical = 0,
                            )
                            controle.save()

                        messages.success(request,f'لقد تم تسجيل الزبون {fnameAR} {lnameAR} بنجاح')
                        #reset input
                        monitor=None;cnie=None;fnameLA =None; lnameLA =None
                        fnameAR =None; lnameAR =None;addressAR=None
                        phone =None;gender =None; nationality =None; category =None
                        is_added = True; nclient=None;ncreation= None
                        placeofbirthAR = None; dateofbirth = None
                        return render(request, 'clients/addclient.html',{'is_added':is_added})
                else:
                    messages.error(request, 'المرجو ملء البيانات المطلوبة.')
                    return render(request, 'clients/addclient.html',{
                        'monitors' :monitors,
                        'monitor':monitor,
                        'fnameLA':fnameLA,
                        'lnameLA':lnameLA,
                        'addressAR':addressAR,
                        'fnameAR':fnameAR,
                        'lnameAR':lnameAR,
                        'placeofbirthAR' :placeofbirthAR,
                        'dateofbirth' :dateofbirth,
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
                    'monitors' :monitors,
                    'is_editpage':False
                }
                return render(request, 'clients/addclient.html',context)
        else :
            context = {
                    'monitors' :monitors,
                    'is_editpage':False

                }
            return render(request, 'clients/addclient.html',context)
    else:
        return redirect('signin')


def updateclient(request, clt_id):
    if request.user is not None and request.user.id != None:
        clientprofile = ClientProfile.objects.filter(pk=clt_id)
        if clientprofile.exists():
            if request.method == 'POST' and 'btnedit' in request.POST :
                gender = int(request.POST['gender'])
                if request.POST['cnie'] and request.POST['addressAR']  and  request.POST['monitor'] and request.POST['fnameLA'] and request.POST['lnameLA'] and request.POST['fnameAR'] \
                    and request.POST['lnameAR'] and request.POST['phone'] and gender and request.POST['category'] \
                    and request.POST['dateofbirth'] and request.POST['placeofbirthAR']:

                    arabic = r'^[ء-ي0-9\.\،\s]+$'
                    if not re.match(arabic,request.POST['lnameLA']):fnameAR=None
                    if not re.match(arabic,request.POST['lnameLA']):lnameAR=None
                    if not re.match(arabic,request.POST['addressAR']):addressAR=None
                    
                    cnie = request.POST['cnie']

                    clientprofile = ClientProfile.objects.get(pk=clt_id)
                    if 'refweb' in request.POST:
                        refweb = request.POST['refweb']
                        if refweb:
                            clientprofile.ncreation = refweb
                        else:
                            refweb = clientprofile.ncreation.split('-')[-1]
                            clientprofile.ncreation = f'1114-{cnie}-{refweb}'

                    clientprofile.cnie = cnie
                    clientprofile.monitor_id = request.POST['monitor']
                    clientprofile.addressAR = request.POST['addressAR']
                    clientprofile.fnameLA = request.POST['fnameLA']
                    clientprofile.lnameLA = request.POST['lnameLA']
                    clientprofile.fnameAR = request.POST['fnameAR']
                    clientprofile.lnameAR = request.POST['lnameAR']
                    if 'photo_clt' in request.FILES:
                        photo_clt = request.FILES['photo_clt']
                        clientprofile.photo_clt = photo_clt
                    #if "random" in str(clientprofile.photo_clt.find):
                     #   messages.success(request,"yes")

                    if clientprofile.gender != request.POST['gender']:
                        if gender == 2:
                            clientprofile.photo_clt = '/photos/random/f.svg' 
                        else :                  
                            clientprofile.photo_clt = '/photos/random/m.svg'
                    clientprofile.gender = gender
                    clientprofile.nationality = request.POST['nationality']
                    clientprofile.category = request.POST['category']
                    clientprofile.phone = request.POST['phone']
                    clientprofile.placeofbirthAR = request.POST['placeofbirthAR']
                    clientprofile.dateofbirth = request.POST['dateofbirth']

                    clientprofile.save()
 
                    messages.success(request,'لقد تم تعديل البيانات بنجاح.')
                else: 
                    messages.error(request, 'Check your values and elements!')
                
                return redirect("updateclient",str(clt_id))            
            elif request.method == 'GET':
                context = None
                if clientprofile.exists():
                    clientprofile = ClientProfile.objects.get(pk=clt_id)
                    monitors = MonitorProfile.objects.all()
                    context= {
                        'client':get_object_or_404(ClientProfile,pk=clt_id),
                        'monitors' :monitors,
                        'monitor':clientprofile.monitor_id,
                        'fnameAR':clientprofile.fnameAR,
                        'fnameLA':clientprofile.fnameLA,
                        'lnameAR':clientprofile.lnameAR,
                        'lnameLA':clientprofile.lnameLA,
                        'addressAR':clientprofile.addressAR,                        
                        'cnie':clientprofile.cnie,
                        'nationality':clientprofile.nationality,
                        'category':clientprofile.category,
                        'dateofbirth':clientprofile.dateofbirth,
                        'placeofbirthAR':clientprofile.placeofbirthAR,
                        'phone':clientprofile.phone,
                        'gender':clientprofile.gender,
                        'is_editpage':True
                    }
                    return render(request, 'clients/addclient.html', context)

            else: 
                return redirect('addclient')
            
            #return render(request, 'accounts/profile.html')
        else:
            context={
                'client':get_object_or_404(ClientProfile,pk=clt_id),
                'is_editpage':True

            }
            return render(request,'clients/addclient.html',context)
    else:
        return redirect('signin')


def paiement(request,clt_id):
    if request.user is not None and not request.user.is_anonymous:
        context = {
            'clt_id':clt_id,
            'isPaid':False,
        }
        client = ClientProfile.objects.filter(pk=clt_id)

        if client.exists():
            client = client.get()

            paidTotal = Finance.objects.filter(client_id__pk=clt_id).all()

            if paidTotal.exists():
                paidSum = paidTotal.extra({'sum': "Sum(paid)"}) \
                            .values('sum')
                paidSum = paidSum[0]['sum']

                context['isPaid']=True
                context["paiement"] = {
                    'paidSum':client.totalpaid,
                    'paidTotal':paidTotal,
                }
                context["rest"] = client.rest
            else:
                context["paiement"] = {
                    'paidSum':0,
                    'paidTotal':0,
                }
                context["rest"] = client.price
            if request.method =='GET':
                context['price'] = client.price
                context['username'] = f'{client.fnameAR} {client.lnameAR}'
                return render(request,"clients/paiement.html",context) 
            elif request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                paid=request.POST.get('paid',None)
                paid = int(paid)
                if paid:
                    rest = client.price- client.totalpaid
                    if rest < paid:
                        response={
                            'message':{
                                'msg':'الثمن المدخل أكبر من الثمن المتبقي',
                                'tag':'danger'
                            }
                        }
                        return JsonResponse(response)
                    finance = Finance(
                        client=client,
                        paid=paid,
                    )
                    finance.save()      
                    rest = client.price- client.totalpaid
                    if rest ==0:
                        client.payed = True
                    response = {
                            'isAdd':True,
                            'rest':rest,
                            'paid':paid,
                            'paidTotal':client.totalpaid,
                            'datanow':now().strftime('%d/%m/%Y'),
                            'message':{
                                'msg':'لقد تمت إضافةالدفعة بنجاح.',
                                'tag':'success'
                            }
                    }
                    return JsonResponse(response)
            
            elif request.method == 'POST': 
                if client.price:
                    if 'paid' in request.POST:
                        paid=request.POST.get('paid')
                        if paid:
                            rest = client.price- client.totalpaid - int(paid)
                            if int(rest) < int(paid) :
                                return redirect('paiement',clt_id=clt_id)
                            finance = Finance(
                                client=client,
                                paid=paid,
                            )
                            finance.save()

                    elif 'price' in request.POST and 'btnsave' in request.POST:
                        price = request.POST['price']
                        if price:
                            client.price = request.POST['price']
                            client.save()
                            messages.success(request,'لقد ثم تعديل المبلغ الإجمالي بنجاح.')
                            context['price'] = client.price
                            rest = int(client.price) - client.totalpaid
                            context['rest'] = rest
                            context['username'] = f'{client.fnameAR} {client.lnameAR}'
                        return render(request,"clients/paiement.html",context) 
                else:
                    messages.error(request,'أرجو تحديد المبلغ الإجمالي أولا.')
        
                    return render(request,"clients/paiement.html",context) 

                return render(request,"clients/paiement.html",context) 
            
        else :
            return redirect('addclient')
    else:
        return redirect('signin')


def controle(request,clt_id):
    if request.user is not None and request.user.id != None:
        client = ClientProfile.objects.filter(id = clt_id)
        if client.exists():
            context=None

            client = client.get()
            controle = Controle.objects.filter(client=clt_id)

            if request.method == 'POST':           
                if 'Theoretic' in request.POST or 'practical' in request.POST and 'saveedu' in request.POST:
                    theoretic = int(request.POST['theoretic'])
                    practical = int(request.POST['practical'])
                    if theoretic or practical:
                        cntEdu = controle.get()
                        cntEdu.theoretic = theoretic
                        cntEdu.practical = practical
                        cntEdu.save()
                        messages.info(request,'لقد تم تعديل الحصص.') 
                if 'savecnt' in request.POST:
                    cnt = controle.get()
                    exam_t1_date=None
                    exam_p1_date=None
                    result=None

                    if 'exam_t1_date' in request.POST:
                        exam_t1_date =  request.POST['exam_t1_date']
                        if exam_t1_date:
                                cnt.exam_t1_date = exam_t1_date
                    if 'exam_p1_date' in request.POST:
                        exam_p1_date    =   request.POST['exam_p1_date']
                        if exam_p1_date: cnt.exam_p1_date = exam_p1_date
                    if 'result' in request.POST:
                        result = request.POST['result']
                        if result != '0': 
                            cnt.result = result
                            if request.POST['result_date']:
                                cnt.result_date = request.POST['result_date']
                            else: cnt.result_date = now()
                    cnt.save()
                    messages.success(request, f'لقد تم تعيين تاريخ الإمتحان بنجاح')
                return redirect(f'/clients/controle/{clt_id}')
            else:
                if not controle.exists():
                    controle = Controle(
                        client = client,
                        theoretic = 0,
                        practical = 0,
                    )
                    controle.save()

                controle = Controle.objects.filter(client=client.id).get()
                eduform = Eduform(instance=controle)
                ctlform = CtlForm(instance=controle, use_required_attribute=False)
                context = {
                    'eduform':eduform,
                    'ctlform':ctlform,
                    'result':controle.result
                }
                return render(request,'clients/controle.html',context)
        else:
            return redirect('clients')

    else:
        return redirect('signin')


@login_required(login_url='signin')
def statistic(request):
    #todo : 'Optimazation & work with OOP'
    context = {}
    #---------------------  df_total_paid all year  -----------------------------------------

    totalpaidpermount = Finance.objects.values('payement_date','paid','client')
    df_total_paid = queryset_to_dataframe(totalpaidpermount)
    df_total_paid['payement_date']= pd.to_datetime(df_total_paid['payement_date']) 
    groupbymonth = [df_total_paid['payement_date'].dt.strftime('%Y'), df_total_paid['client']]
    df_total_paid = df_total_paid.groupby(groupbymonth).aggregate({'paid':"sum"}).reset_index()

    fig_paiement = px.bar(df_total_paid, x='payement_date',y='paid',
            color='client',barmode='group', 
            title="المبلغ الإجمالي كل شهر",
            labels={
                'payement_date':'تاريخ الدفع',
                'paid':'قيمة الدفعة',
                'client':'اسم الزبون',
            }
    ) 
    fig_paiement.update_layout(
                plot_bgcolor='#212529',paper_bgcolor='#212529',

        title={
            'text': "عدد الدفعات لكل عام",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title="التاريخ",
            yaxis_title="المبلغ",
            legend_title='اسم الزبون',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            )
    )

    #---------------------  df_gender_month latest year  -----------------------------------------
 
    totalgenderpermonitor = ClientProfile.objects.filter(date_joined__year=now().year).values('date_joined','gender')
    df_gender_month = queryset_to_dataframe(totalgenderpermonitor)
    df_gender_month['date_joined']= pd.to_datetime(df_gender_month['date_joined'])
    groupbymonth = [df_gender_month['date_joined'].dt.strftime('%Y-%m'), df_gender_month['gender']]
    df_gender_month = df_gender_month.groupby(groupbymonth).size().reset_index(name='gender_count')
    
    fig_gender_month = px.pie(df_gender_month, values='gender_count',names='date_joined',
                 #color='gender',
                 labels={
                     "date_joined": "تاريخ",
                     "gender_count": "عدد الزبناء",
                     "gender": "الجنس"
                 },
    ) 
    fig_gender_month.update_layout(

        plot_bgcolor='#000000',paper_bgcolor='#212529',
        title={
            'text': "عدد الزبناء",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        #xaxis_title="تاريخ",
        #yaxis_title="عدد الزبناء",
        #legend_title="جنس الزبون",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            )   
    )
    
    #---------------------  df_gender_monitor latest year  -----------------------------------------

    totalgenderpermonitor = ClientProfile.objects.filter(date_joined__year=now().year).values('date_joined','gender','monitor')
    df_gender_monitor = queryset_to_dataframe(totalgenderpermonitor)
    df_gender_monitor['date_joined']= pd.to_datetime(df_gender_monitor['date_joined'])
    groupbymonth = [df_gender_monitor['date_joined'].dt.strftime('%Y/%m'), df_gender_monitor['gender'],df_gender_monitor['monitor']]#, df_gender_monitor['gender']
    df_gender_monitor = df_gender_monitor.groupby(groupbymonth).size().reset_index(name='gender_count')
    
    fig_gender_monitor = px.bar(df_gender_monitor, x='date_joined',y='gender_count',
            color='monitor',barmode='group', text="gender_count",
            labels={
                "date_joined": "تاريخ",
                "gender_count": "عدد الزبناء",
                "gender": "الجنس",
                "monitor": "المدرب"
                },
            hover_data=['monitor','gender' ]
    ) 
    fig_gender_monitor.update_layout(
                plot_bgcolor='#212529',paper_bgcolor='#212529',

        title={
            'text': "عدد الزبناء",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        #xaxis_title="تاريخ",
        #yaxis_title="عدد الزبناء",
        #legend_title="جنس الزبون",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
            )  
    )

    #---------------------  total_client_result latest year  -----------------------------------------

    total_client_result = Controle.objects.filter(result_date__year=now().year).values('result_date','result')
    df_total_client_result = queryset_to_dataframe(total_client_result)

    df_total_client_result['result_date']= pd.to_datetime(df_total_client_result['result_date'])
    groupbymonth = [df_total_client_result['result_date'].dt.strftime('%Y/%m'), df_total_client_result['result']]#
    df_total_client_result = df_total_client_result.groupby(groupbymonth).size().reset_index(name='result_count')
    if not df_total_client_result.empty:
        fig_total_client_result = px.bar(df_total_client_result, x='result_date',y='result_count',
                color='result',barmode='group', 
                title="نتيجة الاختبار لكل شهر",
                #hover_name=''
                labels={
                    'result_date':'تاريخ الاختبار',
                    'result':'النتيجة',
                    'result_count':'عدد المرشحين',
                }
        ) 
        fig_total_client_result.update_layout(
                plot_bgcolor='#212529',paper_bgcolor='#212529',
            title={
                #'text': "عدد الدفعات",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                #xaxis_title="تاريخ",
                #yaxis_title="المبلغ",
                #legend_title='اسم الزبون',
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#ffffff"
                )
        )
        chart_total_client_result = fig_total_client_result.to_html()
        context['chart_total_client_result'] = chart_total_client_result

    chart_paiement = fig_paiement.to_html()
    chart_gender_month = fig_gender_month.to_html()
    chart_gender_monitor = fig_gender_monitor.to_html()
    context['chart_paiement']=chart_paiement
    context['chart_gender_month']=chart_gender_month
    context['chart_gender_monitor']=chart_gender_monitor

    return render(request, 'clients/statistic.html', context)


def paiementpdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    client = get_object_or_404(ClientProfile, pk=pk)
    paidTotal = Finance.objects.filter(client_id__pk=pk).all()
    societe = get_object_or_404(Societe)
    context= None
    paidSum = paidTotal.extra({'sum': "Sum(paid)"}) \
                .values('sum')
    paidSum = paidSum[0]['sum']
    rest = client.price- paidSum
    context = {
        'societe':{
            'phone': societe.phone,
            'societename':societe.societe_name,
            'address':societe.address,
        },
        'thisDate':now(),
        'paidSum':paidSum,
        'paidTotal':paidTotal,
        'rest':rest,
        'price':client.price,
        'username':f'{client.fnameLA} {client.lnameLA}',
        'client':{
            'fullname': f'{client.fnameAR} {client.lnameAR}',
            'cnie':client.cnie,
            'nclient':client.nclient
        }
    }
    html_template = get_template('clients/pdf/paiement.html').render(context)

    pdf_file = HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')

    filename = f'paiement-{client.cnie}-{now()}'

    response['Content-Disposition'] = f'attachemnt;  filename="{filename}.pdf"'

    return response 


def contractpdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    client = get_object_or_404(ClientProfile, pk=pk)
    societe = get_object_or_404(Societe)
    context = {'client':client,'societe':societe,'thisDate':now()}

    html_template = get_template('clients/pdf/contract.html').render(context)

    pdf_file = HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf()
   
    response = HttpResponse(pdf_file, content_type='application/pdf')

    filename = f'contrat-{client.cnie}-{now()}'
    response['Content-Disposition'] = f'attachemnt;  filename="{filename}.pdf"'

    return response


def certifiedpdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    client = get_object_or_404(ClientProfile, pk=pk)
    societe = get_object_or_404(Societe)
    context = {'client':client,'societe':societe,'thisDate':now}

    html_template = get_template('clients/pdf/certified.html').render(context)

    pdf_file = HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf()
   
    response = HttpResponse(pdf_file, content_type='application/pdf')


    filename = f'certification-{client.cnie}-{now()}'
    response['Content-Disposition'] = f'attachemnt;  filename="{filename}.pdf"'

    return response  

