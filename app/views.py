from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Admin, University, Student, Sponsor, SponsorStudent
from .serializers import (
    AdminSerializer,
    UniversitySerializer,
    StudentSerializer,
    SponsorSerializer,
    SponsorStudentSerializer,
    SponsorDetailSerializer,
    StudentDetailSerializer
)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# class SponsorViewSet(viewsets.ModelViewSet):
#     queryset = Sponsor.objects.all()
#     serializer_class = SponsorSerializer


class SponsorStudentViewSet(viewsets.ModelViewSet):
    queryset = SponsorStudent.objects.all()
    serializer_class = SponsorStudentSerializer


class SponsorRegisterAPIView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        choice_type = request.data.get('choice_type')
        payment_amount = request.data.get('payment_amount')
        organization = request.data.get('organization')

        if choice_type == 'individual':
            Sponsor.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                choice_type=choice_type,
                payment_amount=payment_amount
            )
        else:
            Sponsor.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                choice_type=choice_type,
                payment_amount=payment_amount,
                organization=organization
            )

        return Response(status=201)


class AddStudentSponsorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]
    def post(self, request):
        data = request.data
        sponsor_id = data.get("sponsor")
        student_id = data.get("student")
        allocated_amount = int(data.get("allocated_amount"))

        sponsor = Sponsor.objects.get(id=sponsor_id)
        student = Student.objects.get(id=student_id)

        sponsor_allocated_amounts = (
            SponsorStudent.objects.filter(sponsor=sponsor)
            .aggregate(total_amount=Sum('allocated_amount'))['total_amount'] or 0
        )

        active_balance = sponsor.payment_amount - sponsor_allocated_amounts

        if active_balance < allocated_amount:
            raise serializers.ValidationError(
                {"error": f"Homiyda yetarli mablag' mavjud emas ({active_balance})"}
            )

        student_received_amount = (
            SponsorStudent.objects.filter(student=student)
            .aggregate(total_amount=Sum('allocated_amount'))['total_amount'] or 0
        )

        student_needed_amount = student.contract_amount - student_received_amount

        if student_needed_amount < allocated_amount:
            raise serializers.ValidationError(
                {"error": "Talaba uchun bunday kattalikdagi summa shart emas"}
            )

        SponsorStudent.objects.create(
            sponsor=sponsor,
            student=student,
            allocated_amount=allocated_amount
        )

        return Response(status=201)


class DashboardSummaryAPIView(APIView):
    def get(self, request):
        total_paid = Sponsor.objects.aggregate(total=Sum('payment_amount'))['total'] or 0
        total_requested = Student.objects.aggregate(total=Sum('allocated_amount'))['total'] or 0 
        total_allocated = SponsorStudent.objects.aggregate(total=Sum('allocated_amount'))['total'] or 0
        total_needed = total_requested - total_allocated

        data = {
            "total_paid": total_paid,
            "total_requested": total_requested,
            "total_needed": total_needed
        }

        return Response(data)


class SponsorDetailAPIView(APIView):
    def get(self, request, pk): 
        sponsor = Sponsor.objects.filter(pk=pk).first()
        
        if sponsor:
            serializer = SponsorDetailSerializer(sponsor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=201)


class StudentDetailAPIView(APIView):
    def get(self, request, pk): 
        student = Student.objects.filter(pk=pk).first()
        
        if student:
            serializer = StudentDetailSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({}, status=status.HTTP_200_OK)
    

class SponsorListAPIVIew(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("full_name", )
    filterset_fields = ('status', )
    

class DashboardChartAPIView(APIView):
    
    def get(self, request):
        data = []


        for i in range(1, 13):
            sponsor_count = Sponsor.objects.filter(
                created_at__month=i).count()
            student_count = Student.objects.filter(
                created_at__month=i).count()
            data.append({
                "month":i,
                "student_count": student_count,
                "sponsor_count": sponsor_count
            })

     
        return Response(data=data)

