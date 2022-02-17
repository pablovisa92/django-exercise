from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from .serializers import CarSerializer, BrandSerializer, ModelSerializer
from .models import Car,Brand,Model

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def car(request):
    template = loader.get_template('car/index.html')
    context = {
        'car_list': Car.objects.all(),
        'brand_list': Brand.objects.all(),
        'model_list': Model.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def carNew(request):
    template = loader.get_template('car/newCar.html')
    context = {
        'brand_list': Brand.objects.all(),
        'model_list': Model.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def carAdd(request):
    brand = Brand.objects.filter(name=request.POST['brand']).first()
    model = Model.objects.filter(name=request.POST['model']).first()
    Car.objects.create(boilerplate=request.POST['boilerplate'], brand=brand, model=model, creation_date=request.POST['creation_date'])
    return HttpResponseRedirect(reverse('car'))

def carEdit(request, boilerplate):
    template = loader.get_template('car/editCar.html')
    context = {
        'car': Car.objects.filter(boilerplate=boilerplate).first(),
        'brand_list': Brand.objects.all(),
        'model_list': Model.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def carSave(request, boilerplate):
    brand = Brand.objects.filter(name=request.POST['brand']).first()
    model = Model.objects.filter(name=request.POST['model']).first()
    Car.objects.filter(boilerplate=boilerplate).update(boilerplate=request.POST['boilerplate'], brand=brand, model=model, creation_date=request.POST['creation_date'])
    return HttpResponseRedirect(reverse('car'))

def carDelete(request, boilerplate):
    Car.objects.filter(boilerplate=boilerplate).delete()
    return HttpResponseRedirect(reverse('car'))

def carFilterByBoilerplate(request):
    template = loader.get_template('car/index.html')
    filtered_car_by_boilerplate = Car.objects.filter(boilerplate=request.POST['boilerplate']).first()
    if (filtered_car_by_boilerplate == None):
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'boilerplate_filter': request.POST['boilerplate'],
            'message_boilerplate': 'No cars found with this boilerplate.'
        }
    else:
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'boilerplate_filter': request.POST['boilerplate'],
            'filtered_car_by_boilerplate': filtered_car_by_boilerplate,
        }
    return HttpResponse(template.render(context, request))

def carFilterByDate(request):
    template = loader.get_template('car/index.html')
    filtered_cars_by_date = Car.objects.filter(creation_date__lt=request.POST['creation_date'])
    if not filtered_cars_by_date:
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'creation_date_filter': request.POST['creation_date'],
            'message_date': 'No cars found with this date.'
        }
    else:
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'creation_date_filter': request.POST['creation_date'],
            'filtered_cars_by_date': filtered_cars_by_date,
        }
    return HttpResponse(template.render(context, request))

def carSearch(request):
    template = loader.get_template('car/index.html')
    brand = Brand.objects.filter(name=request.POST['brand']).first()
    model = Model.objects.filter(name=request.POST['model']).first()
    if (request.POST['creation_date'] != ''):
        search_cars = Car.objects.filter(Q(boilerplate=request.POST['boilerplate']) | Q(brand=brand) | Q(model=model) | Q(creation_date=request.POST['creation_date']))
    else:
        search_cars = Car.objects.filter(Q(boilerplate=request.POST['boilerplate']) | Q(brand=brand) | Q(model=model))
    if not search_cars:
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'boilerplate_search': request.POST['boilerplate'],
            'brand_search': brand,
            'model_search': model,
            'creation_date_search': request.POST['creation_date'],
            'message_search': 'No cars found with this data.'
        }
    else:
        context = {
            'car_list': Car.objects.all(),
            'brand_list': Brand.objects.all(),
            'model_list': Model.objects.all(),
            'boilerplate_search': request.POST['boilerplate'],
            'brand_search': brand,
            'model_search': model,
            'creation_date_search': request.POST['creation_date'],
            'search_cars': search_cars,
        }
    return HttpResponse(template.render(context, request))

def brand(request):
    template = loader.get_template('brand/index.html')
    context = {
        'brand_list':  Brand.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def brandNew(request):
    template = loader.get_template('brand/newBrand.html')
    context = {}
    return HttpResponse(template.render(context, request))

def brandAdd(request):
    Brand.objects.create(name=request.POST['name'])
    return HttpResponseRedirect(reverse('brand'))

def brandEdit(request, name):
    template = loader.get_template('brand/editBrand.html')
    context = {
        'brand': Brand.objects.filter(name=name).first(),
    }
    return HttpResponse(template.render(context, request))

def brandSave(request, name):
    Brand.objects.filter(name=name).update(name=request.POST['name'])
    return HttpResponseRedirect(reverse('brand'))

def brandDelete(request, name):
    Brand.objects.filter(name=name).delete()
    return HttpResponseRedirect(reverse('brand'))

def brandFilter(request):
    template = loader.get_template('brand/index.html')
    brand = Brand.objects.filter(name=request.POST['brand']).first()
    filtered_brands = { 'name': brand.name, 'cars': ', '.join([car.boilerplate for car in Car.objects.filter(brand=brand)])}
    if (filtered_brands == None):
        context = {
            'brand_list': Brand.objects.all(),
            'brand_filter': brand,
            'message_filtered_brands': 'No cars found for the brand selected.'
        }
    else:
        context = {
            'brand_list': Brand.objects.all(),
            'brand_filter': brand,
            'filtered_brands': filtered_brands,
        }
    return HttpResponse(template.render(context, request))

def model(request):
    template = loader.get_template('model/index.html')
    context = {
        'model_list': Model.objects.all(),
    }
    return HttpResponse(template.render(context, request))
    
def modelNew(request):
    template = loader.get_template('model/newModel.html')
    context = {}
    return HttpResponse(template.render(context, request))

def modelAdd(request):
    Model.objects.create(name=request.POST['name'])
    return HttpResponseRedirect(reverse('model'))

def modelEdit(request, name):
    template = loader.get_template('model/editModel.html')
    context = {
        'model': Model.objects.filter(name=name).first(),
    }
    return HttpResponse(template.render(context, request))

def modelSave(request, name):
    Model.objects.filter(name=name).update(name=request.POST['name'])
    return HttpResponseRedirect(reverse('model'))

def modelDelete(request, name):
    Model.objects.filter(name=name).delete()
    return HttpResponseRedirect(reverse('model'))

def apiCars(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def apiCarsDetail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CarSerializer(car)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CarSerializer(car, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        car.delete()
        return HttpResponse(status=204)

def apiBrands(request):
    if request.method == 'GET':
        cars = Brand.objects.all()
        serializer = BrandSerializer(cars, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def apiBrandsDetail(request, pk):
    try:
        brand = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BrandSerializer(brand)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BrandSerializer(brand, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        brand.delete()
        return HttpResponse(status=204)

def apiModels(request):
    if request.method == 'GET':
        cars = Model.objects.all()
        serializer = ModelSerializer(cars, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def apiModelsDetail(request, pk):
    try:
        model = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ModelSerializer(model)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ModelSerializer(model, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        model.delete()
        return HttpResponse(status=204)