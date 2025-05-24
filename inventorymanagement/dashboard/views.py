from django.shortcuts import render, get_object_or_404, redirect
from .models import Part , Order
from django.contrib.auth.decorators import login_required
from .forms import PartForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
import logging
# New imports for PDF generation
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
logger = logging.getLogger(__name__)

@login_required
def index(request):
    parts = Part.objects.all()
    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    logger.debug(f"User: {request.user}, is_superuser: {request.user.is_superuser}, orders count: {orders.count()}")

    part_names = list(parts.values_list('name', flat=True))
    part_references = list(parts.values_list('reference', flat=True))
    part_name_refs = [f"{name} ({ref})" for name, ref in zip(part_names, part_references)]
    part_quantities = list(parts.values_list('quantityinstock', flat=True))

    order_aggregates = orders.values('part__name').annotate(total_quantity=Sum('order_quantity')).order_by('part__name')
    order_product_names = [item['part__name'] for item in order_aggregates]
    order_quantities = [item['total_quantity'] for item in order_aggregates]

    restock_threshold = 10
    low_stock_products = parts.filter(quantityinstock__lte=restock_threshold)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('index')
    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'form': form,
        'parts': parts,
        'part_name_refs': part_name_refs,
        'part_quantities': part_quantities,
        'order_product_names': order_product_names,
        'order_quantities': order_quantities,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    workers= User.objects.all()
    orders = Order.objects.filter(user=request.user)
    restock_threshold = 10
    low_stock_products = Part.objects.filter(quantityinstock__lte=restock_threshold)
    context={
        'workers':workers,
        'orders': orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    worker = User.objects.get(pk=pk)
    restock_threshold = 10
    low_stock_products = Part.objects.filter(quantityinstock__lte=restock_threshold)
    context = {
        'worker': worker,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def product(request):
    products = Part.objects.all()
    restock_threshold = 10
    low_stock_products = Part.objects.filter(quantityinstock__lte=restock_threshold)
    logger.debug(f"User: {request.user}, is_superuser: {request.user.is_superuser}, products count: {products.count()}")
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            part_name=form.cleaned_data.get('name')
            messages.success(request, f'Part {part_name} added successfully')
            return redirect('product')
    else:
        form = PartForm()

    if request.user.is_superuser:
        context = {
            'products': products,
            'form': form,
            'low_stock_products': low_stock_products,
        }
        return render(request, 'dashboard/admin_product.html', context)
    else:
        context = {
            'product': products,
            'form': form,
            'low_stock_products': low_stock_products,
        }
        return render(request, 'dashboard/product.html', context)

@login_required
def admin_part_add(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to add parts.")
        return redirect('product')

    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New part added successfully.")
            return redirect('product')
    else:
        form = PartForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/admin_part_add.html', context)

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = PartForm(instance=product)
    return render(request, 'dashboard/product_edit.html', {'form': form})

@login_required
def product_delete(request, pk):
    item = Part.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('product')
    return render(request, 'dashboard/product_delete.html', {'product': item})

@login_required
def product_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            messages.success(request, f'Part {part.name} updated successfully')
            return redirect('product_detail', pk=pk)
    else:
        form = PartForm(instance=part)
    context = {
        'part': part,
        'form': form,
    }
    return render(request, 'dashboard/product_detail.html', context)

@login_required
def order(request):
    if request.method == 'POST':
        part_id = request.POST.get('part_id')
        order_quantity = request.POST.get('order_quantity')
        try:
            part = Part.objects.get(id=part_id)
            order_quantity = int(order_quantity)
            if order_quantity > 0 and order_quantity <= part.quantityinstock:
                order = Order.objects.create(
                    user=request.user,
                    part=part,
                    order_quantity=order_quantity,
                    is_confirmed=False
                )
                messages.success(request, f"Order placed for {part.name} (Quantity: {order_quantity})")
                return redirect('index')
            else:
                messages.error(request, "Invalid order quantity.")
        except Part.DoesNotExist:
            messages.error(request, "Product does not exist.")
        except ValueError:
            messages.error(request, "Invalid quantity value.")

    # Show all orders if admin, else show only user's orders
    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    restock_threshold = 10
    low_stock_products = Part.objects.filter(quantityinstock__lte=restock_threshold)

    context={
        'orders': orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/order.html',context)

@login_required
def confirm_order(request, order_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to confirm orders.")
        return redirect('order')

    order = get_object_or_404(Order, id=order_id)
    part = order.part

    if part.quantityinstock < order.order_quantity:
        messages.error(request, "Insufficient stock to confirm this order.")
        return redirect('order')

    part.quantityinstock -= order.order_quantity
    part.save()

    order.is_confirmed = True
    order.save()

    # Create Invoice automatically
    from .models import Invoice
    import uuid
    invoice_number = str(uuid.uuid4()).replace('-', '').upper()[:12]
    total_amount = order.order_quantity * part.price
    Invoice.objects.create(
        order=order,
        invoice_number=invoice_number,
        total_amount=total_amount
    )

    messages.success(request, f"Order for {order.part.name} by {order.user.username} has been confirmed.")
    return redirect('order')

@login_required
def receipt_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.is_confirmed:
        messages.error(request, "Order is not confirmed yet.")
        return redirect('order')
    if request.user != order.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to view this receipt.")
        return redirect('order')
    context = {
        'order': order,
    }
    return render(request, 'dashboard/receipt.html', context)



@login_required
def invoice_detail(request, invoice_id):
    from .models import Invoice
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.user != invoice.order.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to view this invoice.")
        return redirect('order')
    context = {
        'invoice': invoice,
    }
    return render(request, 'dashboard/invoice_detail.html', context)

@login_required
def invoice_pdf(request, invoice_id):
    from .models import Invoice
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.user != invoice.order.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to download this invoice.")
        return redirect('order')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, height - inch, f"Invoice {invoice.invoice_number}")

    p.setFont("Helvetica", 12)
    p.drawString(inch, height - inch - 30, f"Invoice Date: {invoice.invoice_date.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(inch, height - inch - 50, f"Order ID: {invoice.order.id}")
    p.drawString(inch, height - inch - 70, f"Customer: {invoice.order.user.username}")

    p.drawString(inch, height - inch - 110, "Part")
    p.drawString(inch + 200, height - inch - 110, "Quantity")
    p.drawString(inch + 300, height - inch - 110, "Price per Unit")
    p.drawString(inch + 420, height - inch - 110, "Total")

    p.line(inch, height - inch - 115, width - inch, height - inch - 115)

    part = invoice.order.part
    quantity = invoice.order.order_quantity
    price = part.price
    total = invoice.total_amount

    p.drawString(inch, height - inch - 130, part.name)
    p.drawString(inch + 200, height - inch - 130, str(quantity))
    p.drawString(inch + 300, height - inch - 130, f"${price}")
    p.drawString(inch + 420, height - inch - 130, f"${total}")

    p.showPage()
    p.save()

    return response
