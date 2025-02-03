.PHONY: heroku install run test clean git
.PHONY: ios

# Default Python interpreter
PYTHON = python3
# Virtual environment directory
VENV = env
# Flask application directory
APP_DIR = FlaskAPI

HOST ?= mroom-api-c7aef75a74b0.herokuapp.com

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