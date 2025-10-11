import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
from loguru import logger

class DataGenerator:
    def __init__(self, num_operations, seed, output_dir, file_name, base_date, range_days: int = 730):
        self.num_operations = num_operations
        self.seed = seed
        self.output_dir = output_dir
        self.file_name = file_name
        self.base_date = base_date
        self.range_days = range_days
        self._set_seed()
        self._check_dirs()
        self._generate_static_data()

    def _set_seed(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def _check_dirs(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _generate_static_data(self):

        self.ports = {
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
        
        self.municipalities = {
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
        
        self.commodities = {
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
            },
            'Wheat': {
                'density': 0.78,
                'harvest_seasonality': [10, 11, 12, 1, 2],
                'base_price': 1200,
                'price_variation': 0.3
            }
        }

    def _choose_commodity(self, state):
        if state in ['MT', 'MS', 'GO']:
            commodity = random.choices(['Soy', 'Corn', 'Cotton', 'Soybean Meal'], weights=[45, 35, 10, 10])[0]
        elif state in ['BA', 'MA', 'PI', 'TO']:
            commodity = random.choices(['Soy', 'Corn', 'Cotton'], weights=[50, 30, 20])[0]
        elif state in ['PR', 'RS']:
            commodity = random.choices(['Soy', 'Corn', 'Wheat'], weights=[40, 40, 20])[0]
        elif state == 'SP':
            commodity = random.choices(['Soy', 'Corn', 'Sugar', 'Coffee'], weights=[30, 30, 25, 15])[0]
        else:
            commodity = random.choice(['Soy', 'Corn'])

        return commodity

    def generate_origin_data(self):
        municipality = random.choice(list(self.municipalities.keys()))
        origin_state = self.municipalities.get(municipality).get('state')
        commodity = self._choose_commodity(state=origin_state)
        lat1 = self.municipalities.get(municipality).get('lat')
        lon1 = self.municipalities.get(municipality).get('lon')

        return municipality, origin_state, commodity, lat1, lon1

    def generate_port_data(self):
        port = random.choice(list(self.ports.keys()))
        lat2 = self.ports.get(port).get('lat')
        lon2 = self.ports.get(port).get('lon')

        return port, lat2, lon2

    def generate_seasonality_mult(self, operation_month, commodity):
        seasonality_mult = 1.0
        seasons = self.commodities.get(commodity).get('harvest_seasonality')
        if operation_month in seasons:
            seasonality_mult = random.uniform(1.2, 1.8)
        else:
            seasonality_mult = random.uniform(0.7, 1.1)
        
        return seasonality_mult

    def generate_tonnage(self, distance, seasonality_mult):
        
        if distance < 500:
            base_tonnage = random.uniform(25, 35)
        elif distance < 1000:
            base_tonnage = random.uniform(30, 40)
        else:
            base_tonnage = random.uniform(35, 45)

        return base_tonnage * seasonality_mult

    def generate_economic_data(self, port, seasonality_mult, distance, tonnage, commodity):
        
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

        cost_per_ton = (base_cost_per_km * distance + fixed_cost) * fuel_factor * seasonality_factor * port_factor
        cost_per_ton *= random.uniform(0.85, 1.15)
        
        total_cost = cost_per_ton * tonnage
        price_var = random.uniform(1 - self.commodities.get(commodity).get('price_variation'), 1 + self.commodities.get(commodity).get('price_variation')) 
        commodity_price = self.commodities.get(commodity).get('base_price') * price_var

        return total_cost, commodity_price, cost_per_ton

    def generate(self):

        data = []

        logger.info(f"Generating {self.num_operations} operations")
        for i in range(self.num_operations):
            municipality, origin_state, commodity, lat1, lon1 = self.generate_origin_data()
            port, lat2, lon2 = self.generate_port_data()

            ## calculate distance
            distance_km = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2) * 111

            ## date
            fmt = "%Y-%m-%d"
            base_date = datetime.strptime(self.base_date, fmt)
            operation_date = base_date + timedelta(days=random.randint(0, self.range_days))
            operation_month = operation_date.month

            ## seasonality multiplier
            season_mult = self.generate_seasonality_mult(operation_month, commodity)

            ## generate tonnage
            tonnage = self.generate_tonnage(distance_km, season_mult)

            ## generate economic data
            total_cost, commodity_price, cost_per_ton = self.generate_economic_data(port, season_mult, distance_km, tonnage, commodity)

            ## append data
            
            data.append({
                'operation_date': operation_date.strftime('%Y-%m-%d'),
                'origin_municipality': municipality,
                'origin_state': origin_state,
                'origin_lat': lat1,
                'origin_lon': lon1,
                'destination_port': port,
                'destination_state': self.ports.get(port).get('state'),
                'destination_lat': lat2,
                'destination_lon': lon2,
                'commodity': commodity,
                'tonnage': round(tonnage, 2),
                'distance_km': round(distance_km, 0),
                'total_freight_value': round(total_cost, 2),
                'value_per_ton': round(cost_per_ton, 2),
                'commodity_reference_price': round(commodity_price, 2),
                'month': operation_month,
                'year': operation_date.year,
                'route': f"{municipality}_{origin_state}->{port}_{self.ports.get(port).get('state')}"
            })


        ## final df
        df = pd.DataFrame(data)
        df = df.sort_values('operation_date').reset_index(drop=True)    
        output_path = os.path.join(self.output_dir, self.file_name)
        df.to_csv(output_path, index=False)
    
        return df