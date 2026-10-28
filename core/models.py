import os
from typing import List, Optional

class FileNode:
    """Representa um arquivo ou diretório na árvore escaneada."""
    def __init__(self, name: str, path: str, is_dir: bool):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children: List['FileNode'] = []
        # Para diretórios, indica se ele foi completamente ignorado nas configurações
        self.is_ignored = False 

    def add_child(self, child: 'FileNode'):
        self.children.append(child)

    def sort_children(self):
        """Ordena: Pastas primeiro, depois arquivos alfabeticamente."""
        self.children.sort(key=lambda x: (not x.is_dir, x.name.lower()))
        for child in self.children:
            if child.is_dir:
                child.sort_children()
