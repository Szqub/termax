from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass

@dataclass
class CommandAnalysis:
    success: bool
    error_type: Optional[str] = None
    suggestion: Optional[str] = None
    details: Dict = None

class CommandAnalyzer:
    def __init__(self):
        self.error_patterns = {
            "permission_denied": r"Permission denied|Access denied",
            "not_found": r"No such file or directory|command not found",
            "syntax_error": r"syntax error|invalid syntax",
            "connection_error": r"Connection refused|Connection timed out",
            "disk_space": r"No space left on device|disk full"
        }
        
    def analyze(self, command: str, stdout: str, stderr: str, return_code: int) -> CommandAnalysis:
        """
        Analizuje wynik wykonania polecenia i zwraca szczegółową analizę
        """
        if return_code == 0 and not stderr:
            return CommandAnalysis(
                success=True,
                details={"stdout": stdout}
            )
            
        error_type = self._detect_error_type(stderr)
        suggestion = self._generate_suggestion(command, error_type, stderr)
        
        return CommandAnalysis(
            success=False,
            error_type=error_type,
            suggestion=suggestion,
            details={
                "stdout": stdout,
                "stderr": stderr,
                "return_code": return_code
            }
        )
        
    def _detect_error_type(self, stderr: str) -> Optional[str]:
        """
        Wykrywa typ błędu na podstawie komunikatu stderr
        """
        for error_type, pattern in self.error_patterns.items():
            if re.search(pattern, stderr, re.IGNORECASE):
                return error_type
        return None
        
    def _generate_suggestion(self, command: str, error_type: Optional[str], stderr: str) -> Optional[str]:
        """
        Generuje sugestię poprawy na podstawie typu błędu
        """
        if not error_type:
            return None
            
        suggestions = {
            "permission_denied": "Spróbuj użyć 'sudo' przed poleceniem",
            "not_found": "Sprawdź czy polecenie jest zainstalowane lub ścieżka jest poprawna",
            "syntax_error": "Sprawdź składnię polecenia",
            "connection_error": "Sprawdź połączenie sieciowe i dostępność hosta",
            "disk_space": "Zwolnij miejsce na dysku"
        }
        
        return suggestions.get(error_type)
        
    def extract_keywords(self, text: str) -> List[str]:
        """
        Wyciąga kluczowe słowa z tekstu
        """
        # Usuń znaki specjalne i podziel na słowa
        words = re.findall(r'\w+', text.lower())
        # Usuń popularne słowa
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return [w for w in words if w not in stop_words]
        
    def analyze_multiple_commands(self, commands: List[Dict]) -> List[CommandAnalysis]:
        """
        Analizuje wyniki wielu poleceń
        """
        return [self.analyze(
            cmd["command"],
            cmd.get("stdout", ""),
            cmd.get("stderr", ""),
            cmd.get("return_code", 1)
        ) for cmd in commands] 