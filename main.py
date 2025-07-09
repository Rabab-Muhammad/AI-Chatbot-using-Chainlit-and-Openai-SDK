import os
import chainlit as cl
from openai import AsyncOpenAI

@cl.on_chat_start
async def on_chat_start():
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        await cl.Message(content="🚨 GEMINI_API_KEY is missing!").send()
        return

    cl.user_session.set("client", AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    ))

    await cl.Message(content="👋 Hello! I'm your Gemini bot.").send()

@cl.on_message
async def on_message(message: cl.Message):
    client = cl.user_session.get("client")
    if not client:
        await cl.Message(content="❌ Gemini client not set.").send()
        return

    try:
        response = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": message.content}]
        )
        await cl.Message(content=response.choices[0].message.content).send()
    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()
