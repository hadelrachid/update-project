import os
import shutil
import tempfile
import unittest
from config.settings import ALLOWED_EXTENSIONS, DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_FILES
from core.filters import FileFilter
from core.report import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_update_project_")
        
        # Cria arquivos fictícios para teste
        self.sub_dir = os.path.join(self.test_dir, "app")
        os.makedirs(self.sub_dir, exist_ok=True)
        
        self.file1 = os.path.join(self.test_dir, "main.py")
        with open(self.file1, "w", encoding="utf-8") as f:
            f.write("print('Hello World')\n")
            
        self.file2 = os.path.join(self.sub_dir, "service.php")
        with open(self.file2, "w", encoding="utf-8") as f:
            f.write("<?php echo 'Service';\n")
            
        self.filter = FileFilter([], set(DEFAULT_IGNORE_FILES), set(DEFAULT_IGNORE_DIRS), ALLOWED_EXTENSIONS)
        self.generator = ReportGenerator()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_report_creates_structured_context(self):
        output_txt = os.path.join(self.test_dir, "output.txt")
        selected = {self.file1, self.file2}
        
        self.generator.generate(self.test_dir, selected, self.filter, output_txt)
        
        self.assertTrue(os.path.exists(output_txt))
        
        with open(output_txt, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verifica se o cabeçalho de auditoria está presente
        self.assertIn("/* PROJETO:", content)
        self.assertIn("/* TOTAL DE ARQUIVOS CONSOLIDADOS: 2", content)
        self.assertIn("/* FERRAMENTA: Update-Project", content)
        
        # Verifica se a árvore está presente
        self.assertIn("📁 app/", content)
        self.assertIn("🐘 service.php", content)
        self.assertIn("🐍 main.py", content)
        
        # Verifica se o código dos arquivos foi embutido
        self.assertIn("print('Hello World')", content)
        self.assertIn("<?php echo 'Service';", content)

if __name__ == '__main__':
    unittest.main()
