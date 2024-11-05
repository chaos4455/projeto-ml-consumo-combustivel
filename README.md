# Predição de Consumo de Combustível - Por Elias Andrade - v0.003

Este projeto utiliza aprendizado de máquina para prever o consumo de combustível.  Sou Elias Andrade, e desenvolvi este projeto como uma demonstração de minhas habilidades em IA e Machine Learning.

## Contato

🏠 Localização: Maringá, Paraná, Brasil
📞 Telefone: +55 (44) 98765-4321
📧 E-mail: elias.andrade@email.com

## Descrição do Projeto

Este projeto visa prever o consumo de combustível de veículos com base em diferentes parâmetros, utilizando técnicas de aprendizado de máquina.  O modelo foi treinado com um dataset sintético, gerado e normalizado para otimizar o desempenho do algoritmo.  A versão atual (v0.003) inclui melhorias na documentação, na clareza do código e instruções para configurar ações do GitHub, Docker, Terraform e Kubernetes.

## Arquitetura do Modelo

O modelo utilizado é uma Regressão Linear, escolhida por sua simplicidade e eficácia para este problema específico.  A escolha da Regressão Linear se justifica pela natureza linear esperada entre as variáveis de entrada (distância, velocidade e tipo de veículo) e a variável de saída (consumo de combustível).  Entretanto, modelos mais complexos poderiam ser explorados para melhorar a precisão das previsões.  O modelo é treinado utilizando 80% dos dados, e os 20% restantes são usados para avaliação do modelo.

### Dados de Treinamento

O modelo foi treinado utilizando um dataset sintético gerado pelo script `generate_dataset.py`. Este dataset contém as seguintes features:

* **distance:** Distância percorrida (km) 📏 - Numérica, gerada aleatoriamente entre 10 e 1000 km.
* **speed:** Velocidade média (km/h) 💨 - Numérica, gerada aleatoriamente entre 30 e 120 km/h.
* **vehicle_type:** Tipo de veículo (carro 🚗, moto 🏍️, caminhão 🚚) - Categórica, escolhida aleatoriamente entre as três opções.
* **consumption:** Consumo de combustível (litros) ⛽ - Numérica, gerada aleatoriamente entre 5 e 50 litros (para simplificação).  Este valor é um placeholder e pode ser refinado com um modelo mais complexo ou com dados reais.

O dataset original (`dataset.csv`) foi normalizado usando `MinMaxScaler` do scikit-learn, resultando no arquivo `normalized_dataset.csv`.  A normalização foi aplicada às colunas 'distance', 'speed' e 'consumption'.  A normalização é crucial para garantir que todas as features contribuam igualmente para o treinamento do modelo, evitando que features com valores maiores dominem o processo de aprendizado.  O `MinMaxScaler` transforma os valores numéricos para um intervalo entre 0 e 1.

### Pré-processamento dos Dados

O pré-processamento dos dados incluiu as seguintes etapas:

1. **Geração de Dados:** Um dataset sintético foi gerado usando o script `generate_dataset.py`. Este script gera dados aleatórios simulando diferentes cenários de condução.  O número de amostras pode ser ajustado alterando a variável `num_samples` no script.
2. **Normalização:** Os dados numéricos foram normalizados usando o `MinMaxScaler` para garantir que todas as features estejam na mesma escala.
3. **One-Hot Encoding:** A variável categórica `vehicle_type` foi convertida em representação numérica usando One-Hot Encoding.  Esta técnica transforma variáveis categóricas em múltiplas variáveis binárias, permitindo que o modelo as utilize no processo de treinamento.  O script `train_model.py` utiliza `pd.get_dummies` para realizar este processo.

### Treinamento do Modelo

O modelo foi treinado usando o script `train_model.py`. Este script utiliza o `train_test_split` para dividir o dataset em conjuntos de treinamento e teste (80% treino, 20% teste), permitindo avaliar o desempenho do modelo em dados não vistos durante o treinamento.  O modelo foi avaliado usando o Mean Squared Error (MSE), uma métrica comum para avaliar modelos de regressão.  O MSE mede a média dos quadrados das diferenças entre os valores previstos e os valores reais. Um MSE menor indica um melhor desempenho do modelo. O modelo treinado é salvo no arquivo `model.joblib` usando a biblioteca `joblib`.

