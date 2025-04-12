from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from rest_framework import viewsets
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


def order_list(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "authentication/access_denied.html")

    orders = Order.objects.all()
    return render(request, "order/order_list.html", {"orders": orders})


def my_orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print("🔐 Користувач увійшов:", request.user)
    print("👤 Його роль:", getattr(request.user, 'role', 'Немає поля role'))

    orders = Order.objects.filter(user=request.user)
    return render(request, "order/my_orders.html", {"orders": orders})

def order_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, pk=pk)
    if request.user.role != 1 and order.user != request.user:
        return render(request, "authentication/access_denied.html")

    return render(request, "order/order_detail.html", {"order": order})


def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, "order/order_create.html", {"form": form})


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 1 and order.user != request.user:
        return render(request, "authentication/access_denied.html")

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, "order/order_edit.html", {"form": form, "order": order})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'], url_path='user/(?P<user_id>[^/.]+)/order')
    def user_orders(self, request, user_id=None):
        orders = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class UserOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)
