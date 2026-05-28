from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserProfile, Country, Zone, State, City, Pincode, Address

@admin.register(Pincode)
class PincodeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'city', 'state_name')
    search_fields = ('code', 'city__name')
    
    def state_name(self, obj):
        return obj.city.state.name

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Zone)
class ZoneAdmin(ImportExportModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)

@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    list_display = ('name', 'country', 'zone')
    list_filter = ('country', 'zone')
    search_fields = ('name',)

@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state__country', 'state')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('email', 'phone', 'full_name', 'is_staff', 'is_active')
    search_fields = ('email', 'phone', 'full_name')
    list_filter = ('is_staff', 'is_active')

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'state', 'pincode', 'is_default')
    list_filter = ('state', 'is_default', 'address_type', 'is_otp_verified')
    search_fields = ('full_name', 'email', 'phone', 'street_address')
    
    fieldsets = (
        ('User Info', {'fields': ('user', 'full_name', 'email', 'phone', 'company')}),
        ('Address Details', {'fields': ('street_address', 'landmark', 'locality', 'address_type')}),
        ('Geography', {'fields': ('country', 'zone', 'state', 'city', 'pincode')}),
        ('Settings & Verification', {'fields': ('is_default', 'is_otp_verified')}),
        ('Admin Logs', {'fields': ('created_by', 'updated_by'), 'classes': ('collapse',)}),
    )
