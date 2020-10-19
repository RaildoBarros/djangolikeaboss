from django.test import TestCase
from vendas.models import Venda

from produtos.models import Produto

from vendas.models import ItemDoPedido


class VendaTestCase(TestCase):
    def setUp(self):
        # self.venda = Venda.objects.create(numero="123", desconto=10, status='PB')
        self.venda = Venda.objects.create(numero="123", desconto=10)
        self.produto = Produto.objects.create(descricao="Produto 1", preco=10)

    def test_verifica_num_vendas(self):
        """ Verifica se o total de vendas é igual a 1 """
        assert Venda.objects.all().count() == 1

    def test_valor_venda(self):
        """ Verifica valor total da venda """
        ItemDoPedido.objects.create(venda=self.venda, produto=self.produto, quantidade=10, desconto=10)

        assert self.venda.valor == 80

    def test_desconto(self):
        assert self.venda.desconto == 10

    def test_item_incluido_lista_itens(self):
        item = ItemDoPedido.objects.create(venda=self.venda, produto=self.produto, quantidade=1, desconto=0)
        self.assertIn(item, self.venda.itemdopedido_set.all())

    def test_checa_nfe_nao_emitida(self):
        self.assertFalse(self.venda.nfe_emitida)

    # Todo: Implementar status primeiro
    # def test_checa_status(self):
    #     self.venda.status = 'PC'
    #     self.venda.save()
    #     self.assertEqual(self.venda.status, 'PB')
