from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import *
import datetime
from django.http import HttpResponse,HttpResponseNotFound, request
from datetime import date,time

# Create your views here.

def testerloginpage(request):
    return render(request,"maintenance/tester/testerloginpage.html")

def testerlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("maintenance:testerloginpage")

    if tester.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("maintenance:testerhomepage1")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

def testerhomepage1(request):
    if request.user.is_superuser:
        messages.add_message(request,messages.INFO,"you must login as a tester")
        logout(request)
        return redirect("maintenance:testerloginpage")

    testername =request.user.username
    test=tester.objects.get(user=request.user)
    assem=assembly.objects.filter(tester=test)
    ids=[]
    for i in assem:
        if ids.__contains__(i.machine_id.id)==False:
            ids.append(i.machine_id.id)
    machines1 = machine.objects.filter(id__in=ids)
    context = {'machines' : machines1,'username' : testername}
    return render(request,"maintenance/tester/testerhomepage.html",context)

def machinedetail(request,machine_id):
    machinedata = machine.objects.get(pk=machine_id)
    test=tester.objects.get(user=request.user)
    categories = assembly.objects.filter(machine_id = machinedata,tester=test)
    context = {'machinedata' : machinedata , 'categories' : categories}
    return render(request,'maintenance/tester/machinedetail.html',context)
    
def assemblydetail(request,machine_id,assembly_id):
    machinedata = machine.objects.get(pk=machine_id)
    assemblydata = assembly.objects.get(pk=assembly_id)
    checkpointsdata = checkpoint.objects.filter(part_id__assembly_id = assembly_id)
    parts=part.objects.filter(assembly_id=assemblydata)
    standerddata = standard.objects.filter(check_id__machine_id=machine_id)
    stanbinary=[]
    stanvalue=[]
    stanrange=[]
    stanryb=[]
    orvalues=[415,230,"_10"]
    for i in checkpointsdata:
        if standard_binary.objects.filter(standard_id__check_id__id=i.id).exists():  
            stanb=standard_binary.objects.filter(standard_id__check_id__id=i.id)[0]
            print(stanb)
            stanbinary.append(stanb)
        elif standard_value.objects.filter(standard_id__check_id__id=i.id).exists():  
            stanv = standard_value.objects.filter(standard_id__check_id__id=i.id)[0]
            stanvalue.append(stanv)
        elif standard_ryb.objects.filter(standard_id__check_id__id=i.id).exists():
            stant=standard_ryb.objects.filter(standard_id__check_id__id=i.id)[0]
            stanryb.append(stant)
        else:  
            stanr = standard_range.objects.filter(standard_id__check_id__id=i.id)[0]
            stanrange.append(stanr)
    context = {'machinedata' : machinedata ,'assemblydata' : assemblydata ,"parts":parts,
    'checkpointsdata' :checkpointsdata,"stanryb":stanryb,"orvalues":orvalues,
    "standerddata":standerddata,"stanb":stanbinary ,"stanv":stanvalue,"stanr":stanrange, "today":date.today()}
    return render(request,'maintenance/tester/assemblydetail.html',context)
     
def partdetail(request,machine_id , assembly_id, part_id):
    machinedata = machine.objects.get(pk=machine_id)
    assemblydata = assembly.objects.get(pk=assembly_id)
    partsdata = part.objects.get(pk=part_id)
    checkpointsdata = checkpoint.objects.filter(part_id = partsdata)
    context = {'machinedata' : machinedata ,'assemblydata' : assemblydata, 'partsdata' : partsdata,'checkpointsdata':checkpointsdata}
    return render(request,'maintenance/tester/partdetail.html',context)

