import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Constants for choices
PROPERTY_TYPES = ['house', 'apartment', 'condo', 'townhouse', 'villa', 'commercial', 'land', 'other']
LISTING_TYPES = ['sale', 'rent', 'both']
PROJECT_TYPES = ['residential', 'commercial', 'mixed_use', 'industrial', 'retail', 'office', 'hospitality']
PROJECT_STATUSES = ['planning', 'under_construction', 'nearing_completion', 'completed', 'on_hold']

# Cities and states
CITIES = [
    ('New York', 'NY'), ('Los Angeles', 'CA'), ('Chicago', 'IL'), ('Houston', 'TX'), 
    ('Phoenix', 'AZ'), ('Philadelphia', 'PA'), ('San Antonio', 'TX'), ('San Diego', 'CA'),
    ('Dallas', 'TX'), ('San Jose', 'CA'), ('Austin', 'TX'), ('Jacksonville', 'FL'),
    ('Fort Worth', 'TX'), ('Columbus', 'OH'), ('Charlotte', 'NC'), ('San Francisco', 'CA'),
    ('Indianapolis', 'IN'), ('Seattle', 'WA'), ('Denver', 'CO'), ('Washington', 'DC'),
    ('Boston', 'MA'), ('El Paso', 'TX'), ('Nashville', 'TN'), ('Detroit', 'MI'),
    ('Oklahoma City', 'OK'), ('Portland', 'OR'), ('Las Vegas', 'NV'), ('Memphis', 'TN'),
    ('Louisville', 'KY'), ('Baltimore', 'MD'), ('Milwaukee', 'WI'), ('Albuquerque', 'NM'),
    ('Tucson', 'AZ'), ('Fresno', 'CA'), ('Mesa', 'AZ'), ('Sacramento', 'CA'),
    ('Atlanta', 'GA'), ('Kansas City', 'MO'), ('Colorado Springs', 'CO'), ('Miami', 'FL')
]

def generate_listings():
    """Generate 100 listing fixtures"""
    listings = []
    
    for i in range(1, 101):
        city, state = random.choice(CITIES)
        listing_type = random.choice(LISTING_TYPES)
        property_type = random.choice(PROPERTY_TYPES)
        
        # Generate prices based on listing type
        price = random.randint(150000, 2000000) if listing_type in ['sale', 'both'] else 0
        rent_price = random.randint(800, 5000) if listing_type in ['rent', 'both'] else None
        deposit_amount = rent_price if rent_price else None
        
        listing = {
            "model": "listings.listing",
            "pk": i,
            "fields": {
                "realtor": random.randint(1, 15),
                "submitted_by": None,
                "title": f"{fake.catch_phrase()} {property_type.title()} in {city}",
                "address": fake.street_address(),
                "city": city,
                "state": state,
                "zipcode": fake.zipcode(),
                "description": f"Beautiful {property_type} featuring {fake.text(max_nb_chars=300)}",
                "listing_type": listing_type,
                "price": price,
                "rent_price": rent_price,
                "deposit_amount": deposit_amount,
                "bedrooms": random.randint(1, 6),
                "bathrooms": round(random.uniform(1.0, 4.5), 1),
                "garage": random.randint(0, 3),
                "sqft": random.randint(500, 5000),
                "lot_size": round(random.uniform(0.1, 2.0), 1),
                "photo_main": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_main.jpg",
                "photo_1": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_1.jpg" if random.choice([True, False]) else "",
                "photo_2": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_2.jpg" if random.choice([True, False]) else "",
                "photo_3": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_3.jpg" if random.choice([True, False]) else "",
                "photo_4": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_4.jpg" if random.choice([True, False]) else "",
                "photo_5": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_5.jpg" if random.choice([True, False]) else "",
                "photo_6": f"photos/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/listing_{i}_6.jpg" if random.choice([True, False]) else "",
                "is_published": random.choice([True, True, True, False]),  # 75% published
                "list_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat() + "Z",
                "property_type": property_type,
                "year_built": random.randint(1950, 2024),
                "hoa_fee": round(random.uniform(0, 500), 2) if random.choice([True, False]) else None,
                "view_count": random.randint(0, 1000),
                "featured": random.choice([True, False, False, False]),  # 25% featured
                "virtual_tour_url": f"https://virtualtour.com/listing_{i}" if random.choice([True, False]) else "",
                "energy_rating": random.choice(['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', '']) if random.choice([True, False]) else "",
                "last_updated": datetime.now().isoformat() + "Z"
            }
        }
        listings.append(listing)
    
    return listings

