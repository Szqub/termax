from typing import Dict, List, Optional
import json
from datetime import datetime
from pathlib import Path

class Memory:
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.command_history: List[Dict] = []
        self.context: Dict = {}
        self.memory_file = Path(f".termax_memory_{self.session_id}.json")
        
    def add_command(self, command: Dict):
        """
        Dodaje wykonane polecenie do historii
        """
        command["timestamp"] = datetime.now().isoformat()
        self.command_history.append(command)
        self._save_memory()
        
    def get_recent_commands(self, limit: int = 5) -> List[Dict]:
        """
        Zwraca ostatnie wykonane polecenia
        """
        return self.command_history[-limit:]
        
    def update_context(self, key: str, value: any):
        """
        Aktualizuje kontekst o nową wartość
        """
        self.context[key] = value
        self._save_memory()
        
    def get_context(self, key: Optional[str] = None) -> any:
        """
        Zwraca wartość z kontekstu
        """
        if key:
            return self.context.get(key)
        return self.context
        
    def clear_context(self):
        """
        Czyści kontekst
        """
        self.context = {}
        self._save_memory()
        
    def _save_memory(self):
        """
        Zapisuje stan pamięci do pliku
        """
        memory_data = {
            "session_id": self.session_id,
            "command_history": self.command_history,
            "context": self.context
        }
        self.memory_file.write_text(json.dumps(memory_data, indent=2))
        
    def load_memory(self):
        """
        Wczytuje stan pamięci z pliku
        """
        if self.memory_file.exists():
            memory_data = json.loads(self.memory_file.read_text())
            self.command_history = memory_data.get("command_history", [])
            self.context = memory_data.get("context", {})
            
    def get_command_suggestion_context(self) -> Dict:
        """
        Zwraca kontekst do generowania sugestii poleceń
        """
        return {
            "recent_commands": self.get_recent_commands(),
            "context": self.context
        } 