import os
import zipfile
import shutil
from typing import List, Callable
from core.filters import FileFilter

class Compressor:
    def compress(
        self,
        root_path: str,
        selected_paths: set,
        file_filter: FileFilter,
        output_zip_path: str,
        progress_callback: Callable[[int, int, str], None] = None
    ):
        """
        Cria o arquivo ZIP de forma atômica e resiliente.
        """
        # Passo 1: Filtrar arquivos válidos com base na lista de selecionados
        files_to_zip = []
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if not file_filter.should_ignore_dir(d)]
            for file in files:
                file_path = os.path.join(root, file)
                
                # Feedback de preparação
                if progress_callback:
                    progress_callback(0, 0, f"Preparando ZIP: {file}")
                
                # Guarda: Verifica exceções
                if file_filter.should_ignore_file(file):
                    continue
                
                # Só compacta se o arquivo em si estiver na lista de selecionados.
                if file_path in selected_paths:
                    # Ignora arquivos temporários e o próprio arquivo ZIP de destino
                    if file_path.endswith('.tmp') or os.path.abspath(file_path) == os.path.abspath(output_zip_path):
                        continue
                    arcname = os.path.relpath(file_path, root_path)
                    files_to_zip.append((file_path, arcname))
        
        total_zip = len(files_to_zip)
        zip_count = 0

        if total_zip == 0:
            if progress_callback:
                progress_callback(0, 0, "Nenhum arquivo selecionado para compactação.")
            return

        # Escrita Atômica: grava primeiro em um temporário ao lado do destino
        temp_zip_path = output_zip_path + ".tmp"
        
        try:
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path, arcname in files_to_zip:
                    zip_count += 1
                    if progress_callback:
                        progress_callback(zip_count, total_zip, arcname)
                    zipf.write(file_path, arcname)

            # Substituição atômica: substitui o ZIP original apenas se a compactação foi 100% concluída
            os.replace(temp_zip_path, output_zip_path)
            
        except Exception:
            if os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except OSError:
                    pass
            raise
