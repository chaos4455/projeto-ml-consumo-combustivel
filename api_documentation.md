# 🚗💨⛽ API de Previsão de Consumo de Combustível

Esta API permite prever o consumo de combustível com base na distância percorrida, velocidade média, tipo de veículo, carga e temperatura.

## Endpoints

### `/`

**Método:** `GET`

**Descrição:** Retorna uma mensagem de boas-vindas.

**Resposta:**

```json
{
  "message": "API de Previsão de Consumo de Combustível v1.1"
}
```

### `/predict/single`

**Método:** `POST`

**Descrição:** Prediz o consumo de combustível para uma única entrada.

**Requisição:**

```json
{
  "distance": 100.0,
  "speed": 60.0,
  "vehicle_type": "carro",
  "load": 500.0,
  "temperature": 25.0
}
```

**Resposta:**

```json
{
  "vehicle_type": "carro",
  "distance": 100.0,
  "speed": 60.0,
  "load": 500.0,
  "temperature": 25.0,
  "predicted_consumption": 8.33,
  "units": "litros"
}
```

**Erros:**

* `400 Bad Request`: Dados de entrada inválidos (tipos de dados incorretos, valores fora do intervalo).
* `500 Internal Server Error`: Erro interno do servidor (erro ao carregar o modelo, erro de previsão).


### `/predict/batch`

**Método:** `POST`

**Descrição:** Prediz o consumo de combustível para um lote de entradas.

**Requisição:**

```json
{
  "predictions": [
    {
      "distance": 100.0,
      "speed": 60.0,
      "vehicle_type": "carro",
      "load": 500.0,
      "temperature": 25.0
    },
    {
      "distance": 200.0,
      "speed": 80.0,
      "vehicle_type": "moto",
      "load": 100.0,
      "temperature": 30.0
    }
  ]
}
```

**Resposta:**

```json
{
  "predictions": [
    {
      "vehicle_type": "carro",
      "distance": 100.0,
      "speed": 60.0,
      "load": 500.0,
      "temperature": 25.0,
      "predicted_consumption": 8.33
    },
    {
      "vehicle_type": "moto",
      "distance": 200.0,
      "speed": 80.0,
      "load": 100.0,
      "temperature": 30.0,
      "predicted_consumption": 8.00
    }
  ]
}
```

**Erros:**

* `400 Bad Request`: Dados de entrada inválidos em qualquer uma das previsões do lote.
* `500 Internal Server Error`: Erro interno do servidor.


### `/metrics`

**Método:** `GET`

**Descrição:** Retorna as métricas da API.

**Resposta:**

```json
{
  "total_requests": 10,
  "errors": 0,
  "avg_response_time": 0.05,
  "uptime": "0:05:30"
}
```

### `/fuel_prices`

**Método:** `GET`

**Descrição:** Retorna os preços atuais dos combustíveis.

**Resposta:**

```json
{
  "diesel": 6.25,
  "gasolina": 5.50,
  "etanol": 4.00,
  "timestamp": "2024-11-05T16:48:00.000Z"
}
```

### `/routes/consumption`

**Método:** `GET`

**Descrição:** Retorna o consumo previsto para rotas específicas.

**Resposta:**

```json
[
  {
    "route": "curitiba",
    "consumption": 12.5,
    "distance": 428,
    "via": "BR-376"
  },
  {
    "route": "saopaulo",
    "consumption": 20.2,
    "distance": 674,
    "via": "BR-376/BR-116"
  },
  // ... outras rotas
]
```


## Documentação dos Scripts Python

### `api_fuel_consumption.py`

Implementa a API FastAPI para previsão de consumo de combustível.  Inclui endpoints para previsões individuais e em lote, tratamento de erros, um painel de monitoramento e endpoints para preços de combustível e consumo em rotas.  Utiliza um modelo de regressão treinado (salvo em `model.joblib`) para fazer as previsões.  O modelo é carregado ao iniciar a API.

**Tratamento de Erros:** A API utiliza o tratamento de exceções do Python para lidar com erros.  Erros de entrada inválida resultam em respostas 400 Bad Request, enquanto erros internos resultam em respostas 500 Internal Server Error.  Mensagens de erro detalhadas são retornadas para ajudar na depuração.

**Modelo Matemático:** A API utiliza um modelo de regressão treinado para fazer as previsões.  O modelo pode ser uma regressão linear ou um modelo mais complexo, como uma RandomForestRegressor ou uma rede neural.  A escolha do modelo depende da complexidade do problema e da precisão desejada.  A equação geral para um modelo de regressão linear é:

**y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ**

Onde:

* y: Consumo de combustível previsto
* β₀: Intercepto
* β₁, β₂, ..., βₙ: Coeficientes de regressão
* x₁, x₂, ..., xₙ: Variáveis preditivas (distância, velocidade, tipo de veículo, carga, temperatura)

Os coeficientes de regressão são aprendidos durante o treinamento do modelo.

### `predict_fuel_consumption.py`

Script de linha de comando simples para previsão de consumo de combustível.  Solicita ao usuário a distância e o tipo de veículo e exibe a previsão.

### `predict_fuel_consumption_v2.py`

Script de linha de comando aprimorado com interface rica usando a biblioteca `rich`.  Inclui animações de carregamento e um relatório formatado.

### `train_model.py`

Treina um modelo de regressão RandomForestRegressor usando o dataset normalizado.  Avalia o modelo e salva o modelo treinado.

### `normalize_data.py`

Normaliza os dados do dataset usando MinMaxScaler.


## Tecnologias Utilizadas

* **FastAPI:** Framework para APIs.
* **Pydantic:** Validação de dados.
* **Scikit-learn:** Biblioteca para aprendizado de máquina.
* **Joblib:** Salvamento e carregamento de modelos.
* **Rich:** Biblioteca para interface de usuário em terminal.
* **Pandas:** Manipulação e análise de dados.
* **NumPy:** Computação numérica.


## Como usar a API

1. **Executar a API:** `uvicorn api_fuel_consumption:app --reload`
2. **Testar os endpoints:** Use um cliente HTTP como Postman ou curl para enviar requisições.


🎉  Espero que esta API seja útil!  🎉

## Histórico de Versões

### v1.1 (05/11/2024 16:48 - Elias Andrade)

* 📝 Melhorias na documentação, incluindo detalhes de implementação e tratamento de erros.
* 🐛 Correções de bugs.
* ✨ Novas funcionalidades: endpoints para preços de combustível e consumo em rotas.
* ✨ Melhorias no endpoint de previsão em lote: agora considera velocidade, carga e temperatura.
* ✨ Adicionada a descrição do modelo matemático utilizado.
