import os
import zipfile
import tempfile
import shutil
from typing import List, Callable
from core.filters import FileFilter

class Compressor:
    def compress(self, root_path: str, selected_paths: set, file_filter: FileFilter, output_zip_path: str, progress_callback: Callable[[int, int, str], None] = None):
        """
        Cria o arquivo ZIP.
        """
        # Passo 1: Filtrar arquivos válidos com base na lista de selecionados
        files_to_zip = []
        for root, dirs, files in os.walk(root_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Feedback de preparação
                if progress_callback:
                    progress_callback(0, 0, f"Preparando ZIP: {file}")
                
                # Guarda de trânsito: Verifica exceções
                if file_filter.should_ignore_file(file):
                    continue
                
                # Só compacta se o arquivo em si estiver na lista de selecionados.
                if file_path in selected_paths:
                    arcname = os.path.relpath(file_path, root_path)
                    files_to_zip.append((file_path, arcname))
        
        total_zip = len(files_to_zip)
        zip_count = 0

        if total_zip == 0:
            if progress_callback:
                progress_callback(0, 0, "Nenhum arquivo selecionado para compactação.")
            return

        import tempfile
        import shutil

        temp_dir = tempfile.gettempdir()
        project_name = os.path.basename(os.path.normpath(root_path))
        temp_zip_base = os.path.join(temp_dir, f"{project_name}_temp.zip")

        if os.path.exists(output_zip_path):
            os.remove(output_zip_path)

        with zipfile.ZipFile(temp_zip_base, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, arcname in files_to_zip:
                # Evitar falhas se o arquivo de destino (zip antigo) tiver sido marcado
                # e removido pelo os.remove acima.
                if os.path.abspath(file_path) == os.path.abspath(output_zip_path):
                    continue
                
                zip_count += 1
                if progress_callback:
                    progress_callback(zip_count, total_zip, arcname)
                zipf.write(file_path, arcname)

        shutil.move(temp_zip_base, output_zip_path)
