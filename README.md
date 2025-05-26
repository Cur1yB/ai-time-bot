# Stateless Chat Graph (LangGraph + Ollama)

Simple chat agent using [LangGraph](https://docs.langgraph.dev), [LangChain](https://www.langchain.com/), and a local model via [Ollama](https://ollama.com/).  
When the user asks for the current time, the agent calls `get_current_time()` and returns the current UTC in ISO-8601 format.

## ⚙️ Setup

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
```

2. **Pull the model**:

   ```bash
   ollama pull mistral
   ```
**Or just run the command**

   ```bash
   make build
   ```
3. **Run the dev agent**:

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   langgraph dev
   ```

Now chat with it! Try asking:
**"What time is it?"**

The agent should respond with the current UTC time using the tool.
