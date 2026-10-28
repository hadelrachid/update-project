import os
from collections import defaultdict

class TreeFormatter:
    ICON_MAP = {
        '.py': '🐍',
        '.js': '📜', '.jsx': '📜', '.ts': '📜', '.tsx': '📜',
        '.html': '🌐', '.htm': '🌐',
        '.css': '🎨', '.scss': '🎨', '.sass': '🎨',
        '.json': '📋',
        '.md': '📝', '.txt': '📝',
        '.yml': '⚙️', '.yaml': '⚙️',
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.svg': '🖼️', '.gif': '🖼️',
        '.sh': '🖥️', '.bat': '🖥️',
        '.env': '🔐',
        '.xml': '🔖'
    }
    DEFAULT_ICON = '📄'

    @classmethod
    def _get_icon_for_extension(cls, filename: str) -> str:
        """Retorna um emoji correspondente à extensão do arquivo."""
        ext = os.path.splitext(filename)[1].lower()
        return cls.ICON_MAP.get(ext, cls.DEFAULT_ICON)

    @classmethod
    def get_tree_string(cls, root_path: str, selected_paths: set, progress_callback=None) -> str:
        """Gera a representação textual da árvore."""
        tree_lines = []
        project_name = os.path.basename(os.path.normpath(root_path))
        
        # Mapeia caminhos selecionados por diretório pai para busca O(1)
        children_map = defaultdict(list)
        for p in selected_paths:
            rel = os.path.relpath(p, root_path)
            if rel == '.':
                continue
            is_dir = os.path.isdir(p)
            parent_dir = os.path.dirname(rel)
            children_map[parent_dir].append((os.path.basename(p), rel, is_dir))
        
        def build_tree(current_rel_path: str, prefix: str):
            children = children_map.get(current_rel_path, [])
            children.sort(key=lambda x: (not x[2], x[0].lower()))
            
            for i, (name, rel_path, is_dir) in enumerate(children):
                if progress_callback:
                    progress_callback(1, 2, f"Formatando árvore: {name}")
                is_last = (i == len(children) - 1)
                connector = "└── " if is_last else "├── "
                
                if is_dir:
                    tree_lines.append(f"{prefix}{connector}📁 {name}/")
                    extension_prefix = "    " if is_last else "│   "
                    build_tree(rel_path, prefix + extension_prefix)
                else:
                    icon = cls._get_icon_for_extension(name)
                    tree_lines.append(f"{prefix}{connector}{icon} {name}")
                    
        tree_lines.append(f"📦 {project_name}/")
        build_tree("", "")
        return "\n".join(tree_lines)