### Previsão do Consumo

O script `predict_consumption.py` utiliza o modelo treinado para gerar previsões de consumo de combustível.  Este script demonstra como carregar o modelo treinado e fazer previsões com base em novos dados de entrada.  A saída do script inclui uma tabela formatada mostrando as previsões e a economia em relação à média do consumo normalizado.  O script gera dados aleatórios de entrada (distância, velocidade, tipo de veículo) e utiliza o modelo carregado para prever o consumo.  A biblioteca `rich` é usada para apresentar os resultados em uma tabela formatada.  O script também inclui tratamento de erros para lidar com arquivos não encontrados e outras exceções.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Pandas:** Manipulação e análise de dados.
* **Scikit-learn:** Biblioteca para aprendizado de máquina (Regressão Linear, MinMaxScaler, train_test_split, mean_squared_error).
* **Joblib:** Salvamento e carregamento de modelos.
* **Rich:** Biblioteca para interface de usuário em terminal.
* **NumPy:** Computação numérica.

## Próximos Passos

* **Aprimoramento do Modelo:** Explorar modelos de aprendizado de máquina mais complexos para melhorar a precisão das previsões.  Considerar modelos como RandomForestRegressor ou GradientBoostingRegressor.
* **Dados Reais:** Utilizar um dataset de dados reais para treinar e avaliar o modelo.  Isso permitirá uma avaliação mais precisa do desempenho do modelo em cenários do mundo real.
* **Interface Gráfica:** Desenvolver uma interface gráfica para facilitar o uso do modelo.  Uma interface gráfica tornaria o modelo mais acessível a usuários sem experiência em programação.
* **Integração com Sistemas:** Integrar o modelo com outros sistemas para automatizar o processo de previsão.  Isso poderia envolver a integração com sistemas de gerenciamento de frotas ou sistemas de monitoramento de veículos.
* **Deploy:** Implementar o modelo em um ambiente de produção.  Isso permitiria que o modelo fosse usado em larga escala para prever o consumo de combustível.
* **GitHub Actions:** Criar uma ação para criar backups versionados dos commits.
* **Docker:** Criar um Dockerfile para containerizar a aplicação.
* **Terraform:** Criar arquivos Terraform para provisionar infraestrutura.
* **Kubernetes:** Criar configurações Kubernetes para implantar a aplicação.


## Arquivos

* `generate_dataset.py`: Gera o dataset de treinamento.
* `normalize_data.py`: Normaliza os dados.
* `train_model.py`: Treina o modelo de aprendizado de máquina.
* `predict_consumption.py`: Prediz o consumo de combustível.
* `model.joblib`: Modelo treinado.
* `dataset.csv`: Dataset original.
* `normalized_dataset.csv`: Dataset normalizado.
* `README.md`: Este arquivo.
* `combined_documentation.md`: Documentação combinada.
* `model_architecture.md`: Arquitetura do modelo.


## Como Executar

1. **Instalar dependências:** `pip install pandas scikit-learn joblib rich numpy`
2. **Gerar dataset:** `python generate_dataset.py`
3. **Normalizar dados:** `python normalize_data.py`
4. **Treinar modelo:** `python train_model.py`
5. **Prever consumo:** `python predict_consumption.py`

## Configuração Avançada

### GitHub Actions

Para configurar o GitHub Actions para criar backups versionados dos commits, crie um arquivo `.github/workflows/backup.yml` com o seguinte conteúdo:

```yaml
name: Backup Commits

on:
  push:
    branches:
      - main

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Create backups directory
        run: mkdir -p backups

      - name: Zip the code
        run: zip -r backups/$(date +%Y%m%d_%H%M%S).zip .

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: backup
          path: backups
```

### Docker

Crie um arquivo `Dockerfile` com o seguinte conteúdo:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "predict_consumption.py"]
```

### Terraform e Kubernetes

As configurações para Terraform e Kubernetes são mais complexas e dependem da sua infraestrutura específica.  Você precisará criar arquivos `.tf` e arquivos de configuração Kubernetes (deployments, services, etc.) de acordo com suas necessidades.
