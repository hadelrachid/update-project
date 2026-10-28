import sys
import os
import argparse

# Adiciona o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import ALLOWED_EXTENSIONS, DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_FILES, is_test_file
from core.filters import FileFilter
from core.scanner import Scanner
from core.report import ReportGenerator
from core.compressor import Compressor
from core.services import ExportProjectService

def run_cli(target_dir: str):
    root_path = os.path.abspath(target_dir)
    if not os.path.isdir(root_path):
        print(f"Erro: O diretório '{root_path}' não foi encontrado.")
        sys.exit(1)

    project_name = os.path.basename(os.path.normpath(root_path))
    print(f"==> Iniciando processamento do projeto: {project_name}")
    print(f"==> Diretório: {root_path}")

    ignore_files = set(DEFAULT_IGNORE_FILES)
    ignore_files.add(f"{project_name}.txt")
    ignore_files.add(f"{project_name}.zip")
    
    file_filter = FileFilter(
        ignore_patterns=[],
        default_ignore_files=ignore_files,
        default_ignore_dirs=set(DEFAULT_IGNORE_DIRS),
        allowed_extensions=ALLOWED_EXTENSIONS
    )

    print("==> Escaneando arquivos do projeto...")
    scanner = Scanner(root_path, file_filter, is_test_file)
    scanner.scan(progress_callback=lambda msg: print(f"    [SCAN] {msg}"))

    # Seleciona todos os arquivos encontrados recursivamente
    selected_paths = set()
    for root, dirs, files in os.walk(root_path):
        # Filtra pastas ignoradas
        dirs[:] = [d for d in dirs if not file_filter.should_ignore_dir(d)]
        for f in files:
            if not file_filter.should_ignore_file(f, is_test_file(f)):
                selected_paths.add(os.path.join(root, f))

    report_gen = ReportGenerator()
    compressor = Compressor()
    service = ExportProjectService(report_gen, compressor)

    def print_text(msg: str):
        print(f"    {msg}")

    def print_val(val: int):
        pass

    success, msg = service.execute(root_path, selected_paths, file_filter, print_text, print_val)
    print(f"==> {msg}")

def run_gui():
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon
    from gui.main_window import MainWindow
    from gui.theme import DARK_STYLE

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    icon_path = os.path.join(base_path, 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Update-Project: AI Codebase Context Packer & Project Archiver")
    parser.add_argument("path", nargs="?", default=None, help="Caminho do projeto para processar via linha de comando (modo CLI)")
    parser.add_argument("--cli", action="store_true", help="Força a execução via linha de comando no diretório atual")

    args = parser.parse_args()

    if args.path:
        run_cli(args.path)
    elif args.cli:
        run_cli(os.getcwd())
    else:
        run_gui()

if __name__ == "__main__":
    main()
