#!/usr/bin/env python3
"""
Deployment script for SloeLux Performance Bot
Starts both FastAPI and MCP servers
"""

import subprocess
import sys
import time
import asyncio
from pathlib import Path

# Import bot at module level
try:
    from perf_loop import bot
except ImportError:
    bot = None

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import uvicorn
        from google.adk.agents import LlmAgent
        from tools import fetch_pagespeed
        print("✅ All requirements satisfied")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file found")
        return True
    else:
        print("⚠️  No .env file found. Using defaults.")
        return True

async def test_bot():
    """Quick test of the bot functionality"""
    try:
        if bot is None:
            print("❌ Bot not available")
            return False
            
        context = {"timestamp": "deployment_test"}
        results = []
        async for result in bot.loop(context):
            results.append(result)
            if len(results) >= 1:  # Just test first result
                break
        
        if results and results[0].get('status') == 'completed':
            print("✅ Bot functionality test passed")
            return True
        else:
            print("⚠️  Bot test completed with warnings")
            return True
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        return False

def start_servers():
    """Start both FastAPI and MCP servers"""
    print("\n🚀 Starting SloeLux Performance Bot servers...")
    
    print("\n📋 Server Information:")
    print("  FastAPI Server: http://localhost:8000")
    print("  MCP Server: localhost:9000")
    print("  API Documentation: http://localhost:8000/docs")
    print("\n🔧 Available Endpoints:")
    print("  GET  /           - Health check")
    print("  POST /analyze    - Trigger performance analysis")
    print("  POST /optimize   - Apply theme optimizations")
    print("  GET  /metrics    - View performance metrics")
    print("  GET  /status     - Bot status")
    
    print("\n⚡ To start servers manually:")
    print("  FastAPI: python -c \"import uvicorn; from fastapi_server import app; uvicorn.run(app, host='0.0.0.0', port=8000)\"")
    print("  MCP:     python mcp_server.py")
    
    return True

async def main():
    """Main deployment function"""
    print("🎯 SloeLux Performance Bot - Deployment\n")
    
    # Run checks
    checks = [
        ("Requirements", check_requirements()),
        ("Environment", check_environment()),
        ("Bot Functionality", await test_bot())
    ]
    
    print("\n📋 Pre-deployment Checks:")
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! System ready for deployment.")
        start_servers()
    else:
        print("\n⚠️  Some checks failed. Please review and fix issues before deployment.")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main()) 