def generate_projects():
    """Generate 100 project fixtures"""
    projects = []
    
    for i in range(1, 101):
        city, state = random.choice(CITIES)
        project_type = random.choice(PROJECT_TYPES)
        status = random.choice(PROJECT_STATUSES)
        
        # Generate dates based on status
        if status == 'completed':
            start_date = fake.date_between(start_date='-3y', end_date='-1y')
            expected_completion = fake.date_between(start_date=start_date, end_date='today')
            launch_date = fake.date_between(start_date=start_date, end_date=expected_completion)
        elif status in ['under_construction', 'nearing_completion']:
            start_date = fake.date_between(start_date='-2y', end_date='today')
            expected_completion = fake.date_between(start_date='today', end_date='+2y')
            launch_date = fake.date_between(start_date='-1y', end_date='today')
        else:  # planning or on_hold
            start_date = fake.date_between(start_date='-1y', end_date='+1y')
            expected_completion = fake.date_between(start_date='+6m', end_date='+3y')
            launch_date = fake.date_between(start_date='today', end_date='+1y')
        
        total_units = random.randint(10, 500)
        available_units = random.randint(0, total_units) if status != 'completed' else random.randint(0, int(total_units * 0.3))
        
        project = {
            "model": "projects.project",
            "pk": i,
            "fields": {
                "name": f"{fake.company()} {project_type.replace('_', ' ').title()}",
                "developer": random.randint(1, 15),
                "project_type": project_type,
                "status": status,
                "address": fake.street_address(),
                "city": city,
                "state": state,
                "zipcode": fake.zipcode(),
                "description": f"Premier {project_type.replace('_', ' ')} development featuring {fake.text(max_nb_chars=400)}",
                "total_units": total_units,
                "available_units": available_units,
                "price_range_min": random.randint(200000, 500000),
                "price_range_max": random.randint(500000, 2000000),
                "start_date": start_date.isoformat(),
                "expected_completion": expected_completion.isoformat(),
                "launch_date": launch_date.isoformat(),
                "total_area": round(random.uniform(50000, 500000), 2),
                "floors": random.randint(1, 50) if project_type != 'land' else None,
                "parking_spaces": random.randint(total_units, total_units * 2),
                "green_building_certified": random.choice([True, False]),
                "main_image": f"projects/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_main.jpg",
                "floor_plan": f"projects/floor_plans/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_floor_plan.jpg" if random.choice([True, False]) else "",
                "brochure": f"projects/brochures/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_brochure.pdf" if random.choice([True, False]) else "",
                "gallery_image_1": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_1.jpg" if random.choice([True, False]) else "",
                "gallery_image_2": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_2.jpg" if random.choice([True, False]) else "",
                "gallery_image_3": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_3.jpg" if random.choice([True, False]) else "",
                "gallery_image_4": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_4.jpg" if random.choice([True, False]) else "",
                "gallery_image_5": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_5.jpg" if random.choice([True, False]) else "",
                "gallery_image_6": f"projects/gallery/2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}/project_{i}_gallery_6.jpg" if random.choice([True, False]) else "",
                "featured": random.choice([True, False, False, False]),  # 25% featured
                "is_published": random.choice([True, True, True, False]),  # 75% published
                "view_count": random.randint(0, 2000),
                "virtual_tour_url": f"https://virtualtour.com/project_{i}" if random.choice([True, False]) else "",
                "website_url": f"https://www.project{i}.com" if random.choice([True, False]) else "",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat() + "Z",
                "updated_at": datetime.now().isoformat() + "Z"
            }
        }
        projects.append(project)
    
    return projects

def generate_project_features():
    """Generate project features (linking projects to amenities)"""
    features = []
    pk = 1
    
    for project_id in range(1, 101):
        # Each project gets 3-8 random amenities
        num_amenities = random.randint(3, 8)
        selected_amenities = random.sample(range(1, 16), num_amenities)
        
        for amenity_id in selected_amenities:
            feature = {
                "model": "projects.projectfeature",
                "pk": pk,
                "fields": {
                    "project": project_id,
                    "amenity": amenity_id,
                    "included": random.choice([True, True, True, False]),  # 75% included
                    "additional_info": fake.sentence() if random.choice([True, False]) else ""
                }
            }
            features.append(feature)
            pk += 1
    
    return features

def main():
    # Generate all fixtures
    print("Generating listings fixtures...")
    listings = generate_listings()
    
    print("Generating projects fixtures...")
    projects = generate_projects()
    
    print("Generating project features fixtures...")
    project_features = generate_project_features()
    
    # Write to files
    print("Writing listings fixtures...")
    with open('src/listings/fixtures/listings.json', 'w') as f:
        json.dump(listings, f, indent=2)
    
    print("Writing projects fixtures...")
    with open('src/projects/fixtures/projects.json', 'w') as f:
        json.dump(projects, f, indent=2)
    
    print("Writing project features fixtures...")
    with open('src/projects/fixtures/project_features.json', 'w') as f:
        json.dump(project_features, f, indent=2)
    
    print("All fixtures generated successfully!")
    print(f"Generated {len(listings)} listings")
    print(f"Generated {len(projects)} projects")
    print(f"Generated {len(project_features)} project features")

if __name__ == "__main__":
    main() 