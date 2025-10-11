# Create a venv using uv if not already created
venv:
	uv venv

# Install all project dependencies
install:
	uv sync

# Clean and reinstall everything from scratch
reinstall:
	rm -rf .venv uv.lock
	make venv
	make install

# Run the ChatBot Action Server
run:
	poe cta

# Optional: clean build artifacts
clean:
	rm -rf models .rasa .venv uv.lock

.PHONY: venv install reinstall run clean
