from typing import cast
from agents import Runner, Agent, OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig
from decouple import config
import chainlit as cl


gemini_api_key=config("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():

    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    run_config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

     # Store session data
    cl.user_session.set("chat_history", [])
    cl.user_session.set("run_config", run_config)


    agent = Agent(
        name="General Assistant",
        instructions="""
            "You are a helpful and knowledgeable assistant. "
            "Answer questions clearly and politely. "
            "You can help with programming, general knowledge, study guidance, and daily life queries. "
            "When appropriate, provide short examples or step-by-step explanations. "
            "Use Markdown formatting for code or lists to make responses easy to read."
    """,
        model=model
    )
    cl.user_session.set("agent", agent)
    await cl.Message(content="👋 Hello! I'm your **General Assistant**.\nHow can I help you today? 🤖").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="🤔 Thinking...")
    await msg.send()

    # ✅ Correct type casting
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    run_config: RunConfig = cast(RunConfig, cl.user_session.get("run_config"))
    chat_history = cl.user_session.get("chat_history") or []

    chat_history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", chat_history, "\n")

        # ✅ Use async version
        result = await Runner.run(
            starting_agent=agent,
            input=chat_history,
            run_config=run_config
        )

        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        cl.user_session.set("chat_history", result.to_input_list())

        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
