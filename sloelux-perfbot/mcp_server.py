# MCP Server for SloeLux Performance Bot
# Simplified implementation for demo

from perf_loop import bot
import asyncio

class SimpleMCPServer:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.functions = {}
    
    def register_function(self, func):
        self.functions[func.__name__] = func
    
    def run(self, host="0.0.0.0", port=9000):
        print(f"MCP Server '{self.name}' running on {host}:{port}")
        print(f"Description: {self.description}")
        print(f"Registered functions: {list(self.functions.keys())}")

server = SimpleMCPServer(name="PerfBot", description="PageSpeed fixer")
server.register_function(bot.run)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=9000) 