from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Car(models.Model):
    boilerplate = models.CharField(max_length=12)
    creation_date = models.DateField('creation date')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    def __str__(self):
        return self.boilerplate