import os
import shutil
import tempfile
import zipfile
import unittest
from config.settings import ALLOWED_EXTENSIONS, DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_FILES
from core.filters import FileFilter
from core.compressor import Compressor

class TestCompressor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_zip_")
        
        self.file1 = os.path.join(self.test_dir, "app.py")
        with open(self.file1, "w", encoding="utf-8") as f:
            f.write("# App Code\n")
            
        self.ignored = os.path.join(self.test_dir, ".env")
        with open(self.ignored, "w", encoding="utf-8") as f:
            f.write("SECRET_KEY=123\n")
            
        self.filter = FileFilter([], set(DEFAULT_IGNORE_FILES), set(DEFAULT_IGNORE_DIRS), ALLOWED_EXTENSIONS)
        self.compressor = Compressor()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compress_creates_valid_zip_without_ignored_files(self):
        zip_output = os.path.join(self.test_dir, "archive.zip")
        selected = {self.file1, self.ignored}
        
        self.compressor.compress(self.test_dir, selected, self.filter, zip_output)
        
        self.assertTrue(os.path.exists(zip_output))
        self.assertFalse(os.path.exists(zip_output + ".tmp")) # Escrita atômica limpa temporários
        
        with zipfile.ZipFile(zip_output, 'r') as z:
            names = z.namelist()
            self.assertIn("app.py", names)
            # .env está na lista de DEFAULT_IGNORE_FILES e não deve ir para o ZIP
            self.assertNotIn(".env", names)

if __name__ == '__main__':
    unittest.main()
