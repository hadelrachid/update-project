DARK_STYLE = """
QMainWindow, QMessageBox, QDialog {
    background-color: #1e1e2e;
}
QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #b4befe;
}
QPushButton:disabled {
    background-color: #45475a;
    color: #a6adc8;
}
QTreeView {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 5px;
    font-size: 13px;
}
QTreeView::item {
    padding: 4px;
}
QTreeView::item:hover {
    background-color: #313244;
}
QTreeView::item:selected {
    background-color: #89b4fa;
    color: #11111b;
}
QProgressBar {
    border: 1px solid #313244;
    border-radius: 5px;
    background-color: #181825;
    text-align: center;
    color: #cdd6f4;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #a6e3a1;
    border-radius: 4px;
}
QLabel {
    font-size: 13px;
    color: #cdd6f4;
}
QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 5px;
    background-color: #1e1e2e;
}
QTabBar::tab {
    background: #181825;
    color: #a6adc8;
    padding: 8px 16px;
    border: 1px solid #313244;
    border-bottom-color: #313244;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background: #1e1e2e;
    color: #89b4fa;
    border-bottom-color: #1e1e2e;
}
QLineEdit, QComboBox, QCheckBox {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 4px;
    padding: 5px;
}
QCheckBox {
    background-color: transparent;
    border: none;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #313244;
    border-radius: 4px;
    background-color: #1e1e2e;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
}
QComboBox::drop-down {
    border: none;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollArea > QWidget > QWidget {
    background-color: transparent;
}
"""
