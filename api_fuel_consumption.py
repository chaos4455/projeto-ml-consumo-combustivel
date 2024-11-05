from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time
from datetime import datetime
import numpy as np
from collections import deque
import threading
import statistics

# Inicialização
console = Console()
app = FastAPI(title="API de Consumo de Combustível", version="1.0.0")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Métricas e KPIs
class APIMetrics:
    def __init__(self):
        self.total_requests = 0
        self.requests_by_endpoint = {}
        self.response_times = deque(maxlen=100)
        self.last_predictions = deque(maxlen=10)
        self.errors = 0
        self.start_time = datetime.now()

metrics = APIMetrics()

# Models Pydantic
class PredictionRequest(BaseModel):
    distance: float
    vehicle_type: str

class BatchPredictionRequest(BaseModel):
    predictions: list[PredictionRequest]

# Carregamento do modelo
try:
    console.print("[bold blue]🤖 Carregando modelo de ML...[/]")
    model = joblib.load('model.joblib')
    console.print("[bold green]✓ Modelo carregado com sucesso![/]")
except Exception as e:
    console.print("[bold red]❌ Erro ao carregar modelo![/]")
    raise e

# Função para atualizar o dashboard
def create_dashboard():
    layout = Layout()
    
    # Estatísticas gerais
    stats_table = Table(title="📊 Estatísticas da API")
    stats_table.add_column("Métrica", style="cyan")
    stats_table.add_column("Valor", style="magenta")
    
    uptime = datetime.now() - metrics.start_time
    avg_response = statistics.mean(metrics.response_times) if metrics.response_times else 0
    
    stats_table.add_row("Total Requisições", str(metrics.total_requests))
    stats_table.add_row("Erros", str(metrics.errors))
    stats_table.add_row("Tempo Médio Resposta", f"{avg_response:.2f}s")
    stats_table.add_row("Uptime", str(uptime).split('.')[0])
    
    # Últimas predições
    predictions_table = Table(title="🔍 Últimas Predições")
    predictions_table.add_column("Veículo", style="blue")
    predictions_table.add_column("Distância", style="green")
    predictions_table.add_column("Consumo", style="yellow")
    
    for pred in metrics.last_predictions:
        predictions_table.add_row(
            pred['vehicle_type'],
            f"{pred['distance']} km",
            f"{pred['consumption']:.2f}L"
        )
    
    return Panel(
        Layout(
            Layout(stats_table, name="stats"),
            Layout(predictions_table, name="predictions"),
        ),
        title="🚗 Dashboard Sistema de Previsão de Consumo",
        border_style="green"
    )

# Função para atualizar o console
def update_console():
    while True:
        with Live(create_dashboard(), refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(create_dashboard())

# Iniciar thread do dashboard
dashboard_thread = threading.Thread(target=update_console, daemon=True)
dashboard_thread.start()

# Rotas da API
@app.get("/")
async def root():
    metrics.total_requests += 1
    return {"message": "API de Previsão de Consumo de Combustível v1.0"}

@app.post("/predict/single")
async def predict_single(request: PredictionRequest):
    start_time = time.time()
    metrics.total_requests += 1
    
    try:
        # Consumo médio em km/l
        consumo_medio = {
            'carro': 12,
            'moto': 25,
            'caminhão': 3.5
        }
        
        if request.vehicle_type not in consumo_medio:
            raise HTTPException(status_code=400, detail="Tipo de veículo inválido")
        
        consumo = request.distance / consumo_medio[request.vehicle_type]
        
        # Atualizar métricas
        metrics.response_times.append(time.time() - start_time)
        metrics.last_predictions.append({
            'vehicle_type': request.vehicle_type,
            'distance': request.distance,
            'consumption': consumo
        })
        
        return {
            "vehicle_type": request.vehicle_type,
            "distance": request.distance,
            "predicted_consumption": consumo,
            "units": "litros"
        }
    
    except Exception as e:
        metrics.errors += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    start_time = time.time()
    metrics.total_requests += 1
    
    try:
        results = []
        for pred_request in request.predictions:
            consumo_medio = {
                'carro': 12,
                'moto': 25,
                'caminhão': 3.5
            }
            
            if pred_request.vehicle_type not in consumo_medio:
                raise HTTPException(status_code=400, detail=f"Tipo de veículo inválido: {pred_request.vehicle_type}")
            
            consumo = pred_request.distance / consumo_medio[pred_request.vehicle_type]
            
            results.append({
                "vehicle_type": pred_request.vehicle_type,
                "distance": pred_request.distance,
                "predicted_consumption": consumo,
                "units": "litros"
            })
            
            metrics.last_predictions.append({
                'vehicle_type': pred_request.vehicle_type,
                'distance': pred_request.distance,
                'consumption': consumo
            })
        
        metrics.response_times.append(time.time() - start_time)
        return {"predictions": results}
    
    except Exception as e:
        metrics.errors += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    metrics.total_requests += 1
    return {
        "total_requests": metrics.total_requests,
        "errors": metrics.errors,
        "avg_response_time": statistics.mean(metrics.response_times) if metrics.response_times else 0,
        "uptime": str(datetime.now() - metrics.start_time)
    }

if __name__ == "__main__":
    console.print("[bold green]🚀 Iniciando API...[/]")
    uvicorn.run(app, host="0.0.0.0", port=8000)
