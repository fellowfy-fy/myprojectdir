from django.db import models
import random
import string
from django.urls import reverse
from django.utils.text import slugify
from myproject import settings

def rand_slug():
    """
    Generates a random slug consisting of 3 characters from the set of ASCII letters and digits.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
    vin = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    car_image = models.ImageField("Изображение", upload_to="cars/images/%Y/%m/%d/")
    
    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
    
    def __str__(self):
        return f"{self.brand} {self.model} (VIN: {self.vin})"
    
class Order(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(auto_now_add=True)
    slug = models.SlugField("URL", max_length=200, null=True, blank=True)
    component_image = models.ImageField("Изображение", upload_to="components/images/%Y/%m/%d/")
    
    class Meta:
        verbose_name = 'Заказ на запчасть'
        verbose_name_plural = 'Заказы на запчасти'


class Answer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    manufacturer = models.CharField("Производитель", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quality = models.CharField("Качество",max_length=100)
    guarantee = models.CharField("Гарантия", max_length=100)
    status = models.CharField("Состояние", max_length=100)
    delivery = models.CharField("Доставка", max_length=100)
    code = models.CharField("Номер детали", max_length=100)
    answer_image = models.ImageField("Изображение", upload_to="answers/images/%Y/%m/%d/")
    
    
    class Meta:
        verbose_name = 'Ответ на заказ'
        verbose_name_plural = 'Ответы на заказ'
