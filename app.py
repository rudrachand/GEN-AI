from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os
import asyncio
import json, re
os.environ["MCP_USE_DEBUG_LOGGING"] = "false"
os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"
load_dotenv()


# llm= ChatGroq(model="openai/gpt-oss-120b")
llm= ChatGroq(model="openai/gpt-oss-20b")

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    config_file = "mcp-config.json"
    print("Initializing chat...")

    # Initialize the MCP client
    client = MCPClient.from_config_file(config_file)

    # Create an MCPAgent with the specified model and memory
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        memory_enabled=True,
    )

    print("\n== Interactive MCP Chat ==")

    try:
        while True:
            user_input = input("You: ").strip()

            # exit/quit handling (fix: use membership, not equality to a list)
            if user_input.lower() in ("exit", "quit", "bye"):
                print("Exiting chat...")
                break

            # clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            # Get the agent's response (fix: it's a string, not an object with .content)
            response = await agent.run(user_input)
            print(response)
            await asyncio.sleep(2)

    except KeyboardInterrupt:
        print("\nChat ended by user.")

    except Exception as e:
        # Show the error, but keep going through finally for cleanup
        print(f"\nAn error occurred: {e}")

    finally:
        # (fix) MCPClient has 'sessions' not 'session'; you can just call close_all_sessions()
        try:
            await client.close_all_sessions()
        except AttributeError:
            # Fallback if API differs
            if hasattr(client, "sessions"):
                # If sessions is an iterable of session objects with an async close()
                sessions = getattr(client, "sessions")
                for s in sessions:
                    try:
                        close = getattr(s, "close", None)
                        if close is not None:
                            maybe_await = close()
                            if asyncio.iscoroutine(maybe_await):
                                await maybe_await
                    except Exception:
                        pass
        print("Chat ended.")

if __name__ == "__main__":    
    asyncio.run(run_memory_chat())
