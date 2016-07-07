from django.conf.urls import url
from sixerrapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^test', views.test, name='test'),
    url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
    url(r'^create_gig/$', views.create_gig, name='create_gig'),
    url(r'^edit_gig/(?P<id>[0-9]+)/$', views.edit_gig, name='edit_gig'),
    url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
]
