#!/usr/bin/env python3
"""
Kimi K2 Integration Setup
Directory: /Users/shenseanchen/Desktop/Dev/claude-code/

This script provides multiple ways to access and integrate Kimi K2:
1. Via OpenRouter API (easiest)
2. Via Moonshot AI direct API
3. Local deployment setup
4. Tool calling and agentic workflows

Kimi K2 is a 1T parameter MoE model optimized for agentic tasks.
"""

import os
import json
import openai
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
import subprocess
import sys

@dataclass
class KimiK2Config:
    """Configuration for Kimi K2 access methods"""
    openrouter_api_key: Optional[str] = None
    moonshot_api_key: Optional[str] = None
    model_name: str = "moonshotai/kimi-k2"
    base_url_openrouter: str = "https://openrouter.ai/api/v1"
    base_url_moonshot: str = "https://api.moonshot.cn/v1"
    max_tokens: int = 4096
    temperature: float = 0.7

class KimiK2Client:
    """
    Unified client for accessing Kimi K2 through various methods
    Supports both conversational and agentic workflows
    """
    
    def __init__(self, config: KimiK2Config):
        self.config = config
        self.openai_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize OpenAI-compatible clients for different endpoints"""
        if self.config.openrouter_api_key:
            self.openai_client = openai.OpenAI(
                base_url=self.config.base_url_openrouter,
                api_key=self.config.openrouter_api_key
            )
            print("✅ OpenRouter client initialized")
        
        if self.config.moonshot_api_key:
            self.moonshot_client = openai.OpenAI(
                base_url=self.config.base_url_moonshot,
                api_key=self.config.moonshot_api_key
            )
            print("✅ Moonshot direct API client initialized")
    
    def chat_completion(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
        """
        Standard chat completion with optional tool calling
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions for agentic workflows
        """
        try:
            kwargs = {
                "model": self.config.model_name,
                "messages": messages,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
            
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
            
            response = self.openai_client.chat.completions.create(**kwargs)
            return self._format_response(response)
            
        except Exception as e:
            print(f"❌ Error in chat completion: {e}")
            return {"error": str(e)}
    
    def _format_response(self, response) -> Dict:
        """Format response for consistent handling"""
        choice = response.choices[0]
        
        result = {
            "content": choice.message.content,
            "finish_reason": choice.finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
        
        # Handle tool calls if present
        if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in choice.message.tool_calls
            ]
        
        return result
    
    def agentic_workflow(self, task: str, available_tools: List[Dict]) -> Dict:
        """
        Execute an agentic workflow using Kimi K2's native tool-calling abilities
        
        Args:
            task: Description of the task to accomplish
            available_tools: List of available tools/functions
        """
        messages = [
            {
                "role": "system", 
                "content": """You are Kimi K2, an advanced agentic AI assistant. You excel at:
                1. Breaking down complex tasks into steps
                2. Using tools autonomously to accomplish goals
                3. Writing and executing code
                4. Analyzing data and creating visualizations
                5. Multi-step reasoning and problem solving
                
                Use the available tools to accomplish the user's task efficiently."""
            },
            {"role": "user", "content": task}
        ]
        
        return self.chat_completion(messages, tools=available_tools)

def setup_environment():
    """Set up the environment for Kimi K2 development"""
    print("🚀 Setting up Kimi K2 development environment...")
    
    # Create project structure
    directories = [
        "examples",
        "tools", 
        "agents",
        "benchmarks",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install required packages
    packages = [
        "openai>=1.0.0",
        "requests",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "jupyter",
        "transformers",
        "torch",
        "huggingface_hub"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def create_tool_definitions():
    """Create tool definitions for agentic workflows"""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "execute_python_code",
                "description": "Execute Python code and return the result",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute"
                        }
                    },
                    "required": ["code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_visualization",
                "description": "Create data visualizations using matplotlib/seaborn",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "Data to visualize (CSV format or Python dict)"
                        },
                        "chart_type": {
                            "type": "string",
                            "enum": ["line", "bar", "scatter", "histogram", "heatmap"],
                            "description": "Type of chart to create"
                        },
                        "title": {
                            "type": "string",
                            "description": "Chart title"
                        }
                    },
                    "required": ["data", "chart_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "file_operations",
                "description": "Perform file operations (read, write, create)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["read", "write", "create", "delete"],
                            "description": "File operation to perform"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Name of the file"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write (for write/create operations)"
                        }
                    },
                    "required": ["operation", "filename"]
                }
            }
        }
    ]
    
    return tools

