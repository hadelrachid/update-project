# config/settings.py
import os
from typing import List, Set, Tuple

ALLOWED_EXTENSIONS = (
    '.php', '.css', '.js', '.txt', '.json', '.md', '.html', '.py', '.xml', '.sql',
    '.yml', '.yaml', '.ini', '.sh', '.bash', '.ts', '.tsx', '.jsx', '.vue'
)

# Diretórios que contêm dependências pesadas, cache e artefatos temporários
# (sempre ignorados em qualquer perfil)
COMMON_IGNORE_DIRS = [
    '.git', '.vscode', '.idea', '__pycache__', 'node_modules', 'vendor',
    '.phpunit.cache', 'dist', 'build', '.system_generated', 'scratch', 'temp', 'storage',
    '.kilo', '.gemini'
]

# Diretórios extras ignorados exclusivamente no perfil 'dist' (distribuição enxuta)
DIST_EXTRA_IGNORE_DIRS = [
    'tests', 'auditoria', 'wiki', 'docs'
]

# Compatibilidade retroativa
DEFAULT_IGNORE_DIRS = COMMON_IGNORE_DIRS + DIST_EXTRA_IGNORE_DIRS

# Arquivos ignorados por padrão
COMMON_IGNORE_FILES = [
    'project.txt', '.env', 'database.sqlite', '.phpunit.result.cache',
    'update_project.py', '.DS_Store', 'Thumbs.db'
]

DEFAULT_IGNORE_FILES = COMMON_IGNORE_FILES

def is_test_file(filename: str) -> bool:
    name = filename.lower()
    return name.startswith('test-') or name.startswith('test_') or name == 'test.php'

def get_ignore_rules_for_profile(profile: str = "audit") -> Tuple[Set[str], Set[str]]:
    """
    Retorna (ignore_dirs, ignore_files) de acordo com o perfil.
    Perfis suportados:
      - 'audit': Mantém testes, documentação e contratos no contexto da IA.
      - 'dist': Remove testes, documentação e auditorias para distribuição enxuta.
    """
    ignore_files = set(COMMON_IGNORE_FILES)
    if profile.lower() == "dist":
        ignore_dirs = set(COMMON_IGNORE_DIRS + DIST_EXTRA_IGNORE_DIRS)
    else:
        # Perfil 'audit' (padrão): NÃO ignora tests, docs ou wiki
        ignore_dirs = set(COMMON_IGNORE_DIRS)
        
    return ignore_dirs, ignore_files
