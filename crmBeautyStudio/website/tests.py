from django.test import TestCase
from django.urls import reverse
from .forms import ServiceForm
from .models import CategoryServices, User

class ClientsListViewTest(TestCase):

    print("Тест вывода в таблицу пользователей")

    def setUp(self):
        # Создаем несколько тестовых пользователей
        print("Создание тестовых пользователей")
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', is_staff=False)
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', is_staff=True)

    def test_clients_list_view(self):
        # Авторизуемся под пользователем
        print("Авторизация под пользователем user1")
        self.client.force_login(self.user1)

        # Посылаем запрос к представлению, отображающему список пользователей
        print("Отправка GET-запроса к представлению clients")
        response = self.client.get(reverse('clients'))

        # Проверяем, что страница отображается успешно
        print("Статус код ответа:", response.status_code)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что данные о пользователе user1 присутствуют на странице
        print("Проверка, что данные пользователя user1 присутствуют на странице")
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.email)

        # Проверяем, что данные о пользователе user2 отсутствуют на странице
        print("Проверка, что данные пользователя user2 отсутствуют на странице")
        self.assertNotContains(response, self.user2.username)
        self.assertNotContains(response, self.user2.email)

""" class ServiceCreationTest(TestCase):

    print("Тест создания услуги")

    def setUp(self):
        # Создаем категорию для использования в тестах
        print("Создание категории для тестов")
        self.category = CategoryServices.objects.create(name_category="Test Category")

    def test_service_creation(self):
        # Подготовка данных для создания услуги
        print("Подготовка данных для создания услуги")
        form_data = {
            'name_service': 'Test Service',
            'price': 100.0,
            'category_service': self.category.id,
            'description': 'Test Description',
            'slug': 'test-service'
        }

        # Создание формы с предоставленными данными
        print("Создание формы с данными")
        form = ServiceForm(data=form_data)

        # Проверка валидности формы
        print("Проверка валидности формы")
        self.assertTrue(form.is_valid())

        # Сохранение услуги из формы
        print("Сохранение услуги из формы")
        service = form.save()

        # Проверка атрибутов сохраненной услуги
        print("Проверка атрибутов сохраненной услуги")
        print("Название услуги:", service.name_service)
        print("Цена услуги:", service.price)
        print("Категория услуги:", service.category_service)
        print("Описание услуги:", service.description)
        print("Слаг услуги:", service.slug)
        self.assertEqual(service.name_service, 'Test Service')
        self.assertEqual(service.price, 100.0)
        self.assertEqual(service.category_service, self.category)
        self.assertEqual(service.description, 'Test Description')
        self.assertEqual(service.slug, 'test-service')
 """