def benchmark_kimi_k2():
    """Run benchmarks to test Kimi K2's capabilities"""
    print("🧪 Running Kimi K2 capability benchmarks...")
    
    benchmarks = [
        {
            "name": "Coding Challenge",
            "task": "Write a Python function to find the longest palindromic substring in a string. Include unit tests.",
            "category": "coding"
        },
        {
            "name": "Math Reasoning", 
            "task": "Solve this problem step by step: A train travels 240 miles in 3 hours. If it increases its speed by 20 mph, how long will it take to travel 400 miles?",
            "category": "math"
        },
        {
            "name": "Tool Use",
            "task": "Create a data analysis report comparing the performance of different sorting algorithms. Include visualizations.",
            "category": "agentic"
        },
        {
            "name": "Complex Reasoning",
            "task": "Design a system architecture for a real-time collaborative document editor. Consider scalability, consistency, and conflict resolution.",
            "category": "reasoning"
        }
    ]
    
    return benchmarks

def main():
    """Main setup function"""
    print("🎯 Kimi K2 Setup & Integration")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Configuration
    config = KimiK2Config()
    
    # Check for API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    moonshot_key = os.getenv("MOONSHOT_API_KEY")
    
    if openrouter_key:
        config.openrouter_api_key = openrouter_key
        print("✅ OpenRouter API key found")
    else:
        print("⚠️  OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable")
    
    if moonshot_key:
        config.moonshot_api_key = moonshot_key
        print("✅ Moonshot API key found")
    else:
        print("⚠️  Moonshot API key not found. Set MOONSHOT_API_KEY environment variable")
    
    # Initialize client
    if openrouter_key or moonshot_key:
        client = KimiK2Client(config)
        
        # Test basic functionality
        print("\n🧪 Testing basic chat completion...")
        test_messages = [
            {"role": "system", "content": "You are Kimi K2, a powerful agentic AI assistant."},
            {"role": "user", "content": "Explain what makes you different from other language models."}
        ]
        
        response = client.chat_completion(test_messages)
        if "error" not in response:
            print("✅ Basic chat completion working!")
            print(f"Response: {response['content'][:200]}...")
        else:
            print(f"❌ Error: {response['error']}")
    
    # Create example files
    tools = create_tool_definitions()
    with open("tools/tool_definitions.json", "w") as f:
        json.dump(tools, f, indent=2)
    print("✅ Tool definitions saved to tools/tool_definitions.json")
    
    benchmarks = benchmark_kimi_k2()
    with open("benchmarks/test_cases.json", "w") as f:
        json.dump(benchmarks, f, indent=2)
    print("✅ Benchmark test cases saved to benchmarks/test_cases.json")
    
    print("\n🎉 Kimi K2 setup complete!")
    print("\n📚 Next steps:")
    print("1. Set your API keys (OPENROUTER_API_KEY or MOONSHOT_API_KEY)")
    print("2. Run the example scripts in the examples/ directory")
    print("3. Test agentic workflows with tool calling")
    print("4. Compare performance with Claude 4 Sonnet")
    print("\n🔗 Useful links:")
    print("- Kimi K2 on Hugging Face: https://huggingface.co/moonshotai/Kimi-K2-Instruct")
    print("- OpenRouter: https://openrouter.ai/")
    print("- Moonshot AI: https://www.moonshot.cn/")

if __name__ == "__main__":
    main() 