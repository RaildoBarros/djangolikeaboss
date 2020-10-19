from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import ItemPedidoForm, ItemDoPedidoModelForm
from .models import Venda, ItemDoPedido
import logging

logger = logging.getLogger('django')


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

class NovoPedido(View):
    def get(self, request):
        return render(request, 'vendas/novopedido.html')

    def post(self, request):
        data = {}
        data['form_item'] = ItemPedidoForm()
        data['numero'] = request.POST['numero']
        data['desconto'] = float(request.POST['numero'].replace(',','.'))
        data['venda_id'] = request.POST['venda_id']

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
            venda.desconto = data['desconto']
            venda.numero = data['numero']
            venda.save()
        else:
            venda = Venda.objects.create(numero=data['numero'], desconto=data['desconto'])

        itens = venda.itemdopedido_set.all()
        data['venda'] = venda
        data['itens'] = itens
        return render(request, 'vendas/novopedido.html', data)

class NovoItemPedido(View):
    def get(self, request, pk):
        pass

    def post(self, request, venda):
        data = {}

        item = ItemDoPedido.objects.filter(produto_id=request.POST['produto_id'], venda_id=venda)
        if item:
            data['mensagem'] = 'Item já incluído no pedido, por favor edite o item!'
            item = item[0]
        else:
            item = ItemDoPedido.objects.create(
                produto_id=request.POST['produto_id'], quantidade=request.POST['quantidade'],
                desconto=request.POST['desconto'], venda_id=venda)

        data['item'] = item
        data['form_item'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(request, 'vendas/novopedido.html', data)

class ListaVendas(View):
    def get(self, request):
        logger.debug('Acessaram a listagem de vendas')
        vendas = Venda.objects.all()
        count_vendas = vendas.count()
        return render(request, 'vendas/listavendas.html', {'vendas': vendas, 'count_vendas': count_vendas})

class EditPedido(View):
    def get(self, request, venda):
        data = {}
        venda = Venda.objects.get(id=venda)
        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemdopedido_set.all()

        return render(request, 'vendas/novopedido.html', data)

class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(request, 'vendas/deletepedidoconfirm.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('listavendas')

class DeleteItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        return render(request, 'vendas/deleteitempedidoconfirm.html', {'item_pedido': item_pedido})

    def post(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        venda_id = item_pedido.venda.id
        item_pedido.delete()
        return redirect('editpedido', venda=venda_id)

class EditItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        form = ItemDoPedidoModelForm(instance=item_pedido)
        return render(request, 'vendas/edititempedido.html', {'item_pedido': item_pedido, 'form': form})

    def post(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        item_pedido.quantidade = request.POST['quantidade']
        item_pedido.desconto = request.POST['desconto']
        item_pedido.save()

        venda_id = item_pedido.venda.id
        return redirect('editpedido', venda=venda_id)