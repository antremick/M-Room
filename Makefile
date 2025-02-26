.PHONY: heroku install run test clean git
.PHONY: ios

# Default Python interpreter
PYTHON = python3
# Virtual environment directory
VENV = env
# Flask application directory
APP_DIR = Flask

HOST ?= mroom-api-c7aef75a74b0.herokuapp.com

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

logs-heroku:
	heroku logs --app mroom-api --tail --source app

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