from django.db import models


class Admin(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class University(models.Model):
    name = models.CharField(max_length=150)


class Student(models.Model):
    STUDENT_TYPE_CHOICES = [
        ("bachelor", "Bakalavr"),
        ("master", "Magistr"),
    ]

    full_name = models.CharField(max_length=150)
    student_type = models.CharField(max_length=50, choices=STUDENT_TYPE_CHOICES)
    allocated_amount = models.BigIntegerField()
    contract_amount = models.BigIntegerField()  
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name="students"
    )
    created_at = models.DateTimeField(auto_now=True, null=None)


class Sponsor(models.Model):
    CHOICE_TYPE_CHOICES = [
        ("individual", "Jismoniy shaxs"),
        ("organization", "Tashkilot"),
    ]

    STATUS_CHOICES = [
        ("new", "Yangi"),
        ("approved", "Tasdiqlangan"),
        ("rejected", "Rad etilgan"),
    ]

    full_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, null=True, blank=True)
    choice_type = models.CharField(max_length=50, choices=CHOICE_TYPE_CHOICES)
    phone_number = models.BigIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    payment_amount = models.IntegerField()


class SponsorStudent(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="sponsor_links"
    )
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="student_links"
    )
    allocated_amount = models.BigIntegerField()

    