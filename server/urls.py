from django.conf.urls import patterns, url

from server import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'send_sms', views.send_sms, name='send_sms'),
    url(r'periodic_check', views.periodic_check, name='periodic_check'),
    url(r'periodic_get_surveys', views.periodic_get_surveys, name='periodic_get_surveys'),
)
