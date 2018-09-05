from django.conf.urls import url
from . import views
urlpatterns=[
url(r'^index/$',views.index,name='index'),
url(r'^index/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.pre_or_next_index,name='pre_or_next_index'),
url(r'^index/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$',views.lun_info,name='lun_info'),
url(r'^lun/(?P<lun_id>[0-9]+)/$',views.lun_vm_info,name='lun_vm_info'),

]
