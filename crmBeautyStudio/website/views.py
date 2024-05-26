from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from .forms import ServiceForm
from .models import Reservation, User
from .models import Services


def home(request):
    # Количество клиентов
    user_count = User.objects.filter(is_staff=False).count()

    # Записи на текущий день
    today = date.today()
    today_reservations = Reservation.objects.filter(date_reservation=today)

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


def loginuser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему")
            return redirect("home")
        else:
            messages.error(
                request, "Возникла ошибка при входе. Проверьте введенные данные."
            )
    else:
        return render(request, "website/login.html")


def logoutuser(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("home")

@login_required
def clientsList(request):
    users = User.objects.filter(is_staff=False)
    user_count = users.count()
    return render(request, "website/clients.html", {"users": users, 'user_count': user_count})

@login_required
def record(request, pk):
    user = get_object_or_404(User, pk=pk)
    reservations = Reservation.objects.filter(id_user=user)
    return render(request, "website/record.html", {"record": user, "reservations": reservations})

@login_required
def profile(request):
    return render(request, 'website/profile.html', {'user': request.user})

@login_required
def servicesList(request):
    services = Services.objects.filter(available=True)
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
            return redirect('services')
    else:
        form = ServiceForm()

    return render(request, 'website/create_service.html', {'form': form})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.delete()
    return redirect("services")

@login_required
def toggle_service_availability(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.available = not service.available
    service.save()
    return JsonResponse({'status': 'success', 'available': service.available})
