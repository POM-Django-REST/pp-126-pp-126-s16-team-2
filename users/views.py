from django.shortcuts import render, get_object_or_404
from users.models import User

def user_list_view(request):
    users = User.objects.all()  # Отримання всіх користувачів
    return render(request, "users/user_list.html", {"users": users})

def user_detail_view(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Пошук користувача за ID
    return render(request, "users/user_detail.html", {"user": user})
