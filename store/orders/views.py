from basket.basket import Basket

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import OrderItemsForm
from .models import Order, OrderItem

User = get_user_model()


def order_list(request):
    my_order = Order.objects.filter(user_id=request.user.id).order_by('-created')
    paginator = Paginator(my_order, 5)
    page = request.GET.get('page')
    myorder = paginator.get_page(page)

    return render(request, 'orders/list.html', {"myorder": myorder})


def order_create(request):
    basket = Basket(request)
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        form = OrderItemsForm(request.POST or None, initial={"name": user.first_name, "email": user.email})
        if request.method == 'POST':
            if form.is_valid():
                # check quantity for every item in basket
                order = form.save(commit=False)
                order.user = User.objects.get(id=request.user.id)
                order.payable = basket.get_total_price()
                order.total_book = len(basket)

                order.save()
                for item in basket:
                    OrderItem.objects.create(order=order,
                                             book=item['book'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                    item['book'].quantity = item['book'].quantity - item['quantity']
                    item['book'].save()

                basket.clear()
                request.session['order_id'] = order.id
                return redirect(reverse('shop:process'))
            else:
                form = OrderItemsForm()
        if len(basket) > 0:
            return render(request, 'orders/order_create.html', {"form": form, 'basket': basket})
        else:
            messages.warning(request, "Your Basket is EMPTY")
            return redirect('/')
    else:
        return redirect('register')
