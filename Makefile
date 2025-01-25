.PHONY: all check-env ensure-input run-script copy-html complete

# Python binary and virtual environment
PYTHON_BIN := python3.10
VENV_DIR := ./venv
SCRIPT := ./no_parent_child_relation/Family_tree_visualizer_no_parent_child.py
INPUT := no_parent_child_relation/Gomez-Cuetara.csv
OUTPUT := ./family_tree.html
FINAL_HTML := ./index.html

# Default rule
all: check-env ensure-input run-script copy-html complete

# Check if the virtual environment exists or create it
check-env:
	@if [ -d $(VENV_DIR) ]; then \
		echo "Virtual environment found. Activating..."; \
	else \
		echo "Virtual environment not found. Creating..."; \
		$(PYTHON_BIN) -m venv $(VENV_DIR); \
		echo "Installing dependencies..."; \
		. $(VENV_DIR)/bin/activate && pip install -r requirements.txt; \
	fi

# Ensure the input file exists and prompt the user to confirm
ensure-input:
	@if [ ! -f $(INPUT) ]; then \
		echo "Error: $(INPUT) does not exist. Please ensure it is in place."; \
		exit 1; \
	fi
	@read -p "Is $(INPUT) ready for processing? (y/n): " CONFIRM; \
	if [ "$$CONFIRM" != "y" ]; then \
		echo "Process aborted by user."; \
		exit 1; \
	fi

# Run the script to generate the HTML
run-script:
	. $(VENV_DIR)/bin/activate && python $(SCRIPT) --input $(INPUT) || \
	(echo "Error: Failed to run the script."; exit 1)

# Copy the generated HTML to index.html
copy-html:
	@if [ ! -f $(OUTPUT) ]; then \
		echo "Error: $(OUTPUT) was not generated. Please check the script."; \
		exit 1; \
	fi
	cp $(OUTPUT) $(FINAL_HTML)
	echo "HTML copied to $(FINAL_HTML)"

# Finalize the process and provide Git commands
complete:
	@echo "\n\nRun completed successfully!"
	@echo "To commit and push changes, use the following commands:"
	@echo "git add ."
	@echo "git commit -m \"Update family tree\""
	@echo "git push"