def updaterange(request,stanid):
    stand = standard_range.objects.get(id=stanid)
    chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
    img = 'rngimg'+str(stanid)
    mins1 = 'mins'+str(stand.standard_id.id)
    mins = request.POST[mins1]

    imgg = request.FILES[img] if img in request.FILES else "noimage.png"
    if frequency.objects.filter(checkpoint_id=stand.standard_id.check_id).exists():
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=True
        cp.save()
        frequ = frequency(currentdate=date.today(),todate=cp.nextdate,
        Fromdate=cp.fromdate ,checked=True,checkpoint_id=chek)
        frequ.save()
        values = request.POST['rangeval']
        if(stand.rangevalue.lower_limit == True):
            if(int(values)>stand.rangevalue.more_than):
                tf=True
            else:
                tf=False
        elif(stand.rangevalue.upper_limit == True):
            if(int(values)<stand.rangevalue.less_than):
                tf=True 
            else:
                tf=False
        standd = standard_range(frequency=frequ,img=imgg,standard_id=stand.standard_id,rangevalue=stand.rangevalue,value=values,status=tf,time=mins)
        standd.save()
        cp.checked=False
        cp.fromdate=cp.nextdate
        nextm=cp.nextdate.month
        year=cp.nextdate.year
        nextm = nextm + cp.freq 
        if nextm > 12 :
            year = year + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
    else:
        today = datetime.date.today()
        year=today.year
        year1=today.year
        month=today.month
        ad = int(stand.standard_id.check_id.freq)
        nextm = month + ad 
        if nextm > 12 :
            year1 = year + 1
            nextm = nextm - 12
        chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
        frequ =frequency(currentdate=date.today(),todate=datetime.date(year1,nextm,1),
        Fromdate=datetime.date(year,month,1) ,checked=True,checkpoint_id=chek)
        frequ.save()
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=False
        cp.fromdate=datetime.date(year1,nextm,1)
        nextm+=ad 
        if nextm > 12 :
            year = year1 + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
        values = request.POST['rangeval']
        if(stand.rangevalue.lower_limit == True):
            if(int(values)>stand.rangevalue.more_than):
                stand.status=True
        elif(stand.rangevalue.upper_limit == True):
            if(int(values)<stand.rangevalue.less_than):
                stand.status=True   
        stand.value=values
        stand.img=imgg
        stand.time=mins
        stand.frequency = frequ
        stand.save()
    return redirect(request.META["HTTP_REFERER"])

def updatebinary(request,stanid):
    stand = standard_binary.objects.get(id=stanid)
    chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
    stat = 'check'+str(stanid)
    img = 'notsatisimg'+str(stanid)
    mins1 = 'mins'+str(stand.standard_id.id)
    mins = request.POST[mins1]
    imgg = request.FILES[img] if img in request.FILES else "noimage.png"
    selval = request.POST[stat]
    if frequency.objects.filter(checkpoint_id=stand.standard_id.check_id).exists():
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=True
        cp.save()
        frequ = frequency(currentdate=date.today(),todate=cp.nextdate,
        Fromdate=cp.fromdate ,checked=True,checkpoint_id=chek)
        frequ.save()
        if(selval == "Satisfied"):
            tf=True
        else:
            tf=False
        standd = standard_binary(frequency=frequ,img=imgg,standard_id=stand.standard_id,status=tf,time=mins)
        standd.save()
        cp.checked=False
        cp.fromdate=cp.nextdate
        nextm=cp.nextdate.month
        year=cp.nextdate.year
        nextm = nextm + cp.freq 
        if nextm > 12 :
            year = year + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
    else:
        today = datetime.date.today()
        year=today.year
        year1=today.year
        month=today.month
        ad = int(stand.standard_id.check_id.freq)
        nextm = month + ad 
        if nextm > 12 :
            year1 = year + 1
            nextm = nextm - 12
        chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
        frequ =frequency(currentdate=date.today(),todate=datetime.date(year1,nextm,1),
        Fromdate=datetime.date(year,month,1) ,checked=True,checkpoint_id=chek)
        frequ.save()
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=False
        cp.fromdate=datetime.date(year1,nextm,1)
        nextm+=ad 
        if nextm > 12 :
            year = year1 + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
        if(selval == "Satisfied"):
            tf=True
        else:
            tf=False 
        stand.img=imgg
        stand.frequency = frequ
        stand.status = tf
        stand.time=mins
        stand.save()
    return redirect(request.META["HTTP_REFERER"])

