from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
<<<<<<< HEAD
=======
from rest_framework import viewsets
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
>>>>>>> Daniil

def order_list(request):
    if not request.user.is_authenticated or request.user.role != 1:  # Перевірка ролі бібліотекаря
        return render(request, "authentication/access_denied.html")

<<<<<<< HEAD
    orders = Order.objects.all()  # Отримуємо всі замовлення
    return render(request, "order/order_list.html", {"orders": orders})  # Правильний шлях до шаблону
=======
    orders = Order.objects.all()
    return render(request, "authentication/order_list.html", {"orders": orders})
>>>>>>> Daniil

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
<<<<<<< HEAD
    return render(request, "order/order_edit.html", {"form": form, "order": order})
=======
    return render(request, "order/order_edit.html", {"form": form, "order": order})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class UserOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'], url_path='user/(?P<user_id>[^/.]+)/order')
    def user_orders(self, request, user_id=None):
        orders = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
>>>>>>> Daniil
