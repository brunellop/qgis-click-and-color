"""Utility comuni per i test del plugin, pattern standard Plugin Builder 3.
Richiede QGIS headless (qgis.testing.start_app) per l'esecuzione reale."""

import sys

QGIS_APP = None


def get_qgis_app():
    global QGIS_APP
    if QGIS_APP is None:
        from qgis.testing import start_app
        QGIS_APP = start_app()
    return QGIS_APP
