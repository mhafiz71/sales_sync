from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Sum
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Sum, Count, F
from django.db.models import Q
import json
from .models import Product, Sale, SaleItem
from .forms import ProductForm # Import the new form

# NOTE: The login view itself is handled by Django's auth system.
# You just need to create the template and url.

@login_required

def products_view(request):    
    all_products = Product.objects.all()
    
    total_products_count = all_products.count()
    
    total_inventory_value = all_products.aggregate(
        total_value=Sum(F('price') * F('stock'))
    )['total_value'] or 0 # 'or 0' handles the case of an empty database

    low_stock_count = all_products.filter(stock__gt=0, stock__lte=10).count()
    out_of_stock_count = all_products.filter(stock=0).count()

    search_query = request.GET.get('q', '')
    products_list = all_products # Start with all products
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'products': products_list,
        'search_query': search_query,
        
        'total_products_count': total_products_count,
        'total_inventory_value': total_inventory_value,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    return render(request, 'core/products.html', context)
@login_required
def sales_view(request):
    filter_date_str = request.GET.get('filter_date')

    sales_queryset = Sale.objects.all().order_by('-created_at')

    if filter_date_str:
        try:
            selected_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
            sales_queryset = sales_queryset.filter(created_at__date=selected_date)
        except (ValueError, TypeError):
            pass

    context = {
        'sales': sales_queryset,
        'filter_date': filter_date_str,
    }

    return render(request, 'core/sales.html', context)


@login_required
def sale_receipt_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    # The template can access related items via sale.saleitem_set.all
    context = {'sale': sale}
    return render(request, 'core/sale_receipt.html', context)

@login_required
def product_create_edit_view(request, pk=None):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('products')

    if pk:
        product = get_object_or_404(Product, pk=pk)
        instance = product
    else:
        instance = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{form.instance.name}' was saved successfully!")
            return redirect('products')
    else:
        form = ProductForm(instance=instance)

    context = {'form': form}
    return render(request, 'core/product_form.html', context)


@login_required
def product_delete_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('products')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' was deleted successfully!")
    return redirect('products')

@login_required
def new_sale_view(request):
    if request.method == 'POST':
        items_json = request.POST.get('items_json')
        if not items_json:
            messages.error(request, "No items were selected for the sale.")
            return redirect('new_sale')
        
        cart_items = json.loads(items_json)

        try:
            # transaction.atomic ensures that if any part fails, the whole operation is rolled back.
            with transaction.atomic():
                # Step 1: Create the main Sale object
                new_sale = Sale.objects.create(customer_name="Walk-in Customer")

                for item_id, item_data in cart_items.items():
                    product = get_object_or_404(Product, id=item_id)
                    quantity = int(item_data['quantity'])

                    if product.stock < quantity:
                        # This will roll back the transaction
                        raise ValueError(f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {quantity}")

                    # Step 2: Create a SaleItem for each product in the cart
                    SaleItem.objects.create(
                        sale=new_sale,
                        product=product,
                        quantity=quantity,
                        price=product.price # IMPORTANT: Store the price at the time of sale
                    )

                    # Step 3: Decrease the product's stock
                    product.stock -= quantity
                    product.save()

            messages.success(request, f"Sale #{new_sale.id} created successfully!")
            # Redirect to the printable receipt for the newly created sale
            return redirect('sale_receipt', sale_id=new_sale.id)
            
        except ValueError as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('new_sale')
        except Exception as e:
            messages.error(request, f"A critical error occurred: {e}")
            return redirect('new_sale')

    # This is for the GET request (loading the page for the first time)
    products = Product.objects.filter(stock__gt=0).order_by('name')
    context = {'products': products}
    return render(request, 'core/new_sale.html', context)


# core/views.py (ensure this view is present)

@login_required
def sale_receipt_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    # The template can access related items via sale.saleitem_set.all
    context = {'sale': sale}
    return render(request, 'core/sale_receipt.html', context)


# core/views.py (add this new view)



@login_required
def sales_report_view(request):
    end_date_str = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    start_date_str = request.GET.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    end_date_inclusive = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    sales_in_range = Sale.objects.filter(created_at__range=(start_date, end_date_inclusive))

    report_data = sales_in_range.aggregate(
        total_revenue=Sum(F('saleitem__quantity') * F('saleitem__price')),
        total_sales_count=Count('id', distinct=True)
    )

    context = {
        'sales': sales_in_range.order_by('-created_at'),
        'start_date': start_date_str,
        'end_date': end_date_str,
        'total_revenue': report_data.get('total_revenue') or 0,
        'total_sales_count': report_data.get('total_sales_count') or 0,
    }
    
    return render(request, 'core/sales_report.html', context)

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        
        return super().dispatch(request, *args, **kwargs)