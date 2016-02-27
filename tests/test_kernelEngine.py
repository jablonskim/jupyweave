from unittest import TestCase
from kernel_engine import KernelEngine
from exceptions.engine_errors import InvalidLanguageNameError


class TestKernelEngine(TestCase):
    """Tests KernelEngine class"""

    def test_init(self):
        """Tests initializing with default available kernel"""
        engine = KernelEngine()
        self.assertIn('Python 3', engine.available_kernel_names_mappings)
        self.assertEqual(engine.available_kernel_names_mappings['Python 3'], 'python3')

    def test_kernel_name_by_language(self):
        """Tests mapping language to kernel name"""
        engine = KernelEngine()

        with self.assertRaises(InvalidLanguageNameError):
            engine.kernel_name_by_language('Invalid language')

        name = engine.kernel_name_by_language('Python 3')
        self.assertEqual(name, 'python3')

    def test_get_kernel(self):
        """Tests creation of kernel for new language and getting existing kernel"""
        engine = KernelEngine()

        self.assertEqual(len(engine.kernels_uuids.keys()), 0)
        self.assertEqual(len(engine.manager.list_kernel_ids()), 0)

        uuid1 = engine.get_kernel('Python 3')

        self.assertEqual(len(engine.kernels_uuids.keys()), 1)
        self.assertEqual(len(engine.manager.list_kernel_ids()), 1)

        with self.assertRaises(InvalidLanguageNameError):
            engine.get_kernel('Invalid language')

        self.assertEqual(len(engine.kernels_uuids.keys()), 1)
        self.assertEqual(len(engine.manager.list_kernel_ids()), 1)

        uuid2 = engine.get_kernel('Python 3')

        self.assertEqual(len(engine.kernels_uuids.keys()), 1)
        self.assertEqual(len(engine.manager.list_kernel_ids()), 1)

        self.assertEqual(uuid1, uuid2)
