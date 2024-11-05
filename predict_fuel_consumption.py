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
        # Consumo médio em km/l para cada tipo de veículo
        consumo_medio = {
            'carro': 12,    # 12 km/l
            'moto': 25,     # 25 km/l
            'caminhão': 3.5 # 3.5 km/l
        }
        
        # Calcula o consumo baseado na distância e no consumo médio
        consumo = distance / consumo_medio[vehicle_type]
        return consumo
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
