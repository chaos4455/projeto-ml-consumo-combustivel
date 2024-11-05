import joblib
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
import colorama
colorama.init()

try:
    model = joblib.load('model.joblib')
except FileNotFoundError:
    print(colorama.Fore.RED + "Erro: Arquivo 'model.joblib' não encontrado." + colorama.Style.RESET_ALL)
    exit()
except Exception as e:
    print(colorama.Fore.RED + f"Erro ao carregar o modelo: {e}" + colorama.Style.RESET_ALL)
    exit()

console = Console()

def predict_consumption(distance, vehicle_type):
    try:
        # Usar diferentes velocidades para diferentes tipos de veículo
        velocidades = {
            'carro': 90,
            'moto': 85,
            'caminhão': 75
        }
        
        input_data = pd.DataFrame({
            'distance': [distance],
            'vehicle_type': [vehicle_type],
            'speed': [velocidades[vehicle_type]]
        })

        # Obter os nomes das colunas do modelo treinado
        feature_names = model.feature_names_in_
        
        # Criar as features one-hot encoded usando os nomes das colunas do modelo
        input_data = pd.get_dummies(input_data, columns=['vehicle_type'], prefix=['vehicle_type'])
        
        # Adicionar colunas ausentes com valor 0
        missing_cols = set(feature_names) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0

        # Selecionar apenas as colunas presentes no modelo treinado
        input_data = input_data[feature_names]

        consumption = model.predict(input_data)[0]
        return consumption
    except Exception as e:
        print(colorama.Fore.RED + f"Erro na predição: {e}" + colorama.Style.RESET_ALL)
        return None

vehicle_types = {
    'carro': 'carro',
    'moto': 'moto',
    'caminhão': 'caminhão'
}

while True:
    distance = float(Prompt.ask("Digite a distância (km)"))
    
    results = {}
    for pt_vehicle, en_vehicle in vehicle_types.items():
        consumption = predict_consumption(distance, en_vehicle)
        if consumption is not None:
            results[pt_vehicle] = consumption
        else:
            print(colorama.Fore.RED + f"Falha na previsão para o veículo {pt_vehicle}. Tentando novamente..." + colorama.Style.RESET_ALL)
            continue
    break

table = Table(title=f"Previsão de Consumo para {distance:.2f} km")
table.add_column("Veículo", style="cyan")
table.add_column("Consumo (litros)", style="magenta")

for vehicle_type, consumption in results.items():
    table.add_row(vehicle_type, f"{consumption:.2f} ⛽")

console.print(table)

consumptions = list(results.values())
if consumptions:
    avg_consumption = np.mean(consumptions)
    for vehicle_type, consumption in results.items():
        economia = (consumption - avg_consumption) * 100 / avg_consumption if avg_consumption !=0 else 0
        print(f"Economia de {vehicle_type} em relação à média: {economia:.2f}%")
else:
    print(colorama.Fore.RED + "Não foi possível calcular a economia. Nenhum consumo previsto." + colorama.Style.RESET_ALL)

print(colorama.Fore.GREEN + "Previsão concluída!" + colorama.Style.RESET_ALL)
