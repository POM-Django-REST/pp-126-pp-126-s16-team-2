from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import CustomUser, Order
from book.models import BorrowedBook  # Якщо BorrowedBook існує для статистики по книгах

def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if CustomUser.objects.filter(email=email).exists():
            return render(request, "authentication/register.html", {
                "error": "Цей email вже зареєстровано"
            })

        user = CustomUser.objects.create_user(email=email, password=password, role=role)
        login(request, user, backend='authentication.backends.EmailBackend')
        return redirect("home")

    return render(request, "authentication/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)

        if user:
            login(request, user, backend='authentication.backends.EmailBackend')
            return redirect("home")
        else:
            return render(request, "authentication/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def user_list_view(request):
    if not request.user.is_authenticated:
        return render(request, "authentication/access_denied.html")

    users = CustomUser.objects.all()
    return render(request, "authentication/user_list.html", {"users": users})


def user_detail_view(request, user_id):
    if not request.user.is_authenticated:
        return render(request, "authentication/access_denied.html")

    user = get_object_or_404(CustomUser, id=user_id)
    borrowed_books = BorrowedBook.objects.filter(member__user=user) if hasattr(user, 'library_member') else []

    return render(request, "authentication/user_detail.html", {
        "user": user,
        "borrowed_books": borrowed_books,
    })


def my_orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user)
    return render(request, "authentication/my_orders.html", {"orders": orders})
