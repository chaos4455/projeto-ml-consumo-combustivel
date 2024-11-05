# 🚗💨⛽ API de Previsão de Consumo de Combustível

Esta API permite prever o consumo de combustível com base na distância percorrida e no tipo de veículo.

## Endpoints

### `/`

**Método:** `GET`

**Descrição:** Retorna uma mensagem de boas-vindas.

**Resposta:**

```json
{
  "message": "API de Previsão de Consumo de Combustível v1.0"
}
```

### `/predict/single`

**Método:** `POST`

**Descrição:** Prediz o consumo de combustível para uma única entrada.

**Requisição:**

```json
{
  "distance": 100.0,
  "vehicle_type": "carro"
}
```

**Resposta:**

```json
{
  "vehicle_type": "carro",
  "distance": 100.0,
  "predicted_consumption": 8.33,
  "units": "litros"
}
```

**Erros:**

* `400 Bad Request`: Tipo de veículo inválido.
* `500 Internal Server Error`: Erro interno do servidor.


### `/predict/batch`

**Método:** `POST`

**Descrição:** Prediz o consumo de combustível para um lote de entradas.

**Requisição:**

```json
{
  "predictions": [
    {
      "distance": 100.0,
      "vehicle_type": "carro"
    },
    {
      "distance": 200.0,
      "vehicle_type": "moto"
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
      "predicted_consumption": 8.33,
      "units": "litros"
    },
    {
      "vehicle_type": "moto",
      "distance": 200.0,
      "predicted_consumption": 8.00,
      "units": "litros"
    }
  ]
}
```

**Erros:**

* `400 Bad Request`: Tipo de veículo inválido.
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


## Documentação dos Scripts Python

### `api_fuel_consumption.py`

Implementa a API FastAPI para previsão de consumo de combustível.  Inclui endpoints para previsões individuais e em lote, tratamento de erros e um painel de monitoramento.

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
