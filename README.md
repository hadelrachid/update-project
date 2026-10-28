# Update-Project 📦🔍

A Python utility and GUI tool designed to aggregate entire codebases into structured context files for AI audits, LLM code reviews, and clean distribution archives.

---

[🇧🇷 Ler em Português](#-visão-geral-em-português) | [🇺🇸 English Overview](#-english-overview)

---

## 🇺🇸 English Overview

### The Problem
When working with Large Language Models (ChatGPT, Claude, Gemini, DeepSeek, etc.) on medium-to-large projects, AI models frequently suffer from **context fragmentation**. Because they cannot inspect hundreds of scattered files simultaneously without losing attention, code audits often lead to hallucinations, false assumptions, or missed architectural contracts.

### The Solution
**Update-Project** scans your project, applies clean exclusion rules (ignoring vendor folders, cache, and build artifacts), and generates:
1. **A Structured Context File (`{project_name}.txt` and `project.txt`)**: Contains the complete directory tree followed by the full source code of each file, cleanly demarcated with file path headers.
2. **A Clean Project Archive (`{project_name}.zip`)**: A ready-to-deploy zip archive containing only valid source files.

You can then attach `{project_name}.txt` directly to any AI tool to perform complete, zero-hallucination code audits and architectural reviews.

---

### 🚀 Getting Started

#### Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt` (PySide6 for GUI mode)

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
Select your project folder, pick or exclude files using the tree view, and click **Processar**.

**2. Command Line Interface (CLI Mode):**
Process any project directly from the terminal without opening a window:
```bash
python main.py /path/to/your/project
```

---

### 🤖 How to Audit Codebases with AI using the Output

1. Run **Update-Project** on your codebase.
2. Locate the generated `{project_name}.txt` in your project folder.
3. Attach `{project_name}.txt` to your preferred AI model (Claude, ChatGPT, Gemini, etc.).
4. Use a structured audit prompt such as:
   ```text
   You are a senior software architect. Analyze the attached consolidated codebase context file.
   Verify:
   1. Consistency of interface contracts and dependency injection.
   2. Input validation, sanitization, and potential security vulnerabilities.
   3. Adherence to Clean Architecture and test coverage.
   Provide a strict, professional technical audit report.
   ```

---

<br>

## 🇧🇷 Visão Geral em Português

### O Problema
Ao auditar ou refatorar projetos com modelos de Inteligência Artificial (ChatGPT, Claude, Gemini, DeepSeek), as IAs frequentemente sofrem de **amnésia de contexto** em projetos com dezenas ou centenas de arquivos separados, gerando análises superficiais ou suposições incorretas.

### A Solução
O **Update-Project** escaneia o repositório, aplica filtros de exclusão inteligentes (ignorando pastas de build, cache e dependências externas) e gera:
1. **Arquivo Estruturado de Contexto (`{project_name}.txt` e `project.txt`)**: Reúne a árvore de arquivos e o código-fonte integral de cada componente com separadores bem definidos.
2. **Arquivo ZIP de Distribuição (`{project_name}.zip`)**: Pacote limpo contendo apenas os arquivos de código válidos.

Com isso, você pode anexar o arquivo consolidado em qualquer IA e obter uma auditoria completa com contexto global da arquitetura.

---

### 🚀 Instalação e Execução

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar com interface gráfica (GUI)
python main.py

# Executar via linha de comando (CLI)
python main.py "C:\caminho\do\seu\projeto"
```

---

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE).
