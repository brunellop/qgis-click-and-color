PLUGINNAME = click_and_color
PY_FILES = __init__.py click_and_color.py
EXTRAS = icon.png icon.svg metadata.txt LICENSE

deploy:
	mkdir -p $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)

zip: clean
	mkdir -p $(PLUGINNAME)
	cp -vf $(PY_FILES) $(EXTRAS) $(PLUGINNAME)
	zip -r $(PLUGINNAME).zip $(PLUGINNAME)
	rm -rf $(PLUGINNAME)

clean:
	rm -f $(PLUGINNAME).zip
	rm -rf $(PLUGINNAME)
