import json
import os
import sys
from PySide6.QtWidgets import (
    QFileSystemModel,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QScrollArea, QLineEdit, QCheckBox, QMessageBox,
    QTreeView, QAbstractItemView, QSplitter, QFileDialog, QSizePolicy
)
from PySide6.QtCore import Qt, QDir, Signal, QSortFilterProxyModel
import fnmatch

from config.settings import DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_FILES

if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(app_dir, "ignore_rules.json")

class CheckableFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checked_paths = set()

    def flags(self, index):
        default_flags = super().flags(index)
        if index.column() == 0:
            return default_flags | Qt.ItemIsUserCheckable
        return default_flags

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            path = self.filePath(index)
            return Qt.Checked if path in self.checked_paths else Qt.Unchecked
        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            path = self.filePath(index)
            # PySide6 sends integer or Qt.CheckState enum
            is_checked = (value == Qt.Checked.value) if hasattr(value, 'value') else (value == 2)
            
            if is_checked:
                self.checked_paths.add(path)
            elif path in self.checked_paths:
                self.checked_paths.remove(path)
            
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return super().setData(index, value, role)

class ExceptionFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ignore_patterns = []

    def set_ignore_patterns(self, patterns):
        self.ignore_patterns = patterns
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        file_name = source_model.fileName(index)
        
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_name.lower(), pattern.lower()):
                return False
        return True

class IgnoreRulesWidget(QWidget):
    rules_saved = Signal()
    def __init__(self):
        super().__init__()
        self.ignore_rows = []
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Vertical)
        
        # --- PARTE SUPERIOR ---
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0,0,0,0)
        
        lbl_tree = QLabel("1. Marque as caixinhas na árvore abaixo para selecionar as pastas ou arquivos:")
        top_layout.addWidget(lbl_tree)
        
        btn_top_layout = QHBoxLayout()
        self.btn_load_dir = QPushButton("📂 Abrir Pasta do Projeto...")
        self.btn_load_dir.setFixedWidth(250)
        self.btn_load_dir.clicked.connect(self.load_directory)
        btn_top_layout.addWidget(self.btn_load_dir)
        btn_top_layout.addStretch()
        top_layout.addLayout(btn_top_layout)
        
        self.fs_model = CheckableFileSystemModel()
        self.fs_model.setRootPath("")
        self.fs_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden)
        
        self.tree_view = QTreeView()
        self.proxy_model = ExceptionFilterProxyModel()
        self.proxy_model.setSourceModel(self.fs_model)
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.setColumnWidth(0, 300)
        top_layout.addWidget(self.tree_view)
        
        btn_add_sel_layout = QHBoxLayout()
        self.btn_add_selected = QPushButton("⬇ Adicionar Marcados à Lista de Exceções")
        self.btn_add_selected.setFixedWidth(350)
        self.btn_add_selected.clicked.connect(self.add_selected_from_tree)
        btn_add_sel_layout.addWidget(self.btn_add_selected)
        btn_add_sel_layout.addStretch()
        top_layout.addLayout(btn_add_sel_layout)
        
        splitter.addWidget(top_widget)
        
        # --- PARTE INFERIOR ---
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0,0,0,0)
        
        lbl_list = QLabel("2. Lista de Exceções Ativas:")
        bottom_layout.addWidget(lbl_list)
        
        btn_layout = QHBoxLayout()
        self.btn_add_manual = QPushButton("+ Nova Exceção Manual")
        self.btn_add_manual.setFixedWidth(200)
        self.btn_add_manual.clicked.connect(lambda: self.add_exception_row("", True))
        
        self.btn_save = QPushButton("💾 Salvar Regras")
        self.btn_save.setFixedWidth(200)
        self.btn_save.clicked.connect(self.save_rules)
        self.btn_save.setStyleSheet("background-color: #2e8b57; color: white; font-weight: bold;")
        
        btn_layout.addWidget(self.btn_add_manual)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()
        bottom_layout.addLayout(btn_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        bottom_layout.addWidget(self.scroll_area)
        
        splitter.addWidget(bottom_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)
        
        self.load_rules()

    def load_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a Pasta do Projeto")
        if folder:
            self.set_directory(folder)

    def set_directory(self, folder):
        source_index = self.fs_model.setRootPath(folder)
        proxy_index = self.proxy_model.mapFromSource(source_index)
        self.tree_view.setRootIndex(proxy_index)

    def add_selected_from_tree(self):
        added_count = 0
        for path in list(self.fs_model.checked_paths):
            name = os.path.basename(path)
            if name:
                self.add_exception_row(name, True)
                added_count += 1
        
        if added_count > 0:
            QMessageBox.information(self, "Sucesso", f"{added_count} item(ns) adicionado(s) às exceções! Não esqueça de Salvar.")
            self.fs_model.checked_paths.clear()
            

            self.tree_view.viewport().update()

    def load_rules(self):
        for rw, txt, chk in self.ignore_rows:
            rw.deleteLater()
        self.ignore_rows.clear()

        rules_to_load = []
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    rules_to_load = data.get("rules", [])
            except Exception:
                rules_to_load = [{"pattern": d, "active": True} for d in (DEFAULT_IGNORE_DIRS + DEFAULT_IGNORE_FILES)]
        else:
            rules_to_load = [{"pattern": d, "active": True} for d in (DEFAULT_IGNORE_DIRS + DEFAULT_IGNORE_FILES)]

        for rule in rules_to_load:
            self.add_exception_row(rule["pattern"], rule["active"])

        if not rules_to_load:
            self.add_exception_row("", True)

    def save_rules(self):
        rules = []
        for rw, txt, chk in self.ignore_rows:
            pattern = txt.text().strip()
            if pattern:
                rules.append({"pattern": pattern, "active": chk.isChecked()})
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({"rules": rules}, f, indent=4)
            QMessageBox.information(self, "Sucesso", "Regras salvas com sucesso!")
            self.rules_saved.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar regras: {e}")

    def add_exception_row(self, initial_text="", is_active=True):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        txt_field = QLineEdit()
        txt_field.setPlaceholderText("Ex: *.zip, docs, .git")
        txt_field.setText(initial_text)
        txt_field.setFixedWidth(300)
        
        chk_active = QCheckBox("Ativo")
        chk_active.setChecked(is_active)
        chk_active.stateChanged.connect(lambda: self._update_proxy_filters())
        txt_field.textChanged.connect(lambda: self._update_proxy_filters())
        
        btn_remove = QPushButton("Excluir")
        btn_remove.setFixedWidth(100)
        
        row_layout.addWidget(txt_field)
        row_layout.addWidget(chk_active)
        row_layout.addWidget(btn_remove)
        row_layout.addStretch()
        
        self.scroll_layout.addWidget(row_widget)
        
        btn_remove.clicked.connect(lambda: self.remove_exception_row(row_widget))
        self.ignore_rows.append((row_widget, txt_field, chk_active))
        self._update_proxy_filters()

    def remove_exception_row(self, row_widget):
        for i, (rw, txt, chk) in enumerate(self.ignore_rows):
            if rw == row_widget:
                self.ignore_rows.pop(i)
                rw.deleteLater()
                self._update_proxy_filters()
                break

    def _update_proxy_filters(self):
        if hasattr(self, 'proxy_model'):
            self.proxy_model.set_ignore_patterns(self.get_ignore_patterns())

    def get_ignore_patterns(self):
        patterns = []
        for rw, txt, chk in self.ignore_rows:
            if not chk.isChecked():
                continue
            t = txt.text().strip()
            if t:
                patterns.append(t)
        return patterns







