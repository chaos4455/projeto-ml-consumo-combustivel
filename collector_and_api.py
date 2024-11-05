from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import asyncio
import aiohttp
import datetime
import uvicorn
from typing import List, Dict
import json
from pydantic import BaseModel
import threading

# Configuração das APIs
ORIGINAL_API_URL = "http://localhost:8000"
COLLECTOR_API_PORT = 8001

app = FastAPI(title="API Coletora de Métricas", version="1.0.0")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    # Tabela para consumo médio por tipo de veículo
    c.execute('''CREATE TABLE IF NOT EXISTS consumo_medio
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  tipo_veiculo TEXT,
                  consumo FLOAT)''')
    
    # Tabela para variação de consumo
    c.execute('''CREATE TABLE IF NOT EXISTS variacao_consumo
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  consumo_medio FLOAT)''')
    
    conn.commit()
    conn.close()

# Função para coletar dados da API original
async def collect_data():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Coletar dados de previsão em lote
                async with session.post(f"{ORIGINAL_API_URL}/predict/batch", 
                    json={
                        "predictions": [
                            {"vehicle_type": "carro", "distance": 100},
                            {"vehicle_type": "moto", "distance": 100},
                            {"vehicle_type": "caminhão", "distance": 100}
                        ]
                    }) as response:
                    data = await response.json()
                    
                    # Gravar no banco
                    conn = sqlite3.connect('metricas.db')
                    c = conn.cursor()
                    timestamp = datetime.datetime.now()
                    
                    # Gravar consumo por tipo
                    for pred in data["predictions"]:
                        c.execute('''INSERT INTO consumo_medio 
                                   (timestamp, tipo_veiculo, consumo)
                                   VALUES (?, ?, ?)''',
                                (timestamp, pred["vehicle_type"], 
                                 pred["predicted_consumption"]))
                    
                    # Gravar média geral
                    media = sum(p["predicted_consumption"] for p in data["predictions"]) / len(data["predictions"])
                    c.execute('''INSERT INTO variacao_consumo 
                               (timestamp, consumo_medio)
                               VALUES (?, ?)''',
                            (timestamp, media))
                    
                    conn.commit()
                    conn.close()
                
            except Exception as e:
                print(f"Erro na coleta: {str(e)}")
            
            await asyncio.sleep(5)  # Esperar 5 segundos

# Rotas da API
@app.get("/consumo-medio/{minutos}")
async def get_consumo_medio(minutos: int):
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    limite_tempo = datetime.datetime.now() - datetime.timedelta(minutes=minutos)
    
    c.execute('''SELECT timestamp, tipo_veiculo, consumo 
                 FROM consumo_medio 
                 WHERE timestamp > ? 
                 ORDER BY timestamp''', (limite_tempo,))
    
    dados = c.fetchall()
    conn.close()
    
    return {
        "labels": [row[0] for row in dados],
        "datasets": [
            {
                "label": veiculo,
                "data": [row[2] for row in dados if row[1] == veiculo]
            }
            for veiculo in ["carro", "moto", "caminhão"]
        ]
    }

@app.get("/variacao-consumo/{minutos}")
async def get_variacao_consumo(minutos: int):
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    limite_tempo = datetime.datetime.now() - datetime.timedelta(minutes=minutos)
    
    c.execute('''SELECT timestamp, consumo_medio 
                 FROM variacao_consumo 
                 WHERE timestamp > ? 
                 ORDER BY timestamp''', (limite_tempo,))
    
    dados = c.fetchall()
    conn.close()
    
    return {
        "labels": [row[0] for row in dados],
        "data": [row[1] for row in dados]
    }

@app.get("/consumo-por-hora")
async def get_consumo_por_hora():
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    c.execute('''SELECT strftime('%H', timestamp) as hora, 
                 AVG(consumo) as media_consumo,
                 tipo_veiculo
                 FROM consumo_medio 
                 GROUP BY hora, tipo_veiculo
                 ORDER BY hora''')
    
    dados = c.fetchall()
    conn.close()
    
    return {
        "labels": list(set(row[0] for row in dados)),
        "datasets": [
            {
                "label": veiculo,
                "data": [row[1] for row in dados if row[2] == veiculo]
            }
            for veiculo in ["carro", "moto", "caminhão"]
        ]
    }

@app.get("/eficiencia-combustivel")
async def get_eficiencia_combustivel():
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    c.execute('''SELECT tipo_veiculo,
                 AVG(consumo) as media,
                 MIN(consumo) as minimo,
                 MAX(consumo) as maximo
                 FROM consumo_medio
                 GROUP BY tipo_veiculo''')
    
    dados = c.fetchall()
    conn.close()
    
    return {
        "labels": [row[0] for row in dados],
        "medias": [row[1] for row in dados],
        "minimos": [row[2] for row in dados],
        "maximos": [row[3] for row in dados]
    }

@app.get("/analise-tendencia/{horas}")
async def get_analise_tendencia(horas: int):
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    limite_tempo = datetime.datetime.now() - datetime.timedelta(hours=horas)
    
    c.execute('''SELECT 
                 strftime('%H:%M', timestamp) as tempo,
                 AVG(consumo) as media_consumo
                 FROM consumo_medio 
                 WHERE timestamp > ?
                 GROUP BY tempo
                 ORDER BY timestamp''', (limite_tempo,))
    
    dados = c.fetchall()
    conn.close()
    
    return {
        "labels": [row[0] for row in dados],
        "data": [row[1] for row in dados]
    }

@app.get("/comparativo-semanal")
async def get_comparativo_semanal():
    conn = sqlite3.connect('metricas.db')
    c = conn.cursor()
    
    c.execute('''SELECT 
                 strftime('%w', timestamp) as dia_semana,
                 tipo_veiculo,
                 AVG(consumo) as media_consumo
                 FROM consumo_medio
                 GROUP BY dia_semana, tipo_veiculo
                 ORDER BY dia_semana''')
    
    dados = c.fetchall()
    conn.close()
    
    dias = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    
    return {
        "labels": dias,
        "datasets": [
            {
                "label": veiculo,
                "data": [next((row[2] for row in dados if row[0] == str(i) and row[1] == veiculo), 0)
                        for i in range(7)]
            }
            for veiculo in ["carro", "moto", "caminhão"]
        ]
    }

# Inicialização
@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(collect_data())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=COLLECTOR_API_PORT)
