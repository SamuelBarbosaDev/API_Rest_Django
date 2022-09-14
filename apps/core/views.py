from django.shortcuts import render


# Create your views here.

def base(request):
    template_name='core/base.html'
    context={
        'name':'name'
    }
    return render(request , template_name=template_name, context= context)
