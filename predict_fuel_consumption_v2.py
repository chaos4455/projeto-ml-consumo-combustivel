import joblib
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
import colorama
import time
from rich.spinner import Spinner
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

colorama.init()
console = Console()

def loading_animation(message, seconds):
    with console.status(f"[bold blue]{message}") as status:
        time.sleep(seconds)

def inicializar_sistema():
    console.clear()
    console.print("[bold yellow]🚗 Sistema de Previsão de Consumo de Combustível v2.0[/]", justify="center")
    time.sleep(4)
    
    loading_animation("Inicializando sistema...", 4)
    
    try:
        console.print("\n[bold blue]Carregando modelo de ML...[/]")
        time.sleep(4)
        model = joblib.load('model.joblib')
        console.print("[bold green]✓ Modelo carregado com sucesso![/]")
        time.sleep(4)
        return model
    except FileNotFoundError:
        console.print("[bold red]❌ Erro: Arquivo 'model.joblib' não encontrado.[/]")
        exit()
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao carregar o modelo: {e}[/]")
        exit()

def predict_consumption(distance, vehicle_type, model):
    try:
        console.print(f"\n[cyan]Analisando dados para {vehicle_type}...[/]")
        time.sleep(4)
        
        # Consumo médio em km/l para cada tipo de veículo
        consumo_medio = {
            'carro': 12,    # 12 km/l
            'moto': 25,     # 25 km/l
            'caminhão': 3.5 # 3.5 km/l
        }
        
        # Simula uso do modelo (você pode substituir isso pelo seu modelo real)
        consumo = distance / consumo_medio[vehicle_type]
        
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Calculando consumo para {vehicle_type}...", total=100)
            for i in range(100):
                time.sleep(0.04)  # Total de 4 segundos
                progress.update(task, advance=1)
        
        return consumo
    except Exception as e:
        console.print(f"[bold red]❌ Erro na predição: {e}[/]")
        return None

def main():
    model = inicializar_sistema()
    
    console.print("\n[bold yellow]📊 Iniciando análise de consumo[/]")
    time.sleep(4)
    
    vehicle_types = {
        'carro': 'carro',
        'moto': 'moto',
        'caminhão': 'caminhão'
    }
    
    while True:
        console.print("\n[bold cyan]Digite a distância em quilômetros:[/]")
        distance = float(Prompt.ask(""))
        
        console.print("\n[bold yellow]Iniciando cálculos...[/]")
        time.sleep(4)
        
        results = {}
        for pt_vehicle, en_vehicle in vehicle_types.items():
            consumption = predict_consumption(distance, en_vehicle, model)
            if consumption is not None:
                results[pt_vehicle] = consumption
            else:
                console.print(f"[bold red]Falha na previsão para {pt_vehicle}. Tentando novamente...[/]")
                continue
        break
    
    console.print("\n[bold green]Gerando relatório final...[/]")
    time.sleep(4)
    
    table = Table(title=f"🔍 Previsão de Consumo para {distance:.2f} km")
    table.add_column("Veículo", style="cyan", justify="center")
    table.add_column("Consumo (litros)", style="magenta", justify="center")
    
    for vehicle_type, consumption in results.items():
        table.add_row(vehicle_type, f"{consumption:.2f} ⛽")
    
    console.print("\n")
    console.print(Panel(table, title="Resultados", border_style="green"))
    
    time.sleep(4)
    console.print("\n[bold yellow]Calculando economia relativa...[/]")
    time.sleep(4)
    
    consumptions = list(results.values())
    if consumptions:
        avg_consumption = np.mean(consumptions)
        for vehicle_type, consumption in results.items():
            economia = (consumption - avg_consumption) * 100 / avg_consumption if avg_consumption != 0 else 0
            text = Text()
            text.append(f"{vehicle_type}: ", style="cyan")
            if economia < 0:
                text.append(f"{abs(economia):.2f}% mais econômico que a média", style="green")
            else:
                text.append(f"{economia:.2f}% menos econômico que a média", style="red")
            console.print(text)
            time.sleep(4)
    else:
        console.print("[bold red]Não foi possível calcular a economia. Nenhum consumo previsto.[/]")
    
    time.sleep(4)
    console.print("\n[bold green]✨ Análise concluída com sucesso![/]")

if __name__ == "__main__":
    main()
