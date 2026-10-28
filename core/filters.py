import fnmatch
import os

class FileFilter:
    def __init__(self, ignore_patterns: list, default_ignore_files: set, default_ignore_dirs: set, allowed_extensions: tuple):
        self.ignore_patterns = ignore_patterns if ignore_patterns else []
        self.default_ignore_files = default_ignore_files
        self.default_ignore_dirs = default_ignore_dirs
        self.allowed_extensions = allowed_extensions

    def should_ignore_file(self, filename: str, is_test: bool = False) -> bool:
        if filename in self.default_ignore_files or filename.endswith('.tmp'):
            return True
        if is_test:
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
