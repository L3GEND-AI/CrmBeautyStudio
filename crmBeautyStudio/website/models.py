from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class Gallery(models.Model):
    tittle = models.CharField(max_length=250, verbose_name="Заголовок")
    description = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Описание"
    )
    image = models.CharField(blank=True, null=True, verbose_name="Фрагмент URL Фото")

    class Meta:
        db_table = "gallery"
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return self.tittle.__str__()

class Blognews(models.Model):
    tittle = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.CharField(blank=True, null=True)
    maintext = models.TextField()

    class Meta:
        db_table = "blognews"

class CategoryServices(models.Model):
    name_category = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="Фрагмент URL"
    )

    class Meta:

        db_table = "category_services"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name_category.__str__()

class Services(models.Model):
    name_service = models.CharField(max_length=50, verbose_name="Название")
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    category_service = models.ForeignKey(
        CategoryServices,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="Категория услуги",
    )
    description = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Описание"
    )
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="Фрагмент URL"
    )
    available = models.BooleanField(default=True, verbose_name='Доступность услуги')

    class Meta:

        db_table = "services"
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name_service.__str__()

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Номер телефона должен соответствовать формату: '+999999999'.",
    )
    PhoneNumber = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    # PhoneNumber = models.CharField(max_length=200, blank=True, null=True, verbose_name='Номер телефона')

    discount = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Скидка в %",
    )
    lastenter = models.DateField(blank=True, null=True, verbose_name="Последний вход")

    class Meta:

        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username.__str__()

class Reservation(models.Model):
    time_reservation = models.TimeField()
    date_reservation = models.DateField()
    id_service = models.ForeignKey(
        "Services", models.DO_NOTHING, db_column="id_service"
    )
    id_user = models.ForeignKey("User", models.DO_NOTHING, db_column="id_user")
    feedback = models.CharField(max_length=200, blank=True, null=True)
    wishes = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20)

    class Meta:

        db_table = "reservation"
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.id_service.__str__()
