from django.shortcuts import render
from .models import Order

def order_list(request):
    if not request.user.is_authenticated or request.user.role != 1:  # Перевірка ролі бібліотекаря
        return render(request, "authentication/access_denied.html")

    orders = Order.objects.all()
    return render(request, "authentication/order_list.html", {"orders": orders})

def my_orders_view(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'role') or request.user.role == 0:  # Перевірка аутентифікації
        return render(request, "authentication/access_denied.html")

    orders = Order.objects.filter(user=request.user)  # Фільтруємо тільки замовлення поточного користувача
    return render(request, "authentication/my_orders.html", {"orders": orders})

from django.shortcuts import get_object_or_404, render
from .models import Order

def order_detail(request, pk):
    if not request.user.is_authenticated or not hasattr(request.user, 'role'):  # Перевірка автентифікації
        return render(request, "authentication/access_denied.html")

    order = get_object_or_404(Order, pk=pk)  # Отримуємо конкретне замовлення за його ID
    return render(request, "order/order_detail.html", {"order": order})  # Рендеринг шаблону з деталями замовлення

