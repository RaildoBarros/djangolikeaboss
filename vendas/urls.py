from django.urls import path
from .views import (
    DashboardView, NovoPedido, NovoItemPedido, ListaVendas,
    EditPedido, DeletePedido, DeleteItemPedido, EditItemPedido
)

urlpatterns = [
    path('', ListaVendas.as_view(), name="listavendas"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('novopedido/', NovoPedido.as_view(), name="novopedido"),
    path('editpedido/<int:venda>/', EditPedido.as_view(), name="editpedido"),
    path('deletepedido/<int:venda>/', DeletePedido.as_view(), name="deletepedido"),
    path('deleteitempedido/<int:item>/', DeleteItemPedido.as_view(), name="deleteitempedido"),
    path('edititempedido/<int:item>/', EditItemPedido.as_view(), name="edititempedido"),
    path('novoitempedido/<int:venda>/', NovoItemPedido.as_view(), name="novoitempedido"),
]