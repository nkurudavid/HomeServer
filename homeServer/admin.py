from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import User, ServiceCategory, Service, TeamMember, Team, Booking, ServiceReview

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'is_manager', 'is_client', 'is_active', 'last_login',)
    search_fields = ('email', 'first_name', 'last_name',)
    list_filter = ('is_manager', 'is_client', 'is_active',)
    fieldsets = (
        ('User Credential', {'fields': ('email', 'password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'gender', 'phone_number', 'location', 'picture',)}),
        ('Permissions', {'fields': (('is_manager','is_client'),('is_active', 'is_staff', 'is_superuser'), 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('New User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'gender', 'phone_number', 'location', 'picture', 'is_manager', 'is_client', 'is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
    )
    ordering = ('email',)
    list_editable = ()
    list_per_page = 20
    filter_horizontal = ('user_permissions',)



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'bland_image')
    search_fields = ('title',)
    list_per_page = 20

    def bland_image(self, obj):
        return mark_safe('<img src="/../../media/%s" width="80" />' % (obj.image))
    bland_image.short_description = 'Category Image'



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'service_name', 'price', 'hours')
    search_fields = ('category__title', 'service_name')
    list_filter = ('category',)
    list_per_page = 20



@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'phone', 'work_id', 'image')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender',)
    list_per_page = 20



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('manager', 'team_name')
    search_fields = ('team_name',)
    list_per_page = 20



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_no', 'client', 'service', 'status', 'service_time', 'created_date')
    search_fields = ('booking_no', 'client__email', 'service__service_name')
    list_filter = ('status',)
    list_per_page = 20



@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'client_comment')
    search_fields = ('booking__booking_no',)
    list_filter = ('rating',)
    list_per_page = 20



admin.site.unregister(Group)