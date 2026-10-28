# config/settings.py

ALLOWED_EXTENSIONS = (
    '.php', '.css', '.js', '.txt', '.json', '.md', '.html', '.py', '.xml', '.sql',
    '.yml', '.yaml', '.ini', '.sh', '.bash', '.ts', '.tsx', '.jsx', '.vue'
)

DEFAULT_IGNORE_DIRS = [
    '.git', '.vscode', '.idea', '__pycache__', 'node_modules', 'tests', 'temp',
    'auditoria', 'wiki', 'docs', 'vendor', '.phpunit.cache', 'dist', 'build',
    '.kilo', '.system_generated', 'scratch', 'storage'
]

DEFAULT_IGNORE_FILES = [
    'project.txt', '.env', 'database.sqlite', '.phpunit.result.cache',
    'update_project.py', '.DS_Store', 'Thumbs.db'
]

def is_test_file(filename: str) -> bool:
    name = filename.lower()
    return name.startswith('test-') or name.startswith('test_') or name == 'test.php'
