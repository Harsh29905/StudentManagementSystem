from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer
from .permissions import StudentPermission

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [StudentPermission]

    filter_backends=[
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ["course", "age", "email",'marks','name']
    serach_fields = ['name','email']
    ordering_fields = ['name','age','marks','created_at']
    ordering = ['name']

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)