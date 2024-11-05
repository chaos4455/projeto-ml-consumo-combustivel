"""
Gera um dataset sintético para prever o consumo de combustível. 🚗💨⛽

Este script cria um DataFrame Pandas com dados aleatórios simulando distância percorrida, velocidade média, tipo de veículo e consumo de combustível.  Os dados são então salvos em um arquivo CSV.

🎉 Características do Dataset: 🎉

* **distance:** Distância percorrida (km) 📏 - Inteiro aleatório entre 10 e 1000.
* **speed:** Velocidade média (km/h) 💨 - Inteiro aleatório entre 30 e 120.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Escolhido aleatoriamente.
* **consumption:** Consumo de combustível (litros) ⛽ - Inteiro aleatório entre 5 e 50 (para simplificação).


⚙️ Parâmetros Ajustáveis: ⚙️

O número de amostras pode ser ajustado alterando a variável `num_samples`.

⚠️ Considerações: ⚠️

* Os dados gerados são sintéticos e podem não refletir com precisão o consumo de combustível na vida real.
* O consumo de combustível é um placeholder e pode ser refinado com um modelo mais complexo.

"""
import pandas as pd
import numpy as np
import sys

# Parâmetros do dataset
num_samples = 1000
features = ['distance', 'speed', 'vehicle_type']

# Gerar dados sintéticos
data = {
    'distance': np.random.randint(10, 1000, num_samples),
    'speed': np.random.randint(30, 120, num_samples),
    'vehicle_type': np.random.choice(['carro', 'moto', 'caminhão'], num_samples),
    'consumption': np.random.randint(5, 50, num_samples) # Placeholder
}

df = pd.DataFrame(data)
df.to_csv('dataset.csv', index=False)

sys.stdout.buffer.write(b"Dataset gerado com sucesso! \u2705\n")
