from datetime import datetime
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("time-server")

@mcp.tool()
def get_time() -> str:
    """Return the current time (HH:MM:SS)."""
    return datetime.now().strftime("%H:%M:%S")

@mcp.tool()
def get_day_month_year() -> str:
    """Return the current day of the week."""
    return datetime.now().strftime("%A, %B, %Y")

if __name__ == "__main__":
    mcp.run()