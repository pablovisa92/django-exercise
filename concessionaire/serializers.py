from rest_framework import serializers, viewsets
from .models import Car, Brand, Model

# Serializers define the API representation.
class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

    def create(self, validated_data):
        return Brand.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = ['name']
    
    def create(self, validated_data):
        return Model.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class CarSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()
    model = ModelSerializer()
    class Meta:
        model = Car
        fields = ['boilerplate', 'brand', 'model', 'creation_date']

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        model_data = validated_data.pop('model')
        Brand.objects.create(**brand_data)
        Model.objects.create(**model_data)
        validated_data['brand'] = Brand.objects.filter(name=brand_data.get('name')).first()
        validated_data['model'] = Model.objects.filter(name=model_data.get('name')).first()
        car = Car.objects.create(**validated_data)
        
        return car
    
    def update(self, instance, validated_data):
        import logging
        logger = logging.getLogger("mylogger")
        logger.info(self.context['request'].data['brand'].get('name'))
        instance.brand = Brand.objects.filter(name=self.context['request'].data['brand'].get('name')).first()
        instance.model = Model.objects.filter(name=self.context['request'].data['model'].get('name')).first()
        instance.boilerplate = validated_data.get('boilerplate', instance.boilerplate)
        instance.creation_date = validated_data.get('creation_date', instance.creation_date)
        instance.save()

        return instance

# ViewSets define the view behavior.
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer