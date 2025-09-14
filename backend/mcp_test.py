from fastmcp import FastMCP

mcp = FastMCP("pocket-broker")

@mcp.tool()
def hello() -> str:
    """Say hello"""
    print("Tool called from VAPI!")
    return "Hello from FastMCP"

@mcp.tool()
def create_assistant(prompt: str) -> dict:
    """Create a new VAPI voice assistant with given prompt"""
    from vapi_client import create_voice_assistant
    return create_voice_assistant(prompt)


if __name__ == "__main__":
    mcp.run()
