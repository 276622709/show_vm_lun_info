from django.db import models

# Create your models here.
class Lun_info(models.Model):
  lun=models.CharField(max_length=200)
  all_space=models.BigIntegerField()
  free_space=models.BigIntegerField()
  date=models.DateTimeField()
class Vm_info(models.Model):
  vm_name=models.CharField(max_length=200)
  vm_id=models.CharField(max_length=200)
  vm_cpu=models.BigIntegerField()
  vm_mem=models.BigIntegerField()
  vm_disk=models.BigIntegerField()
  vm_used_space=models.BigIntegerField()
  date=models.DateTimeField()
  lun_id=models.ManyToManyField(Lun_info)
class Vm_used_space_day(models.Model):
  date=models.DateTimeField()
  vm_id=models.CharField(max_length=200)
  vm_used_space=models.BigIntegerField()
  
