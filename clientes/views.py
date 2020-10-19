from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person
from produtos.models import Produto
from vendas.models import Venda
from .forms import PersonForm


from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


@login_required
def persons_list(request):
    nome = request.GET.get('nome', None)
    sobrenome = request.GET.get('sobrenome', None)
    checkbox = request.GET.get('checkbox', None)
    radio = request.GET.get('radio', None)
    select = request.GET.get('select', None)

    # if checkbox == 'on':
    #     persons = Person.objects.filter()

    if nome or sobrenome:
        persons = Person.objects.filter(first_name=nome) | Person.objects.filter(last_name=sobrenome)
    else:
        persons = Person.objects.all()

    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})



class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minha_variavel'] = 'Olá, seja bem vindo ao curso de Django!'
        return context
class MyView(View):

    def get(self, request, *args, **kwargs):
        # return HttpResponse('Olá pessoal!')
        return render(request, 'home3.html')

# Herda de LoginRequiredMixin para exigir autenticação
class PersonList(LoginRequiredMixin, ListView):
    model = Person

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        primeiro_acesso = self.request.session.get('primeiro_acesso', False)
        if not primeiro_acesso:
            context['message'] = 'Seja bem vindo ao seu primeiro acesso hoje!'
            self.request.session['primeiro_acesso'] = True
        else:
            context['message'] = 'Você já acessou hoje!'

        return context


class PersonDetail(DetailView):
    model = Person

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Person.objects.select_related('doc').get(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['vendas'] = Venda.objects.filter(
            pessoa_id=self.object.id)
        return context

class PersonCreate(CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age','salary', 'bio', 'photo']
    success_url = '/clientes/person_list/'

class PersonUpdate(UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'age','salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list')

class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('clientes.deletar_clientes',)

    model = Person
    # success_url = reverse_lazy('person_list')

    def get_success_url(self):
        reverse_lazy('person_list')

class ProdutoBulk(View):
    def get(selfself, request):
        produtos = ['Banana', 'Maçã', 'Limão', 'Laranja', 'Pera', 'Melancia']
        list_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            list_produtos.append(p)
        Produto.objects.bulk_create(list_produtos)

def api(request):
    a = {'nome': 'Raildo', 'idade': 29, 'salario': 20000}
    produto = Produto.objects.last()
    b = model_to_dict(produto)

    l = []
    produtos = Produto.objects.all()
    for produto in produtos:
        l.append(model_to_dict(produto))

    return JsonResponse(l, status=200, safe=False)

class APICBV(View):
    def get(self, request):
        data = {'nome': 'Raildo'}

        produto = Produto.objects.last()
        b = model_to_dict(produto)

        l = []
        produtos = Produto.objects.all()
        for produto in produtos:
            l.append(model_to_dict(produto))

        return JsonResponse(l, status=200, safe=False)

