from django.contrib import admin
from .actions import nfe_emitida, nfe_nao_emitida

from .models import Venda, ItemDoPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemDoPedido
    extra = 1

class VendaAdmin(admin.ModelAdmin):
    list_filter = ('pessoa__doc','pessoa__salary')
    list_display = ('id', 'pessoa', 'nfe_emitida',)
    readonly_fields = ('valor',)
    autocomplete_fields = ('pessoa',)
    search_fields = ('id', 'pessoa__first_name', 'pessoa__doc__num_doc')
    actions = [nfe_emitida, nfe_nao_emitida]
    inlines = [ItemPedidoInline]

admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)
