from .models.mistral import call_mistral
from .models.llama2 import call_llama2

def route_model(model: str, prompt: str):
    if model == "mistral":
        return call_mistral(prompt)
    elif model == "llama2":
        return call_llama2(prompt)
    else:
        raise ValueError("Invalid model specified")
