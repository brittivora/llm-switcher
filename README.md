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

