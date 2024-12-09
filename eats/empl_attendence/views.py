from django.shortcuts import render
from .models import Register
# Create your views here.
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        emo_name = request.POST.get('emo_name')
        empid = request.POST.get('empid')
        emp_email = request.POST.get('emp_email')
        phone_number = request.POST.get('phone_number')
        image = request.FILES.get('image')

        register = Register(emo_name=emo_name, empid=empid, emp_email=emp_email, phone_number=phone_number, image=image)
        register.save()
    
    return render(request, 'register.html')

