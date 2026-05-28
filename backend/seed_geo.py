
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import Country, Zone, State, City, Pincode

def seed_geo():
    print("Seeding with 100% REAL LOOKING names for all 3600 cities...")
    Pincode.objects.all().delete()
    City.objects.all().delete()

    india, _ = Country.objects.get_or_create(code='IN', defaults={'name': 'India'})
    zones = ['North', 'South', 'East', 'West']
    zone_objs = {z: Zone.objects.get_or_create(name=z, country=india)[0] for z in zones}

    STATE_ZONES = {
        'North': ['Delhi', 'Rajasthan', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Uttarakhand', 'Uttar Pradesh', 'Jammu and Kashmir', 'Ladakh'],
        'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana', 'Andaman and Nicobar Islands', 'Lakshadweep', 'Puducherry'],
        'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'Sikkim', 'Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Tripura'],
        'West': ['Goa', 'Gujarat', 'Maharashtra', 'Dadra and Nagar Haveli and Daman and Diu', 'Madhya Pradesh', 'Chhattisgarh']
    }

    REAL_TOP = {
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Noida', 'Meerut', 'Ghaziabad', 'Prayagraj', 'Bareilly', 'Aligarh'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane', 'Aurangabad', 'Solapur', 'Amravati', 'Navi Mumbai', 'Kolhapur'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer', 'Bikaner', 'Bhilwara', 'Alwar', 'Bharatpur', 'Sikar'],
        # ... (I'll use a generator for others to ensure 100 unique names)
    }

    PREFIXES = ['Ram', 'Shanti', 'Vijay', 'Krishna', 'Mohan', 'Suraj', 'Gopal', 'Aman', 'Kushal', 'Vikram', 'Ravi', 'Uday', 'Anand', 'Bharat', 'Jay', 'Shiv', 'Durga', 'Mantra', 'Prem', 'Satya', 'Kalyan', 'Om', 'Vishwa', 'Guru', 'Hari', 'Govind', 'Rudra', 'Brahma', 'Indra', 'Varun']
    SUFFIXES = ['pur', 'nagar', 'ganj', 'garh', 'abad', 'kunj', 'ghat', 'vihar', 'dham', 'wara', 'pada', 'pally', 'pet', 'puram', 'gram', 'city', 'town', 'valley', 'park', 'square', 'heights', 'colony', 'path', 'marg']

    state_to_zone = {s: zone_objs[z] for z, states in STATE_ZONES.items() for s in states}
    all_states = State.objects.all()
    
    for state in all_states:
        state.zone = state_to_zone.get(state.name, zone_objs['North'])
        state.save()
        print(f"Seeding {state.name}...")
        
        # Real names if available
        real_list = REAL_TOP.get(state.name, [])
        cities = []
        
        # Generate exactly 100 names
        used_names = set()
        for i in range(100):
            if i < len(real_list):
                name = real_list[i]
            else:
                # Generate a unique-looking Indian city name
                while True:
                    name = random.choice(PREFIXES) + random.choice(SUFFIXES)
                    if name not in used_names and name not in real_list:
                        break
            
            used_names.add(name)
            city, _ = City.objects.get_or_create(name=name, state=state)
            cities.append(city)
            
        # Pincodes
        prefix = str((hash(state.name) % 80) + 10).zfill(2)
        for i in range(200):
            code = f"{prefix}{str(2000 + i)}"
            target_city = random.choice(cities)
            Pincode.objects.get_or_create(code=code, defaults={'city': target_city})

    print("Geo Seed completed with 100% unique looking names!")

if __name__ == "__main__":
    seed_geo()
