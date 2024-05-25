from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import User
from .models import CategoryServices, Services


def home(request):
    context: dict[str, str] = {"title": "Я&Ты - Главная"}
    return render(request, "website/home.html")


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


def clientsList(request):
    users = User.objects.all()
    user_count = User.objects.count()
    return render(request, "website/clients.html", {"users": users, 'user_count': user_count})


def record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(User, pk=pk)
        print(f"Record found: {record}, ID: {record.id}")
        return render(request, "website/record.html", {"record": record})
    else:
        messages.error(
            request, "Вы должны авторизоваться для просмотра данной страницы"
        )
        return redirect("home")


def servicesList(request):
    services = Services.objects.all()
    return render(request, "website/services.html", {"services": services})
