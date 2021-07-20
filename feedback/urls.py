from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',homepageview,name = "homepage"),
    path('userloginpage/',userloginpage,name = "userloginpage"),
    path('userlogin/',userlogin,name="userlogin"),
    path('userhomepage/',userhomepage,name = "userhomepage"),
    path('logout/',logoutuser,name="logout"),
    path('feedback/',feedbackpage,name="feedbackform"),
    path('myfeedback/',myfeedbackpage,name="myfeedbackform"),
    path('feedbackvalidate/',feedbackval,name="form"),    
    path('stafloginpage/',stafloginpage,name = "stafloginpage"),
    path('staflogin/',staflogin,name="staflogin"),
    path('stafhomepage/',stafhomepage,name = "stafhomepage"),
    path('hodloginpage/',hodloginpage,name = "hodloginpage"),
    path('hodlogin/',hodlogin,name="hodlogin"),
    path('hodhomepage/',hodhomepage,name = "hodhomepage"),
    path('emaillogin/',emaillog,name="emaillogin"),

    path('editform/<int:taskid>/',editformview,name="editformview"),
    path('updateatempt/<int:taskid>/',updateatempt,name="updateatempt"),
    
    path('championlogin/',championlogin,name="championlogin"),
    path('championloginpage/',championloginpage,name = "championloginpage"),
    path('championhomepage/',championhomepage,name = "championhomepage"),
    path('championresolved/',championresolved,name = "championresolved"),
    

    path('edituserform/<int:taskid>/',edituserform,name="edituserform"),
    path('saveuserform/<int:taskid>/',saveuserform,name="saveuserform"),

    path('atemptupdate/<int:taskid>/',formsave2,name="atemptupdate"),
    path('formupdate/<int:taskid>/',formsave1,name="formupdate"),
    path('forwadform/<int:taskid>/',fwdform,name="forwardform"),

    path('atemptupdate/<int:taskid>/',formsave2,name="atemptupdate"),
    path('forwadform/<int:taskid>/',fwdform,name="forwardform"),


    path('allisues/<int:taskid>/',allissues,name="allissues"),
    path('dateupdate/<int:taskid>/',accountdateupdate,name="dateupdate"),

    # this is for hod

    path('editformhod/<int:taskid>/',editformviewhod,name="editformviewhod"),
    path('formupdatehod/<int:taskid>/',formsave1hod,name="formupdatehod"),
    path('deparetmentshod/',hoddepartment,name="departments"),
    path('hodtobeasigned/',hodtobeassigned,name="hodtobeasigned"),
    path('hodasignedissues/',hodasignedissues,name="hodasignedissues"),
    path('hodresolvedissues/',hodresolvedissues,name="hodresolvedissues"),
    path('assignfilter/<int:taskid>/',assignfilter,name="assignfilter"),
    path('resolvedfilter/<int:taskid>/',resolvedfilter,name="resolvedfilter"),
    path('hodstaffassigned/',hodstaffassigned,name="hodstaffassigned"),
    path('depfilter/<int:taskid>/',depfilter,name="depfilter"),
    path('stafffilter/<int:taskid>/',stafffilter,name="stafffilter"),

    
#this is for resolved for champion
    path('resolvedchamp/<int:taskid>/',resolvedchamp,name="resolvedchamp"),
    path('verified/<int:taskid>/',verified,name="verified"),
    path('resolveissue/<int:taskid>/',resolveissue,name="resolveissue"),
    path('updatestatus/<int:taskid>/',updatestatus,name="updatestatus"),

    


#nav bar content for staff person  
    path('tobeasigned/',tobeasigned,name="tobeasigned"),
    path('asignedissues/',asignedissues,name="asignedissues"),
    path('resolvedissues/',resolvedissues,name="resolvedissues"),
    path('resolvedissuesuser/',resolvedissuesuser,name="resolvedissuesuser"),
    path('staffupcoming/',staffupcoming,name="staffupcoming"),
    path('reassign/<int:id>/',championreassign,name="reassign"),
    path('hodfilter/<int:taskid>/',hodfilter,name="hodfilter"),

    


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)