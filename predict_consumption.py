"""
Prediz o consumo de combustível usando o modelo treinado. 🎉⛽

Este script carrega um modelo de regressão linear treinado, gera dados de entrada aleatórios a cada 3 segundos e faz previsões de consumo de combustível. Os resultados são apresentados em uma tabela usando a biblioteca `rich`.

**Funcionalidades Principais:**

* **Carregamento do Modelo:** Carrega o modelo treinado a partir do arquivo `model.joblib`.
* **Geração de Dados:** Gera dados aleatórios de entrada (distância, velocidade, tipo de veículo).
* **Previsão:** Usa o modelo carregado para prever o consumo de combustível.
* **Interface Rich:** Apresenta os resultados em uma tabela formatada usando a biblioteca `rich`.
* **Tratamento de Erros:** Inclui tratamento de erros para lidar com arquivos não encontrados e outras exceções.
* **Cálculo de Economia:** Calcula a economia em relação à média do consumo normalizado.

**Dados de Entrada:**

* **distance:** Distância percorrida (km) 📏 - Número aleatório entre 10 e 100.
* **speed:** Velocidade média (km/h) 💨 - Número aleatório entre 40 e 120.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Escolhido aleatoriamente.

**Considerações:**

* Os dados gerados são aleatórios e podem não refletir cenários reais.
* A precisão das previsões depende da qualidade do modelo treinado.

"""
import pandas as pd
import joblib
import numpy as np
import time
import random
from rich.console import Console
from rich.table import Table
from rich.progress import track
import colorama
import sys
from colorama import Fore, Style

colorama.init()

try:
    model = joblib.load('model.joblib')
    dataset = pd.read_csv('normalized_dataset.csv')
    avg_consumption = dataset['consumption'].mean()  # Média do consumo normalizado
except FileNotFoundError:
    error_message = f"Erro: Arquivo 'model.joblib' ou 'normalized_dataset.csv' não encontrado. ❌"
    sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    exit()
except Exception as e:
    error_message = f"Erro ao carregar o modelo ou dataset: {e} ❌"
    sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    exit()


iteration = 0
console = Console()
while True:
    try:
        iteration += 1
        # Gerar dados aleatórios
        distance = random.uniform(10, 100)  # Distância entre 10 e 100 km
        speed = random.uniform(40, 120)  # Velocidade entre 40 e 120 km/h
        vehicle_type = random.choice(['carro', 'moto', 'caminhão'])

        # Criar um DataFrame com os dados de entrada, garantindo a presença de todas as colunas
        input_data = pd.DataFrame({
            'distance': [distance],
            'speed': [speed],
            'vehicle_type': [vehicle_type]
        })

        input_data = pd.get_dummies(input_data, columns=['vehicle_type'], drop_first=True)

        # Adicionar colunas faltantes com valor 0 se necessário
        missing_cols = set(model.feature_names_in_) - set(input_data.columns)
        for c in missing_cols:
            input_data[c] = 0

        # Reordenar colunas para corresponder ao modelo
        input_data = input_data[model.feature_names_in_]

        # Prever o consumo
        consumption = model.predict(input_data)[0]
        economia = (consumption - avg_consumption) * 100 / avg_consumption  # Economia em %

        # Interface Rich com 4 grids
        table = Table(title=f"Previsão de Consumo - Iteração {iteration}")
        table.add_column("Métricas", style="cyan", no_wrap=True)
        table.add_column("Valores", style="magenta")

        table.add_row("Tempo", time.strftime('%H:%M:%S'))
        table.add_row("Distância (km)", f"{distance:.2f} 📏")
        table.add_row("Velocidade (km/h)", f"{speed:.2f} 💨")
        table.add_row("Tipo de Veículo", f"{vehicle_type} 🚗🏍️🚚")
        table.add_row("Consumo Previsto (litros)", f"{consumption:.2f} ⛽")

        if economia >= 0:
            economia_str = f"+{economia:.2f}%"  # Verde para economia positiva
        else:
            economia_str = f"{economia:.2f}%"  # Vermelho para economia negativa

        table.add_row("Economia", economia_str)

        console.print(table)

        time.sleep(3)  # Aguardar 3 segundos

    except KeyError as e:
        error_message = f"Tempo: {time.strftime('%H:%M:%S')}, Erro: Coluna '{e}' não encontrada no modelo. ❌"
        sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    except Exception as e:
        error_message = f"Tempo: {time.strftime('%H:%M:%S')}, Erro na predição: {e} ❌"
        sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
