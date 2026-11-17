from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Business Hours Server")

@mcp.resource("hours://business")
def get_business_hours() -> str:
    """Provides the current hours of operation for the business."""
    return (
        "Store Hours of Operation:\n"
        "Monday - Friday: 9:00 AM - 6:00 PM\n"
        "Saturday: 10:00 AM - 4:00 PM\n"
        "Sunday: Closed"
    )

if __name__ == "__main__":
    mcp.run()