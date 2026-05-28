from rest_framework import serializers
from .models import UserProfile, Address, Country, Zone, State, City, Pincode

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'country']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'code', 'country', 'zone']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'state']

class PincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields = ['id', 'code', 'city']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone', 'full_name', 'email', 'created_at']

class AddressSerializer(serializers.ModelSerializer):
    # Nested serializers for reading
    country_obj = CountrySerializer(source='country', read_only=True)
    state_obj = StateSerializer(source='state', read_only=True)
    city_obj = CitySerializer(source='city', read_only=True)
    pincode_obj = PincodeSerializer(source='pincode', read_only=True)
    zone_obj = ZoneSerializer(source='zone', read_only=True)

    country = serializers.PrimaryKeyRelatedField(read_only=True)
    state = serializers.PrimaryKeyRelatedField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    zone = serializers.PrimaryKeyRelatedField(read_only=True)
    pincode = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = [
            'id', 'address_type', 'full_name', 'email', 'phone', 
            'street_address', 'landmark', 'locality', 
            'country', 'zone', 'state', 'city', 'pincode',
            'company', 'is_default', 'is_otp_verified',
            'raw_state', 'raw_city', 'raw_pincode',
            'country_obj', 'state_obj', 'city_obj', 'pincode_obj', 'zone_obj'
        ]

        read_only_fields = ['user', 'created_by', 'updated_by']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['created_by'] = user
        
        # Simple string-to-model mapping for frontend compatibility
        country_name = self.context['request'].data.get('country_name', 'India')
        state_name = self.context['request'].data.get('state_name', validated_data.get('raw_state', ''))
        city_name = self.context['request'].data.get('city_name', validated_data.get('raw_city', ''))
        pincode_code = self.context['request'].data.get('pincode_code', validated_data.get('raw_pincode', ''))
        zone_name = self.context['request'].data.get('zone_name', '').strip()
        
        country, _ = Country.objects.get_or_create(name=country_name, defaults={'code': country_name[:2].upper()})
        
        state_defaults = {'country': country}
        if zone_name:
            zone_obj, _ = Zone.objects.get_or_create(name=zone_name, country=country)
            state_defaults['zone'] = zone_obj
            validated_data['zone'] = zone_obj

        state, created = State.objects.get_or_create(name=state_name, defaults=state_defaults)
        
        if not created and zone_name and not state.zone:
            zone_obj, _ = Zone.objects.get_or_create(name=zone_name, country=country)
            state.zone = zone_obj
            state.save()
            if 'zone' not in validated_data:
                validated_data['zone'] = zone_obj
        elif state.zone and 'zone' not in validated_data:
            validated_data['zone'] = state.zone

        city, _ = City.objects.get_or_create(name=city_name, state=state)

        
        # Handle Pincode lookup/creation
        if pincode_code:
            pincode, _ = Pincode.objects.get_or_create(code=pincode_code, defaults={'city': city})
            validated_data['pincode'] = pincode
        
        validated_data['country'] = country
        validated_data['state'] = state
        validated_data['city'] = city
        
        return super().create(validated_data)
