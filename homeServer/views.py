# Import necessary modules
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, ServiceCategory, Service, Booking, Team
from .serializers import UserSerializer, ServiceCategorySerializer, ServiceSerializer, BookingSerializer, TeamSerializer, TeamMemberSerializer




# Create a viewset for the User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # User signup view
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # User login view
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # User profile view
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # Update user profile view
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete user account view
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"})



# Create a viewset for the ServiceCategory model
class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

# Create a viewset for the Service model
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    # Retrieve services by category
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def by_category(self, request, pk):
        services = self.queryset.filter(category=pk)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)



# Create a viewset for the Booking model
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # Create a new booking
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    # Retrieve bookings made by the user (client)
    @action(detail=False, methods=['get'])
    def user_bookings(self, request):
        bookings = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    # Retrieve the team assigned to a booking
    @action(detail=True, methods=['get'])
    def team(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        
        team = booking.assigned_to_team
        serializer = TeamSerializer(team)
        return Response(serializer.data)


# Create a viewset for the Team model
class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    # Retrieve team members for a specific team
    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({"error": "Team not found"}, status=404)
        
        members = team.members.all()
        serializer = TeamMemberSerializer(members, many=True)
        return Response(serializer.data)