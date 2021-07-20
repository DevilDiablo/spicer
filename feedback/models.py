from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.


class HODlogindata(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username

class Meta:
    unique_together=[" HODlogindata","userlogindata","stafflogindata","championdata"]
    
class department(models.Model):
    Dname=models.CharField(max_length=50)
    Dtoken = models.CharField(max_length=4,blank=True, null=True,unique=True)
    hod=models.ForeignKey(HODlogindata, on_delete=models.DO_NOTHING)
    dimg=models.ImageField(null=True, blank=True,upload_to='departmentimgs/')

    def __str__(self):
        return self.Dname

class userlogindata(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username

class stafflogindata(models.Model):
    did=models.ForeignKey(department,on_delete=models.DO_NOTHING,null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username

class championdata(models.Model):
    did=models.ForeignKey(department,on_delete=models.DO_NOTHING,null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.user.username

class issues(models.Model):
    issuename=models.CharField(max_length=100)
    issuedesc=models.CharField(max_length=255)
    issuedepartment=models.ForeignKey(department,on_delete=models.DO_NOTHING,null=True, blank=True)
    issueimg=models.ImageField(null=True, blank=True,upload_to='issuesimgs/',height_field='issueimg_height',width_field='issueimg_width')
    issueimg_height = models.IntegerField(default=200,blank=True, null=True)
    issueimg_width = models.IntegerField(default=200,blank=True, null=True)
    issue_token = models.CharField(max_length=4,blank=True, null=True,unique=True)
    
    def __str__(self):
        return '{} {} {}'.format(self.id,self.issuedepartment, self.issuename)

class complaint(models.Model):
    token=models.CharField(max_length=100,null=True,blank=True)
    uname=models.ForeignKey(userlogindata, on_delete=models.DO_NOTHING)
    did=models.ForeignKey(department,on_delete=models.DO_NOTHING,null=True)
    cid=models.ForeignKey(championdata,on_delete=models.DO_NOTHING,null=True,blank=True)
    opendate=models.DateField(auto_now=False, auto_now_add=True)
    accountdate=models.DateField(null=True,blank=True)
    issue=models.CharField(max_length=500)
    corrective=models.CharField(max_length=400,blank=True)
    status=models.BooleanField(default=False)
    update = models.CharField(max_length=255,null=True,blank=True)
    verification=models.BooleanField(default=False)
    crictcality=models.BooleanField(default=False)
    forward=models.BooleanField(default=False)
    img = models.ImageField(null=True, blank=True,upload_to='userissuesimgs/', default='userissuesimgs/noimage.png')
    resolved_img = models.ImageField(null=True, blank=True,upload_to='resolvedimgs/')
    complaint_issue = models.ForeignKey(issues,on_delete=models.DO_NOTHING)
    resolved_date = models.DateField(null=True,blank=True)
    resolved_txt = models.CharField(max_length=255,null=True,blank=True)
    verified_date=models.DateField(null=True,blank=True)  
    staff=models.ForeignKey(stafflogindata,on_delete=models.DO_NOTHING,null=True,blank=True)
    def __str__(self):
        return '{} {} {} {}'.format(self.id,self.did.Dname, self.accountdate,self.token)

    def get_token(self):
        t = self.did.Dtoken + self.complaint_issue.issue_token + str(self.id)
        return t

class attempts(models.Model):
    complid=models.ForeignKey(complaint,on_delete=models.DO_NOTHING)
    champid=models.ForeignKey(championdata,on_delete=models.DO_NOTHING)
    count=models.IntegerField()

    def __str__(self):
        return '{} {} {} {}'.format(self.complid.id,self.complid.did.Dname,self.champid.user.username,self.count)

