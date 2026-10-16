# server.py
from datetime import datetime
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("time-server")

@mcp.tool(
    name="Get_Current_Time",
    description="Return the current time in HH:MM:SS (24-hour) format, based on the server's local clock.",
)
def get_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

@mcp.tool(
    name="Get_The_Day_Month_And_Year",
    description="Return the current day of the week (e.g. 'Monday'), based on the server's local clock.",
)
def get_day_month_year() -> str:
    return datetime.now().strftime("%A, %B, %Y")

if __name__ == "__main__":
    mcp.run()