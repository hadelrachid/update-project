import os
from datetime import datetime
from typing import Callable, List
from core.tree_formatter import TreeFormatter
from core.filters import FileFilter
from version import __version__, __app_name__

class ReportGenerator:
    def generate(
        self,
        root_path: str,
        selected_paths: set,
        file_filter: FileFilter,
        output_file: str,
        progress_callback: Callable[[int, int, str], None] = None
    ):
        tree_str = TreeFormatter.get_tree_string(root_path, selected_paths, progress_callback)
        
        files_to_read = []
        for p in selected_paths:
            if file_filter.is_allowed_for_report(p):
                # Evita ler o próprio arquivo de saída se já existir
                if os.path.abspath(p) == os.path.abspath(output_file) or p.endswith('.tmp'):
                    continue
                files_to_read.append(p)
        
        files_to_read.sort()
        total_files = len(files_to_read)
        project_name = os.path.basename(os.path.normpath(root_path))
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        profile_name = getattr(file_filter, 'profile', 'audit').upper()
        
        # Escrita Atômica: grava primeiro em um arquivo temporário (.tmp)
        temp_output = output_file + ".tmp"
        
        read_errors = []
        
        try:
            with open(temp_output, 'w', encoding='utf-8') as f_out:
                # 1. Manifesto Estruturado de Auditoria para LLMs
                f_out.write("/* " + "="*76 + " */\n")
                f_out.write(f"/* PROJETO: {project_name}\n")
                f_out.write(f"/* DATA DE GERAÇÃO: {now_str}\n")
                f_out.write(f"/* PERFIL DE EXPORTAÇÃO: {profile_name}\n")
                f_out.write(f"/* TOTAL DE ARQUIVOS CONSOLIDADOS: {total_files}\n")
                f_out.write(f"/* FERRAMENTA: {__app_name__} v{__version__} (Codebase Context Packer & Auditor)\n")
                f_out.write("/* FINALIDADE: Auditoria de código, revisão estática e contexto integral para IAs\n")
                f_out.write("/* " + "-"*76 + " */\n")
                f_out.write("/* DIRETRIZES DE AUDITORIA PARA MODELOS DE IA (LLMs):\n")
                f_out.write("/* 1. Analise exclusivamente as evidências presentes neste contexto consolidado.\n")
                f_out.write("/* 2. Diferencie fatos comprovados no código de inferências ou suposições.\n")
                f_out.write("/* 3. Se faltar contexto para confirmar uma tese, declare explicitamente a limitação.\n")
                f_out.write("/* 4. Cite sempre os caminhos de arquivos e símbolos ao sustentar cada apontamento.\n")
                f_out.write("/* " + "="*76 + " */\n\n")
                
                # 2. Árvore de Diretórios
                f_out.write("/* " + "-"*76 + " */\n")
                f_out.write("/* ESTRUTURA DO PROJETO (ÁRVORE HIERÁRQUICA DE ARQUIVOS)\n")
                f_out.write("/* " + "-"*76 + " */\n\n")
                f_out.write(tree_str + "\n\n")
                
                # 3. Conteúdo dos arquivos
                f_out.write("/* " + "="*76 + " */\n")
                f_out.write("/* CONTEÚDO DOS ARQUIVOS CONSOLIDADOS DO PROJETO\n")
                f_out.write("/* " + "="*76 + " */\n\n")
                
                for i, f_path in enumerate(files_to_read, 1):
                    relative_path = os.path.relpath(f_path, root_path).replace("\\", "/")
                    if progress_callback:
                        progress_callback(i, total_files, f"Lendo arquivo ({i}/{total_files}): {relative_path}")
                    
                    f_out.write("/* " + "-"*76 + " */\n")
                    f_out.write(f"// Arquivo: {project_name}/{relative_path}\n")
                    f_out.write("/* " + "-"*76 + " */\n\n")
                    
                    try:
                        with open(f_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                            content = f_in.read()
                            f_out.write(content + "\n\n")
                    except Exception as e:
                        read_errors.append((relative_path, str(e)))
                        f_out.write(f"// [Erro de leitura no arquivo: {e}]\n\n")
            
            # Se a gravação foi bem-sucedida, substitui o arquivo final atomicamente
            os.replace(temp_output, output_file)
            
        except Exception:
            if os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                except OSError:
                    pass
            raise

        return {
            "total_files": total_files,
            "read_errors": read_errors,
            "profile": profile_name
        }
