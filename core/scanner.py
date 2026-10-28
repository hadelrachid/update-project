import os
from core.models import FileNode
from core.filters import FileFilter

class Scanner:
    def __init__(self, root_path: str, file_filter: FileFilter, is_test_file_fn: callable):
        self.root_path = root_path
        self.total_dirs = 0
        self.total_files = 0
        self.file_filter = file_filter
        self.is_test_file_fn = is_test_file_fn

    def scan(self, progress_callback=None, item_callback=None) -> FileNode:
        root_name = os.path.basename(os.path.normpath(self.root_path))
        root_node = FileNode(root_name, self.root_path, is_dir=True)
        if item_callback:
            # Envia a raiz com parent_path Vazio
            item_callback("", self.root_path, True, root_name)
            
        self._build_tree(root_node, progress_callback, item_callback)
        root_node.sort_children()
        return root_node

    def _build_tree(self, node: FileNode, progress_callback=None, item_callback=None):
        try:
            items = os.listdir(node.path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(node.path, item)
            is_dir = os.path.isdir(full_path)
            
            if is_dir:
                if self.file_filter.should_ignore_dir(item):
                    continue
            else:
                if self.file_filter.should_ignore_file(item, self.is_test_file_fn(item)):
                    continue

            child_node = FileNode(item, full_path, is_dir)
            node.add_child(child_node)

            if is_dir:
                self.total_dirs += 1
                if progress_callback:
                    progress_callback(f"Escaneando pasta: {item}")
                if item_callback:
                    item_callback(node.path, full_path, True, item)
                self._build_tree(child_node, progress_callback, item_callback)
            else:
                self.total_files += 1
                if progress_callback:
                    if self.total_files % 10 == 0:
                        progress_callback(f"Encontrados {self.total_files} arquivos...")
                if item_callback:
                    item_callback(node.path, full_path, False, item)
