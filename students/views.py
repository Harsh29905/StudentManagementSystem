from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from .models import Student, Course
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login

@login_required
@ensure_csrf_cookie
def student_dashboard(request):
    courses = Course.objects.all()
    return render(
        request,
        "students/student_dashboard.html",
        {"courses": courses}
    )


def home(request):
    return render(request, "students/base.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("student_dashboard")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


# Create your views here.
def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html",{"students" : students})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html',{'form':form, 'title':"Create Student"})


@login_required
def student_update(request, id):
    student = get_object_or_404(
        Student,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "students/student_form.html", {
        "form": form,
        "title": "Update Student",
    })


@login_required
def student_delete(request, id):
    student = get_object_or_404(
        Student,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {"student": student}
    )


@api_view(['GET'])
def student_api_list(request):
    student = Student.objects.all()
    serializer = StudentSerializer(student, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def student_api_create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def student_api_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['PUT'])
def student_api_update(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(
        student, data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def student_api_partial_update(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(
        student, data=request.data, partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def student_api_delete(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"error":"Student not found"},
            status=status.HTTP_400_BAD_REQUEST
        )
    student.delete()
    return Response(
        status=status.HTTP_204_NO_CONTENT
    )

class StudentListCreateAPI(APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentDetailAPI(APIView):

    def get_student(self, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return None

    def get(self, request, id):
        student = self.get_student(id)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, id):
        student = self.get_student(id)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id):
        student = self.get_student(id)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(
            student, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        student = self.get_student(id)

        if student is None:
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import render, redirect
from .models import Student, Course
from .forms import StudentForm, CourseForm


@login_required
def student_dashboard(request):
    students = Student.objects.filter(user=request.user)

    context = {
        "total_students": students.count(),
        "total_courses": Course.objects.count(),
        "average_marks": students.aggregate(
            avg=Avg("marks")
        )["avg"],
    }

    return render(
        request,
        "students/student_dashboard.html",
        context,
    )


@login_required
def reports(request):
    students = Student.objects.filter(user=request.user)

    context = {
        "total_students": students.count(),
        "average_marks": students.aggregate(
            avg=Avg("marks")
        )["avg"],
        "top_students": students.order_by("-marks", "name")[:5],
    }

    return render(request, "students/reports.html", context)


@login_required
def student_list(request):
    students = Student.objects.filter(user=request.user).select_related("course")

    query = request.GET.get("q", "").strip()
    course_id = request.GET.get("course", "")
    ordering = request.GET.get("ordering", "name")

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )

    if course_id.isdigit():
        students = students.filter(course_id=course_id)

    allowed_ordering = [
        "name", "-name", "age", "-age", "marks", "-marks"
    ]

    if ordering not in allowed_ordering:
        ordering = "name"

    students = students.order_by(ordering)

    return render(request, "students/student_list.html", {
        "students": students,
        "courses": Course.objects.all(),
        "query": query,
        "selected_course": course_id,
        "ordering": ordering,
    })


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "students/student_create.html", {
        "form": form,
    })


@login_required
def course_list(request):
    courses = Course.objects.all().order_by("name")

    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()

    return render(request, "students/course_list.html", {
        "courses": courses,
        "form": form,
    })

from django.shortcuts import render

def home(request):
    return render(request, "students/home.html")