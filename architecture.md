# Arquitetura do Projeto de Previsão de Consumo de Combustível 🚗💨

Este documento descreve a arquitetura do projeto de previsão de consumo de combustível, incluindo os componentes principais, suas interações e o fluxo de dados.

## Componentes Principais

O projeto consiste nos seguintes componentes principais:

* **Dataset:** Um dataset contendo dados de consumo de combustível, incluindo distância percorrida, velocidade média, tipo de veículo e consumo.  Este dataset é gerado sinteticamente pelo script `generate_dataset.py` e normalizado pelo script `normalize_data.py`.  💾
* **Modelo de Machine Learning:** Um modelo de regressão linear treinado para prever o consumo de combustível com base nos dados do dataset.  O modelo é treinado pelo script `train_model.py` e salvo no arquivo `model.joblib`. 🧠
* **API REST (FastAPI):** Uma API RESTful que expõe o modelo de machine learning para previsões.  A API é implementada usando o framework FastAPI e permite previsões individuais e em lote.  A API também inclui endpoints para obter informações sobre os preços dos combustíveis e o consumo previsto para diferentes rotas. 🌐
* **Scripts de Previsão:** Scripts Python (`predict_consumption.py` e `predict_fuel_consumption_v2.py`) que demonstram como usar o modelo treinado para fazer previsões. 🔮
* **Dashboard:** Um painel de monitoramento que exibe as métricas da API, como o número total de requisições, erros, tempo médio de resposta e uptime. 📊


## Fluxo de Dados

1. **Geração e Normalização de Dados:** O script `generate_dataset.py` gera um dataset sintético de consumo de combustível.  Este dataset é então normalizado pelo script `normalize_data.py` usando o `MinMaxScaler` do scikit-learn. ➡️
2. **Treinamento do Modelo:** O script `train_model.py` utiliza o dataset normalizado para treinar um modelo de regressão linear.  O modelo treinado é salvo no arquivo `model.joblib`. ➡️
3. **Previsões da API:** A API FastAPI (`api_fuel_consumption.py`) carrega o modelo treinado e o utiliza para fazer previsões de consumo de combustível com base nas requisições recebidas. ➡️
4. **Monitoramento:** O dashboard monitora as métricas da API e exibe informações em tempo real. ➡️


## Diagrama

```
     +-----------------+     +-----------------+     +-----------------+
     | generate_dataset | --> | normalize_data  | --> | train_model     |
     +-----------------+     +-----------------+     +-----------------+
                                         ^
                                         |
                                         |  (Modelo Treinado)
     +-----------------+     +-----------------+     |
     |   API (FastAPI)  | <-- | model.joblib    |     |
     +-----------------+     +-----------------+     |
                                         |
                                         v
                                     +-----------------+
                                     | predict_consumption |
                                     +-----------------+
                                         |
                                         v
                                     +-----------------+
                                     |       Dashboard     |
                                     +-----------------+

```

## Melhorias Futuras 💡

* Integrar com um banco de dados para persistir os dados e as previsões.
* Implementar testes unitários e de integração.
* Explorar modelos de machine learning mais avançados.
* Criar uma interface de usuário mais sofisticada para o dashboard.


## Tecnologias

* **Python:** Linguagem de programação principal. 🐍
* **Pandas:** Manipulação e análise de dados. 🐼
* **Scikit-learn:** Biblioteca para aprendizado de máquina. 🤖
* **Joblib:** Salvamento e carregamento de modelos. 💾
* **FastAPI:** Framework para APIs RESTful. 🌐
* **Rich:** Biblioteca para interface de usuário em terminal (utilizada no dashboard). ✨
