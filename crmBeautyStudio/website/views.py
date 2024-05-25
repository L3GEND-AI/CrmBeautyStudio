from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from .models import User
from .models import Services


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

@login_required
def clientsList(request):
    users = User.objects.all()
    user_count = User.objects.count()
    return render(request, "website/clients.html", {"users": users, 'user_count': user_count})

@login_required
def record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(User, pk=pk)
        print(f"Record found: {record}, ID: {record.id}") #debug
        return render(request, "website/record.html", {"record": record})
    else:
        messages.error(
            request, "Вы должны авторизоваться для просмотра данной страницы"
        )
        return redirect("home")

@login_required
def profile(request):
    return render(request, 'website/profile.html', {'user': request.user})

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
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'website/edit_service.html', {'form': form, 'service': service})