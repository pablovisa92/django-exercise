from django.urls import include, path, re_path
from . import views
from .serializers import CarViewSet, BrandViewSet, ModelViewSet
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'models', ModelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.car, name='car'),
    path('car/new', views.carNew, name='carNew'),
    path('car/add', views.carAdd, name='carAdd'),
    path('car/edit/<str:boilerplate>', views.carEdit, name='carEdit'),
    path('car/delete/<str:boilerplate>', views.carDelete, name='carDelete'),
    path('car/save/<str:boilerplate>', views.carSave, name='carSave'),
    path('car/filterByBoilerplate', views.carFilterByBoilerplate, name='carFilterByBoilerplate'),
    path('car/filterByDate', views.carFilterByDate, name='carFilterByDate'),
    path('car/search', views.carSearch, name='carSearch'),
    path('brand', views.brand, name='brand'),
    path('brand/new', views.brandNew, name='brandNew'),
    path('brand/add', views.brandAdd, name='brandAdd'),
    path('brand/edit/<str:name>', views.brandEdit, name='brandEdit'),
    path('brand/delete/<str:name>', views.brandDelete, name='brandDelete'),
    path('brand/save/<str:name>', views.brandSave, name='brandSave'),
    path('brand/filter', views.brandFilter, name='brandFilter'),
    path('model', views.model, name='model'),
    path('model/new', views.modelNew, name='modelNew'),
    path('model/add', views.modelAdd, name='modelAdd'),
    path('model/edit/<str:name>', views.modelEdit, name='modelEdit'),
    path('model/delete/<str:name>', views.modelDelete, name='modelDelete'),
    path('model/save/<str:name>', views.modelSave, name='modelSave'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    re_path(r'^api/cars/$', views.apiCars),
    re_path(r'^api/cars/(?P<pk>[0-9]+)/$', views.apiCarsDetail),
    re_path(r'^api/brands/$', views.apiBrands),
    re_path(r'^api/brands/(?P<pk>[0-9]+)/$', views.apiBrandsDetail),
    re_path(r'^api/models/$', views.apiModels),
    re_path(r'^api/models/(?P<pk>[0-9]+)/$', views.apiModelsDetail),
]