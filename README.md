# 🧠 General Assistant — Python · OpenAI Agents SDK · Chainlit - Assignment-1

A simple AI agent built with **Python**, **OpenAI Agents SDK**, and **Chainlit**.  
The bot uses **Google Gemini** (via the OpenAI-compatible endpoint) and provides an interactive web UI.

---

## 🎯 Objectives

- Build a simple agent using **Python** and the **OpenAI Agents SDK**  
- Use **Chainlit** to create an interactive chat interface  
- Connect Chainlit with the agent so it can leverage **LLM** capabilities

---

## ⚙️ Implementation Steps

1. **Environment Setup**
   - Install dependencies: `agents`, `chainlit`, `python-decouple`
   - Create a `.env` file to store your `GEMINI_API_KEY` securely

2. **Agent Initialization**
   - Use `AsyncOpenAI` client to connect to Gemini API  
   - Define `OpenAIChatCompletionsModel`  
   - Configure `RunConfig`  
   - Create an `Agent` with helpful instructions  

3. **Chainlit Interface**
   - `@cl.on_chat_start` greets the user and initializes session state  
   - `@cl.on_message` handles user input, calls the agent, and returns the response  

4. **Conversation Management**
   - Store conversation in `cl.user_session`  
   - Keep both user messages and assistant replies  

---

## 📦 Requirements

```txt
agents>=0.2.0
chainlit>=2.6.9
python-decouple>=3.8
