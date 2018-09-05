from django.shortcuts import render,get_object_or_404

# Create your views here.
from .models import Lun_info, Vm_info
import calendar
import datetime
from calendar import month_name
from dateutil.relativedelta import relativedelta
# Create index view used for show lun info
class EmployeeScheduleCalendar(calendar.HTMLCalendar):
  def __init__(self,firstweekday=0):
    self.firstweekday = firstweekday # 0 = Monday, 6 = Sunday
    self.year=datetime.datetime.now().year
    self.month=datetime.datetime.now().month
    self.day=datetime.datetime.now().day
    self.next_month=(datetime.datetime.now() + relativedelta(months=1)).month
    self.pre_month=(datetime.datetime.now() + relativedelta(months=-1)).month
    self.pre_year=(datetime.datetime.now() + relativedelta(months=-1)).year
    self.next_year=(datetime.datetime.now() + relativedelta(months=1)).year
  def formatday(self, day, weekday):
    if day == 0:
      return '<td class="noday">&nbsp;</td>' # day outside month
    elif day == datetime.datetime.now().day:
      return '<td align="center" class="%s"><div class="red"><a href="%s">%d</a></div></td>' % (self.cssclasses[weekday], '/index'+'/'+str(self.year)+'/'+str(self.month)+'/'+str(day)+'/', day)
    else:
      return '<td align="center" class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], '/index'+'/'+str(self.year)+'/'+str(self.month)+'/'+str(day)+'/', day)
  def formatmonthname(self, theyear, themonth, withyear=True):
    if withyear:
        s = '%s %s' % (month_name[themonth], theyear)
    else:
        s = '%s' % month_name[themonth]
    return '<tr><th colspan="7" class="month"><a href="%s">上一月</a>  %s  <a href="%s">下一月</a></th></tr>' % ('/index/'+str(self.pre_year)+'/'+str(self.pre_month)+'/',s,'/index/'+str(self.next_year)+'/'+str(self.next_month)+'/')
###########################################################################################################################
class EmployeeScheduleCalendar_per_or_next(calendar.HTMLCalendar):
  def __init__(self,firstweekday,current_year,current_month,current_day):
    self.firstweekday = firstweekday # 0 = Monday, 6 = Sunday
    self.year=current_year
    self.month=current_month
    self.day=current_day
#    self.day=datetime.datetime.now().day
#    self.next_month=(datetime.datetime.now() + relativedelta(months=1)).month
    if 1<current_month<12:
      self.pre_month=current_month-1
      self.next_month=current_month+1
      self.pre_year=current_year
      self.next_year=current_year
    elif current_month==1:
      self.pre_month=12
      self.next_month=2
      self.pre_year=current_year-1
      self.next_year=current_year
    else:
      self.pre_month=11
      self.next_month=2
      self.pre_year=current_year
      self.next_year=current_year+1
  def formatday(self, day, weekday):
    if day == 0:
      return '<td class="noday">&nbsp;</td>' # day outside month
#    elif day == self.day and self.month == datetime.datetime.now().month and self.year == datetime.datetime.now().year:
    elif day == self.day:
      print("ganbadei")
      return '<td align="center" class="%s"><div class="red"><a href="%s">%d</a></div></td>' % (self.cssclasses[weekday], '/index'+'/'+str(self.year)+'/'+str(self.month)+'/'+str(day)+'/', day)
    else:
      return '<td align="center" class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], '/index'+'/'+str(self.year)+'/'+str(self.month)+'/'+str(day)+'/', day)
  def formatmonthname(self, theyear, themonth, withyear=True):
    if withyear:
        s = '%s %s' % (month_name[themonth], theyear)
    else:
        s = '%s' % month_name[themonth]
    return '<tr><th colspan="7" class="month"><a href="%s">上一月</a>  %s  <a href="%s">下一月</a> <a href="%s">返回当前月</a></th></tr>' % ('/index/'+str(self.pre_year)+'/'+str(self.pre_month)+'/',s,'/index/'+str(self.next_year)+'/'+str(self.next_month)+'/','/index/'+str(datetime.datetime.now().year)+'/'+str(datetime.datetime.now().month)+'/')
