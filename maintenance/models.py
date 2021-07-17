from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.


class tester(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class reviewer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username

class mainhodlogindata(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class machine(models.Model):
    machine_name = models.CharField(max_length=50)
    hod = models.ForeignKey(mainhodlogindata,on_delete=models.DO_NOTHING,null=True,blank=True)
    reviewer = models.ForeignKey(reviewer,on_delete=models.DO_NOTHING,null=True,blank=True)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True, null=True)

    def __str__(self):
        return self.machine_name

    def save(self, *args, **kwargs):
        h=str(self.id)
        qrcode_img = qrcode.make('https://spicer-feedback.herokuapp.com/checkqrcode/'+h+'/')
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.machine_name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class assembly(models.Model):
    machine_id = models.ForeignKey(machine, on_delete=models.DO_NOTHING)
    assembly_name = models.CharField(max_length=50)
    tester=models.ForeignKey(tester,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.assembly_name


class part(models.Model):
    part_desc = models.CharField(max_length=200)
    assembly_id = models.ForeignKey(assembly, on_delete=models.DO_NOTHING)
    machine_id = models.ForeignKey(machine, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.part_desc


class checkpoint(models.Model):
    check_desc = models.CharField(max_length=200)
    part_id = models.ForeignKey(part, on_delete=models.DO_NOTHING)
    machine_id = models.ForeignKey(machine, on_delete=models.DO_NOTHING)
    fromdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    nextdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    checked = models.BooleanField(default=False)
    freq = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.check_desc)


class standard(models.Model):
    STANDARD_TYPE = (
        ('B', 'Binary'),
        ('R', 'Range'),
        ('V', 'Value'),
        ('T', 'RYB'),
    )
    check_id = models.ForeignKey(checkpoint, on_delete=models.DO_NOTHING)
    standard_desc = models.CharField(max_length=200, null=True)
    standard_type = models.CharField(max_length=1, choices=STANDARD_TYPE)

    def __str__(self):
        return '{} {}'.format(self.standard_desc, self.standard_type)


class frequency(models.Model):
    currentdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    Fromdate = models.DateField(auto_now=False, auto_now_add=False)
    todate = models.DateField(auto_now=False, auto_now_add=False)
    checked = models.BooleanField(default=False)
    checkpoint_id = models.ForeignKey(checkpoint, on_delete=models.DO_NOTHING)
    def __str__(self):
        return '{}'.format(self.checkpoint_id)


class standard_binary(models.Model):
    frequency = models.ForeignKey(frequency, on_delete=models.DO_NOTHING, null=True, blank=True)
    standard_id = models.ForeignKey(standard, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False) 
    img = models.ImageField(null=True, blank=True, upload_to='stanbinary/')
    time = models.IntegerField(null=True, blank=True)
    approved = models.BooleanField(default=False,null=True, blank=True)
    approved_date =  models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    def __str__(self):
        return '{} {}'.format(self.standard_id, self.status)


class range_value(models.Model):
    lower_limit = models.BooleanField(default=False, null=True, blank=True)
    upper_limit = models.BooleanField(default=False, null=True, blank=True)
    less_than = models.IntegerField(null=True, blank=True)
    more_than = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return '{} {}'.format(self.lower_limit, self.upper_limit)

class standard_range(models.Model):
    frequency = models.ForeignKey(frequency, on_delete=models.DO_NOTHING, null=True, blank=True)
    standard_id = models.ForeignKey(standard, on_delete=models.DO_NOTHING)
    rangevalue = models.ForeignKey(range_value, on_delete=models.DO_NOTHING, null=True)
    value = models.IntegerField(null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='stanrange/')
    status = models.BooleanField(default=False)
    time = models.IntegerField(null=True, blank=True)
    approved = models.BooleanField(default=False,null=True, blank=True) 
    approved_date =  models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.standard_id)


class standard_value(models.Model):
    frequency = models.ForeignKey(frequency, on_delete=models.DO_NOTHING, null=True, blank=True)
    standard_id = models.ForeignKey(standard, on_delete=models.DO_NOTHING)
    value = models.IntegerField(null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='stanvalue/')
    status = models.BooleanField(default=False)
    time = models.IntegerField(null=True, blank=True)
    approved = models.BooleanField(default=False,null=True, blank=True) 
    approved_date =  models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.standard_id, self.value)


class standard_ryb(models.Model):
    frequency = models.ForeignKey(frequency, on_delete=models.DO_NOTHING, null=True, blank=True)
    standard_id = models.ForeignKey(standard, on_delete=models.DO_NOTHING)
    r = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    b = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)
    time = models.IntegerField(null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='rybimg/')
    approved = models.BooleanField(default=False,null=True, blank=True)
    approved_date =  models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.standard_id)

