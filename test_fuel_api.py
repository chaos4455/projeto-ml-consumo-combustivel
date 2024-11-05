import requests
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich import box
from datetime import datetime
import statistics
from rich.live import Live

console = Console()

# Configuração da API
API_URL = "http://localhost:8000"

class TestMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = datetime.now()
        self.response_times = []
        self.predictions = []

metrics = TestMetrics()

def make_request(endpoint, data=None):
    try:
        start_time = time.time()
        if data:
            response = requests.post(f"{API_URL}{endpoint}", json=data)
        else:
            response = requests.get(f"{API_URL}{endpoint}")
        
        elapsed_time = time.time() - start_time
        metrics.response_times.append(elapsed_time)
        metrics.total_requests += 1
        
        if response.status_code == 200:
            metrics.successful_requests += 1
            return response.json()
        else:
            metrics.failed_requests += 1
            return None
    except Exception as e:
        metrics.failed_requests += 1
        console.print(f"[bold red]❌ Erro na requisição: {str(e)}[/]")
        return None

def create_dashboard():
    # Tabela de Métricas
    metrics_table = Table(title="📊 Métricas de Teste", box=box.ROUNDED)
    metrics_table.add_column("Métrica", style="cyan")
    metrics_table.add_column("Valor", style="magenta")
    
    uptime = datetime.now() - metrics.start_time
    avg_response = statistics.mean(metrics.response_times) if metrics.response_times else 0
    
    metrics_table.add_row("Total de Requisições", f"🔢 {metrics.total_requests}")
    metrics_table.add_row("Requisições com Sucesso", f"✅ {metrics.successful_requests}")
    metrics_table.add_row("Falhas", f"❌ {metrics.failed_requests}")
    metrics_table.add_row("Tempo Médio (s)", f"⏱️ {avg_response:.3f}")
    metrics_table.add_row("Tempo de Execução", f"⏰ {str(uptime).split('.')[0]}")
    
    # Tabela de Últimas Previsões
    predictions_table = Table(title="🔍 Últimas Previsões", box=box.ROUNDED)
    predictions_table.add_column("Veículo", style="blue")
    predictions_table.add_column("Distância (km)", style="green")
    predictions_table.add_column("Consumo (L)", style="yellow")
    
    for pred in metrics.predictions[-5:]:
        predictions_table.add_row(
            pred['vehicle_type'],
            str(pred['distance']),
            f"{pred['consumption']:.2f}"
        )
    
    layout = Layout()
    layout.split_column(
        Layout(metrics_table, name="metrics"),
        Layout(predictions_table, name="predictions")
    )
    
    return Panel(
        layout,
        title="🚗 Dashboard de Testes da API",
        border_style="green"
    )

def run_tests():
    console.clear()
    console.print("[bold yellow]🚀 Iniciando Testes da API[/]\n")
    
    # Verificar conexão com a API
    console.print("[cyan]Verificando conexão com a API...[/]")
    response = make_request("/")
    if not response:
        console.print("[bold red]❌ API não está respondendo![/]")
        return
    
    console.print("[bold green]✅ API está online![/]\n")
    time.sleep(1)
    
    questions = [
        ("Viagem curta de carro", 50, "carro"),
        ("Viagem média de carro", 200, "carro"),
        ("Viagem longa de carro", 500, "carro"),
        ("Delivery de moto", 100, "moto"),
        ("Viagem de moto", 300, "moto"),
        ("Entrega local de caminhão", 150, "caminhão"),
        ("Entrega regional de caminhão", 450, "caminhão"),
        ("Viagem interestadual de carro", 1000, "carro"),
        ("Viagem de moto longa", 800, "moto"),
        ("Entrega nacional de caminhão", 2000, "caminhão"),
    ]
    
    with Live(create_dashboard(), refresh_per_second=1) as live:
        for desc, distance, vehicle in questions:
            console.print(f"\n[bold cyan]Testando: {desc}[/]")
            
            data = {
                "distance": distance,
                "vehicle_type": vehicle
            }
            
            response = make_request("/predict/single", data)
            
            if response:
                metrics.predictions.append({
                    'vehicle_type': vehicle,
                    'distance': distance,
                    'consumption': response['predicted_consumption']
                })
                
                console.print(Panel(
                    f"Distância: {distance} km\n"
                    f"Veículo: {vehicle}\n"
                    f"Consumo Previsto: {response['predicted_consumption']:.2f} litros",
                    title="✅ Resultado",
                    border_style="green"
                ))
            else:
                console.print("[bold red]❌ Falha na previsão[/]")
            
            time.sleep(2)
            live.update(create_dashboard())
    
    # Relatório Final
    console.print("\n[bold green]📑 Relatório Final dos Testes[/]")
    console.print(create_dashboard())

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        console.print(f"[bold red]❌ Erro: {str(e)}[/]")
