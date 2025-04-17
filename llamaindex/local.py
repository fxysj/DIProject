from llama_index.llms.ollama import Ollama

llm = Ollama(model="gemma:2b", request_timeout=60.0)
print(llm.complete("What is the capital of France?"))