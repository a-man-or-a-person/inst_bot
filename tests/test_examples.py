import ast
from pathlib import Path
import unittest


class ExampleSafetyTests(unittest.TestCase):
    def test_examples_require_explicit_execution_and_environment_credentials(self):
        root = Path(__file__).resolve().parents[1]
        for name in ("main.py", "post_reel.py", "post_reel_phone.py"):
            with self.subTest(script=name):
                tree = ast.parse((root / name).read_text(encoding="utf-8"))
                guards = [node for node in tree.body if isinstance(node, ast.If)]
                self.assertEqual(len(guards), 1)
                self.assertEqual(ast.unparse(guards[0].test), "__name__ == '__main__'")
                self.assertFalse(any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) for node in tree.body))
                calls = [node for node in ast.walk(guards[0]) if isinstance(node, ast.Call)]
                credentials = {kw.arg: ast.unparse(kw.value) for call in calls for kw in call.keywords if kw.arg in ("username", "password")}
                self.assertEqual(credentials, {"username": "os.environ['INSTAGRAM_USERNAME']", "password": "os.environ['INSTAGRAM_PASSWORD']"})


if __name__ == "__main__":
    unittest.main()
