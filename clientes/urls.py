from django.urls import path
from .views import persons_list, api, APICBV
from .views import persons_new
from .views import persons_update
from .views import persons_delete
from .views import HomePageView, MyView, PersonList, PersonDetail, PersonCreate, PersonUpdate, PersonDelete, ProdutoBulk
from django.views.generic.base import TemplateView


urlpatterns = [
    path('api/', api, name="api"),
    path('apicbv/', APICBV.as_view(), name="apicbv"),

    path('list/', persons_list, name="person_list"),
    path('new/', persons_new, name="person_new"),
    path('update/<int:id>/', persons_update, name="persons_update"),
    path('delete/<int:id>/', persons_delete, name="persons_delete"),
    path('home2/', TemplateView.as_view(template_name='home2.html')),
    path('home3/', HomePageView.as_view()),
    path('view/', MyView.as_view()),
    path('person_list/', PersonList.as_view(), name='person_list'),
    path('person_detail/<int:pk>', PersonDetail.as_view(), name='person_detail'),
    path('person_create/', PersonCreate.as_view(), name='person_create'),
    path('person_update/<int:pk>', PersonUpdate.as_view(), name='person_update'),
    path('person_delete/<int:pk>', PersonDelete.as_view(), name='person_delete'),
    path('person_bulk/', ProdutoBulk.as_view(), name='person_bulk'),
]