###########################################################################################################################
def index(request):
  current_year=datetime.datetime.now().year
  current_month=datetime.datetime.now().month
  current_day=datetime.datetime.now().day
  time=str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)
  time_dir={'year':datetime.datetime.now().year,'month':datetime.datetime.now().month,'day':datetime.datetime.now().day}
  calendar_info = EmployeeScheduleCalendar(calendar.MONDAY)
  cal=calendar_info.formatmonth(current_year,current_month)
  try:
    result=Lun_info.objects.filter(date__year=current_year).filter(date__month=current_month).filter(date__day=current_day)[0]
  except IndexError:
    result="还没有数据产生、请核对日期后重新选择"
    calendar_info = EmployeeScheduleCalendar(calendar.MONDAY)
    cal=calendar_info.formatmonth(current_year,current_month)
    return render(request,'vm/index.html',context={'calendar_info':cal,'result':result,'time':time,'time_dir':time_dir})
  result=Lun_info.objects.filter(date__year=current_year).filter(date__month=current_month).filter(date__day=current_day).filter(lun__icontains='lun').order_by('lun')
  return render(request,'vm/index.html',context={'calendar_info':cal,'result':result,'time':time,'time_dir':time_dir})
def pre_or_next_index(request,year,month):
  current_page_year=int(year)
  current_page_month=int(month)

  if 1<current_page_month<12:
    pre_page_month=current_page_month-1
    next_page_month=current_page_month+1
    pre_page_year=current_page_year
    next_page_year=current_page_year
  elif current_page_month==1:
    pre_page_month=12
    next_page_month=2
    pre_page_year=current_page_year-1
    next_page_year=current_page_year
  else:
    pre_page_month=11
    next_page_month=2
    pre_page_year=current_page_year
    next_page_year=current_page_year+1
  calendar_info = EmployeeScheduleCalendar_per_or_next(calendar.MONDAY,current_page_year,current_page_month,'50')
  cal=calendar_info.formatmonth(current_page_year,current_page_month)
  return render(request,'vm/index_per_or_next.html',context={'calendar_info':cal})
def lun_info(request,year,month,day):
#  filter_time=year+'-'+month+'-'+day
#  filter_time=str(filter_time)
  current_page_year=int(year)
  current_page_month=int(month)
  current_page_day=int(day)

  time=str(year)+'-'+str(month)+'-'+str(day)
  time_dir={'year':int(year),'month':int(month),'day':int(day)}
  if 1<current_page_month<12:
    pre_page_month=current_page_month-1
    next_page_month=current_page_month+1
    pre_page_year=current_page_year
    next_page_year=current_page_year
  elif current_page_month==1:
    pre_page_month=12
    next_page_month=2
    pre_page_year=current_page_year-1
    next_page_year=current_page_year
  else:
    pre_page_month=11
    next_page_month=2
    pre_page_year=current_page_year
    next_page_year=current_page_year+1
#  try:
#    result=Lun_info.objects.get(date__year=year).get(date__month=month).get(date__day=day)
#  except:
#    return render()
  try:
    result=Lun_info.objects.filter(date__year=current_page_year).filter(date__month=current_page_month).filter(date__day=current_page_day)[0]
  except IndexError:
    result="当天没有收集数据"
    calendar_info = EmployeeScheduleCalendar_per_or_next(calendar.MONDAY,current_page_year,current_page_month,current_page_day)
    cal=calendar_info.formatmonth(current_page_year,current_page_month)
    return render(request,'vm/result_no_value.html',context={'calendar_info':cal,'result':result,'time':time,'time_dir':time_dir})
  result=Lun_info.objects.filter(date__year=current_page_year).filter(date__month=current_page_month).filter(date__day=current_page_day).filter(lun__icontains='lun').order_by('lun')
  calendar_info = EmployeeScheduleCalendar_per_or_next(calendar.MONDAY,current_page_year,current_page_month,current_page_day)
  cal=calendar_info.formatmonth(current_page_year,current_page_month)
  return render(request,'vm/result.html',context={'calendar_info':cal,'result':result,'time':time,'time_dir':time_dir})
#  return render(request,'vm/index.html',context={'calendar_info':cal})
def lun_vm_info(request,lun_id):
  vm_info=Lun_info.objects.get(id=lun_id).vm_info_set.all()
  lun_info=Lun_info.objects.get(id=lun_id)
  return render(request,'vm/vm_info.html',context={'vm_info':vm_info,'lun_info':lun_info})
