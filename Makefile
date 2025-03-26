.PHONY: heroku install run test clean git
.PHONY: ios

# Default Python interpreter
PYTHON = python3
# Virtual environment directory
VENV = env
# Flask application directory
APP_DIR = Flask

HOST ?= mroom-staging-031597615ed8.herokuapp.com

# Add near the top with other variables
VENV_PATH = ~/venvs/mroom

# Deploy to Heroku
heroku:
	git subtree push --prefix $(APP_DIR) heroku main

staging:
	git subtree push --prefix $(APP_DIR) staging main

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


ios:
	@echo "🏗️  Creating iOS build..."
	cd MRoom && npx expo prebuild -p ios
	@echo "📦 Installing Pods..."
	cd MRoom/ios && pod install
	@echo "✅ iOS setup complete! You can now open ios/MRoom.xcworkspace"

buildings:
	curl -v -X GET http://${HOST}/buildings || true

rooms:
	curl -v -X GET http://${HOST}/rooms || true

logs-heroku:
	heroku logs --app mroom-api --tail --source app

logs-staging:
	heroku logs --app mroom-staging --tail --source app

shell-heroku:
	heroku run bash --app mroom-api

db-heroku:
	heroku pg:psql --app mroom-api

# ... existing code ...

APP_NAME = $(shell echo ${HOST} | cut -d'.' -f1)

# Show table structure. Usage: make describe-table TABLE=table_name
describe-table:
	@if [ -z "$(TABLE)" ]; then \
		echo "Error: Please specify a table name using TABLE=table_name"; \
		echo "Example: make describe-table TABLE=users"; \
		exit 1; \
	fi
	heroku pg:psql --app mroom-api -c "\d $(TABLE)"

upload-building:
	curl -v -X POST http://${HOST}/buildings \
		-H "Content-Type: application/json" \
		-H "Accept: application/json" \
		-d '{"name": "Test Building", "short_name": "TEST"}'

# Update the env target
env:
	source $(VENV_PATH)/bin/activate

load-data-staging:
	heroku run python API/load_data.py --app mroom-staging

# Add a new command to load data into production
load-data-prod:
	heroku run python API/load_data.py --app mroom-api

heroku-restart:
	heroku restart --app mroom-staging

heroku-rebuild-python:
	heroku buildpacks:clear --app mroom-staging
	heroku buildpacks:set heroku/python --app mroom-staging
	heroku config:set PYTHON_VERSION=3.12.0 --app mroom-staging
	git commit --allow-empty -m "Force rebuild with Python 3.12"
	git push staging main

