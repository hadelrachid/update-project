import os
import shutil
import tempfile
import unittest
from core.filters import create_file_filter
from core.report import ReportGenerator
from core.compressor import Compressor
from core.services import ExportProjectService

class TestExportProjectService(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_service_")
        
        self.file1 = os.path.join(self.test_dir, "index.php")
        with open(self.file1, "w", encoding="utf-8") as f:
            f.write("<?php echo 'Home';\n")
            
        self.filter = create_file_filter(profile="audit", root_path=self.test_dir)
        self.service = ExportProjectService(ReportGenerator(), Compressor())

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_service_executes_and_syncs_project_txt(self):
        project_name = os.path.basename(os.path.normpath(self.test_dir))
        named_txt = os.path.join(self.test_dir, f"{project_name}.txt")
        legacy_txt = os.path.join(self.test_dir, "project.txt")
        zip_path = os.path.join(self.test_dir, f"{project_name}.zip")
        
        logs = []
        success, msg = self.service.execute(
            self.test_dir,
            {self.file1},
            self.filter,
            progress_text_cb=lambda t: logs.append(t),
            progress_val_cb=lambda v: None
        )
        
        self.assertTrue(success)
        self.assertIn("criados com sucesso!", msg)
        self.assertIn("Perfil: AUDIT", msg)
        
        # Verifica se ambos os relatórios e o zip foram gerados
        self.assertTrue(os.path.exists(named_txt))
        self.assertTrue(os.path.exists(legacy_txt))
        self.assertTrue(os.path.exists(zip_path))
        
        # Verifica se não ficaram arquivos .tmp residuais
        self.assertFalse(os.path.exists(named_txt + ".tmp"))
        self.assertFalse(os.path.exists(legacy_txt + ".tmp"))
        self.assertFalse(os.path.exists(zip_path + ".tmp"))

if __name__ == '__main__':
    unittest.main()
