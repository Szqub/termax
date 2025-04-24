# Termax - AI System Administrator Assistant

Termax to zaawansowany asystent AI do zarządzania systemem operacyjnym z poziomu terminala. Pozwala na wykonywanie skomplikowanych operacji systemowych przy użyciu naturalnego języka.

## 🚀 Funkcje

- 🤖 Generowanie i wykonywanie poleceń shell na podstawie naturalnego języka
- 📊 Analiza wyników poleceń w czasie rzeczywistym
- 🔄 Automatyczne poprawianie błędów i sugestie
- 📝 Tworzenie i wykonywanie skryptów
- 🔍 Zaawansowana analiza hostów i infrastruktury
- 💾 Pamięć kontekstowa i historia poleceń

## 📦 Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/Szqub/termax.git
cd termax

# Instalacja zależności
pip install -e .
```

## 🛠️ Wymagania

- Python 3.8 lub nowszy
- Ollama lub inny lokalny model LLM
- Uprawnienia root/sudo (dla niektórych operacji)

## 🎯 Przykłady użycia

### Interaktywna sesja

```bash
termax repl
```

### Skanowanie hosta

```bash
termax scan example.com
```

### Informacje o systemie

```bash
termax system-info
```

## 🔧 Konfiguracja

Ustaw zmienną środowiskową `TERMAX_MODEL` aby wybrać model LLM:

```bash
export TERMAX_MODEL="ollama/mistral"
```

## 📚 Dokumentacja

Szczegółowa dokumentacja dostępna jest w katalogu `docs/`.

## 🤝 Współpraca

Zapraszamy do współpracy! Prosimy o:

1. Fork repozytorium
2. Utworzenie brancha dla nowej funkcji
3. Commita zmian
4. Utworzenia Pull Request

## 📝 Licencja

MIT License - zobacz plik [LICENSE](LICENSE) dla szczegółów.





