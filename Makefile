.PHONY: heroku install run test clean

# Default Python interpreter
PYTHON = python3
# Virtual environment directory
VENV = env

# Deploy to Heroku
heroku:
	git push heroku main

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -r requirements.txt

# Run the Flask application locally
run:
	. $(VENV)/bin/activate && flask run

# Clean up generated files and virtual environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

logs:
	heroku logs --tail --source app

shell:
	heroku run bash

db:
	heroku pg:psql

# Show table structure. Usage: make describe-table TABLE=table_name
describe-table:
	@if [ -z "$(TABLE)" ]; then \
		echo "Error: Please specify a table name using TABLE=table_name"; \
		echo "Example: make describe-table TABLE=users"; \
		exit 1; \
	fi
	heroku pg:psql -c "\d $(TABLE)"

load-data:
	heroku run python API/load_data.py

.PHONY: ios android web

# Install dependencies
install:
	npm install

# Run Expo development server
start:
	npx expo start

# iOS build and setup
ios:
	@echo "🏗️  Creating iOS build..."
	npx expo prebuild -p ios
	@echo "📦 Installing Pods..."
	cd ios && pod install
	@echo "✅ iOS setup complete! You can now open ios/MRoom.xcworkspace"

# Android build
android:
	@echo "🏗️  Creating Android build..."
	npx expo prebuild -p android
	@echo "✅ Android setup complete!"

# Clean builds
clean:
	rm -rf node_modules
	rm -rf ios/Pods
	rm -rf android/build

# Branch management targets
.PHONY: prod-branch deploy-prod

# Create and switch to production branch
prod-branch:
	git checkout -b prod
	git push -u origin prod

# Deploy to production (when on prod branch)
deploy-prod:
	@if [ "$(shell git branch --show-current)" = "prod" ]; then \
		echo "Deploying to production..."; \
		git push origin prod; \
	else \
		echo "Error: You must be on the prod branch to deploy to production"; \
		echo "Run 'git checkout prod' first"; \
		exit 1; \
	fi

# Update production branch with latest main changes
update-prod:
	git checkout prod
	git merge main
	git push origin prod

