from rest_framework import serializers
from .models import User, Booking, ServiceCategory, Service, TeamMember, Team, ServiceReview


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Exclude fields that are not applicable for all models.
        excluded_fields = kwargs.pop('exclude', [])
        super().__init__(*args, **kwargs)
        for field_name in excluded_fields:
            self.fields.pop(field_name, None)


class ServiceReviewSerializer(BaseModelSerializer):
    class Meta:
        model = ServiceReview
        fields = ('id', 'rating', 'client_comment')


class TeamMemberSerializer(BaseModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'first_name', 'last_name', 'gender', 'phone', 'work_id', 'picture')


class TeamSerializer(BaseModelSerializer):
    members = TeamMemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'members')


class BookingSerializer(BaseModelSerializer):
    service_reviews = ServiceReviewSerializer(many=True)
    assigned_team = TeamSerializer()

    class Meta:
        model = Booking
        fields = ('id', 'booking_no', 'status', 'service_time', 'created_date', 'created_date', 'manager_comment', 'service_reviews', 'assigned_team')


class UserSerializer(BaseModelSerializer):
    bookings = serializers.PrimaryKeyRelatedField(many=True, queryset=Booking.objects.all(), required=False, default=[])
    password = serializers.CharField(write_only=True)  # Define the password field as write-only

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email','password', 'gender', 'is_manager', 'is_client', 'phone_number', 'location', 'picture', 'bookings')
        

class ServiceSerializer(BaseModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name', 'description', 'price', 'hours')


class ServiceCategorySerializer(BaseModelSerializer):
    services = ServiceSerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = ('id', 'title', 'image', 'services')
