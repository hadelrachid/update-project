import os
from collections import defaultdict

class TreeFormatter:
    ICON_MAP = {
        '.py': '🐍',
        '.php': '🐘',
        '.js': '📜', '.jsx': '📜', '.ts': '📜', '.tsx': '📜',
        '.html': '🌐', '.htm': '🌐',
        '.css': '🎨', '.scss': '🎨', '.sass': '🎨',
        '.json': '📋',
        '.md': '📝', '.txt': '📝',
        '.yml': '⚙️', '.yaml': '⚙️',
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.svg': '🖼️', '.gif': '🖼️',
        '.sh': '🖥️', '.bat': '🖥️',
        '.env': '🔐',
        '.xml': '🔖', '.sql': '🗄️'
    }
    DEFAULT_ICON = '📄'

    @classmethod
    def _get_icon_for_extension(cls, filename: str) -> str:
        """Retorna um emoji correspondente à extensão do arquivo."""
        ext = os.path.splitext(filename)[1].lower()
        return cls.ICON_MAP.get(ext, cls.DEFAULT_ICON)

    @classmethod
    def get_tree_string(cls, root_path: str, selected_paths: set, progress_callback=None) -> str:
        """Gera a representação textual hierárquica completa da árvore de arquivos e pastas."""
        tree_lines = []
        project_name = os.path.basename(os.path.normpath(root_path))
        
        # Mapeia estrutura hierárquica completa: parent_rel_path -> set de (nome, rel_path, is_dir)
        children_map = defaultdict(dict)
        
        for p in selected_paths:
            rel = os.path.relpath(p, root_path).replace("\\", "/")
            if rel == '.' or rel == '':
                continue
            
            parts = rel.split('/')
            
            # Adiciona os diretórios ancestrais na hierarquia
            current_parent = ""
            for i in range(len(parts) - 1):
                dir_name = parts[i]
                dir_rel = f"{current_parent}/{dir_name}" if current_parent else dir_name
                children_map[current_parent][dir_name] = (dir_name, dir_rel, True)
                current_parent = dir_rel
            
            # Adiciona o arquivo (ou diretório folha)
            leaf_name = parts[-1]
            is_dir = os.path.isdir(p)
            children_map[current_parent][leaf_name] = (leaf_name, rel, is_dir)
        
        def build_tree(current_rel_path: str, prefix: str):
            items_dict = children_map.get(current_rel_path, {})
            # Converte para lista e ordena: primeiro pastas, depois arquivos (ordem alfabética)
            items = list(items_dict.values())
            items.sort(key=lambda x: (not x[2], x[0].lower()))
            
            for i, (name, rel_path, is_dir) in enumerate(items):
                if progress_callback:
                    progress_callback(1, 2, f"Formatando árvore: {name}")
                is_last = (i == len(items) - 1)
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
