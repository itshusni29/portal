from django import forms
from .models import Product
from django import forms  
#from apps.home.models import Employee
from django.forms import fields



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


'''
class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = "__all__"  
        '''