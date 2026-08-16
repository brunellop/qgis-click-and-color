import unittest
from unittest.mock import MagicMock

from click_and_color import classFactory


class ClickAndColorInitTest(unittest.TestCase):
    """Verifica minima: il plugin si istanzia senza errori.
    Richiede un ambiente QGIS headless (es. qgis.testing) per essere
    eseguito davvero: qui iface e' un mock solo per verificare che
    classFactory/__init__ non sollevino eccezioni impreviste."""

    def test_class_factory(self):
        fake_iface = MagicMock()
        plugin = classFactory(fake_iface)
        self.assertIsNotNone(plugin)


if __name__ == "__main__":
    unittest.main()
