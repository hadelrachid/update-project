import os
from datetime import datetime
from typing import Callable, List
from core.tree_formatter import TreeFormatter
from core.filters import FileFilter

class ReportGenerator:
    def generate(self, root_path: str, selected_paths: set, file_filter: FileFilter, output_file: str, progress_callback: Callable[[int, int, str], None] = None):
        tree_str = TreeFormatter.get_tree_string(root_path, selected_paths, progress_callback)
        
        files_to_read = []
        for p in selected_paths:
            if file_filter.is_allowed_for_report(p):
                # Evita ler o próprio arquivo de saída se já existir
                if os.path.abspath(p) == os.path.abspath(output_file):
                    continue
                files_to_read.append(p)
        
        files_to_read.sort()
        total_files = len(files_to_read)
        project_name = os.path.basename(os.path.normpath(root_path))
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            # Cabeçalho estruturado para LLMs / IAs e auditoria
            f_out.write("/* " + "="*70 + " */\n")
            f_out.write(f"/* PROJETO: {project_name}\n")
            f_out.write(f"/* DATA DE GERAÇÃO: {now_str}\n")
            f_out.write(f"/* TOTAL DE ARQUIVOS CONSOLIDADOS: {total_files}\n")
            f_out.write("/* FERRAMENTA: Update-Project (Codebase Context Packer)\n")
            f_out.write("/* FINALIDADE: Auditoria de código, revisão estática e contexto para IAs (LLMs)\n")
            f_out.write("/* " + "="*70 + " */\n\n")
            
            # Árvore de Diretórios
            f_out.write("/* " + "-"*70 + " */\n")
            f_out.write("/* ESTRUTURA DO PROJETO (ÁRVORE DE ARQUIVOS)\n")
            f_out.write("/* " + "-"*70 + " */\n\n")
            f_out.write(tree_str + "\n\n")
            
            # Código dos arquivos
            f_out.write("/* " + "="*70 + " */\n")
            f_out.write("/* CONTEÚDO DOS ARQUIVOS DO PROJETO\n")
            f_out.write("/* " + "="*70 + " */\n\n")
            
            for i, f_path in enumerate(files_to_read, 1):
                relative_path = os.path.relpath(f_path, root_path).replace("\\", "/")
                if progress_callback:
                    progress_callback(i, total_files, f"Lendo arquivo: {relative_path}")
                
                f_out.write("/* " + "-"*70 + " */\n")
                f_out.write(f"// Arquivo: {project_name}/{relative_path}\n")
                f_out.write("/* " + "-"*70 + " */\n\n")
                
                try:
                    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                        f_out.write(f_in.read() + "\n\n")
                except Exception as e:
                    f_out.write(f"// [Erro ao ler arquivo: {e}]\n\n")
