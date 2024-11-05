# Arquitetura do Modelo de Previsão de Consumo de Combustível 🚀

Este documento descreve a arquitetura do modelo de Machine Learning treinado para prever o consumo de combustível, incluindo os dados utilizados, o tipo de saída e como os inputs podem ser usados.

## Dados de Treinamento 📊

O modelo foi treinado utilizando um dataset sintético gerado pelo script `generate_dataset.py`. Este dataset contém as seguintes features:

* **distance:** Distância percorrida (km) 📏 - Numérica.
* **speed:** Velocidade média (km/h) 💨 - Numérica.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Categórica.

O dataset original (`dataset.csv`) foi normalizado usando `MinMaxScaler` do scikit-learn, resultando no arquivo `normalized_dataset.csv`.  A normalização foi aplicada às colunas 'distance', 'speed' e 'consumption'.  A normalização utiliza a seguinte fórmula:

**x' = (x - min(x)) / (max(x) - min(x))**

Onde:

* **x:** Valor original da feature
* **x':** Valor normalizado da feature
* **min(x):** Valor mínimo da feature no dataset
* **max(x):** Valor máximo da feature no dataset


## Arquitetura do Modelo 🧠

O modelo utilizado é uma Regressão Linear ([`LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) do scikit-learn), treinado pelo script `train_model.py`.  A variável alvo é o consumo de combustível (`consumption`).  A variável categórica `vehicle_type` foi convertida para representação numérica usando One-Hot Encoding.

A regressão linear assume uma relação linear entre as variáveis independentes (distance, speed, vehicle_type) e a variável dependente (consumption).  A equação da regressão linear é:

**y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ**

Onde:

* **y:** Variável dependente (consumo de combustível)
* **β₀:** Intercepto
* **β₁, β₂, ..., βₙ:** Coeficientes de regressão
* **x₁, x₂, ..., xₙ:** Variáveis independentes (distance, speed, vehicle_type - one-hot encoded)

O modelo aprende os coeficientes de regressão (β) que melhor se ajustam aos dados de treinamento, minimizando a soma dos quadrados dos erros (SSE).  A fórmula do SSE é:

**SSE = Σ(yᵢ - ŷᵢ)²**

Onde:

* **yᵢ:** Valor real da variável dependente
* **ŷᵢ:** Valor previsto da variável dependente

O modelo treinado é salvo em `model.joblib`.

![Linear Regression Diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Linear_regression.svg/1280px-Linear_regression.svg.png)


## Melhorias com Redes Neurais

Para melhorar a precisão do modelo, podemos explorar o uso de redes neurais.  Uma rede neural pode capturar relações não-lineares entre as variáveis, o que pode ser benéfico se a relação entre as variáveis de entrada e o consumo de combustível não for estritamente linear.  Uma arquitetura simples de rede neural para este problema poderia ser uma rede feedforward com uma ou mais camadas ocultas.  A função de ativação da camada de saída seria linear para prever o consumo de combustível.  A função de perda seria o Mean Squared Error (MSE).  O otimizador poderia ser o Adam ou o Gradient Descent.

**Exemplo de arquitetura:**

* Camada de entrada: 4 neurônios (distance, speed, vehicle_type_carro, vehicle_type_moto)
* Camada oculta 1: 8 neurônios (função de ativação: ReLU)
* Camada oculta 2: 4 neurônios (função de ativação: ReLU)
* Camada de saída: 1 neurônio (função de ativação: linear)


## Saída do Modelo ⛽

O modelo retorna uma previsão numérica representando o consumo de combustível em litros.  O script `predict_consumption.py` utiliza o modelo treinado para gerar previsões com base em dados de entrada.

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

## Melhorias Futuras e Próximos Passos 💡

* Implementar e avaliar uma rede neural para comparar o desempenho com a regressão linear.
* Incluir mais features no dataset, como condições climáticas, tipo de combustível e terreno.
* Desenvolver uma interface gráfica para facilitar o uso do modelo.


## Resumo 📝

Basicamente, o modelo aprendeu a relação entre a distância percorrida, a velocidade média e o tipo de veículo para prever o consumo de combustível.

## Histórico de Versões

### v0005 (05/11/2024 17:48 - Cline)

* 📝 Melhorias na documentação, incluindo fórmulas matemáticas e diagramas.
* ✨ Adicionadas seções de melhorias futuras e próximos passos, incluindo a possibilidade de usar redes neurais.
