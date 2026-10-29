import unittest
from config.settings import ALLOWED_EXTENSIONS, DEFAULT_IGNORE_DIRS, DEFAULT_IGNORE_FILES, is_test_file
from core.filters import FileFilter, create_file_filter

class TestFileFilter(unittest.TestCase):
    def setUp(self):
        self.filter = FileFilter(
            ignore_patterns=['*.bak', 'temp_*'],
            default_ignore_files=set(DEFAULT_IGNORE_FILES),
            default_ignore_dirs=set(DEFAULT_IGNORE_DIRS),
            allowed_extensions=ALLOWED_EXTENSIONS
        )

    def test_should_ignore_default_dirs(self):
        self.assertTrue(self.filter.should_ignore_dir('.git'))
        self.assertTrue(self.filter.should_ignore_dir('node_modules'))
        self.assertTrue(self.filter.should_ignore_dir('vendor'))
        self.assertFalse(self.filter.should_ignore_dir('src'))
        self.assertFalse(self.filter.should_ignore_dir('core'))

    def test_should_ignore_default_files(self):
        self.assertTrue(self.filter.should_ignore_file('.env'))
        self.assertTrue(self.filter.should_ignore_file('project.txt'))
        self.assertTrue(self.filter.should_ignore_file('cache.tmp'))
        self.assertFalse(self.filter.should_ignore_file('main.py'))
        self.assertFalse(self.filter.should_ignore_file('index.php'))

    def test_should_ignore_patterns(self):
        self.assertTrue(self.filter.should_ignore_file('backup.bak'))
        self.assertTrue(self.filter.should_ignore_file('temp_file.txt'))

    def test_is_allowed_for_report(self):
        # Arquivos minificados não devem ir para o relatório
        self.assertFalse(self.filter.is_allowed_for_report('app.min.js'))
        self.assertFalse(self.filter.is_allowed_for_report('style.min.css'))

    def test_is_test_file_helper(self):
        self.assertTrue(is_test_file('test_core.py'))
        self.assertTrue(is_test_file('test-app.js'))
        self.assertTrue(is_test_file('test.php'))
        self.assertFalse(is_test_file('tester.py'))
        self.assertFalse(is_test_file('main.py'))

    def test_profiles_audit_vs_dist(self):
        # Perfil audit (padrão): NÃO ignora a pasta tests
        filter_audit = create_file_filter(profile="audit")
        self.assertFalse(filter_audit.should_ignore_dir('tests'))
        self.assertFalse(filter_audit.should_ignore_file('test_user.py', is_test=True))
        self.assertTrue(filter_audit.should_ignore_dir('.git'))

        # Perfil dist: IGNORA a pasta tests e arquivos de teste
        filter_dist = create_file_filter(profile="dist")
        self.assertTrue(filter_dist.should_ignore_dir('tests'))
        self.assertTrue(filter_dist.should_ignore_file('test_user.py', is_test=True))
        self.assertTrue(filter_dist.should_ignore_dir('.git'))

if __name__ == '__main__':
    unittest.main()
