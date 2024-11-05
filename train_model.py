"""
Treina um modelo de regressão linear para prever o consumo de combustível. 🚗💨⛽

Este script treina um modelo de regressão linear usando o dataset normalizado e avalia seu desempenho usando o Mean Squared Error (MSE). O modelo treinado é então salvo para uso posterior.

⚙️ Etapas do Treinamento: ⚙️

1. **Carregamento de Dados:** Lê o dataset normalizado (`normalized_dataset.csv`).
2. **Preparação de Dados:** Separa as features (X) do target (y) e aplica One-Hot Encoding à variável categórica `vehicle_type`.
3. **Divisão de Dados:** Divide os dados em conjuntos de treino e teste (80% treino, 20% teste).
4. **Treinamento do Modelo:** Treina um modelo de `LinearRegression` usando os dados de treino.
5. **Avaliação do Modelo:** Avalia o modelo usando o MSE nos dados de teste.
6. **Salvamento do Modelo:** Salva o modelo treinado em um arquivo (`model.joblib`).

📊 Métricas de Avaliação: 📊

* **Mean Squared Error (MSE):** Mede a média dos quadrados das diferenças entre os valores previstos e os valores reais. Um MSE menor indica um melhor desempenho do modelo.

📦 Entrada e Saída: 📦

* **Entrada:** `normalized_dataset.csv`
* **Saída:** `model.joblib`

"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import sys

try:
    df = pd.read_csv('dataset.csv')
except FileNotFoundError:
    error_message = "Erro: O arquivo 'dataset.csv' não foi encontrado. ❌"
    sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    exit()

# Separar features e target
X = df[['distance', 'speed', 'vehicle_type']]
y = df['consumption']

# One-hot encoding para vehicle_type
X = pd.get_dummies(X, columns=['vehicle_type'], prefix=['vehicle_type'])

# Split dos dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar features numéricas (apenas distance e speed)
scaler = StandardScaler()
numeric_cols = ['distance', 'speed']
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

# Treinar modelo
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

# Avaliar modelo
y_pred = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, y_pred)}")
print(f"MSE: {mean_squared_error(y_test, y_pred)}")

# Verificar importância das features
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
})
print("\nImportância das Features:")
print(feature_importance.sort_values('importance', ascending=False))

# Fazer algumas predições de teste
test_data = pd.DataFrame({
    'distance': [1000, 1000, 1000],
    'speed': [90, 85, 75],
    'vehicle_type': ['carro', 'moto', 'caminhão']
})

test_data = pd.get_dummies(test_data, columns=['vehicle_type'], prefix=['vehicle_type'])
test_data[numeric_cols] = scaler.transform(test_data[numeric_cols])

predictions = model.predict(test_data)
print("\nPredições de teste (1000km):")
print(f"Carro: {predictions[0]:.2f}L")
print(f"Moto: {predictions[1]:.2f}L")
print(f"Caminhão: {predictions[2]:.2f}L")

# Salvar modelo
joblib.dump(model, 'model.joblib')
success_message = "Modelo treinado e salvo com sucesso! ✅"
sys.stdout.buffer.write(success_message.encode('utf-8') + b'\n')

# Verificar o conteúdo do dataset
print(df.groupby('vehicle_type')['consumption'].describe())
