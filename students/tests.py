
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Student, Course


class StudentAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="user2",
            password="testpass123"
        )

        # Add any other required Course fields from your model.
        self.course = Course.objects.create(
            name="Python",
            duration=8
        )

        self.student = Student.objects.create(
            user=self.user,
            name="Rahul Patel",
            email="rahul@example.com",
            age=21,
            marks=90,
            course=self.course
        )

        self.client.force_authenticate(user=self.user)

        self.list_url = reverse("student-v3-list")
        self.detail_url = reverse(
            "student-v3-detail",
            args=[self.student.pk]
        )

    def test_list_own_students(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_student(self):
        response = self.client.post(
            self.list_url,
            {
                "name": "Amit Shah",
                "email": "amit@example.com",
                "age": 20,
                "marks": 85,
                "course": self.course.pk
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Student.objects.filter(
                email="amit@example.com",
                user=self.user
            ).exists()
        )

    def test_cannot_access_other_users_student(self):
        self.student.user = self.other_user
        self.student.save()

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_unauthenticated_access_is_denied(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )
