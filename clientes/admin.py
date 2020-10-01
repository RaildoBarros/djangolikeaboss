from django.contrib import admin
from .models import Person, Documento


class PersonAdmin(admin.ModelAdmin):
    # fields = (('first_name','last_name'),('age','salary'),'bio','photo','doc')
    list_display = ('first_name','last_name','age','salary','bio','tem_foto','doc')
    fieldsets = (
        ('Dados pessoais', {
             'fields': (('first_name', 'last_name'), 'doc')
          }),
        ('Dados complementares', {
            'classes': ('collapse',),
            'fields': ('age','salary','bio','photo')
        }),
    )
    list_filter = ('age','salary')
    search_fields = ('id', 'first_name',)

    def tem_foto(self, obj):
        if obj.photo:
            return 'Sim'
        else:
            return 'Não'
    tem_foto.short_description = 'Possui foto'




admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
