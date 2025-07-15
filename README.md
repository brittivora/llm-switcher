# 🧠 LLM Switcher API (FastAPI + Groq)

This project implements a minimal FastAPI service that allows users to send prompts to two different open-source LLMs via HTTP. The models are served using Groq's blazing-fast inference APIs.

## 🚀 Features

- Accepts a user prompt via HTTP (`/generate`)
- Routes request to either `llama2` or `mistral` model via query parameter
- Logs:
  - Latency (in ms)
  - Token count
  - Prompt + response
- Models:  
  - **LLaMA 2** (Groq's `llama3-8b-8192`)
  - **Mistral** (Groq's `mistral-saba-24b`)

## 📁 Project Structure

```
├── main.py                 # FastAPI application entry point
├── models_utils.py         # Model routing logic
├── models/
│   ├── llama2.py          # LLaMA2 model implementation
│   └── mistral.py         # Mistral model implementation
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
└── logs/
    └── prompts_log.csv    # Auto-generated request logs
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Note**: Get your Groq API key from [Groq Console](https://console.groq.com/)

### 3. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Generate Text

**Endpoint**: `POST /generate`

**Parameters**:
- `model` (query parameter): Either `"llama2"` or `"mistral"`
- Request body: JSON with `prompt` field

**Example Request**:
```bash
curl -X POST "http://localhost:8000/generate?model=llama2" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'
```

**Example Response**:
```json
{
  "model": "llama2",
  "prompt": "Explain quantum computing in simple terms",
  "response": "Quantum computing is a revolutionary technology that uses quantum mechanics...",
  "token_count": 156,
  "latency_ms": 1234.56
}
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Model Configurations

### LLaMA2 (via Groq)
- **Model ID**: `llama3-8b-8192`
- **Temperature**: 0.7
- **Max Tokens**: 200
- **Implementation**: Standard HTTP requests

### Mistral (via Groq)
- **Model ID**: `mistral-saba-24b`
- **Temperature**: 1.0
- **Max Tokens**: 512
- **Implementation**: Streaming responses

## Logging

All requests are automatically logged to `logs/prompts_log.csv` with the following fields:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO format timestamp |
| `model` | Model used (llama2/mistral) |
| `prompt` | User input prompt |
| `response` | Model response |
| `token_count` | Estimated token usage |
| `latency_ms` | Response time in milliseconds |

## Error Handling

The API includes comprehensive error handling:

- **Missing API Key**: Runtime error on startup
- **Invalid Model**: ValueError for unsupported models
- **API Failures**: Detailed error messages with response context
- **Network Issues**: Proper exception handling and logging

## Development

### Adding New Models

1. Create a new file in `models/` directory
2. Implement the model calling function
3. Add routing logic in `models_utils.py`
4. Update the enum in `main.py`

### Example Model Implementation

```python
# models/new_model.py
import time

def call_new_model(prompt: str):
    start = time.time()
    
    # Your model calling logic here
    response = "Generated response"
    
    latency = round((time.time() - start) * 1000, 2)
    token_count = len(prompt.split()) + len(response.split())
    
    return response, token_count, latency
```

## Security Considerations

- API key is loaded from environment variables
- CORS is currently set to allow all origins (configure for production)
- No authentication implemented (add as needed)
- Input validation through Pydantic models

## Performance Notes

- Token counting uses simple word splitting (consider using proper tokenizers)
- CSV logging is synchronous (consider async for high-throughput scenarios)
- No rate limiting implemented
- Memory usage grows with log file size

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Requests**: HTTP client for LLaMA2
- **Groq**: Official Groq client for Mistral
- **Python-dotenv**: Environment variable management
