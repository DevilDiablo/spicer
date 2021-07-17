from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import *
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import *
from maintenance.models import *
from maintenance.views import *

# python standard lib
import base64, secrets, io

# django and pillow lib
from PIL import Image
from django.core.files.base import ContentFile




def get_image_from_data_url( data_url, resize=True, base_width=600 ):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl       = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        w_percent    = (base_width/float(image.size[0]))
        h_size       = int((float(image.size[1])*float(w_percent)))
        image        = image.resize((base_width,h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

    # file and filename
    return file, ( _filename, _extension )


def homepageview(request):
    if request.user.is_authenticated:
        if userlogindata.objects.filter(user=request.user).exists():
            return redirect("userhomepage")
        elif stafflogindata.objects.filter(user=request.user).exists():
            return redirect("stafhomepage")
        elif championdata.objects.filter(user=request.user).exists():
            return redirect("championhomepage")
        elif HODlogindata.objects.filter(user=request.user).exists():
            return redirect("hodhomepage")
        elif mainhodlogindata.objects.filter(user=request.user).exists():
            return redirect("maintenance:hodhomepage")
        elif reviewer.objects.filter(user=request.user).exists():
            return redirect("maintenance:reviewerhomepage")
        elif tester.objects.filter(user=request.user).exists():
            return redirect("maintenance:testerhomepage1")
        else:
            logout(request)
            return render(request, "feedback/Homepage.html")  
    else:
        return render(request, "feedback/Homepage.html")
    

def userloginpage(request):
    return render(request,"feedback/userloginpage.html")

@login_required(redirect_field_name='')
def emaillog(request):
    if request.user.is_authenticated:
        if userlogindata.objects.filter(user=request.user).exists():
            return redirect("userhomepage")
        elif stafflogindata.objects.filter(user=request.user).exists():
            return redirect("stafhomepage")
        elif championdata.objects.filter(user=request.user).exists():
            return redirect("championhomepage")
        elif HODlogindata.objects.filter(user=request.user).exists():
            return redirect("hodhomepage")
        elif mainhodlogindata.objects.filter(user=request.user).exists():
            return redirect("maintenance:hodhomepage")
        elif reviewer.objects.filter(user=request.user).exists():
            return redirect("maintenance:reviewerhomepage")
        elif tester.objects.filter(user=request.user).exists():
            return redirect("maintenance:testerhomepage1")
        else:
            logout(request)
            messages.add_message(request, messages.INFO, "You have not been added for your designation please contact admin")
            return redirect("homepage")

def qrcodeview(request,id):
    if request.user.is_authenticated:
        if mainhodlogindata.objects.filter(user=request.user).exists():
            return redirect(reverse('maintenance:machinedetailhod', kwargs={"machine_id": id}))
        elif reviewer.objects.filter(user=request.user).exists():
            return redirect(reverse('maintenance:', kwargs={"machine_id": id}))
        elif tester.objects.filter(user=request.user).exists():
            return redirect(reverse('maintenance:', kwargs={"machine_id": id}))
    else:
        messages.add_message(request, messages.INFO, "Login and scan the QR code")
        return redirect("homepage") 

def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("userloginpage")

    if userlogindata.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("userhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def userhomepage(request):
    if request.user.is_superuser:
        messages.add_message(request,messages.INFO,"you must login as user")
        logout(request)
        return redirect("userloginpage")
    workunits = ["My feedbacks"]
    context = {'workunits' : workunits,'username' : request.user.username}
    return render(request,"feedback/userhomepage.html",context)

def logoutuser(request):
    logout(request)
    return redirect("homepage")

@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def feedbackpage(request):
    list1=department.objects.all()
    context={"list":list1}
    if request.user.is_authenticated:
        return render(request,'feedback/feedbackform.html',context)
    else:
        messages.info(request, 'Login to give feedback')
        return redirect("userloginpage")
        
@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def myfeedbackpage(request):
    uname =request.user.username
    user_id = User.objects.get(username=uname)
    userlogin_id = userlogindata.objects.get(user = user_id).pk
    workunits = complaint.objects.filter(uname=userlogin_id).order_by('-opendate')
    context = {'workunits' : workunits,'username' : uname}
    return render(request,"feedback/myfeedbackform.html",context)
@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def feedbackval(request):
    issues=request.POST['issue']
    department1=request.POST['department']
    crict=request.POST['crictcality']
    id1= department.objects.get(Dname=department1)
    user=userlogindata.objects.filter(user=request.user)[0]
    complaint(uname=user,did=id1,issue=issues,crictcality=crict).save()
    messages.info(request,"Feedback Created successfully")
    return redirect("userhomepage")

def stafloginpage(request):
    return render(request,"staf/userloginpage.html")

def staflogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("stafloginpage")

    if stafflogindata.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("stafhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def stafhomepage(request):
    staff_id = stafflogindata.objects.get(user=request.user)
    stafflogin_id = staff_id.did
    workunits = complaint.objects.filter(did = stafflogin_id).order_by('-opendate')
    sorts = complaint.objects.filter(did = stafflogin_id,accountdate__gte=datetime.date.today()).order_by('-accountdate')
    du = attempts.objects.filter(count__lt=4).filter(complid__did=stafflogin_id)
    du1 = attempts.objects.filter(count__lt=4).filter(complid__did=stafflogin_id,
    complid__accountdate__lt=datetime.date.today(),complid__verification=False)
    print(du1)
    over=attempts.objects.filter(count=4).filter(complid__did=stafflogin_id,
            complid__accountdate__lt=datetime.date.today())
    list2=championdata.objects.filter(did=stafflogin_id)
    context = {'workunits' : workunits,'username' :request.user,'dept':stafflogin_id,
    "over":over,"sorts":sorts,"du":du,"list2":list2,"du1":du1}
    return render(request,"staf/userhomepage.html",context)

def hodloginpage(request):
    return render(request,"hod/userloginpage.html")

def hodlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("hodloginpage")

    if HODlogindata.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("hodhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])


@allowed_users(allowed_roles=['hod'])
# @login_required(login_url='hodlogin')
def hodhomepage(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    print(hod)
    units = complaint.objects.filter(did__in = hod,crictcality=True) 
    workunits = complaint.objects.filter(forward = True,did__in = hod) 
    sorts = complaint.objects.filter(did__in = hod, forward = True).order_by('accountdate')
    du = attempts.objects.filter(count__lt=4).filter(complid__did__in=hod)
    over=attempts.objects.filter(count=4).filter(complid__did__in=hod,
            complid__accountdate__lt=datetime.date.today())
    list2=department.objects.filter(hod=hodlogin_id)
    context = {'workunits' : workunits,'username' :request.user,'dept':hod,
    "over":over,"sorts":sorts,"du":du,'list2':list2}
    return render(request,"hod/userhomepage.html",context)


@allowed_users(allowed_roles=['hod'])
# @login_required(login_url='hodlogin')
def hoddepartment(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod = hodlogin_id)
    context={'list':hod}
    return render(request,"hod/department.html",context)


@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def editformview(request,taskid):
    workunits = complaint.objects.get(id=taskid)
    id1=workunits.did.id
    list2=championdata.objects.filter(did__id=id1)
    context={"list2":list2,"workunits":workunits}
    return render(request,"staf/editformview.html",context)


@allowed_users(allowed_roles=['hod'])
# @login_required(login_url='hodlogin')
def editformviewhod(request,taskid):
    comp=complaint.objects.get(id=taskid)
    id1=comp.did.id
    list2=championdata.objects.filter(did__id=id1)
    print(list2)
    workunits = complaint.objects.get(id=taskid)
    context={"list2":list2,"workunits":workunits}
    return render(request,"hod/editformview.html",context)


@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def edituserform(request,taskid):
    workunits = issues.objects.get(id=taskid)
    dep=department.objects.get(Dname=workunits.issuedepartment)
    context={"depart":dep,"i":workunits}
    return render(request,"feedback/edituserformview.html",context)


@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def formsave1(request,taskid):
    staf1 = stafflogindata.objects.get(user=request.user)
    corrective1=request.POST['corrective']
    accountdate=request.POST['accountdate']
    champid=request.POST['champion']
    crict=request.POST['criticality']
    print(champid,accountdate,corrective1,crict)
    if(corrective1=="" and accountdate=="" and champid=="0"):
        entry=complaint.objects.get(id=taskid)
        entry.crictcality=crict
        entry.save()
        return redirect("stafhomepage")
    else:
        print(champid)
        chap=championdata.objects.get(id=champid)
        entry=complaint.objects.get(id=taskid)
        entry.accountdate=accountdate
        entry.cid=chap
        entry.crictcality=crict
        entry.corrective=corrective1
        entry.staff=staf1
        entry.save()
        attempts.objects.create(complid=entry,champid=chap,count=1).save()
        return redirect("stafhomepage")


@allowed_users(allowed_roles=['hod'])
# @login_required(login_url='hodlogin')
def formsave1hod(request,taskid):
    corrective1=request.POST['corrective']
    accountdate=request.POST['accountdate']
    champid=request.POST['champion']
    print(champid,accountdate,corrective1)
    chap=championdata.objects.get(id=champid)
    print(chap)
    entry=complaint.objects.get(id=taskid)
    entry.accountdate=accountdate
    entry.cid=chap.user
    entry.corrective=corrective1
    entry.save()
    attempts.objects.create(complid=entry,champid=chap,count=1).save()
    return redirect("departments")

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def formsave2(request,taskid):
    corrective1=request.POST['corrective']
    champid=request.POST['champion']
    print(champid,corrective1)
    chap=championdata.objects.get(id=champid)
    entry=attempts.objects.get(id=taskid)
    entry.complid.cid=chap
    entry.champid=chap
    entry.complid.corrective=corrective1
    entry.save()
    return redirect("stafhomepage")


@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def fwdform(request,taskid):
    entry=complaint.objects.get(id=taskid)
    entry.forward=True
    entry.save()
    return redirect(request.META["HTTP_REFERER"])


@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def allissues(request,taskid):
    dep=department.objects.get(id=taskid)
    issuesss=issues.objects.filter(issuedepartment=dep)
    context={"issue":issuesss,"depart":dep}
    return render(request,"feedback/allissues.html",context)


@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def saveuserform(request,taskid):
    workunits = issues.objects.get(id=taskid)
    dep=department.objects.get(Dname=workunits.issuedepartment)
    issue1=request.POST['editissuetext']
    crict=request.POST['crictcality']
    testt = request.POST['test'] if 'test' in request.POST else ""
    if(testt != ""):
        avatar_file = get_image_from_data_url(request.POST['test'])[0]
    else:
        avatar_file = request.FILES['id_image'] if 'id_image' in request.FILES else "noimage.png"
    print(avatar_file)
    user=userlogindata.objects.get(user=request.user)
    comp = complaint(uname=user,did=dep,issue=issue1,crictcality=crict,img=avatar_file,complaint_issue=workunits)
    comp.save()
    comp.token = comp.did.Dtoken + comp.complaint_issue.issue_token + str(comp.id)
    comp.save()
    #complaint(uname=user,did=dep,issue=issue1,crictcality=crict,img=avatar_file,complaint_issue=workunits).save()
    return redirect("userhomepage")

@allowed_users(allowed_roles=['hod'])
# @login_required(login_url='hodlogin')
def updateatempt(request,taskid):
    workunits = attempts.objects.get(id=taskid)
    list2=championdata.objects.all()
    context={"list2":list2,"workunits":workunits}
    return render(request,"staf/updateformview.html",context)

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def accountdateupdate(request,taskid):
    date=request.POST['accdate']
    up=attempts.objects.get(id=taskid)
    at=complaint.objects.get(id=up.complid.id)
    at.accountdate=date
    up.count=up.count+1
    up.save()
    at.save()
    print(date)
    return redirect("stafhomepage")


def championloginpage(request):
    return render(request,"champion/championloginpage.html")

def championlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.filter(username = username)[0]
    except:
        messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
        return redirect("championloginpage")

    if championdata.objects.filter(user = User.objects.filter(username = username)[0]).exists():
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect("championhomepage")
    messages.add_message(request, messages.INFO, "invalid credentials ! check username and password")
    return redirect(request.META["HTTP_REFERER"])

@allowed_users(allowed_roles=['champion'])
# @login_required(login_url='championlogin')
def championhomepage(request):
    if request.user.is_superuser:
        messages.add_message(request,messages.INFO,"you must login as staff")
        logout(request)
        return redirect("championloginpage")
    championname =request.user.username
    champion_id = User.objects.get(username=championname)
    championlogin_id = championdata.objects.get(user = champion_id)
    workunits = attempts.objects.filter(complid__cid = championlogin_id,count__lt=4,complid__status=False)
    print(workunits)
    #wait 5 mins ............................
    context = {'workunits' : workunits,'username' : championname}
    return render(request,"champion/championhomepage.html",context)

@allowed_users(allowed_roles=['champion'])
# @login_required(login_url='championlogin')
def championresolved(request):
    championname =request.user.username
    
    champion_id = User.objects.get(username=championname)
    championlogin_id = championdata.objects.get(user = champion_id)
    
    workunits = complaint.objects.filter(cid = championlogin_id)
    print("championname", workunits)
    context = {'workunits' : workunits,'username' : championname}
    return render(request,"champion/championresolvedpage.html",context)

@allowed_users(allowed_roles=['champion'])
# @login_required(login_url='championlogin')
def resolvedchamp(request,taskid):
    entry=complaint.objects.get(id=taskid)
    entry.status=True
    entry.save()
    return redirect("championhomepage")

@allowed_users(allowed_roles=['user'])
@login_required(login_url='userlogin')
def verified(request,taskid):
    entry=complaint.objects.get(id=taskid)
    entry.verification=True
    entry.verified_date=datetime.date.today()
    entry.save()
    return redirect("userhomepage")

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def tobeasigned(request):
    uname =request.user.id
    staff_id = stafflogindata.objects.get(user=uname)
    stafflogin_id = staff_id.did
    workunits = complaint.objects.filter(did = stafflogin_id)
    sorts = complaint.objects.filter(did = stafflogin_id,
    accountdate__lt=datetime.date.today(),verification=False).order_by('-accountdate')
    du = attempts.objects.filter(count__lt=4).filter(complid__did=stafflogin_id,
            complid__accountdate__lt=datetime.date.today())
    du1 = attempts.objects.filter(count__lt=4).filter(complid__did=stafflogin_id,
    complid__accountdate__lt=datetime.date.today(),complid__verification=False)
    over=attempts.objects.filter(count=4).filter(complid__did=stafflogin_id,
            complid__accountdate__lt=datetime.date.today())
    list2=championdata.objects.filter(did=stafflogin_id)
    print(list2)
    context = {'workunits' : workunits,'username' :request.user,'dept':stafflogin_id,
    "over":over,"sorts":sorts,"du":du,"list2":list2,"du1":du1}
    return render(request,"staf/tobeasigned.html",context)

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def asignedissues(request):
    uname =request.user.id
    staff_id = stafflogindata.objects.get(user=uname)
    stafflogin_id =staff_id.did
    atempttabel =attempts.objects.filter(complid__did=stafflogin_id,complid__accountdate__gte=datetime.date.today())
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel}
    return render(request,"staf/asignedissues.html",context)

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def resolvedissues(request):
    uname =request.user.id
    staff_id = stafflogindata.objects.get(user=uname)
    stafflogin_id = staff_id.did
    workunits = complaint.objects.filter(did = stafflogin_id)
    context = {'workunits' : workunits,'username' :request.user,'dept':stafflogin_id}
    return render(request,"staf/resolved.html",context)

@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def resolvedissuesuser(request):
    uname =request.user.id
    uname =request.user.username
    user_id = User.objects.get(username=uname)
    userlogin_id = userlogindata.objects.get(user = user_id).pk
    workunits = complaint.objects.filter(uname=userlogin_id)
    context = {'workunits' : workunits,'username' : uname}
    return render(request,"feedback/resolved.html",context)

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def championreassign(request,id):
    att=attempts.objects.get(id=id)
    comp=complaint.objects.get(id=att.complid.id)
    champid=int(request.POST['champion'])
    champdate=request.POST['champdate']
    champ=championdata.objects.get(id=champid)
    comp.cid=champ
    comp.accoundate=champdate
    comp.save()
    attempts(complid=comp,champid=champ,count=1).save()
    return redirect("stafhomepage") 

@allowed_users(allowed_roles=['user'])
# @login_required(login_url='userlogin')
def resolvedissuesuser(request):
    uname =request.user.id
    uname =request.user.username
    user_id = User.objects.get(username=uname)
    userlogin_id = userlogindata.objects.get(user = user_id).pk
    workunits = complaint.objects.filter(uname=userlogin_id)
    context = {'workunits' : workunits,'username' : uname}
    return render(request,"feedback/resolved.html",context)

@allowed_users(allowed_roles=['champion'])
# @login_required(login_url='championlogin')
def resolveissue(request,taskid):
    workunit= complaint.objects.get(id=taskid)
    resolvepic = request.FILES['rimage'] if 'rimage' in request.FILES else "noimage.png"
    workunit.resolved_img = resolvepic
    workunit.status=True
    workunit.resolved_date = datetime.date.today()
    workunit.save()
    return redirect("championhomepage")

@allowed_users(allowed_roles=['staff'])
# @login_required(login_url='staflogin')
def staffupcoming(request):
    staff=stafflogindata.objects.get(user=request.user)
    # comps=complaint.objects.filter(did=staff.did,verification=False).order_by('accountdate')
    # workunits = complaint.objects.filter(forward = True,did = hod) 
    # sorts = complaint.objects.filter(did = , forward = False).order_by('accountdate')
    # du = attempts.objects.filter(count__lt=4).filter(complid__did=hod)
    over=attempts.objects.filter(count__lt=4).filter(complid__did=staff.did,complid__verification=False,
            complid__accountdate__gte=datetime.date.today(),complid__crictcality=False)
    issues1=issues.objects.filter(issuedepartment=staff.did)
    comps=complaint.objects.filter(accountdate__gte=datetime.date.today(),did=staff.did)
    print(comps)
 
    return render(request,"staf/upcoming.html",{'comps':comps,'issues':issues1})

def hodtobeassigned(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    print(hod)
    units = complaint.objects.filter(did__in = hod,crictcality=True) 
    workunits = complaint.objects.filter(forward = True,did__in = hod) 
    sorts = complaint.objects.filter(did__in = hod, forward = True).order_by('accountdate')
    du = attempts.objects.filter(count__lt=4).filter(complid__did__in=hod)
    over=attempts.objects.filter(count=4).filter(complid__did__in=hod,
            complid__accountdate__lt=datetime.date.today())
    list2=department.objects.filter(hod=hodlogin_id)
    context = {'workunits' : workunits,'username' :request.user,'dept':hod,
    "over":over,"sorts":sorts,"du":du,'list2':list2}
    return render(request,"hod/hodtobeasigned.html",context)

def hodasignedissues(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.filter(hod = staff_id)
    atempttabel =attempts.objects.filter(complid__did__in=stafflogin_id,complid__accountdate__gte=datetime.date.today(),complid__forward=True)
    print(atempttabel)
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel,'dept1':hod}
    return render(request,"hod/assignedissues.html",context)

def assignfilter(request,taskid):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.get(id = taskid)
    print(stafflogin_id)
    atempttabel =attempts.objects.filter(complid__did=stafflogin_id,complid__accountdate__gte=datetime.date.today(),complid__forward=True)
    print(atempttabel)
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel,'dept1':hod}
    return render(request,"hod/assignedissues.html",context)



def hodresolvedissues(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.filter(hod = staff_id)
    workunits = complaint.objects.filter(did__in = stafflogin_id, forward=True)
    context = {'workunits' : workunits,'username' :request.user,'dept':stafflogin_id,'dept1':hod}
    return render(request,"hod/hodresolved.html",context)

def resolvedfilter(request,taskid):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.get(id = taskid)
    workunits = complaint.objects.filter(did = stafflogin_id, forward=True)
    context = {'workunits' : workunits,'username' :request.user,'dept':stafflogin_id,'dept1':hod}
    return render(request,"hod/hodresolved.html",context)

def hodfilter(request,taskid):
    hod = department.objects.get(id=taskid)
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    units = complaint.objects.filter(did = hod,crictcality=True) 
    workunits = complaint.objects.filter(forward = True,did = hod) 
    sorts = complaint.objects.filter(did = hod, forward = True).order_by('accountdate')
    du = attempts.objects.filter(count__lt=4).filter(complid__did=hod)
    over=attempts.objects.filter(count=4).filter(complid__did=hod,
            complid__accountdate__lt=datetime.date.today())
    list2=department.objects.filter(hod=hodlogin_id)
    context = {'workunits' : workunits,'username' :request.user,'dept':hod,
    "over":over,"sorts":sorts,"du":du,'list2':list2}
    return render(request,"hod/hodtobeasigned.html",context)

def hodstaffassigned(request):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.filter(hod = staff_id)
    atempttabel =attempts.objects.filter(complid__did__in=stafflogin_id,complid__accountdate__gte=datetime.date.today(),complid__forward=False)
    print(atempttabel)
    list2=stafflogindata.objects.filter(did__in=stafflogin_id)
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel,"dept1":list2,"dept2":hod}
    return render(request,"hod/hodstaff.html",context)

def depfilter(request,taskid):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)
    stafflogin_id = department.objects.get(id = taskid)
    atempttabel =attempts.objects.filter(complid__did=stafflogin_id,complid__accountdate__gte=datetime.date.today(),complid__forward=False)
    print(atempttabel)
    list2=stafflogindata.objects.filter(did=stafflogin_id)
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel,"dept1":list2,"dept2":hod}
    return render(request,"hod/hodstaff.html",context)

def stafffilter(request,taskid):
    hodname =request.user.username
    hod_id = User.objects.get(username=hodname)
    hodlogin_id = HODlogindata.objects.get(user = hod_id)
    hod = department.objects.filter(hod=hodlogin_id)
    uname =request.user.id
    staff_id = HODlogindata.objects.get(user=uname)

    staf=stafflogindata.objects.get(id=taskid).did
    stafflogin_id = department.objects.get(id = staf.id)

    atempttabel =attempts.objects.filter(complid__did=staf,complid__accountdate__gte=datetime.date.today(),complid__forward=False,complid__staff__id=taskid)
    print(atempttabel)
    list2=stafflogindata.objects.filter(did=staf)
    context = {'username' :request.user,'dept':stafflogin_id,'att':atempttabel,"dept1":list2,"dept2":hod}
    return render(request,"hod/hodstaff.html",context)