PYTHON=python3

.PHONY: clean
clean: 
	
	${PYTHON} -m pip uninstall selenium
	rm -rf .venv/
	rm *.log