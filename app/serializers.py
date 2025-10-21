from rest_framework import serializers
from .models import Admin, University, Student, Sponsor, SponsorStudent
from django.db.models import Sum


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "id", "login", "password"


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "id", "name"


class StudentSerializer(serializers.ModelSerializer):
    student_type_display = serializers.CharField(
        source="get_student_type_display", read_only=True
    )
    university_name = serializers.CharField(source="university.name", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "student_type",
            "student_type_display",
            "contract_amount",
            "university",
            "university_name",
        ]


class SponsorSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()

    def get_spent_amount(self, obj):
      return obj.payment_amount.aggregate(total=Sum('allocated_amount'))['total'] or 0

    class Meta:
        model = Sponsor
        exclude = ("organization", "status")

class SponsorStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    sponsor_name = serializers.CharField(source="sponsor.full_name", read_only=True)

    class Meta:
        model = SponsorStudent
        fields = [
            "id",
            "student",
            "student_name",
            "sponsor",
            "sponsor_name",
            "allocated_amount",
        ]

class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class StudentDetailSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = "__all__"

