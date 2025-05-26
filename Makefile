freeze:
	. .venv/bin/activate && pip freeze > requirements.txt

build:
	curl -fsSL https://ollama.com/install.sh | sh
	ollama pull mistral

dev:
	python -m venv .venv && source .venv/bin/activate
	pip install -r requirements.txt
	langgraph dev
