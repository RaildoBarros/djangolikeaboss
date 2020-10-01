from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Venda


class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.view_dashboard'):
            return HttpResponse('Acesso negado, você precisa de permissão!')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {}
        data['media'] = Venda.objects.media()
        data['media_desc'] = Venda.objects.media_desconto()
        data['min'] = Venda.objects.min()
        data['max'] = Venda.objects.max()
        data['n_ped'] = Venda.objects.n_ped()
        data['n_ped_nfe'] = Venda.objects.n_ped_nfe()


        return render(request, 'vendas/dashboard.html', data)
