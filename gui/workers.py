import os
from PySide6.QtCore import QThread, Signal
from typing import List

from core.scanner import Scanner
from core.models import FileNode
from core.compressor import Compressor
from core.report import ReportGenerator

class ScanWorker(QThread):
    progress = Signal(str)
    item_found = Signal(str, str, bool, str)
    finished = Signal(FileNode)

    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner

    def run(self):
        try:
            self.progress.emit("Iniciando varredura...")
            
            def prog_cb(msg):
                self.progress.emit(msg)
                
            def item_cb(parent_path, full_path, is_dir, name):
                self.item_found.emit(parent_path, full_path, is_dir, name)
                
            root_node = self.scanner.scan(prog_cb, item_cb)
            self.finished.emit(root_node)
        except Exception as e:
            self.progress.emit(f"Erro na varredura: {str(e)}")
            self.finished.emit(None)


class ProcessWorker(QThread):
    progress_text = Signal(str)
    progress_value = Signal(int)
    finished = Signal(bool, str) # success, message

    def __init__(self, export_service, root_path: str, selected_paths: list, file_filter):
        super().__init__()
        self.export_service = export_service
        self.root_path = root_path
        self.selected_paths = set(selected_paths)
        self.file_filter = file_filter

    def run(self):
        try:
            self.progress_value.emit(0)
            
            def text_cb(msg): self.progress_text.emit(msg)
            def val_cb(val): self.progress_value.emit(val)

            success, msg = self.export_service.execute(
                self.root_path, 
                self.selected_paths, 
                self.file_filter, 
                text_cb, 
                val_cb
            )
            self.finished.emit(success, msg)
        except Exception as e:
            self.finished.emit(False, f"Erro crítico: {str(e)}")
