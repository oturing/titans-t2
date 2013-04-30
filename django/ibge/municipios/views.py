
from .models import Municipio, MesoRegiao, REGIOES, UFS

from django import http
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class HomeListView(ListView):
    queryset = [dict(id=id, nome=nome) for id, nome in REGIOES]
    template_name='municipios/home.html'

class UFListView(ListView):
    queryset = [dict(sigla=sigla, nome=nome) for sigla, nome in sorted(UFS.items())]
    template_name='municipios/ufs.html'

class MunicipioListView(ListView):
    def get_queryset(self):
        queryset = Municipio.objects.all()
        if len(self.args) > 0:
            uf = self.args[0]
            queryset = queryset.filter(uf=uf)
        return queryset

class MunicipioDetailView(DetailView):
    model = Municipio
