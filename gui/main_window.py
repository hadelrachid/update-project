import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTreeView, QFileDialog, QMessageBox, QProgressBar,
    QApplication, QStyle, QTabWidget, QLineEdit, QComboBox, QScrollArea
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from core.models import FileNode
from gui.workers import ScanWorker, ProcessWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Project - Packer & Documenter")
        self.resize(800, 600)

        self.root_path = ""
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Nome do Arquivo/Pasta"])
        self.tree_model.itemChanged.connect(self._on_item_changed)
        
        self.ignore_rows = []

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab 1: Compactador
        self.tab_packer = QWidget()
        self._setup_tab_packer()
        self.tabs.addTab(self.tab_packer, "Compactador")

        # Tab 2: Configurações / Exceções
        self.tab_config = QWidget()
        self._setup_tab_config()
        self.tabs.addTab(self.tab_config, "Exceções de Compactação")

    def _setup_tab_packer(self):
        layout = QVBoxLayout(self.tab_packer)

        # Top Bar
        top_layout = QHBoxLayout()
        self.btn_open = QPushButton("Abrir Pasta do Projeto...")
        self.btn_open.clicked.connect(self.open_project)
        self.lbl_path = QLabel("Nenhuma pasta selecionada.")
        top_layout.addWidget(self.btn_open)
        top_layout.addWidget(self.lbl_path, 1)
        layout.addLayout(top_layout)

        # Tree View
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setColumnWidth(0, 400)
        layout.addWidget(self.tree_view)

        # Status & Counts
        status_layout = QHBoxLayout()
        self.lbl_counts = QLabel("Pastas: 0 | Arquivos: 0")
        self.lbl_status = QLabel("Aguardando ação...")
        status_layout.addWidget(self.lbl_counts)
        status_layout.addStretch()
        status_layout.addWidget(self.lbl_status)
        layout.addLayout(status_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        layout.addWidget(self.progress_bar)

        # Bottom Bar
        self.btn_process = QPushButton("Compactar e Gerar Relatório")
        self.btn_process.clicked.connect(self.process_project)
        self.btn_process.setEnabled(False)
        layout.addWidget(self.btn_process)

    def _setup_tab_config(self):
        layout = QVBoxLayout(self.tab_config)
        from gui.ignore_rules_widget import IgnoreRulesWidget
        self.ignore_rules_widget = IgnoreRulesWidget()
        self.ignore_rules_widget.rules_saved.connect(self._on_rules_saved)
        layout.addWidget(self.ignore_rules_widget)

    def get_ignore_patterns(self):
        return self.ignore_rules_widget.get_ignore_patterns()

    def _on_rules_saved(self):
        if self.root_path:
            self._start_scan()

    def open_project(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecione a Pasta do Projeto")
        if directory:
            self.root_path = os.path.normpath(directory)
            self.lbl_path.setText(self.root_path)
            self.ignore_rules_widget.set_directory(self.root_path)
            self._start_scan()

    def _start_scan(self):
        self.btn_open.setEnabled(False)
        self.btn_process.setEnabled(False)
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Nome do Arquivo/Pasta"])
        self.tree_model.setSortRole(Qt.UserRole + 1)
        self.progress_bar.setRange(0, 0) # Indeterminate
        
        self.path_to_item = {}
        
        ignore_patterns = self.get_ignore_patterns()
        
        from config.settings import ALLOWED_EXTENSIONS, is_test_file
        from core.filters import FileFilter
        from core.scanner import Scanner

        file_filter = FileFilter(ignore_patterns, [], [], ALLOWED_EXTENSIONS)
        scanner = Scanner(self.root_path, file_filter, is_test_file)

        self.scan_worker = ScanWorker(scanner)
        self.scan_worker.progress.connect(self.lbl_status.setText)
        self.scan_worker.item_found.connect(self._on_item_found)
        self.scan_worker.finished.connect(self._on_scan_finished)
        self.scan_worker.start()

    def _on_item_found(self, parent_path: str, full_path: str, is_dir: bool, name: str):
        item = QStandardItem(name)
        item.setCheckable(True)
        item.setCheckState(Qt.Checked)
        item.setEditable(False)
        
        # Sort key para pastas virem primeiro
        sort_key = f"0_{name.lower()}" if is_dir else f"1_{name.lower()}"
        item.setData(sort_key, Qt.UserRole + 1)
        item.setData(full_path, Qt.UserRole)
        
        style = QApplication.style()
        if is_dir:
            item.setIcon(style.standardIcon(QStyle.SP_DirIcon))
        else:
            item.setIcon(style.standardIcon(QStyle.SP_FileIcon))
            
        if not parent_path: # Root node
            self.tree_model.invisibleRootItem().appendRow(item)
            self.path_to_item[full_path] = item
            self.tree_view.expandToDepth(0)
        else:
            parent_item = self.path_to_item.get(parent_path)
            if parent_item:
                parent_item.appendRow(item)
                self.path_to_item[full_path] = item

    def _on_scan_finished(self, root_node: FileNode):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        
        # Recupera as contagens do scanner que injetamos
        total_files = self.scan_worker.scanner.total_files
        total_dirs = self.scan_worker.scanner.total_dirs
        
        self.lbl_counts.setText(f"Pastas: {total_dirs} | Arquivos: {total_files}")
        self.lbl_status.setText("Varredura concluída. Selecione os arquivos e clique em Compactar.")
        
        # Ordena a árvore inteira automaticamente
        self.tree_model.sort(0, Qt.AscendingOrder)

        self.btn_open.setEnabled(True)
        self.btn_process.setEnabled(True)

    def _on_item_changed(self, item: QStandardItem):
        """Propaga o check/uncheck para os filhos e atualiza o pai se necessário."""
        self.tree_model.itemChanged.disconnect(self._on_item_changed)
        
        state = item.checkState()
        
        # Propagar para baixo
        def set_children_state(parent: QStandardItem, s: Qt.CheckState):
            for row in range(parent.rowCount()):
                child = parent.child(row)
                child.setCheckState(s)
                set_children_state(child, s)
        
        set_children_state(item, state)
        
        # Propagar para cima (Opcional: se todos os filhos desmarcados, desmarca o pai)
        # Para manter a simplicidade e performance, vamos apenas propagar para baixo.
        
        self.tree_model.itemChanged.connect(self._on_item_changed)

    def process_project(self):
        # Coletar caminhos selecionados
        selected_paths = []
        
        def collect_checked(item: QStandardItem):
            if item.checkState() == Qt.Checked:
                selected_paths.append(item.data(Qt.UserRole))
            # Mesmo se o pai estiver desmarcado, ele pode ter sido PartiallyChecked, mas 
            # usando 2-states é mais simples. Vamos iterar sobre os filhos.
            for row in range(item.rowCount()):
                collect_checked(item.child(row))
                
        root_item = self.tree_model.item(0, 0)
        if root_item:
            collect_checked(root_item)

        if not selected_paths:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo ou pasta selecionado!")
            return

        self.btn_open.setEnabled(False)
        self.btn_process.setEnabled(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        ignore_patterns = self.get_ignore_patterns()

        from config.settings import ALLOWED_EXTENSIONS
        from core.filters import FileFilter
        from core.report import ReportGenerator
        from core.compressor import Compressor
        from core.services import ExportProjectService

        file_filter = FileFilter(ignore_patterns, [], [], ALLOWED_EXTENSIONS)
        report_generator = ReportGenerator()
        compressor = Compressor()
        export_service = ExportProjectService(report_generator, compressor)

        self.process_worker = ProcessWorker(export_service, self.root_path, selected_paths, file_filter)
        self.process_worker.progress_text.connect(self.lbl_status.setText)
        self.process_worker.progress_value.connect(self.progress_bar.setValue)
        self.process_worker.finished.connect(self._on_process_finished)
        self.process_worker.start()

    def _on_process_finished(self, success: bool, message: str):
        self.progress_bar.setValue(100)
        self.btn_open.setEnabled(True)
        self.btn_process.setEnabled(True)
        self.lbl_status.setText("Pronto." if success else "Erro durante o processo.")
        
        if success:
            QMessageBox.information(self, "Sucesso", message)
        else:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro:\n{message}")




