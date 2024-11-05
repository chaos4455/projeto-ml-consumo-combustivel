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
import inquirer

# Parâmetros do dataset
num_samples = 70000
features = ['distance', 'speed', 'vehicle_type']

# Definir características base de consumo por tipo de veículo (L/100km)
def get_consumo_base(perfil):
    consumo_padrao = {
        'carro': {'urbano': 12, 'estrada': 9},
        'moto': {'urbano': 6, 'estrada': 4},
        'caminhão': {'urbano': 35, 'estrada': 28}
    }
    
    if perfil == 'economico':
        return {
            'carro': {'urbano': 8, 'estrada': 6},
            'moto': {'urbano': 4, 'estrada': 3},
            'caminhão': {'urbano': 25, 'estrada': 20}
        }
    elif perfil == 'gastao':
        return {
            'carro': {'urbano': 16, 'estrada': 12},
            'moto': {'urbano': 8, 'estrada': 6},
            'caminhão': {'urbano': 45, 'estrada': 35}
        }
    else:  # realista
        return consumo_padrao

# Gerar dados sintéticos
def main():
    perfil = get_user_preference()
    consumo_base = get_consumo_base(perfil)
    
    data = {
        'distance': np.random.randint(10, 1000, num_samples),
        'speed': np.random.randint(30, 120, num_samples),
        'vehicle_type': np.random.choice(['carro', 'moto', 'caminhão'], num_samples)
    }

    # Calcular consumo realista
    consumos = []
    for i in range(num_samples):
        veiculo = data['vehicle_type'][i]
        velocidade = data['speed'][i]
        distancia = data['distance'][i]
        
        # Determinar se é condição urbana ou estrada baseado na velocidade
        is_urbano = velocidade < 80
        
        # Selecionar consumo base apropriado
        consumo_ref = consumo_base[veiculo]['urbano'] if is_urbano else consumo_base[veiculo]['estrada']
        
        # Fatores que afetam o consumo
        fator_velocidade = 1.0 + (velocidade - 60) * 0.008  # Aumentado o impacto da velocidade
        fator_aleatorio = np.random.uniform(0.9, 1.1)  # Variação de ±10% para outros fatores
        
        # Calcular consumo final
        consumo = (distancia / 100) * consumo_ref * fator_velocidade * fator_aleatorio
        consumos.append(round(consumo, 2))

    data['consumption'] = consumos

    df = pd.DataFrame(data)
    df.to_csv('dataset.csv', index=False)

    sys.stdout.buffer.write(b"Dataset gerado com sucesso! \u2705\n")

def get_user_preference():
    questions = [
        inquirer.List('perfil',
                     message='Qual perfil de consumo você deseja para o dataset?',
                     choices=[
                         ('Realista - Valores próximos da realidade', 'realista'),
                         ('Econômico - Veículos mais eficientes', 'economico'),
                         ('Gastão - Veículos com alto consumo', 'gastao')
                     ])
    ]
    return inquirer.prompt(questions)['perfil']

if __name__ == "__main__":
    main()