def updaterybvalue(request,stanid):
    stand = standard_ryb.objects.get(id=stanid)
    chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
    r=request.POST['r']
    y=request.POST['y']
    b=request.POST['b']
    mins1 = 'mins'+str(stand.standard_id.id)
    mins = request.POST[mins1]

    img = 'imgg'+str(stanid)
    imgg = request.FILES[img] if img in request.FILES else "noimage.png"


    if frequency.objects.filter(checkpoint_id=stand.standard_id.check_id).exists():
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        tf=True
        cp.checked=True
        cp.save()
        frequ = frequency(currentdate=date.today(),todate=cp.nextdate,
        Fromdate=cp.fromdate ,checked=True,checkpoint_id=chek)
        frequ.save()
        standr = standard_ryb(frequency=frequ,standard_id=stand.standard_id,r=r,y=y,b=b,status=tf,time=mins)
        standr.save()
        cp.checked=False
        cp.fromdate=cp.nextdate
        nextm=cp.nextdate.month
        year=cp.nextdate.year
        nextm = nextm + cp.freq 
        if nextm > 12 :
            year = year + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
    else:
        today = datetime.date.today()
        year=today.year
        year1=today.year

        month=today.month
        ad = int(stand.standard_id.check_id.freq)
        nextm = month + ad 
        if nextm > 12 :
            year1= year + 1
            nextm = nextm - 12
        print(nextm)
        chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
        frequ =frequency(currentdate=date.today(),todate=datetime.date(year1,nextm,1),
        Fromdate=datetime.date(year,month,1) ,checked=True,checkpoint_id=chek)
        frequ.save()
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=False
        cp.fromdate=datetime.date(year1,nextm,1)
        nextm+=ad 
        if nextm > 12 :
            year = year1 + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
        tf=True
        stand.frequency = frequ
        stand.status = tf
        stand.r=r
        stand.y=y
        stand.b=b
        stand.time=mins
        stand.save()
    return redirect(request.META["HTTP_REFERER"])

def updateval(request,stanid):
    
    stand = standard_value.objects.get(id=stanid)
    chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
    if(stand.standard_id.standard_desc == "415V/230 V+/_ 10V"):
        val=request.POST['check'+str(stand.id)]
    else:
        val=request.POST["val"]
    
    print(val)
    mins1 = 'mins'+str(stand.standard_id.id)
    mins = request.POST[mins1]

    img = 'imgg'+str(stanid)
    imgg = request.FILES[img] if img in request.FILES else "noimage.png"

    if frequency.objects.filter(checkpoint_id=stand.standard_id.check_id).exists():
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        tf=True
        cp.checked=True
        cp.save()
        frequ = frequency(currentdate=date.today(),todate=cp.nextdate,
        Fromdate=cp.fromdate ,checked=True,checkpoint_id=chek)
        frequ.save()
        standr = standard_value(frequency=frequ,standard_id=stand.standard_id,value=val,status=tf,time=mins,img=imgg)
        standr.save()
        cp.checked=False
        cp.fromdate=cp.nextdate
        nextm=cp.nextdate.month
        year=cp.nextdate.year
        nextm = nextm + cp.freq 
        if nextm > 12 :
            year = year + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
    else:
        today = datetime.date.today()
        year=today.year
        year1=today.year

        month=today.month
        ad = int(stand.standard_id.check_id.freq)
        nextm = month + ad 
        if nextm > 12 :
            year1= year + 1
            nextm = nextm - 12
        print(nextm)
        chek=checkpoint.objects.get(id=stand.standard_id.check_id.id)
        frequ =frequency(currentdate=date.today(),todate=datetime.date(year1,nextm,1),
        Fromdate=datetime.date(year,month,1) ,checked=True,checkpoint_id=chek)
        frequ.save()
        cp = checkpoint.objects.get(id=stand.standard_id.check_id.id)
        cp.checked=False
        cp.fromdate=datetime.date(year1,nextm,1)
        nextm+=ad 
        if nextm > 12 :
            year = year1 + 1
            nextm = nextm - 12
        cp.nextdate=datetime.date(year,nextm,1)
        cp.save()
        tf=True
        stand.frequency = frequ
        stand.status = tf
        stand.value = val
        stand.time=mins
        stand.img = imgg
        stand.save()
    return redirect(request.META["HTTP_REFERER"])

def reviewerlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("maintenance:reviewerloginpage")

    if reviewer.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("maintenance:reviewerhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

def reviewerloginpage(request):
    return render(request,"maintenance/reviewer/rewiewerlogin.html")


def reviewerhomepage(request):
    if request.user.is_superuser:
        messages.add_message(request,messages.INFO,"you must login as a Reviewer")
        logout(request)
        return redirect("maintenance:reviewerloginpage")

    testername =request.user.username   
    test=reviewer.objects.get(user=request.user) 
    machines1 = machine.objects.filter(reviewer=test)
    context = {'machines' : machines1,'username' : testername}
    return render(request,"maintenance/reviewer/reviewerhomepage.html",context)


def machinedetailrev(request,machine_id):
    machinedata = machine.objects.get(pk=machine_id)
    categories = assembly.objects.filter(machine_id = machinedata)
    context = {'machinedata' : machinedata , 'categories' : categories}
    return render(request,'maintenance/reviewer/machinedetailrev.html',context)

def checkdetails(request,taskid):
    stand=standard.objects.filter(check_id__part_id__assembly_id__id=taskid)
    machinedata = assembly.objects.get(id=taskid)
    context={'stand':stand,"machinedata":machinedata}
    return render(request,"maintenance/reviewer/detailview.html",context)

def standdetailview(request,taskid):
    today=datetime.date.today()
    year=today.year
    stan=standard.objects.get(id=taskid)
    if stan.standard_type=="B":
        st=standard_binary.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=False)
    elif stan.standard_type=="R":
        st=standard_range.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=False)
    elif stan.standard_type=="V":
        st=standard_value.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=False)
    elif stan.standard_type=="T":
        st=standard_ryb.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=False)

    if len(st)==0:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'size':size,'desc':desc}
    else:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'type':stan.standard_type,'size':size,'desc':desc}
    return render(request,'maintenance/reviewer/standetaailview.html',context)

def standapprove(request,standid,stid):
    stan=standard.objects.get(id=standid)
    if stan.standard_type=="B":
        st=standard_binary.objects.get(standard_id=stan,id=stid)
    elif stan.standard_type=="R":
        st=standard_range.objects.get(standard_id=stan,id=stid)
    elif stan.standard_type=="V":
        st=standard_value.objects.get(standard_id=stan,id=stid)
    else:
        st=standard_ryb.objects.get(standard_id=stan,id=stid)
    st.approved = True
    st.approved_date = datetime.date.today()
    st.save()
    return redirect(request.META["HTTP_REFERER"])

def hodloginpage(request):
    return render(request,"maintenance/hod/hodloginpage.html")

def hodlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("maintenance:hodloginpage")

    if mainhodlogindata.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("maintenance:hodhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

def hodhomepage(request):
    if request.user.is_superuser:
        messages.add_message(request,messages.INFO,"you must login as a Reviewer")
        logout(request)
        return redirect("maintenance:hodloginpage")
    hodname =request.user.username    
    hodd = mainhodlogindata.objects.get(user=request.user)
    machines1 = machine.objects.filter(hod=hodd)
    context = {'machines' : machines1,'username' : hodname}
    return render(request,"maintenance/hod/hodhome.html",context)

def machinedetailhod(request,machine_id):
    machinedata = machine.objects.get(pk=machine_id)
    categories = assembly.objects.filter(machine_id = machinedata)
    context = {'machinedata' : machinedata , 'categories' : categories}
    return render(request,'maintenance/hod/machinedetailhod.html',context)
    
def checkdetailshod(request,taskid):
    stand=standard.objects.filter(check_id__part_id__assembly_id__id=taskid)
    machinedata = assembly.objects.get(id=taskid)
    context={'stand':stand,"machinedata":machinedata}
    return render(request,"maintenance/hod/detailview.html",context)

def standdetailviewhod(request,taskid):
    today=datetime.date.today()
    year=today.year
    stan=standard.objects.get(id=taskid)
    if stan.standard_type=="B":
        st=standard_binary.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True,status=False)
    elif stan.standard_type=="R":
        st=standard_range.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True,status=False)
    elif stan.standard_type=="V":
        st=standard_value.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True,status=False)
    elif stan.standard_type=="T":
        st=standard_ryb.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True,status=False)

    if len(st)==0:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'size':size,'desc':desc}
    else:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'type':stan.standard_type,'size':size,'desc':desc}
    return render(request,'maintenance/hod/standetaailview.html',context)

def standapproved(request,taskid):
    today=datetime.date.today()
    year=today.year
    stan=standard.objects.get(id=taskid)
    if stan.standard_type=="B":
        st=standard_binary.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True)
    elif stan.standard_type=="R":
        st=standard_range.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True)
    elif stan.standard_type=="V":
        st=standard_value.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True)
    elif stan.standard_type=="T":
        st=standard_ryb.objects.filter(standard_id=stan,frequency__currentdate__year=year,approved=True)

    years=[]

    for i in st:
        if i.frequency.currentdate.year not in years:
            years.append(i.frequency.currentdate.year)
        
    if len(st)==0:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'size':size,'desc':desc}
    else:
        size=len(st)
        desc=stan.standard_desc
        context={'st':st,'type':stan.standard_type,'size':size,'desc':desc,'years':years}
    return render(request,'maintenance/reviewer/standapproved.html',context)