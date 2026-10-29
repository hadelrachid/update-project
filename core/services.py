import os
import shutil
from typing import Callable, List
from core.filters import FileFilter
from core.report import ReportGenerator
from core.compressor import Compressor

class ExportProjectService:
    def __init__(self, report_generator: ReportGenerator, compressor: Compressor):
        self.report_generator = report_generator
        self.compressor = compressor

    def execute(
        self,
        root_path: str,
        selected_paths: set,
        file_filter: FileFilter,
        progress_text_cb: Callable[[str], None],
        progress_val_cb: Callable[[int], None]
    ):
        project_name = os.path.basename(os.path.normpath(root_path))
        
        named_report_path = os.path.join(root_path, f"{project_name}.txt")
        legacy_report_path = os.path.join(root_path, 'project.txt')
        zip_path = os.path.join(root_path, f"{project_name}.zip")

        # 1. Gerar Relatório de Contexto (0 a 50%)
        def report_progress(count: int, total: int, msg: str):
            percent = int((count / total) * 50) if total > 0 else 50
            progress_val_cb(percent)
            progress_text_cb(msg)

        progress_text_cb("Iniciando geração do relatório de contexto estruturado...")
        report_meta = self.report_generator.generate(
            root_path,
            selected_paths,
            file_filter,
            named_report_path,
            report_progress
        )
        
        # Mantém project.txt sincronizado de forma segura e atômica
        sync_warning = None
        temp_legacy = legacy_report_path + ".tmp"
        try:
            shutil.copy2(named_report_path, temp_legacy)
            os.replace(temp_legacy, legacy_report_path)
        except Exception as e:
            if os.path.exists(temp_legacy):
                try:
                    os.remove(temp_legacy)
                except OSError:
                    pass
            sync_warning = f"Aviso: Não foi possível sincronizar 'project.txt' ({e})"
            progress_text_cb(sync_warning)

        # 2. Gerar ZIP do Projeto (50 a 100%)
        def zip_progress(count: int, total: int, msg: str):
            percent = 50 + int((count / total) * 50) if total > 0 else 100
            progress_val_cb(percent)
            progress_text_cb(f"Compactando: {msg}")

        progress_text_cb("Iniciando compactação em arquivo ZIP...")
        self.compressor.compress(root_path, selected_paths, file_filter, zip_path, zip_progress)
        
        progress_val_cb(100)
        progress_text_cb("Processo concluído com sucesso!")
        
        total_consolidated = report_meta.get("total_files", len(selected_paths)) if report_meta else len(selected_paths)
        profile_label = getattr(file_filter, 'profile', 'audit').upper()
        
        msg = f"Relatórios ({project_name}.txt e project.txt) e ZIP ({project_name}.zip) criados com sucesso! [Perfil: {profile_label} | {total_consolidated} arquivos consolidados]"
        if sync_warning:
            msg += f" | {sync_warning}"

        return True, msg
