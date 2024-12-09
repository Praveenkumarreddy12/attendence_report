from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register
import base64
import os
from django.core.files.base import ContentFile

def register(request):
    if request.method == 'POST':
        emo_name = request.POST.get('emo_name')
        empid = request.POST.get('empid')
        emp_email = request.POST.get('emp_email')
        phone_number = request.POST.get('phone_number')
        photo_data = request.POST.get('photo')

        # Process the photo data
        if photo_data:
            # Extract the base64 string from the Data URL
            format, imgstr = photo_data.split(';base64,')  # Split the Data URL
            ext = format.split('/')[-1]  # Get the file extension
            # Create a ContentFile from the base64 string
            image_file = ContentFile(base64.b64decode(imgstr), name=f"{empid}_photo.{ext}")

            # Save the data to your model
            register = Register(
                emo_name=emo_name,
                empid=empid,
                emp_email=emp_email,
                phone_number=phone_number,
                image=image_file  # Assuming you have a field for the photo in your model
            )
            register.save()

        # return redirect('success_url')  # Redirect to a success page or another view

    return render(request, 'register.html')  # Render the registration form

