from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class Customer(models.Model):
    '''Пользователь'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField("Номер телефона", max_length=255)
    address = models.CharField("Адрес", max_length=255)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Category(models.Model):
    '''Категория'''
    name = models.CharField("Имя категории", max_length=255)
    slug = models.SlugField("URL", unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    '''Товар'''
    title = models.CharField("Наименование", max_length=255)
    slug = models.SlugField("URL", unique=True)
    image = models.ImageField('Изображение', blank=True, upload_to='uploads/img/')
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0.00)
    description = models.TextField('Описание', blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    is_available = models.BooleanField('Доступен', default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class SmartPhone(Product):
    '''Смартфоны'''
    os = models.CharField('Операционная система', max_length=255, blank=True)
    display = models.CharField('Экран', max_length=255, blank=True)
    camera = models.CharField('Камера', max_length=255, blank=True)
    memory = models.CharField('Память', max_length=255, blank=True)
    battery = models.CharField('Аккумулятор', max_length=255, blank=True)
    cpu = models.CharField('Процессор', max_length=255, blank=True)
    sim = models.CharField('SIM-карты', max_length=255, blank=True)
    communication = models.CharField('Стандарты связи', max_length=255, blank=True)
    weight = models.CharField('Вес', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

    def __str__(self) -> str:
        return f'{self.category.name} {self.title}'


class Notebook(Product):
    '''Ноутбуки'''
    os = models.CharField('Операционная система', max_length=255, blank=True)
    display = models.CharField('Экран', max_length=255, blank=True)
    graphic = models.CharField('Видеокарта', max_length=255, blank=True)
    memory = models.CharField('Память', max_length=255, blank=True)
    battery = models.CharField('Аккумулятор', max_length=255, blank=True)
    cpu = models.CharField('Процессор', max_length=255, blank=True)
    weight = models.CharField('SIM-карты', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    def __str__(self) -> str:
        return f'{self.category.name} {self.title}'



class CartProduct(models.Model):
    '''Товары в корзине'''
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Пользователь")
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE,
                              verbose_name="Корзина", related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField("Количество", default=1)
    final_price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return "Продукт: {} (Для корзины)".format(self.product.title)


class Cart(models.Model):
    '''Корзина'''
    onwer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Владелец")
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveBigIntegerField("Количество", default=0)
    final_price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return str(self.id)
