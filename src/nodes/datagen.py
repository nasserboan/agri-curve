"""Data generation node - moved from pipelines/datagen/nodes.py"""
import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

def generate_logistics_transport_data(
    num_operations=5000,
    seed=42,
    data_dir='data',
    output_filename='logistics_transport_data.csv'
):
    """
    Generates synthetic logistics transport operations data between producer 
    municipalities and Brazilian ports for cost forecasting analysis.
    
    Parameters:
    num_operations (int): Number of transport operations to generate
    seed (int): Seed for data reproducibility
    data_dir (str): Directory to save the data
    
    Returns:
    pandas.DataFrame: DataFrame with transport operations data
    """
    
    random.seed(seed)
    np.random.seed(seed)
    
    # Ensure output directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    ports = {
        'Santos': {'lat': -23.944841, 'lon': -46.330376, 'state': 'SP'},
        'Paranaguá': {'lat': -25.520000, 'lon': -48.508889, 'state': 'PR'},
        'Rio Grande': {'lat': -32.034315, 'lon': -52.099266, 'state': 'RS'},
        'Itaqui': {'lat': -2.592778, 'lon': -44.366667, 'state': 'MA'},
        'Belém': {'lat': -1.455833, 'lon': -48.504167, 'state': 'PA'},
        'Itacoatiara': {'lat': -3.143056, 'lon': -58.444167, 'state': 'AM'},
        'Vitória': {'lat': -20.315556, 'lon': -40.312222, 'state': 'ES'},
        'Suape': {'lat': -8.421667, 'lon': -35.006667, 'state': 'PE'},
        'Ilhéus': {'lat': -14.795833, 'lon': -39.045833, 'state': 'BA'},
        'Navegantes': {'lat': -26.896944, 'lon': -48.632222, 'state': 'SC'}
    }
    
    municipalities = {
        # 10 major agricultural cities
        'Sorriso': {'lat': -12.544722, 'lon': -55.711389, 'state': 'MT'},
        'Lucas do Rio Verde': {'lat': -13.050556, 'lon': -55.911111, 'state': 'MT'},
        'Primavera do Leste': {'lat': -15.559167, 'lon': -54.2975, 'state': 'MT'},
        'Rondonópolis': {'lat': -16.470833, 'lon': -54.635833, 'state': 'MT'},
        'Rio Verde': {'lat': -17.798056, 'lon': -50.930556, 'state': 'GO'},
        'Dourados': {'lat': -22.221111, 'lon': -54.805556, 'state': 'MS'},
        'São Desidério': {'lat': -12.363056, 'lon': -44.974167, 'state': 'BA'},
        'Cascavel': {'lat': -24.955556, 'lon': -53.455556, 'state': 'PR'},
        'Cruz Alta': {'lat': -28.638611, 'lon': -53.606389, 'state': 'RS'},
        'Balsas': {'lat': -7.532500, 'lon': -46.035556, 'state': 'MA'}
    }
    
    commodities = {
        'Soy': {
            'density': 0.75,
            'harvest_seasonality': [2, 3, 4, 5],
            'base_price': 1800,
            'price_variation': 0.3
        },
        'Corn': {
            'density': 0.72,
            'harvest_seasonality': [6, 7, 8, 9],
            'base_price': 950,
            'price_variation': 0.25
        },
        'Cotton': {
            'density': 0.32,
            'harvest_seasonality': [6, 7, 8],
            'base_price': 8500,
            'price_variation': 0.4
        },
        'Sugar': {
            'density': 0.8,
            'harvest_seasonality': [4, 5, 6, 7, 8, 9, 10],
            'base_price': 2200,
            'price_variation': 0.35
        },
        'Coffee': {
            'density': 0.65,
            'harvest_seasonality': [5, 6, 7, 8],
            'base_price': 12500,
            'price_variation': 0.5
        },
        'Soybean Meal': {
            'density': 0.6,
            'harvest_seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'base_price': 2100,
            'price_variation': 0.3
        },
        'Soybean Oil': {
            'density': 0.92,
            'harvest_seasonality': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'base_price': 4500,
            'price_variation': 0.4
        }
    }
    
    data = []
    
    for i in range(num_operations):
        municipality = random.choice(list(municipalities.keys()))
        port = random.choice(list(ports.keys()))
        
        origin_state = municipalities[municipality]['state']
        if origin_state in ['MT', 'MS', 'GO']:
            commodity = random.choices(['Soy', 'Corn', 'Cotton', 'Soybean Meal'], 
                                     weights=[45, 35, 10, 10])[0]
        elif origin_state in ['BA', 'MA', 'PI', 'TO']:
            commodity = random.choices(['Soy', 'Corn', 'Cotton'], 
                                     weights=[50, 30, 20])[0]
        elif origin_state in ['PR', 'RS']:
            commodity = random.choices(['Soy', 'Corn', 'Wheat'], 
                                     weights=[40, 40, 20])[0]
        elif origin_state == 'SP':
            commodity = random.choices(['Soy', 'Corn', 'Sugar', 'Coffee'], 
                                     weights=[30, 30, 25, 15])[0]
        else:
            commodity = random.choice(['Soy', 'Corn'])
        
        if commodity not in commodities:
            commodity = 'Soy'
        
        lat1, lon1 = municipalities[municipality]['lat'], municipalities[municipality]['lon']
        lat2, lon2 = ports[port]['lat'], ports[port]['lon']
        distance_km = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2) * 111
        
        base_date = datetime(2023, 1, 1)
        operation_date = base_date + timedelta(days=random.randint(0, 730))
        operation_month = operation_date.month

        seasonality_mult = 1.0
        if operation_month in commodities[commodity]['harvest_seasonality']:
            seasonality_mult = random.uniform(1.2, 1.8)
        else:
            seasonality_mult = random.uniform(0.7, 1.1)
        
        if distance_km < 500:
            base_tonnage = random.uniform(25, 35)
        elif distance_km < 1000:
            base_tonnage = random.uniform(30, 40)
        else:
            base_tonnage = random.uniform(35, 45)
        
        tonnage = base_tonnage * seasonality_mult

        base_cost_per_km = random.uniform(0.12, 0.18)
        fixed_cost = random.uniform(50, 150)

        fuel_factor = random.uniform(0.9, 1.3)
        seasonality_factor = seasonality_mult * 0.3 + 0.7
        port_factor = 1.0
        
        if port in ['Santos', 'Paranaguá']:
            port_factor = random.uniform(1.1, 1.3)
        elif port in ['Rio Grande', 'Itaqui']:
            port_factor = random.uniform(1.0, 1.2)
        else:
            port_factor = random.uniform(0.9, 1.1)

        cost_per_ton = (base_cost_per_km * distance_km + fixed_cost) * fuel_factor * seasonality_factor * port_factor
        cost_per_ton *= random.uniform(0.85, 1.15)
        
        total_value = cost_per_ton * tonnage
        commodity_price = commodities[commodity]['base_price'] * random.uniform(
            1 - commodities[commodity]['price_variation'],
            1 + commodities[commodity]['price_variation']
        )
        
        data.append({
            'operation_date': operation_date.strftime('%Y-%m-%d'),
            'origin_municipality': municipality,
            'origin_state': municipalities[municipality]['state'],
            'origin_lat': municipalities[municipality]['lat'],
            'origin_lon': municipalities[municipality]['lon'],
            'destination_port': port,
            'destination_state': ports[port]['state'],
            'destination_lat': ports[port]['lat'],
            'destination_lon': ports[port]['lon'],
            'commodity': commodity,
            'tonnage': round(tonnage, 2),
            'distance_km': round(distance_km, 0),
            'total_freight_value': round(total_value, 2),
            'value_per_ton': round(cost_per_ton, 2),
            'commodity_reference_price': round(commodity_price, 2),
            'month': operation_month,
            'year': operation_date.year,
            'route': f"{municipality}_{municipalities[municipality]['state']}-{port}_{ports[port]['state']}"
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('operation_date').reset_index(drop=True)
    
    output_path = os.path.join(data_dir, output_filename)
    df.to_csv(output_path, index=False)
    
    return df