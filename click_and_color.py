import os
from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsCategorizedSymbolRenderer, QgsGeometry, QgsFeatureRequest
from qgis.PyQt.QtWidgets import QAction, QColorDialog
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt


class ClickAndColorTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.setCursor(Qt.CrossCursor)
        self.canvasClicked.connect(self.onClick)

    def onClick(self, point, button):
        layer = self.canvas.currentLayer()
        if not layer or not layer.isSpatial():
            return

        renderer = layer.renderer()
        if not isinstance(renderer, QgsCategorizedSymbolRenderer):
            return

        point_layer = self.toLayerCoordinates(layer, point)
        geom_point = QgsGeometry.fromPointXY(point_layer)

        # Raggio di tolleranza di 8 pixel per catturare agevolmente punti e linee
        tolerance = self.canvas.mapUnitsPerPixel() * 8
        search_geom = geom_point.buffer(tolerance, 5)

        req = QgsFeatureRequest().setFilterRect(search_geom.boundingBox())
        attr_field = renderer.classAttribute()

        for feat in layer.getFeatures(req):
            if feat.geometry() and feat.geometry().intersects(search_geom):
                valore_cat = feat[attr_field]

                cat_index = renderer.categoryIndexForValue(valore_cat)
                if cat_index != -1:
                    category = renderer.categories()[cat_index]
                    colore_attuale = category.symbol().color()

                    nuovo_colore = QColorDialog.getColor(
                        colore_attuale,
                        None,
                        f"Seleziona colore per '{valore_cat}'"
                    )

                    if nuovo_colore.isValid():
                        nuovo_simbolo = category.symbol().clone()
                        nuovo_simbolo.setColor(nuovo_colore)
                        renderer.updateCategorySymbol(cat_index, nuovo_simbolo)

                        layer.triggerRepaint()
                        from qgis.utils import iface
                        iface.layerTreeView().refreshLayerSymbology(layer.id())
                        layer.emitStyleChanged()
                    return


class ClickAndColorPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.canvas = iface.mapCanvas()
        self.tool = None
        self.actions = []
        self.menu = "&Click && Color"
        self.toolbar = self.iface.addToolBar("Click & Color")
        self.toolbar.setObjectName("ClickAndColor")

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        icon = QIcon(icon_path)

        action = QAction(icon, "Click & Color", self.iface.mainWindow())
        action.setCheckable(True)
        action.triggered.connect(self.toggle_tool)

        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)

        self.tool = ClickAndColorTool(self.canvas)
        self.tool.deactivated.connect(self.on_deactivate)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def toggle_tool(self, checked):
        if checked:
            self.canvas.setMapTool(self.tool)
        else:
            self.canvas.unsetMapTool(self.tool)

    def on_deactivate(self):
        if self.actions:
            self.actions[0].setChecked(False)
