from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse



def get_model_for_count(*models_names):
    return [models.Count(model_name) for model_name in models_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={"ct_model": ct_model, "slug": obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:6]
            products.extend(model_products)
                
        return products



class LatestProducts:

    objects = LatestProductsManager()


# получение категори и подсчет товаров в этой категории
class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_category_for_navbar(self):
        models = get_model_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models).values())

        return [dict(name=c['name'], slug=c['slug'], 
                    count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]
    
    #print(Category.objects.get_category_for_navbar())
    #[{'name': 'Ноутбуки', 'slug': 'notebooks', 'count': 2}, {'name': 'Смартфоны', 'slug': 'smartphones', 'count': 2}]


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
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    '''Товар'''
    title = models.CharField("Наименование", max_length=255)
    slug = models.SlugField("URL", unique=True)
    image = models.ImageField('Изображение', blank=True, upload_to='img/')
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


    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Notebook(Product):
    '''Ноутбуки'''
    os = models.CharField('Операционная система', max_length=255, blank=True)
    display = models.CharField('Экран', max_length=255, blank=True)
    graphic = models.CharField('Видеокарта', max_length=255, blank=True)
    memory = models.CharField('Память', max_length=255, blank=True)
    battery = models.CharField('Аккумулятор', max_length=255, blank=True)
    cpu = models.CharField('Процессор', max_length=255, blank=True)
    weight = models.CharField('Вес', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    def __str__(self) -> str:
        return f'{self.category.name} {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


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
        return "Продукт: {} (Для корзины)".format(self.content_object.title)


class Cart(models.Model):
    '''Корзина'''
    onwer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Владелец")
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveBigIntegerField("Количество", default=0)
    final_price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0.00)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return str(self.id)

