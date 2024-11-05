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
import random  # Adicione no topo do arquivo

# Inicialização
console = Console()
app = FastAPI(title="API de Consumo de Combustível", version="1.1.0") # Updated version here

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
    return {"message": "API de Previsão de Consumo de Combustível v1.1"} # Updated version here

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

# Adicione estas constantes/configurações na sua API
FUEL_PRICES = {
    "diesel": 6.25  # Preço atual do diesel
}

# Endpoint para preços dos combustíveis
@app.get("/fuel_prices")
async def get_fuel_prices():
    return {
        "diesel": 6.25,  # Preço fixo do diesel para exemplo
        "timestamp": datetime.now().isoformat()
    }

# Adicione esta constante no início do arquivo, junto com as outras configurações
VEHICLE_TYPE_MAPPING = {
    'carro': 0,
    'moto': 1,
    'caminhão': 2
}

# Ajuste o endpoint de previsão em lote
@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    try:
        predictions = []
        for pred_request in request.predictions:
            velocidade = random.uniform(80, 100)
            carga = random.uniform(20000, 30000)
            temperatura = random.uniform(20, 30)
            
            X = np.array([[
                2,  # tipo caminhão
                pred_request.distance,
                velocidade,
                carga,
                temperatura
            ]])
            
            consumo_base = float(model.predict(X)[0])
            variacao = random.uniform(0.95, 1.05)
            consumo_final = consumo_base * variacao
            
            predictions.append({
                "vehicle_type": pred_request.vehicle_type,
                "distance": pred_request.distance,
                "predicted_consumption": round(consumo_final, 2)
            })
        
        return {"predictions": predictions}
    except Exception as e:
        print(f"Erro na previsão: {str(e)}")
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

# Adicione estas constantes no início do arquivo
ROTAS = {
    'curitiba': {'distancia': 428, 'via': 'BR-376'},
    'saopaulo': {'distancia': 674, 'via': 'BR-376/BR-116'},
    'guarapuava': {'distancia': 317, 'via': 'BR-466'},
    'londrina': {'distancia': 115, 'via': 'BR-376'},
    'cascavel': {'distancia': 286, 'via': 'BR-376/BR-277'}
}

# Adicione este novo endpoint
@app.get("/routes/consumption")
async def get_routes_consumption():
    metrics.total_requests += 1
    start_time = time.time()
    
    try:
        routes_consumption = []
        for route, info in ROTAS.items():
            # Adicionar variação na velocidade para cada rota
            velocidade = random.uniform(80, 100)  # Velocidade entre 80-100 km/h
            carga = random.uniform(20000, 30000)  # Peso da carga em kg
            temperatura = random.uniform(20, 30)  # Temperatura ambiente
            
            # Preparar dados para o modelo com todas as 5 features esperadas
            X = np.array([[
                2,  # tipo caminhão (usando caminhão como padrão)
                info['distancia'],
                velocidade,
                carga,
                temperatura
            ]])
            
            # Fazer previsão usando o modelo
            consumo_base = float(model.predict(X)[0])
            
            # Adicionar pequena variação aleatória (±5%)
            variacao = random.uniform(0.95, 1.05)
            consumo_final = consumo_base * variacao
            
            routes_consumption.append({
                "route": route,
                "consumption": round(consumo_final, 2),
                "distance": info['distancia'],
                "via": info['via']
            })
        
        # Atualizar métricas
        metrics.response_times.append(time.time() - start_time)
        
        return routes_consumption
    
    except Exception as e:
        metrics.errors += 1
        print(f"Erro ao calcular consumo das rotas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    console.print("[bold green]🚀 Iniciando API...[/]")
    uvicorn.run(app, host="0.0.0.0", port=8000)
