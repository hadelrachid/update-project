# Update-Project 📦🔍

[![Tests](https://github.com/hadelrachid/update-project/actions/workflows/tests.yml/badge.svg)](https://github.com/hadelrachid/update-project/actions/workflows/tests.yml)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/hadelrachid/update-project/releases/tag/v1.1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)

A resilient Python utility and desktop GUI tool designed to aggregate entire codebases into structured context files for AI audits, LLM code reviews, and clean distribution archives.

---

[🇧🇷 Ler em Português](#-visão-geral-em-português) | [🇺🇸 English Overview](#-english-overview)

---

## 🇺🇸 English Overview

### The Problem
When working with Large Language Models (ChatGPT, Claude, Gemini, DeepSeek, etc.) on medium-to-large projects, AI models frequently suffer from **context fragmentation**. Because they cannot inspect hundreds of scattered files simultaneously without losing attention, code audits often lead to hallucinations, false assumptions, or missed architectural contracts.

### The Solution
**Update-Project** scans your project, applies clean exclusion rules, and generates:
1. **A Structured Context File (`{project_name}.txt` and `project.txt`)**: Contains an AI Audit Manifesto, directory tree hierarchy, and full source code of each file, cleanly demarcated with file path headers.
2. **A Clean Project Archive (`{project_name}.zip`)**: A ready-to-deploy zip archive containing only valid source files.

---

### ✨ Key Features (v1.1.0)

- **Export Profiles (`audit` vs `dist`):**
  - **`audit` (Default):** Includes source code, test suites, architectural contracts, and technical documentation so AI reviewers have the complete ground truth.
  - **`dist`:** Lean package ignoring tests, internal docs, and audits for clean deployment.
- **Atomic File Operations:** Reports and archives are written to temporary files (`.tmp`) and atomically replaced (`os.replace`), preventing corrupt files if an interruption occurs.
- **AI Audit Manifesto:** Embedded header with metadata (timestamp, profile, total files, tool version) and standardized instructions instructing LLMs to analyze code exclusively based on concrete evidence.
- **100% Parity between CLI and GUI:** Centralized filtering rules ensure identical outputs regardless of whether you run the command line or the PySide6 desktop interface.
- **Resilient Report Synchronization:** Atomic propagation to `project.txt` with explicit diagnostic warnings.

---

### 🚀 Getting Started

#### Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt` (`PySide6>=6.5.0` for GUI mode)

```bash
# 1. Clone repository
git clone https://github.com/hadelrachid/update-project.git
cd update-project

# 2. Install dependencies
pip install -r requirements.txt
```

#### Usage Modes

**1. Graphical Interface (GUI Mode):**
Simply run without arguments to open the desktop application:
```bash
python main.py
```
Select your project folder, pick your profile (**Auditoria** vs **Distribuição**), customize exception rules if needed, and click **Gerar Contexto**.

**2. Command Line Interface (CLI Mode):**
Process any project directly from the terminal:
```bash
# Audit Profile (includes tests and docs for AI analysis)
python main.py /path/to/your/project --profile audit

# Distribution Profile (lean package without tests)
python main.py /path/to/your/project --profile dist
```

Check the version anytime:
```bash
python main.py --version
```

---

### 🧪 Running Tests

To run the automated unit test suite locally:

```bash
python -m unittest discover -s tests -t .
```

---

<br>

## 🇧🇷 Visão Geral em Português

### O Problema
Ao auditar ou refatorar projetos com modelos de Inteligência Artificial (ChatGPT, Claude, Gemini, DeepSeek), as IAs frequentemente sofrem de **amnésia e fragmentação de contexto** em projetos com dezenas de arquivos, gerando análises superficiais, suposições erradas e alucinações.

### A Solução
O **Update-Project** escaneia o repositório, aplica filtros de exclusão inteligentes e gera:
1. **Arquivo Estruturado de Contexto (`{project_name}.txt` e `project.txt`)**: Reúne manifesto de auditoria com diretrizes para LLMs, árvore hierárquica e o código-fonte integral de cada componente.
2. **Arquivo ZIP de Distribuição (`{project_name}.zip`)**: Pacote limpo contendo apenas os arquivos de código válidos.

---

### ✨ Novidades da Versão v1.1.0

- **Perfis de Exportação (`audit` e `dist`):**
  - **`audit` (Padrão):** Mantém a suíte completa de testes, contratos de arquitetura e documentação técnica, fornecendo a base de evidências para auditorias de IA.
  - **`dist`:** Distribuição enxuta para deploy, excluindo testes, wikis e auditorias.
- **Gravação Atômica (Resiliência Operacional):** Os relatórios `.txt` e o arquivo `.zip` são gerados em arquivos temporários e substituídos atomicamente via `os.replace`. Em caso de erro ou interrupção, o arquivo anterior não é corrompido ou perdido.
- **Manifesto de Auditoria para IAs:** Cabeçalho estruturado com metadados (perfil, data, total de arquivos) e instruções orientando o modelo a analisar apenas evidências reais do código.
- **Paridade Total entre CLI e GUI:** Regras centralizadas garantem resultados rigorosamente idênticos na linha de comando e na interface gráfica.

---

### 🚀 Instalação e Execução

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar com interface gráfica (GUI)
python main.py

# Executar via linha de comando (CLI) com perfil de auditoria
python main.py "C:\caminho\do\seu\projeto" --profile audit

# Executar testes automatizados
python -m unittest discover -s tests -t .
```

---

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE).
