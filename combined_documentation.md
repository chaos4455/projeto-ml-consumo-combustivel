# Documentação Combinada do Projeto de Previsão de Consumo de Combustível

Este documento combina a documentação de todos os arquivos `.py` e `.md` do projeto.

## Arquitetura do Modelo

```
# Arquitetura do Modelo de Previsão de Consumo de Combustível 🚀

Este documento descreve a arquitetura do modelo de Machine Learning treinado para prever o consumo de combustível, incluindo os dados utilizados, o tipo de saída e como os inputs podem ser usados.

## Dados de Treinamento 📊

O modelo foi treinado utilizando um dataset sintético gerado pelo script `generate_dataset.py`. Este dataset contém as seguintes features:

* **distance:** Distância percorrida (km) 📏 - Numérica.
* **speed:** Velocidade média (km/h) 💨 - Numérica.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Categórica.

O dataset original (`dataset.csv`) foi normalizado usando `MinMaxScaler` do scikit-learn, resultando no arquivo `normalized_dataset.csv`.  A normalização foi aplicada às colunas 'distance', 'speed' e 'consumption'.

## Arquitetura do Modelo 🧠

O modelo utilizado é uma Regressão Linear (`LinearRegression` do scikit-learn), treinado pelo script `train_model.py`.  A variável alvo é o consumo de combustível (`consumption`).  A variável categórica `vehicle_type` foi convertida para representação numérica usando One-Hot Encoding.

## Saída do Modelo ⛽

O modelo retorna uma previsão numérica representando o consumo de combustível em litros.  O script `predict_consumption.py` utiliza o modelo treinado para gerar previsões com base em dados de entrada aleatórios.

## Inputs do Modelo e seu Uso ⚙️

Os inputs necessários para o modelo são:

* **distance:** Distância percorrida (km) 📏 - Valor numérico normalizado entre 0 e 1.
* **speed:** Velocidade média (km/h) 💨 - Valor numérico normalizado entre 0 e 1.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Representação One-Hot Encoding (carro, moto, caminhão).

Para usar o modelo, você precisa fornecer esses três inputs no mesmo formato usado durante o treinamento.  O script `predict_consumption.py` demonstra como gerar e usar esses inputs.  O modelo carregado de `model.joblib` pode ser usado diretamente com o `predict` method.

**Exemplo de uso:**

```python
import pandas as pd
import joblib

model = joblib.load('model.joblib')

input_data = pd.DataFrame({
    'distance': [0.5],  # Exemplo de distância normalizada
    'speed': [0.6],     # Exemplo de velocidade normalizada
    'vehicle_type_moto': [1], # One-hot encoding para moto
    'vehicle_type_carro': [0],
    'vehicle_type_caminhão': [0]
})

prediction = model.predict(input_data)[0]
print(f"Consumo previsto: {prediction}  لیتر")
```

Lembre-se que os valores de distância e velocidade devem ser normalizados antes de serem usados no modelo.

## Resumo 📝

Basicamente, o modelo aprendeu a relação entre a distância percorrida, a velocidade média e o tipo de veículo para prever o consumo de combustível.
```

## README

```
# Predição de Consumo de Combustível

Este projeto utiliza aprendizado de máquina para prever o consumo de combustível.

## Arquivos

* `generate_dataset.py`: Gera o dataset de treinamento.
* `normalize_data.py`: Normaliza os dados.
* `train_model.py`: Treina o modelo de aprendizado de máquina.
* `predict_consumption.py`: Prediz o consumo de combustível.

## Como executar

1. **Instalar dependências:**  (A ser definido após a especificação das bibliotecas)
2. **Gerar dataset:** `python generate_dataset.py`
3. **Normalizar dados:** `python normalize_data.py`
4. **Treinar modelo:** `python train_model.py`
5. **Prever consumo:** `python predict_consumption.py`

## Detalhes do Modelo

* **Modelo:** (A ser definido)
* **Recursos:** (A ser definido)

## Próximos passos

* Implementar a geração de dados.
* Implementar a normalização dos dados.
* Implementar o treinamento do modelo.
* Implementar a predição do consumo.
```

## generate_dataset.py

```python
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
```

## normalize_data.py

```python
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
```

## train_model.py

```python
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
```

## predict_consumption.py

```python
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

```

Este documento foi gerado automaticamente e pode conter erros.  Por favor, revise cuidadosamente.
