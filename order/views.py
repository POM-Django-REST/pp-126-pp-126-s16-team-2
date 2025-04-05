from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm

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

def order_detail(request, pk):
    if not request.user.is_authenticated or not hasattr(request.user, 'role'):  # Перевірка автентифікації
        return render(request, "authentication/access_denied.html")

    order = get_object_or_404(Order, pk=pk)  # Отримуємо конкретне замовлення за його ID
    return render(request, "order/order_detail.html", {"order": order})  # Рендеринг шаблону з деталями замовлення

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, "order/order_create.html", {"form": form})

def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, "order/order_edit.html", {"form": form, "order": order})