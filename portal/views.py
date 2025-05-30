from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Student
import json
from decimal import Decimal, InvalidOperation

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
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'add':
                name = data.get('name')
                subject = data.get('subject')
                marks = data.get('marks')

                try:
                    marks = Decimal(str(marks))  # Convert to Decimal
                except (InvalidOperation, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid marks value'}, status=400)

                student, created = Student.objects.get_or_create(
                    name=name,
                    subject=subject,
                    teacher=request.user,
                    defaults={'marks': marks}
                )

                if not created:
                    student.marks += marks
                    student.save()

                return JsonResponse({'status': 'success', 'new_total': float(student.marks)})

            elif action == 'edit':
                student_id = data.get('id')
                name = data.get('name')
                subject = data.get('subject')
                marks = data.get('marks')

                try:
                    marks = Decimal(str(marks))  # Convert to Decimal
                except (InvalidOperation, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid marks value'}, status=400)

                student = Student.objects.get(id=student_id, teacher=request.user)
                student.name = name
                student.subject = subject
                student.marks = marks  # Overwrites marks (not additive)
                student.save()

                return JsonResponse({'status': 'success', 'new_total': float(student.marks)})

            elif action == 'update':
                student_id = data.get('id')
                subject = data.get('subject')
                marks = data.get('marks')

                try:
                    marks = Decimal(str(marks))  # Convert to Decimal
                except (InvalidOperation, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid marks value'}, status=400)

                student = Student.objects.get(id=student_id, teacher=request.user)
                if student.subject != subject:
                    return JsonResponse({'status': 'error', 'message': 'Subject mismatch'}, status=400)
                student.marks += marks
                student.save()

                return JsonResponse({'status': 'success', 'new_total': float(student.marks)})

            elif action == 'delete':
                student_id = data.get('id')
                student = Student.objects.get(id=student_id, teacher=request.user)
                student.delete()
                return JsonResponse({'status': 'success'})

            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def student_detail_view(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    return render(request, 'portal/student_details.html', {'student': student})