from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

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
            model_products = ct_model.model_class(
            )._base_manager.all().order_by('-id')[:6]
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
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c,
            self.CATEGORY_NAME_COUNT_NAME[c.name] )) for c in qs
        ]
        return data

        # OLD
        # qs = list(self.get_queryset().annotate(*models).values())

        # return [dict(name=c['name'], slug=c['slug'],
        #             count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]

        # print(Category.objects.get_category_for_navbar())
        # [{'name': 'Ноутбуки', 'slug': 'notebooks', 'count': 2}, {'name': 'Смартфоны', 'slug': 'smartphones', 'count': 2}]

class Customer(models.Model):
    '''Пользователь'''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(
        "Номер телефона", max_length=255, null=True, blank=True)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы', related_name='related_customer')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self) -> str:
        return f"Покупатель: {self.user.username}"


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

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    '''Товар'''
    title = models.CharField("Наименование", max_length=255)
    slug = models.SlugField("URL", unique=True)
    image = models.ImageField('Изображение', blank=True, upload_to='img/')
    price = models.DecimalField(
        'Цена', max_digits=9, decimal_places=2, default=0.00)
    description = models.TextField('Описание', blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    is_available = models.BooleanField('Доступен', default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class SmartPhone(Product):
    '''Смартфоны'''
    os = models.CharField('Операционная система', max_length=255, blank=True)
    display = models.CharField('Экран', max_length=255, blank=True)
    camera = models.CharField('Камера', max_length=255, blank=True)
    memory = models.CharField('Память', max_length=255, blank=True)
    battery = models.CharField('Аккумулятор', max_length=255, blank=True)
    cpu = models.CharField('Процессор', max_length=255, blank=True)
    sim = models.CharField('SIM-карты', max_length=255, blank=True)
    communication = models.CharField(
        'Стандарты связи', max_length=255, blank=True)
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
    # c = Cart.objects.create()
    # cp = CartProduct.objects.create(content_object=notebook, user=customer, cart=c, final_price=notebook.price)
    user = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Пользователь")
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE,
                             verbose_name="Корзина", related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id')  # note or phone
    qty = models.PositiveIntegerField("Количество", default=1)
    final_price = models.DecimalField(
        'Цена', max_digits=9, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return "Продукт: {} (Для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товыры в корзине'

class Cart(models.Model):
    '''Корзина'''
    # Создаем cp = CartProduct и добавляем в корзину
    # cart = Cart.objects.get(id=)
    # cart.products.add(cp)
    owner = models.ForeignKey(
        Customer, null=True, on_delete=models.CASCADE, verbose_name="Владелец")
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name="related_cart")# Будет ссылаться на Cart.id
    total_products = models.PositiveBigIntegerField("Количество", default=0)
    final_price = models.DecimalField(
        'Цена', max_digits=9, decimal_places=2, default=0.00)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs):
        #sql функции интерпретированные Django
        cart_data=self.products.aggregate(models.Sum('final_price'), models.Count('id'))
        print(cart_data) #{'final_price__sum': None, 'id__count': 0}
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        self.total_products = cart_data['id__count'] 
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'



class Order(models.Model):
    '''Заказ'''
    STATUS_NEW = 'new'
    STATUS_IN_PROGRES = 'in_progress'
    STATUS_IS_READY = 'is_ready'
    STATUS_COMPLETE = 'complete'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRES, 'Заказ в обработке'),
        (STATUS_IS_READY, 'Заказ готов'),
        (STATUS_COMPLETE, 'Заказ выполнен'),

    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Покупатель', related_name='related_orders')
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    phone = models.CharField('Телефон', max_length=20)
    cart = models.ForeignKey(Cart, verbose_name='Корзина',
                             on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField('Адрес', max_length=1024, null=True, blank=True)
    status = models.CharField(
        'Статус заказа', max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    
    buying_type = models.CharField(
        'Тип заказа', max_length=100, choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)
    comment = models.TextField('Коментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField('Дата заказа', auto_now=True)
    order_date = models.DateField('Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы' 