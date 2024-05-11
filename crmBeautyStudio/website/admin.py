from django.contrib import admin
from website.models import Reservation, User
from website.models import Services, CategoryServices
from website.models import Blognews, Gallery

# Register your models here.
admin.site.register(User)
admin.site.register(Reservation)


# Регистрация модели в админ - панели, но уже позволит ваносить изменения в отображаемый контент.
@admin.register(CategoryServices)
class CategoryServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name_category",)}


# Тут происходит автозаполнение поля slug по примеру поля name_category


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name_service",)}


# admin.site.register(Gallery)
admin.site.register(Blognews)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"image": ("tittle",)}
