import pandas as pd
import random
from faker import Faker

fake = Faker('es_MX')  # Spanish locale for realistic city names

# Define ranges and options
CITIES = ['CDMX', 'Guadalajara', 'Monterrey', 'Puebla', 'Cancún', 'Mérida', 'Querétaro', 'Tijuana', 'León', 'Toluca']
YEARS = list(range(2000, 2025))

def generate_entry(entry_id):
    ciudad = random.choice(CITIES)
    precio = random.randint(400_000, 8_000_000)  # in MXN
    habitaciones = random.randint(1, 6)
    baños = random.randint(1, habitaciones)
    terreno_m2 = random.randint(40, 500)
    antiguedad = random.randint(0, 50)  # years
    tiene_garaje = random.choice([True, False])
    zona_segura = random.choices([True, False], weights=[0.7, 0.3])[0]  # 70% chance of being safe
    año_venta = random.choice(YEARS)

    return {
        'id': entry_id,
        'ciudad': ciudad,
        'precio': precio,
        'habitaciones': habitaciones,
        'baños': baños,
        'terreno_m2': terreno_m2,
        'antiguedad': antiguedad,
        'tiene_garaje': tiene_garaje,
        'zona_segura': zona_segura,
        'año_venta': año_venta
    }

# Generate 10,000 entries
data = [generate_entry(i + 1) for i in range(10_000)]

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("datos_casas_mexico.xlsx", index=False)
print("Archivo Excel 'datos_casas_mexico.xlsx' .")
