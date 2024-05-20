from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


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
            messages.error(request, "Возникла ошибка при входе. Проверьте введенные данные.")
    else:
        return render(request, "website/login.html")


def logoutuser(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("home")

def clientsList(request):
    users = User.objects.all()
    return render(request, "website/clients.html", {"users": users})

def userdata(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        return render(request, "website/userdata.html", {"user": user})
    else:
        messages.error(request, "Вы должны авторизоваться для просмотра данной страницы")
        return redirect("home")