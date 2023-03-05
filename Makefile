init_venv:
	python -m venv .venv

activate:
	source ./.venv/bin/activate

install_package:
	python -m pip install -U pip
	python -m pip install -U selenium

init: init_venv activate install_package
	
.PHONY: clean
clean: 
	python -m pip uninstall selenium
	rm -rf venv/
	rm *.log