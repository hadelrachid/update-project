import fnmatch
import os
from typing import List, Set, Tuple
from config.settings import (
    ALLOWED_EXTENSIONS,
    get_ignore_rules_for_profile,
    is_test_file
)

class FileFilter:
    def __init__(
        self,
        ignore_patterns: list = None,
        default_ignore_files: set = None,
        default_ignore_dirs: set = None,
        allowed_extensions: tuple = ALLOWED_EXTENSIONS,
        profile: str = "audit"
    ):
        self.ignore_patterns = ignore_patterns if ignore_patterns else []
        self.default_ignore_files = default_ignore_files if default_ignore_files is not None else set()
        self.default_ignore_dirs = default_ignore_dirs if default_ignore_dirs is not None else set()
        self.allowed_extensions = allowed_extensions
        self.profile = profile.lower()

    def should_ignore_file(self, filename: str, is_test: bool = False) -> bool:
        if filename in self.default_ignore_files or filename.endswith('.tmp'):
            return True
        # No perfil 'dist', exclui arquivos de teste. No perfil 'audit', mantém testes.
        if is_test and self.profile == "dist":
            return True
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                return True
        return False

    def should_ignore_dir(self, dirname: str) -> bool:
        if dirname in self.default_ignore_dirs:
            return True
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(dirname.lower(), pattern.lower()):
                return True
        return False

    def is_allowed_for_report(self, filepath: str) -> bool:
        if not os.path.isfile(filepath):
            return False
        if not filepath.endswith(self.allowed_extensions):
            return False
        if filepath.endswith('.min.css') or filepath.endswith('.min.js'):
            return False
        
        filename = os.path.basename(filepath)
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                return False
        return True


def create_file_filter(
    profile: str = "audit",
    custom_ignore_patterns: list = None,
    root_path: str = ""
) -> FileFilter:
    """
    Fábrica centralizada para garantir paridade total entre CLI e GUI.
    """
    ignore_dirs, ignore_files = get_ignore_rules_for_profile(profile)
    
    if root_path:
        project_name = os.path.basename(os.path.normpath(root_path))
        ignore_files.add(f"{project_name}.txt")
        ignore_files.add(f"{project_name}.zip")
        ignore_files.add("project.txt")

    return FileFilter(
        ignore_patterns=custom_ignore_patterns or [],
        default_ignore_files=ignore_files,
        default_ignore_dirs=ignore_dirs,
        allowed_extensions=ALLOWED_EXTENSIONS,
        profile=profile
    )
