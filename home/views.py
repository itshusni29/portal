

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.files import File
import mimetypes
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import FileForm
from .models import File
#from employee.forms import EmployeeForm  
#from employee.models import Employee 

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

#    CRUD 1

def home (request):
    all_products = Product.objects.all().order_by('-created_at')
    return render(request, 'home/home.html', {"products": all_products})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product')
        purchase_price = request.POST.get('purchase')
        sale_price = request.POST.get('sale')
        quantity = request.POST.get('qty')
        gender = request.POST.get('gender')
        notes = request.POST.get('notes')
        pdf_file = request.FILES.get('pdf')
        
        if product_name and purchase_price and sale_price and quantity and gender and notes and pdf_file:
            try:
                validate_pdf_file(pdf_file)
            except ValidationError as e:
                return render(request, 'home/add.html', {'error': e})
            
        filename = os.path.join('pdf_files', pdf_file.name)
        file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, filename), pdf_file)

        product = Product(
            product=product_name,
            purchase=purchase_price,
            sale=sale_price,
            qty=quantity,
            gender=gender,
            notes=notes,
            pdf=file_path
        )
        product.save()
        return redirect('home')

    return render(request, 'home/add.html')

def validate_pdf_file(file):
    if not file.name.endswith('.pdf') or mimetypes.guess_type(file.name)[0] != 'application/pdf':
        raise ValidationError('Only PDF files are allowed.')

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product is not None:
        return render(request, 'home/edit.html', {"object": product})

def edit_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            product.product = request.POST['product']
            product.purchase = request.POST['purchase']
            product.sale = request.POST['sale']
            product.qty = request.POST['qty']
            product.gender = request.POST['gender']
            product.notes = request.POST['notes']
            product.save()
            return redirect('home')
    except Product.DoesNotExist:
        pass  # or handle the exception as per your application's requirements
    
    return render(request, 'home/edit.html', {'product': product})

 
    
'''
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.purchase = request.POST.get('purchase')
        product.sale = request.POST.get('sale')
        product.qty = request.POST.get('qty')
        product.gender = request.POST.get('gender')
        product.notes = request.POST.get('notes')
        product.save()
        return redirect('product', product_id=product.id)

    context = {'object': product}
    return render(request, 'home/edit.html', context)
'''

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
    except Product.DoesNotExist:
        pass  # or handle the exception as per your application's requirements
    return redirect('home')
# CRUD 1






def file_list(request):
    files = File.objects.all()
    return render(request, 'file_manager/file_list.html', {'files': files})

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'file_manager/upload_file.html', {'form': form})

def delete_file(request, pk):
    file = File.objects.get(pk=pk)
    file.delete()
    return redirect('file_list')
