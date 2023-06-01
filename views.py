

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import Product
from django.shortcuts import render, redirect, get_object_or_404

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

        if product_name and purchase_price and sale_price and quantity and gender and notes:
            product = Product(
                product=product_name,
                purchase=purchase_price,
                sale=sale_price,
                qty=quantity,
                gender=gender,
                notes=notes
            )
            product.save()
            return redirect('home')

    return render(request, 'home/add.html')


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product is not None:
        return render(request, 'home/edit.html', {"object": product})

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

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
    except Product.DoesNotExist:
        pass  # or handle the exception as per your application's requirements
    return redirect('home')
# CRUD 1


# CRUD 2
'''
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")'''
# CRUD 2