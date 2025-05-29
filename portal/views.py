from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Student
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    students = Student.objects.filter(teacher=request.user)
    return render(request, 'portal/home.html', {'students': students})

@login_required
def manage_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        subject = data.get('subject')
        marks = data.get('marks')
        action = data.get('action')
        
        if action == 'add':
            student, created = Student.objects.get_or_create(
                name=name,
                subject=subject,
                teacher=request.user,
                defaults={'marks': marks}
            )
            if not created:
                student.marks += float(marks)
                student.save()
            return JsonResponse({'status': 'success'})
        
        elif action == 'edit':
            student_id = data.get('id')
            try:
                student = Student.objects.get(id=student_id, teacher=request.user)
                student.name = name
                student.subject = subject
                student.marks = marks
                student.save()
                return JsonResponse({'status': 'success'})
            except Student.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        
        elif action == 'delete':
            student_id = data.get('id')
            try:
                student = Student.objects.get(id=student_id, teacher=request.user)
                student.delete()
                return JsonResponse({'status': 'success'})
            except Student.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def student_detail_view(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    return render(request, 'portal/student_details.html', {'student': student})