import string
from django.conf import settings
import weasyprint
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404

from cart.views import get_cart, cart_clear

from .models import OrderItem, Order, Product
from .forms import OrderCreateForm
from .task import order_created


# Create your views here.


def order_create(request):
    cart = get_cart(request)
    cart_qty = sum(item['quantity'] for item in cart.values())
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            cf = order_form.cleaned_data
            transport = cf['transport']

            if transport == 'Recipient pickup':
                transport_cost = 0

            order = order_form.save(commit=False)
            order.transport_cost = Decimal(transport_cost)
            order.save()

            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                cart_item = cart[str(product.id)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )
            cart_clear(request)

            order_created.delay(order.id)

            return render(request, 'order_created.html',{
                'order':order
            })

    else:
        order_form = OrderCreateForm()

    return render(request, 'order_create.html', {
        'cart':cart,
        'order_form':order_form,
        'transport_cost':transport_cost
    })


@staff_member_required
def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename:order_{order.id}.pdf'

    #generate pdf
    html = render_to_string('pdf.html', {'order': order})
    stylesheet = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheet)

    return response