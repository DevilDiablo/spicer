from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'maintenance'

urlpatterns=[
    path('testerloginpage/',testerloginpage,name = "testerloginpage"),
    path('testerlogin/',testerlogin,name="testerlogin"),
    path('testerhomepage/',testerhomepage1,name = "testerhomepage1"),
    path('machinedetail/<int:machine_id>/',machinedetail,name="machinedetail"),
    path('testerhomepage/<int:machine_id>/<int:assembly_id>/',assemblydetail,name="assemblydetail"),
    path('testerhomepage/<int:machine_id>/<int:assembly_id>/<int:part_id>/',partdetail,name="partdetail"),
    path('updaterange/<int:stanid>/',updaterange,name="updaterange"),
    path('updatebin/<int:stanid>/',updatebinary,name="updatebin"),
    path('updateryb/<int:stanid>/',updaterybvalue,name="updateryb"),
    path('updateval/<int:stanid>/',updateval,name="updateval"),
    #####################################################################
    path('rewieverloginpage/',reviewerloginpage,name = "reviewerloginpage"),
    path('reviewerlogin/',reviewerlogin,name="reviewerlogin"),
    path('reviewerhomepage/',reviewerhomepage,name = "reviewerhomepage"),
    path('machinedetailrev/<int:machine_id>/',machinedetailrev,name="machinedetailrev"),
    path('checkdetails/<int:taskid>/',checkdetails,name="checkdetails"),
    path('standdetailview/<int:taskid>/',standdetailview,name="standdetailview"),
    path('standapprove/<int:standid>/<int:stid>/',standapprove,name="standapprove"),
    ######################################################################
    path('hodloginpage/',hodloginpage,name = "hodloginpage"),
    path('hodlogin/',hodlogin,name="hodlogin"),
    path('hodhomepage/',hodhomepage,name="hodhomepage"),
    path('machinedetailhod/<int:machine_id>/',machinedetailhod,name="machinedetailhod"),
    path('checkdetailshod/<int:taskid>/',checkdetailshod,name="checkdetailshod"),
    path('standdetailviewhod/<int:taskid>/',standdetailviewhod,name="standdetailviewhod"),
    path('standapproved/<int:taskid>/',standapproved,name="standapproved"),





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)