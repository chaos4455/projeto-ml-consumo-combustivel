"""
Normaliza os dados do dataset usando MinMaxScaler. 📊📈

Este script lê um arquivo CSV, normaliza as colunas numéricas usando o `MinMaxScaler` do scikit-learn e salva o resultado em um novo arquivo CSV.

⚙️ Processo de Normalização: ⚙️

O `MinMaxScaler` transforma os valores numéricos para um intervalo entre 0 e 1.  Isso é útil para muitos algoritmos de Machine Learning que funcionam melhor com dados normalizados.

✅ Colunas Normalizadas: ✅

* **distance:** Distância percorrida (km) 📏
* **speed:** Velocidade média (km/h) 💨
* **consumption:** Consumo de combustível (litros) ⛽

⚠️ Tratamento de Erros: ⚠️

O script inclui tratamento de erros para o caso do arquivo 'dataset.csv' não ser encontrado.

📦 Entrada e Saída: 📦

* **Entrada:** `dataset.csv`
* **Saída:** `normalized_dataset.csv`

"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys

try:
    df = pd.read_csv('dataset.csv')
except FileNotFoundError:
    error_message = "Erro: O arquivo 'dataset.csv' não foi encontrado. ❌"
    sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    exit()

# Selecionar colunas numéricas para normalizar
numerical_cols = ['distance', 'speed', 'consumption']
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

df.to_csv('normalized_dataset.csv', index=False)
success_message = "Dados normalizados com sucesso! ✅"
sys.stdout.buffer.write(success_message.encode('utf-8') + b'\n')
