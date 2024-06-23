from time import localtime
from django.urls import reverse
import pytz
from datetime import date, datetime, timedelta
import json
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ServiceForm, BlognewsForm, UserEditForm, StaffChangeForm, StaffCreationForm
from .models import Reservation, User, Services, Blognews

def keep_alive(request):
    return HttpResponse("OK")


def home(request):
    # Количество клиентов
    user_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    # Записи на текущий день
    today = date.today()
    today_reservations = Reservation.objects.filter(date_reservation=today).order_by('time_reservation')

    # Процент заполненности
    total_slots = 100
    occupancy_percentage = (today_reservations.count() / total_slots) * 100

    # График записей на неделю
    weekly_reservations_labels = []
    weekly_reservations_data = []
    for i in range(7):
        day = today + timedelta(days=i)
        weekly_reservations_labels.append(day.strftime('%d.%m'))
        weekly_reservations_data.append(Reservation.objects.filter(date_reservation=day).count())

    # Последние отзывы
    recent_feedbacks = Reservation.objects.exclude(feedback__isnull=True).exclude(feedback__exact='').order_by('-date_reservation')[:5]

    context = {
        'user_count': user_count,
        'today_reservations': today_reservations,
        'occupancy_percentage': occupancy_percentage,
        'weekly_reservations_labels': json.dumps(weekly_reservations_labels),
        'weekly_reservations_data': json.dumps(weekly_reservations_data),
        'recent_feedbacks': [res.feedback for res in recent_feedbacks]
    }
    return render(request, "website/home.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def staff_list(request):
    staff_list = User.objects.filter(is_staff=True)
    return render(request, 'website/staff_list.html', {'staff_list': staff_list})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_staff(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник успешно зарегистрирован')
            return redirect('staff_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = StaffCreationForm()
    return render(request, 'website/register_staff.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_staff(request, pk):
    staff = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = StaffChangeForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник успешно обновлен')
            return redirect('staff_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = StaffChangeForm(instance=staff)
    return render(request, 'website/edit_staff.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request, pk):
    staff = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Сотрудник успешно удален')
        return redirect('staff_list')
    return render(request, 'website/staff_list.html')

@login_required
def all_reservations(request):
    today = timezone.now().date()
    end_date = today + timedelta(days=9)
    reservations = Reservation.objects.filter(date_reservation__range=[today, end_date]).order_by('time_reservation')
    context = {
        'reservations': reservations,
    }
    return render(request, 'website/all_reservations.html', context)

@login_required
def history(request):
    completed_reservations = Reservation.objects.filter(status__in=['Выполнено', 'Отменено']).order_by('-date_reservation', '-time_reservation')
    context = {
        'completed_reservations': completed_reservations,
    }
    return render(request, 'website/history.html', context)

@login_required
def update_reservation_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Отменено', 'Выполнено']:
            reservation.status = status
            reservation.save()
    return redirect(reverse('home') if 'home' in request.META.get('HTTP_REFERER', '') else reverse('all_reservations'))

@login_required
def clientsList(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    user_count = users.count()
    return render(request, "website/clients.html", {"users": users, 'user_count': user_count})

@login_required
def record(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Получаем последние 3 записи пользователя, отсортированные по возрастанию даты и времени
    reservations = Reservation.objects.filter(id_user=user).order_by('date_reservation', 'time_reservation')[:3]

    return render(request, "website/record.html", {"record": user, "reservations": reservations})

#Профиль
@login_required
def log_user_action(request, action_description):
    user_actions = request.session.get('user_actions', [])
    user_actions.append({
        'description': action_description,
        'timestamp': timezone.now().strftime("%d-%m-%Y %H:%M:%S")  # Сохраняем время как строку
    })

    # Сохраняем только последние 3 действия
    user_actions = user_actions[-3:]
    request.session['user_actions'] = user_actions

@login_required
def profile(request):
    user_actions = request.session.get('user_actions', [])
    actions = []

    for action in user_actions:
        action_description = action['description']
        # Преобразуем строку времени в объект datetime
        utc_timestamp = datetime.strptime(action['timestamp'], "%d-%m-%Y %H:%M:%S")
        # Присваиваем временной зоне объект UTC
        utc_timestamp = pytz.utc.localize(utc_timestamp)
        # Преобразуем время действия из UTC в локальное время
        local_timestamp = timezone.localtime(utc_timestamp)
        actions.append({
            'description': action_description,
            'timestamp': local_timestamp.strftime("%d-%m-%Y %H:%M:%S")
        })

    context = {
        'user': request.user,
        'user_actions': actions
    }
    return render(request, 'website/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            log_user_action(request, "Редактирование профиля")
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'website/edit_profile.html', {'form': form})


#Конец профиля

#Услуги

@login_required
def servicesList(request):
    services = Services.objects.all()
    return render(request, "website/services.html", {"services": services})

@login_required
def service_detail(request, pk):
    services = get_object_or_404(Services, pk=pk)
    return render(request, 'website/service_detail.html', {'service': services})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Services, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            log_user_action(request, "Изменение услуги")
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'website/edit_service.html', {'form': form, 'service': service})

@login_required
def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            log_user_action(request, "Создание услуги")
            return redirect('services')
    else:
        form = ServiceForm()

    return render(request, 'website/create_service.html', {'form': form})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.delete()
    log_user_action(request, "Удаление услуги")
    return redirect("services")

@login_required
def toggle_service_availability(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.available = not service.available
    service.save()
    log_user_action(request, "Отключение услуги")
    return JsonResponse({'status': 'success', 'available': service.available})

#Конец услуг

#Блог
@login_required
def news_list(request):
    news = Blognews.objects.all()
    return render(request, 'website/news_list.html', {'news': news})

@login_required
def news_detail(request, id):
    news_item = get_object_or_404(Blognews, id=id)
    return render(request, 'website/news_detail.html', {'news_item': news_item})

@login_required
def add_news(request):
    if request.method == 'POST':
        form = BlognewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно добавлена.')
            log_user_action(request, "Создание новости")
            return redirect('news_list')
        else:
            messages.error(request, 'Ошибка при добавлении новости.')
    else:
        form = BlognewsForm()
    return render(request, 'website/add_edit_news.html', {'form': form, 'title': 'Добавить новость'})

@login_required
def edit_news(request, id):
    news_item = get_object_or_404(Blognews, id=id)
    if request.method == 'POST':
        form = BlognewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена.')
            log_user_action(request, "Изменение новости")
            return redirect('news_detail', id=id)
        else:
            messages.error(request, 'Ошибка при обновлении новости.')
    else:
        form = BlognewsForm(instance=news_item)
    return render(request, 'website/add_edit_news.html', {'form': form, 'title': 'Редактировать новость'})

@login_required
def delete_news(request, id):
    news_item = get_object_or_404(Blognews, id=id)
    if request.method == "POST":
        news_item.delete()
        messages.success(request, 'Новость успешно удалена.')
        log_user_action(request, "Удаление новости")
        return redirect('news_list')
    else:
        messages.error(request, 'Не удалось удалить новость.')
        return redirect('news_detail', id=id)
#Конец блога

def loginuser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                messages.success(request, "Вы успешно вошли в систему")
                if user.is_superuser:
                    return redirect("staff_list")
                else:
                    return redirect("home")
            else:
                messages.error(request, "Данная страница доступна только сотрудникам.")
                return render(request, "website/login.html")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль.")

    return render(request, "website/login.html")



def logoutuser(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("home")