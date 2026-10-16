from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must contain atleast 2 characters."
            )
        return value
    
    def validate_marks(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Marks must be between 0 and 100."
            )
        return value

    def validate_age(self, value):
        if value < 5 or value > 100:
            raise serializers.ValidationError(
                "Age must be between 5 and 100."
            )
        return value

    def validate(self, data):
        email = data.get('email')
        if email:
            existing_student = Student.objects.filter(
                email__iexact = email.strip()
            )

            if self.instance:
                existing_student = existing_student.exclude(
                    pk = self.instance.pk
                )

            if existing_student.exists():
                raise serializers.ValidationError({
                    "email" : "A student with this email already exists."
                })
        return data