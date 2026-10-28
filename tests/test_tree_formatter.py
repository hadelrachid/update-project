import os
import unittest
from core.tree_formatter import TreeFormatter

class TestTreeFormatter(unittest.TestCase):
    def test_icon_mapping(self):
        self.assertEqual(TreeFormatter._get_icon_for_extension('script.py'), '🐍')
        self.assertEqual(TreeFormatter._get_icon_for_extension('index.php'), '🐘')
        self.assertEqual(TreeFormatter._get_icon_for_extension('schema.sql'), '🗄️')
        self.assertEqual(TreeFormatter._get_icon_for_extension('data.json'), '📋')
        self.assertEqual(TreeFormatter._get_icon_for_extension('unknown.xyz'), '📄')

    def test_tree_structure_with_nested_ancestors(self):
        root = os.path.abspath("dummy_project")
        
        # Simula arquivos aninhados em subpastas
        selected = {
            os.path.join(root, "src", "Core", "Kernel.php"),
            os.path.join(root, "src", "Plugins", "hello.py"),
            os.path.join(root, "README.md")
        }
        
        tree = TreeFormatter.get_tree_string(root, selected)
        
        # O projeto raiz deve estar presente
        self.assertIn("📦 dummy_project/", tree)
        # As pastas ancestrais intermediárias devem ser criadas
        self.assertIn("📁 src/", tree)
        self.assertIn("📁 Core/", tree)
        self.assertIn("📁 Plugins/", tree)
        # Os arquivos com emojis devem estar presentes
        self.assertIn("🐘 Kernel.php", tree)
        self.assertIn("🐍 hello.py", tree)
        self.assertIn("📝 README.md", tree)

if __name__ == '__main__':
    unittest.main()
