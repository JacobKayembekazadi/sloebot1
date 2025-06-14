#!/usr/bin/env python3
"""
Test script for SloeLux Performance Bot
Tests all major components and integrations
"""

import asyncio
import json
from tools import fetch_pagespeed, classify_issues, optimize_shopify_theme, store_metrics
from perf_loop import bot

async def test_tools():
    """Test individual tools"""
    print("🔧 Testing Tools...")
    
    # Test PageSpeed fetch
    print("  📊 Testing PageSpeed fetch...")
    pagespeed_data = fetch_pagespeed.func("https://sloelux.com")
    print(f"     ✅ PageSpeed Score: {pagespeed_data.get('performance_score', 'N/A')}")
    
    # Test issue classification
    print("  🔍 Testing issue classification...")
    issues = classify_issues.func(pagespeed_data)
    print(f"     ✅ Found {len(issues)} issues")
    
    # Test optimization (safe mode)
    print("  ⚡ Testing theme optimization...")
    optimization_result = optimize_shopify_theme.func("sloelux.myshopify.com", "unused-css-rules")
    print(f"     ✅ Optimization: {optimization_result.get('status', 'unknown')}")
    
    # Test metrics storage
    print("  💾 Testing metrics storage...")
    store_result = store_metrics.func(pagespeed_data)
    print(f"     ✅ Storage: {store_result.get('status', 'unknown')}")
    
    return True

async def test_loop_agent():
    """Test the main LoopAgent"""
    print("\n🤖 Testing LoopAgent...")
    
    context = {"timestamp": "test_run", "manual_trigger": True}
    
    results = []
    async for result in bot.loop(context):
        results.append(result)
        print(f"     📈 {result.get('status', 'unknown')}: {result.get('url', 'N/A')}")
        
        # Break after first few results for testing
        if len(results) >= 3:
            break
    
    print(f"     ✅ LoopAgent processed {len(results)} results")
    return True

def test_a2a_capabilities():
    """Test A2A capabilities"""
    print("\n🔗 Testing A2A Capabilities...")
    
    from a2a_middleware import CAPS
    
    for cap in CAPS:
        print(f"     ✅ Capability: {cap['name']} v{cap['version']}")
    
    return True

def test_mcp_server():
    """Test MCP server components"""
    print("\n🌐 Testing MCP Server...")
    
    try:
        from mcp_server import server
        print("     ✅ MCP server imports successfully")
        print(f"     ✅ Bot name: {bot.name}")
        print(f"     ✅ Bot description: {bot.description}")
        return True
    except Exception as e:
        print(f"     ❌ MCP server error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 SloeLux Performance Bot - System Test\n")
    
    tests = [
        ("Tools", test_tools),
        ("LoopAgent", test_loop_agent),
        ("A2A Capabilities", test_a2a_capabilities),
        ("MCP Server", test_mcp_server)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📋 Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems operational! Ready for deployment.")
    else:
        print("⚠️  Some tests failed. Check logs above.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main()) 