from django.db.models import Model, CharField, ForeignKey, CASCADE, ImageField, DateTimeField, SET_NULL, JSONField
from django.db.models import IntegerField, URLField, DecimalField, BigIntegerField, TextField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models.enums import TextChoices
from parler.models import TranslatableModel, TranslatedFields


class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_number = CharField(max_length=20, null=True, blank=True, unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Category(TranslatableModel):
    class Meta:
        verbose_name_plural = 'Categories'

    translations = TranslatedFields(
        name=CharField(max_length=255)
    )
    urllib = URLField()


class Products(TranslatableModel):
    class Meta:
        verbose_name_plural = 'Products'

    translateions = TranslatedFields(
        name=CharField(max_length=200),
        description=TextField()
    )
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField(default=0)
    main_image = ImageField(upload_to='products/')
    discount = IntegerField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')

    @property
    def discount_price(self):
        return self.price - (self.price * self.discount / 100)


class ProductImage(Model):
    product = ForeignKey('apps.Products', on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='products_images/')


class Attributes(Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    product = ForeignKey('apps.Products', on_delete=CASCADE, related_name='attributes')


class Wishlist(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='wishlist')
    product = ForeignKey('apps.Products', on_delete=CASCADE, related_name='wishlist')


class OrderItem(Model):
    product = ForeignKey('apps.Products', on_delete=CASCADE, related_name='items')
    attribute = ForeignKey('apps.Attributes', on_delete=CASCADE, related_name='items', null=True, blank=True)
    quantity = IntegerField()
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='items', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)

    @property
    def total_price(self):
        base_price = self.product.price
        attribute_price = self.attribute.price if self.attribute else 0
        return (base_price + attribute_price) * self.quantity


class Order(Model):
    class OrderType(TextChoices):
        TAKE_AWAY = 'take away', 'Take away'
        DELIVERY = 'delivery', 'Delivery'

    class OrderStatus(TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        DELIVERED = 'delivered', 'Delivered'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    total_price = DecimalField(max_digits=10, decimal_places=2)
    item = ForeignKey('apps.OrderItem', on_delete=SET_NULL, related_name='order', null=True, blank=True)
    status = CharField(max_length=100, choices=OrderStatus, default=OrderStatus.PENDING)
    type = CharField(max_length=100, choices=OrderType)
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)


class Address(Model):
    address = CharField(max_length=255)
    entrance_hall = CharField(max_length=100)
    floor = CharField(max_length=100)
    room = CharField(max_length=100)
    description = CharField(max_length=100)
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='address')
    created_at = DateTimeField(auto_now_add=True)


class Payment(Model):
    class PaymentMethod(TextChoices):
        CARD = 'card', 'Card'
        BANK = 'bank', 'Bank'
        CASH = 'cash', 'Cash'

    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='payment')
    payment_method = CharField(max_length=100, choices=PaymentMethod)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)


class TelegramUser(Model):
    user_id = BigIntegerField()
    first_name = CharField(max_length=255, null=True, blank=True)
    last_name = CharField(max_length=255, null=True, blank=True)
    username = CharField(max_length=255, null=True, blank=True)
    language_code = CharField(max_length=255, null=True, blank=True)


class Settings(Model):
    phone_number = CharField(max_length=20, null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    delivery_price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = TextField(null=True, blank=True)
    work_time = JSONField(null=True, blank=True)


class Notification(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
    title = CharField(max_length=255)
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
