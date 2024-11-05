"""
Pipeline completo de previsão de consumo de combustível com Rich, Colorama e emojis. 🚗💨⛽

Este script executa todo o pipeline de previsão de consumo de combustível, desde a geração do dataset até a predição, utilizando a biblioteca `rich` para um log detalhado e visualmente atraente.

**Etapas do Pipeline:**

1. **Geração de Dataset:** Gera um dataset sintético usando `generate_dataset.py`.
2. **Normalização de Dados:** Normaliza os dados numéricos usando `normalize_data.py`.
3. **Treinamento do Modelo:** Treina um modelo de regressão linear usando `train_model.py`.
4. **Previsão:** Faz previsões de consumo usando `predict_consumption.py`.

**Funcionalidades:**

* **Log Detalhado:** Usa a biblioteca `rich` para exibir um log detalhado e formatado de cada etapa.
* **Ícones e Emojis:** Emprega ícones e emojis para melhorar a legibilidade e o apelo visual do log.
* **Tratamento de Erros:** Inclui tratamento de erros para lidar com possíveis problemas em cada etapa.
* **Colorama:** Usa o Colorama para adicionar cores ao log.

"""
import subprocess
import time
from rich.console import Console
from rich.progress import track
import colorama
from colorama import Fore, Style

colorama.init()
console = Console()

def run_script(script_path, description):
    try:
        with console.status(f"[bold green]Executando {description}...[/]") as status:
            result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
            console.print(f"[bold green]{description} concluído com sucesso! ✅[/]")
            return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Erro ao executar {description}: {e}[/]")
        console.print(f"[bold red]Saída de erro: {e.stderr}[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]Erro inesperado ao executar {description}: {e}[/]")
        return None

with console.status("[bold blue]Iniciando pipeline...[/]"):
    time.sleep(1)

stages = [
    ("Geração de Dataset", "generate_dataset.py"),
    ("Normalização de Dados", "normalize_data.py"),
    ("Treinamento do Modelo", "train_model.py"),
    ("Previsão", "predict_consumption.py")
]

for description, script_path in track(stages, description="Executando pipeline..."):
    output = run_script(script_path, description)
    if output:
        console.print(output)

console.print("[bold green]Pipeline concluído com sucesso! 🎉[/]")
