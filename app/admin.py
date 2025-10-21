from django.contrib import admin
from .models import Admin, University, Student, Sponsor, SponsorStudent

admin.site.register(Admin)
admin.site.register(University)
admin.site.register(Sponsor)
admin.site.register(SponsorStudent)

class SponsorStudentTabularInline(admin.TabularInline):
    extra = 1
    model = SponsorStudent 

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [SponsorStudentTabularInline, ]
    list_display = ("id", "full_name", "allocated_amount")
    list_display_links = ("id", "full_name")