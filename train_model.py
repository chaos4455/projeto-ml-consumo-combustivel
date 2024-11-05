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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import sys

try:
    df = pd.read_csv('normalized_dataset.csv')
except FileNotFoundError:
    error_message = "Erro: O arquivo 'normalized_dataset.csv' não foi encontrado. ❌"
    sys.stdout.buffer.write(error_message.encode('utf-8') + b'\n')
    exit()

# Separar features e target
X = df.drop('consumption', axis=1)
y = df['consumption']

# Converter colunas categóricas para numéricas (One-Hot Encoding)
X = pd.get_dummies(X, columns=['vehicle_type'], drop_first=True)

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Avaliar o modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Salvar o modelo treinado
joblib.dump(model, 'model.joblib')
success_message = "Modelo treinado e salvo com sucesso! ✅"
sys.stdout.buffer.write(success_message.encode('utf-8') + b'\n')
