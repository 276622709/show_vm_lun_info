#!/usr/bin/env python  
#coding:utf-8  
from vm.models import Lun_info,Vm_info
import datetime  
from django import template  
  
register = template.Library()  

@register.filter()  
def format_value(value):  
  return round(value/1024/1024/1024,2)
@register.filter()  
def cal_diff_value(time,lun_name):
  myday=datetime.datetime(time['year'],time['month'],time['day'])
  delta = datetime.timedelta(days=-1)
  yestoday=myday+delta
  print(yestoday.year)
  print(yestoday.month)
  print(yestoday.day)
  print(lun_name)
  try:
    lun_object_yestoday=Lun_info.objects.filter(date__year=yestoday.year).filter(date__month=yestoday.month).filter(date__day=yestoday.day).filter(lun=lun_name)[0]  
  except IndexError:
    return("昨天没有数据")  
    
  lun_object_today=Lun_info.objects.filter(date__year=time['year']).filter(date__month=time['month']).filter(date__day=time['day']).filter(lun=lun_name)[0]
  reduce_value=lun_object_yestoday.free_space-lun_object_today.free_space  
  return str(round(reduce_value/1024/1024/1024,2))+"GB"
@register.filter()  
def vm_func(date,vm_show_id):
  myday=datetime.datetime(date.year,date.month,date.day)
  delta = datetime.timedelta(days=-1)
  yestoday=myday+delta
  try:
    vm_object_yestoday=Vm_info.objects.filter(date__year=yestoday.year).filter(date__month=yestoday.month).filter(date__day=yestoday.day).filter(vm_id=vm_show_id)[0]  
  except IndexError:
    return("昨天没有数据")  
  vm_object_today=Vm_info.objects.filter(date__year=date.year).filter(date__month=date.month).filter(date__day=date.day).filter(vm_id=vm_show_id)[0]
  reduce_value=vm_object_today.vm_used_space-vm_object_yestoday.vm_used_space  
  return str(round(reduce_value/1024/1024,2))+"MB"
  
