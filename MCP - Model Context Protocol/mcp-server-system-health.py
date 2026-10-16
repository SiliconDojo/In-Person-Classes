import subprocess

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("System-Monitor")

@mcp.tool()
def get_system_health() -> str:
    """Return the output of the Top command to show CPU and Memory usage of system"""
    result = subprocess.run(['top', '-l', '1', '-n', '0'], capture_output=True, text=True)
    return result.stdout

@mcp.tool()
def get_network() -> str:
    """Return the Ping results from google.com"""
    result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True)
    return result.stdout 

@mcp.tool()
def get_storage() -> str:
    """Return the Utilization of the Local hard Drive"""
    result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
    return result.stdout 

if __name__ == "__main__":
    mcp.run()