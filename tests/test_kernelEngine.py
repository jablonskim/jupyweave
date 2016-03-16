from unittest import TestCase
from kernel_engine import KernelEngine
from exceptions.engine_errors import InvalidLanguageNameError


class TestKernelEngine(TestCase):
    """Tests KernelEngine class"""

    def test_init(self):
        """Tests initializing with default available kernel"""
        engine = KernelEngine()
        self.assertIn('Python 3', engine.__available_kernel_names_mappings)
        self.assertEqual(engine.__available_kernel_names_mappings['Python 3'], 'python3')

    def test_kernel_name_by_language(self):
        """Tests mapping language to kernel name"""
        engine = KernelEngine()

        with self.assertRaises(InvalidLanguageNameError):
            engine.kernel_name_by_language('Invalid language')

        name = engine.kernel_name_by_language('Python 3')
        self.assertEqual(name, 'python3')

    def test_get_client(self):
        """Tests getting clients for different languages and contexts"""
        engine = KernelEngine()
        client1 = engine.get_client('Python 3')
        client2 = engine.get_client('Python 3')
        client3 = engine.get_client('Python 3', 'test')

        self.assertEqual(client1, client2)
        self.assertNotEqual(client1, client3)

