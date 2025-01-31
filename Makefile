.PHONY: heroku install run test clean git

# Default Python interpreter
PYTHON = python3
# Virtual environment directory
VENV = env
# Flask application directory
APP_DIR = FlaskAPI

# Deploy to Heroku
heroku:
	git subtree push --prefix $(APP_DIR) heroku main

# Quick git commands
git:
	git add .
	git commit -m "pushing"
	git push

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -r $(APP_DIR)/requirements.txt

# Run the Flask application locally
run:
	. $(VENV)/bin/activate && cd $(APP_DIR) && flask run

# Clean up generated files and virtual environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 