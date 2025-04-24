import subprocess
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path

class TermaxAgent:
    def __init__(self, model_name: str = "ollama/mistral"):
        self.model_name = model_name
        self.command_history: List[Dict] = []
        self.context: Dict = {}
        self.session_id = None
        
    def execute_command(self, command: str) -> Tuple[str, str, int]:
        """
        Wykonuje polecenie shell i zwraca stdout, stderr oraz kod wyjścia
        """
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            return stdout, stderr, process.returncode
        except Exception as e:
            return "", str(e), 1

    def analyze_command_result(self, command: str, stdout: str, stderr: str, return_code: int) -> Dict:
        """
        Analizuje wynik wykonania polecenia i zwraca informacje o statusie
        """
        success = return_code == 0
        analysis = {
            "command": command,
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code
        }
        
        self.command_history.append(analysis)
        return analysis

    def get_command_suggestion(self, user_input: str) -> str:
        """
        Generuje sugestię polecenia na podstawie inputu użytkownika
        """
        # TODO: Implementacja z użyciem modelu LLM
        pass

    def create_script(self, commands: List[str], script_name: str) -> str:
        """
        Tworzy skrypt shell z podanych komend
        """
        script_content = "#!/bin/bash\n\n"
        for cmd in commands:
            script_content += f"{cmd}\n"
            
        script_path = Path(script_name)
        script_path.write_text(script_content)
        script_path.chmod(0o755)
        
        return str(script_path)

    def get_context(self) -> Dict:
        """
        Zwraca aktualny kontekst agenta
        """
        return {
            "command_history": self.command_history,
            "context": self.context,
            "session_id": self.session_id
        }

    def update_context(self, new_context: Dict):
        """
        Aktualizuje kontekst agenta
        """
        self.context.update(new_context) 