# core/views.py
from django.shortcuts import render, redirect
from .models import Student
from django.core.files.storage import FileSystemStorage
import pandas as pd
from  .forms import StudentForm,RollNumberForm
def home(request):
    return render(request, 'myapp/home.html')

def upload_student_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Read the Excel file using pandas
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            # Iterate through rows and save data to the database
            for index, row in df.iterrows():
                Student.objects.create(
                    name=row['Name'],
                    roll_number=row['Roll Number'],
                    grade=row['Grade'],
                    # Add other fields as needed
                )

            return redirect('success')  # Redirect to a success page or any other page

        except Exception as e:
            error_message = f"Error processing the Excel file: {str(e)}"
            return render(request, 'myapp/error.html', {'error_message': error_message})

    return render(request, 'myapp/upload_student_file.html')
def view_student_data(request):
    students = Student.objects.all()
    return render(request, 'myapp/view_student_data.html', {'students': students})
def manual_student_entry(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or any other page
    else:
        form = StudentForm()

    return render(request, 'myapp/manual_student_entry.html', {'form': form})
def success(request):
    return render(request, 'myapp/success.html')
def get_student_by_roll_number(request):
    if request.method == 'POST':
        form = RollNumberForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            try:
                student = Student.objects.get(roll_number=roll_number)
                return render(request, 'myapp/student_details.html', {'student': student})
            except Student.DoesNotExist:
                error_message = 'Student with roll number {} not found.'.format(roll_number)
                return render(request, 'myapp/error.html', {'error_message': error_message})
    else:
        form = RollNumberForm()

    return render(request, 'myapp/get_student_by_roll_number.html', {'form': form})