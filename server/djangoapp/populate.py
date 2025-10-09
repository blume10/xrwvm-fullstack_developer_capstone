from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]
    
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(name=data['name'], description=data['description'])
        )

    car_model_data = [
        {"name": "Pathfinder", "body_type": "SUV", "year": 2023, "make": car_make_instances[0]},
        {"name": "Qashqai", "body_type": "SUV", "year": 2023, "make": car_make_instances[0]},
        {"name": "XTRAIL", "body_type": "SUV", "year": 2023, "make": car_make_instances[0]},
        {"name": "A-Class", "body_type": "Sedan", "year": 2023, "make": car_make_instances[1]},
        {"name": "C-Class", "body_type": "Sedan", "year": 2023, "make": car_make_instances[1]},
        {"name": "E-Class", "body_type": "Sedan", "year": 2023, "make": car_make_instances[1]},
        {"name": "A4", "body_type": "Sedan", "year": 2023, "make": car_make_instances[2]},
        {"name": "A5", "body_type": "Sedan", "year": 2023, "make": car_make_instances[2]},
        {"name": "A6", "body_type": "SUV", "year": 2023, "make": car_make_instances[2]},
        {"name": "Sorrento", "body_type": "SUV", "year": 2023, "make": car_make_instances[3]},
        {"name": "Carnival", "body_type": "SUV", "year": 2023, "make": car_make_instances[3]},
        {"name": "Cerato", "body_type": "Sedan", "year": 2023, "make": car_make_instances[3]},
        {"name": "Corolla", "body_type": "Sedan", "year": 2023, "make": car_make_instances[4]},
        {"name": "Camry", "body_type": "Sedan", "year": 2023, "make": car_make_instances[4]},
        {"name": "Kluger", "body_type": "SUV", "year": 2023, "make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            make=data['make'],
            body_type=data['body_type'],
            year=data['year']
        )
  
