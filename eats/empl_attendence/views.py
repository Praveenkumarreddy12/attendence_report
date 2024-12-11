from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register, Attendence
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
#  pip show face_recognition
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Register
import cv2
from django.core.files.base import ContentFile
import os
import numpy as np

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
            uploaded_image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Get all the images from the Register model
            registers = Register.objects.all()

            # Initialize a variable to store the recognized face
            recognized_face = None

            # Loop through all the images in the Register model
            for register in registers:
                # Load the image from the Register model
                image = cv2.imdecode(np.frombuffer(register.image.read(), np.uint8), cv2.IMREAD_COLOR)

                # Convert images to grayscale for comparison
                uploaded_image_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Use ORB to find keypoints and descriptors
                orb = cv2.ORB_create()
                uploaded_keypoints, uploaded_descriptors = orb.detectAndCompute(uploaded_image_gray, None)
                image_keypoints, image_descriptors = orb.detectAndCompute(image_gray, None)

                # Use Brute-Force matcher
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(uploaded_descriptors, image_descriptors)

                # Sort matches by distance
                matches = sorted(matches, key=lambda x: x.distance)

                # If the number of matches is above a certain threshold, consider it a match
                if len(matches) > 100:  # Example threshold
                    recognized_face = register
                    break

            # If a face is recognized, render the login.html with the recognized face's details
            if recognized_face:
                Attendence.objects.create(empid=recognized_face.empid)
                # Update total no.of days by increasing one in Register
                recognized_face.total_days += 1
                recognized_face.save()

                return render(request, 'log.html', {'register':"Emp id : "+str(recognized_face), 'match': True})
            else:
                return render(request, 'log.html', {'register': "Not reconized", 'match': True})
                # return HttpResponse('Face not recognized')

    return render(request, 'log.html')

def attendence(request):
        if request.method == 'POST':
            empid = request.POST.get('empid')
            attendence = Attendence.objects.filter(empid=empid)
            total_days = Register.objects.filter(empid=empid).first().total_days if Register.objects.filter(empid=empid).exists() else 0
            return render(request, 'attendence.html', {'attendence': attendence, 'total_days': total_days})
        return render(request, 'attendence.html')

