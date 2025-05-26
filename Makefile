freeze:
	. .venv/bin/activate && pip freeze > requirements.txt

build:
	curl -fsSL https://ollama.com/install.sh | sh
	ollama pull mistral

dev:
	langgraph dev
