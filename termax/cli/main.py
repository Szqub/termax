import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from typing import Optional
import os
from pathlib import Path

from ..core.agent import TermaxAgent
from ..core.memory import Memory
from ..core.analyzer import CommandAnalyzer
from ..commands.system import SystemCommands
from ..commands.network import NetworkCommands

app = typer.Typer()
console = Console()

def create_agent() -> TermaxAgent:
    """
    Tworzy instancję agenta z odpowiednią konfiguracją
    """
    model_name = os.getenv("TERMAX_MODEL", "ollama/mistral")
    return TermaxAgent(model_name=model_name)

@app.command()
def repl():
    """
    Uruchamia interaktywną sesję z agentem
    """
    agent = create_agent()
    memory = Memory()
    analyzer = CommandAnalyzer()
    system_cmds = SystemCommands()
    network_cmds = NetworkCommands()
    
    console.print(Panel.fit(
        "Termax - AI System Administrator Assistant\n"
        "Wpisz 'exit' aby zakończyć sesję",
        title="Termax",
        border_style="blue"
    ))
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]termax[/]")
            
            if user_input.lower() in ["exit", "quit"]:
                break
                
            # Analiza polecenia i generowanie odpowiedzi
            command = agent.get_command_suggestion(user_input)
            if not command:
                console.print("[red]Nie udało się wygenerować polecenia[/]")
                continue
                
            # Wykonanie polecenia
            stdout, stderr, return_code = agent.execute_command(command)
            
            # Analiza wyniku
            analysis = analyzer.analyze(command, stdout, stderr, return_code)
            
            # Wyświetlenie wyniku
            if analysis.success:
                console.print("[green]Polecenie wykonane pomyślnie:[/]")
                console.print(command)
                if stdout:
                    console.print(stdout)
            else:
                console.print("[red]Wystąpił błąd:[/]")
                console.print(command)
                if stderr:
                    console.print(stderr)
                if analysis.suggestion:
                    console.print(f"[yellow]Sugestia: {analysis.suggestion}[/]")
                    
            # Aktualizacja pamięci
            memory.add_command({
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "return_code": return_code,
                "analysis": analysis.__dict__
            })
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Wystąpił błąd: {str(e)}[/]")

@app.command()
def scan(host: str = typer.Argument(..., help="Host do przeskanowania")):
    """
    Wykonuje skanowanie sieciowe hosta
    """
    network_cmds = NetworkCommands()
    result = network_cmds.scan_host(host)
    
    if "error" in result:
        console.print(f"[red]Błąd: {result['error']}[/]")
        return
        
    console.print(Panel.fit(
        f"Host: {result['host']}\n"
        f"Status: {result['state']}\n"
        "Otwarte porty:\n" +
        "\n".join(f"- {p['port']} ({p['service']})" for p in result['ports'] if p['state'] == 'open'),
        title="Wynik skanowania",
        border_style="green"
    ))

@app.command()
def system_info():
    """
    Wyświetla informacje o systemie
    """
    system_cmds = SystemCommands()
    info = system_cmds.get_system_info()
    memory = system_cmds.get_memory_info()
    disk = system_cmds.get_disk_usage()
    
    console.print(Panel.fit(
        f"System: {info['os']} ({info['platform']})\n"
        f"Procesor: {info['processor']} rdzeni\n"
        f"Python: {info['python_version']}\n\n"
        f"Pamięć: {memory['percent']}% użyta\n"
        f"Dysk: {disk['percent']}% użyty",
        title="Informacje systemowe",
        border_style="blue"
    ))

if __name__ == "__main__":
    app() 