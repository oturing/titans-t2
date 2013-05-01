from django.conf.urls import patterns, include, url

from . import api # views que produzem JSON

from .views import HomeListView, UFListView, MunicipioListView, MunicipioDetailView

urlpatterns = patterns('',
    #url(r'^api/uf/([A-Za-z]{2})/', MunicipioPorUFListView.as_view()),
    url(r'^$', HomeListView.as_view(), name='home'),
    url(r'^ufs/$', UFListView.as_view(), name='ufs'),
    url(r'^munis/([A-Z]{2})$', MunicipioListView.as_view(), name='munis'),
    url(r'^muni/(?P<pk>\d+)/$', MunicipioDetailView.as_view(), name='muni_detail'),
    url(r'^api/regiao/(\d)/', api.UFListView.as_view()),
    url(r'^api/uf/([A-Z]{2})/', api.MesoRegiaoListView.as_view()),
    url(r'^api/mesoreg/(?P<meso>\d+)/', api.MunicipioListView.as_view()),
    url(r'^api/uf$', api.UFListView.as_view()),
    url(r'^api/muni', api.MunicipioListView.as_view()),
    url(r'^api/regiao', api.RegiaoListView.as_view()),
    url(r'^api/mesoreg', api.MesoRegiaoListView.as_view()),
)

