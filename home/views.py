from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileForm
from .models import File
import os

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    return render(request, 'home/index.html', context)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    context['segment'] = load_template
    return render(request, 'home/' + load_template, context)

@login_required(login_url="/login/")
def file_list(request):
    files = File.objects.all()
    return render(request, 'home/file_list.html', {'files': files})

@login_required(login_url="/login/")
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in ['.xlsx', '.csv']:
                return HttpResponse("Invalid file format. Only XLSX and CSV files are allowed.")
            form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'home/upload_file.html', {'form': form})

@login_required(login_url="/login/")
def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    file.delete()
    return redirect('file_list')
