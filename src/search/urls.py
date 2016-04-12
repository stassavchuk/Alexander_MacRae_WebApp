from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^agreements/$', views.agreements, name='agreements'),
    url(r'^sec_filings/$', views.sec_filings, name='sec_filings'),
    url(r'^filers/$', views.filers, name='filers'),

    url(r'^test/$', views.test_view, name='test'),
    url(r'^test-1/$', views.test_view, name='sort-test'),
    url(r'^test-2/$', views.test_view, name='filter-test'),

    url(r'^test/$', views.test_view, name='test'),

    url(r'^result/(?P<res_type>.*)$', views.test_view, name='result'),
]
