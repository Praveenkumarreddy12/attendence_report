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


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register
import cv2
import face_recognition
from django.core.files.base import ContentFile
import os

def login(request):
    if request.method == 'POST':
        # Get the uploaded image from the webcam
        image_data = request.POST.get('image')

        # Process the image data
        if image_data:
            # Extract the base64 string from the Data URL
            format, imgstr = image_data.split(';base64,')  # Split the Data URL
            ext = format.split('/')[-1]  # Get the file extension
            # Create a ContentFile from the base64 string
            image_file = ContentFile(base64.b64decode(imgstr), name=f"webcam_image.{ext}")

            # Load the uploaded image
            uploaded_image = face_recognition.load_image_file(image_file)

            # Get all the images from the Register model
            registers = Register.objects.all()

            # Initialize a variable to store the recognized face
            recognized_face = None

            # Loop through all the images in the Register model
            for register in registers:
                # Load the image from the Register model
                image = face_recognition.load_image_file(register.image)

                # Get the face encodings of the uploaded image and the image from the Register model
                uploaded_image_encoding = face_recognition.face_encodings(uploaded_image)[0]
                image_encoding = face_recognition.face_encodings(image)[0]

                # Compare the face encodings
                match = face_recognition.compare_faces([image_encoding], uploaded_image_encoding)

                # If the faces match, set the recognized face to the current Register object
                if match[0]:
                    recognized_face = register
                    break

            # If a face is recognized, render the login.html with the recognized face's details
            if recognized_face:
                return render(request, 'login.html', {'register': recognized_face})
            else:
                return HttpResponse('Face not recognized')

    return render(request, 'login.html')



