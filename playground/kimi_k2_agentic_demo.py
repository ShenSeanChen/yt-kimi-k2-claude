#!/usr/bin/env python3
"""
Kimi K2 Agentic Capabilities Demo
Directory: /Users/shenseanchen/Desktop/Dev/claude-code/examples/

This script demonstrates Kimi K2's revolutionary agentic capabilities:
- Native tool calling and workflow orchestration
- Autonomous multi-step task execution
- Superior performance on agentic benchmarks (Tau2: 70.6%, AceBench: 76.5%)
- Real-world problem solving with minimal human oversight
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.kimi_k2_setup import KimiK2Client, KimiK2Config, create_tool_definitions
import json
import time
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, Any

class KimiK2AgenticDemo:
    """Demonstration of Kimi K2's agentic capabilities"""
    
    def __init__(self):
        self.config = KimiK2Config()
        # Try to get API key from environment
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("MOONSHOT_API_KEY")
        if api_key:
            self.config.openrouter_api_key = api_key
            self.client = KimiK2Client(self.config)
        else:
            print("⚠️  No API key found. Please set OPENROUTER_API_KEY or MOONSHOT_API_KEY")
            self.client = None
        
        self.tools = create_tool_definitions()
        self.tool_implementations = self._setup_tool_implementations()
    
    def _setup_tool_implementations(self) -> Dict[str, callable]:
        """Setup actual implementations for the tools"""
        return {
            "execute_python_code": self._execute_python_code,
            "create_visualization": self._create_visualization,
            "web_search": self._web_search,
            "file_operations": self._file_operations
        }
    
    def _execute_python_code(self, code: str) -> Dict[str, Any]:
        """Execute Python code safely"""
        try:
            # Create a restricted execution environment
            exec_globals = {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "range": range,
                    "sum": sum,
                    "max": max,
                    "min": min,
                    "abs": abs,
                    "round": round,
                    "sorted": sorted,
                    "list": list,
                    "dict": dict,
                    "str": str,
                    "int": int,
                    "float": float,
                },
                "numpy": np,
                "pandas": pd,
                "matplotlib": plt,
                "time": time,
                "os": os
            }
            exec_locals = {}
            
            # Capture output
            from io import StringIO
            import contextlib
            
            output_buffer = StringIO()
            with contextlib.redirect_stdout(output_buffer):
                exec(code, exec_globals, exec_locals)
            
            output = output_buffer.getvalue()
            
            return {
                "success": True,
                "output": output,
                "locals": {k: str(v) for k, v in exec_locals.items() if not k.startswith('_')}
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_visualization(self, data: str, chart_type: str, title: str = "") -> Dict[str, Any]:
        """Create data visualizations"""
        try:
            # Parse data (assuming CSV format or JSON)
            if data.startswith('[') or data.startswith('{'):
                # JSON format
                import json
                data_obj = json.loads(data)
                df = pd.DataFrame(data_obj)
            else:
                # CSV format
                from io import StringIO
                df = pd.read_csv(StringIO(data))
            
            plt.figure(figsize=(10, 6))
            
            if chart_type == "line":
                df.plot(kind='line')
            elif chart_type == "bar":
                df.plot(kind='bar')
            elif chart_type == "scatter":
                if len(df.columns) >= 2:
                    plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
            elif chart_type == "histogram":
                df.hist()
            elif chart_type == "heatmap":
                import seaborn as sns
                sns.heatmap(df.corr(), annot=True)
            
            if title:
                plt.title(title)
            
            # Save plot
            os.makedirs("visualizations", exist_ok=True)
            filename = f"visualizations/chart_{int(time.time())}.png"
            plt.savefig(filename)
            plt.close()
            
            return {
                "success": True,
                "filename": filename,
                "message": f"Chart saved as {filename}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Simulate web search (in real implementation, use actual search API)"""
        # This is a mock implementation
        # In production, you'd use Google Search API, Bing API, etc.
        return {
            "success": True,
            "results": [
                {
                    "title": f"Search result {i+1} for '{query}'",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"This is a mock search result snippet for query: {query}"
                }
                for i in range(num_results)
            ]
        }
    
    def _file_operations(self, operation: str, filename: str, content: str = "") -> Dict[str, Any]:
        """Perform file operations"""
        try:
            if operation == "read":
                with open(filename, 'r') as f:
                    content = f.read()
                return {"success": True, "content": content}
            
            elif operation == "write" or operation == "create":
                with open(filename, 'w') as f:
                    f.write(content)
                return {"success": True, "message": f"File {filename} {'created' if operation == 'create' else 'written'}"}
            
            elif operation == "delete":
                os.remove(filename)
                return {"success": True, "message": f"File {filename} deleted"}
            
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_data_analysis_workflow(self):
        """Test autonomous data analysis workflow"""
        print("📊 Testing Data Analysis Workflow...")
        
        task = """
        I need you to perform a comprehensive data analysis on algorithm performance. Here's what I want:
        
        1. Generate sample performance data for 5 sorting algorithms (Bubble, Quick, Merge, Heap, Radix)
        2. Create datasets with different input sizes (100, 1000, 10000, 100000 elements)
        3. Simulate execution times with realistic complexity patterns
        4. Create multiple visualizations:
           - Line plot showing performance vs input size
           - Bar chart comparing algorithms at largest input size
           - Heatmap showing relative performance
        5. Calculate and display statistical analysis (mean, std, efficiency ratios)
        6. Generate a summary report with recommendations
        
        Use the available tools to accomplish this entire workflow autonomously.
        """
        
        return self._execute_agentic_workflow("Data Analysis Workflow", task)
    
    def test_web_research_workflow(self):
        """Test autonomous web research and synthesis"""
        print("🔍 Testing Web Research Workflow...")
        
        task = """
        Research and analyze the current state of large language models. I need:
        
        1. Search for recent developments in LLM architectures
        2. Find information about performance benchmarks
        3. Research cost and efficiency comparisons
        4. Look up open-source vs proprietary model trends
        5. Compile findings into a structured report
        6. Create visualizations showing model comparison data
        7. Save the complete analysis to a markdown file
        
        Be thorough and autonomous in your research approach.
        """
        
        return self._execute_agentic_workflow("Web Research Workflow", task)
    
    def test_code_project_workflow(self):
        """Test autonomous code project creation"""
        print("💻 Testing Code Project Workflow...")
        
        task = """
        Create a complete Python project for a task management system:
        
        1. Design the project structure and architecture
        2. Implement core classes (Task, Project, User, TaskManager)
        3. Add data persistence (JSON-based storage)
        4. Create a CLI interface for task operations
        5. Write comprehensive unit tests
        6. Generate documentation (README, API docs)
        7. Create example usage scenarios
        8. Set up project configuration files (requirements.txt, setup.py)
        
        Make this a production-ready project with proper error handling and logging.
        """
        
        return self._execute_agentic_workflow("Code Project Workflow", task)
    
    def test_multi_step_analysis(self):
        """Test complex multi-step analysis task"""
        print("🧮 Testing Multi-Step Analysis...")
        
        task = """
        Perform a comprehensive analysis of programming language popularity trends:
        
        1. Create synthetic data representing GitHub repository counts, job postings, 
           and developer survey results for 10 programming languages over 5 years
        2. Implement statistical analysis including:
           - Trend analysis (growth rates, correlations)
           - Seasonal patterns detection
           - Predictive modeling for future trends
        3. Create an interactive dashboard with multiple visualizations
        4. Generate insights and recommendations
        5. Export results in multiple formats (CSV, JSON, PDF report)
        6. Create a presentation summary with key findings
        
        This should demonstrate sophisticated data science workflow automation.
        """
        
        return self._execute_agentic_workflow("Multi-Step Analysis", task)
    
    def test_problem_solving_workflow(self):
        """Test autonomous problem-solving capabilities"""
        print("🧠 Testing Problem Solving Workflow...")
        
        task = """
        Solve this complex optimization problem autonomously:
        
        **Problem**: Design an optimal delivery route system for a food delivery service
        
        Requirements:
        1. Generate a realistic city map with restaurants and delivery addresses
        2. Implement multiple routing algorithms (Dijkstra, A*, Genetic Algorithm)
        3. Consider real-world constraints:
           - Traffic patterns by time of day
           - Driver capacity limits
           - Food temperature constraints (max delivery time)
           - Fuel costs and vehicle efficiency
        4. Create visualizations showing:
           - Route optimization comparisons
           - Performance metrics over time
           - Cost analysis
        5. Run simulations and generate performance reports
        6. Provide recommendations for the optimal solution
        
        This tests your ability to break down complex problems and solve them systematically.
        """
        
        return self._execute_agentic_workflow("Problem Solving Workflow", task)
    
    def _execute_agentic_workflow(self, workflow_name: str, task: str) -> Dict:
        """Execute an agentic workflow with tool calling"""
        if not self.client:
            return {"error": "No API client available"}
        
        print(f"\n🤖 Executing: {workflow_name}")
        print("-" * 60)
        
        start_time = time.time()
        
        # Initial request with tools available
        response = self.client.agentic_workflow(task, self.tools)
        
        # Handle tool calls iteratively
        conversation_history = [
            {
                "role": "system", 
                "content": """You are Kimi K2, an advanced agentic AI with exceptional tool-use capabilities:
                - Tau2 retail benchmark: 70.6% (competitive with Claude Sonnet 4: 75.0%)
                - AceBench: 76.5% (competitive with top models)
                
                You excel at autonomous multi-step workflows. Break down complex tasks,
                use tools strategically, and execute comprehensive solutions."""
            },
            {"role": "user", "content": task}
        ]
        
        max_iterations = 10
        iteration = 0
        
        while "tool_calls" in response and iteration < max_iterations:
            iteration += 1
            print(f"🔧 Tool call iteration {iteration}")
            
            # Add assistant's response to conversation
            conversation_history.append({
                "role": "assistant",
                "content": response.get("content", ""),
                "tool_calls": response.get("tool_calls", [])
            })
            
            # Execute tool calls
            for tool_call in response.get("tool_calls", []):
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                
                print(f"  🛠️  Calling {tool_name} with args: {list(tool_args.keys())}")
                
                # Execute the tool
                if tool_name in self.tool_implementations:
                    tool_result = self.tool_implementations[tool_name](**tool_args)
                else:
                    tool_result = {"error": f"Tool {tool_name} not implemented"}
                
                # Add tool result to conversation
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(tool_result)
                })
            
            # Get next response
            response = self.client.chat_completion(conversation_history, self.tools)
        
        execution_time = time.time() - start_time
        
        result = {
            "workflow": workflow_name,
            "execution_time": execution_time,
            "iterations": iteration,
            "final_response": response,
            "conversation_history": conversation_history,
            "success": "error" not in response
        }
        
        if result["success"]:
            print(f"✅ {workflow_name} completed in {execution_time:.2f}s ({iteration} tool iterations)")
            
            # Save workflow results
            os.makedirs("agentic_outputs", exist_ok=True)
            output_file = f"agentic_outputs/{workflow_name.lower().replace(' ', '_')}_workflow.json"
            
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"💾 Workflow saved to: {output_file}")
        else:
            print(f"❌ {workflow_name} failed: {response.get('error', 'Unknown error')}")
        
        return result
    
    def run_agentic_demo(self):
        """Run comprehensive agentic capabilities demo"""
        print("🚀 Kimi K2 Agentic Capabilities Demo")
        print("=" * 60)
        print("Testing state-of-the-art agentic performance...")
        print("Expected performance based on benchmarks:")
        print("- Tau2 retail: 70.6% (vs Claude Sonnet 4: 75.0%)")
        print("- AceBench: 76.5% (vs Claude Sonnet 4: 76.2%)")
        print("- Native tool calling and workflow orchestration")
        print("=" * 60)
        
        if not self.client:
            print("❌ Cannot run demo without API access")
            return
        
        # Run all agentic tests
        workflows = [
            self.test_data_analysis_workflow,
            self.test_web_research_workflow,
            self.test_code_project_workflow,
            self.test_multi_step_analysis,
            self.test_problem_solving_workflow
        ]
        
        results = []
        total_start_time = time.time()
        
        for workflow in workflows:
            try:
                result = workflow()
                results.append(result)
                print("\n" + "="*40 + "\n")
            except Exception as e:
                print(f"❌ Workflow failed with exception: {e}")
                results.append({"error": str(e), "success": False})
        
        total_time = time.time() - total_start_time
        
        # Generate summary report
        self._generate_agentic_summary(results, total_time)
    
    def _generate_agentic_summary(self, results: list, total_time: float):
        """Generate comprehensive agentic capabilities summary"""
        print("\n🎯 KIMI K2 AGENTIC DEMO SUMMARY")
        print("=" * 60)
        
        successful_workflows = [r for r in results if r.get("success", False)]
        failed_workflows = [r for r in results if not r.get("success", False)]
        
        print(f"✅ Successful workflows: {len(successful_workflows)}/{len(results)}")
        print(f"❌ Failed workflows: {len(failed_workflows)}")
        print(f"⏱️  Total execution time: {total_time:.2f}s")
        
        if successful_workflows:
            avg_time = sum(r["execution_time"] for r in successful_workflows) / len(successful_workflows)
            total_iterations = sum(r.get("iterations", 0) for r in successful_workflows)
            avg_iterations = total_iterations / len(successful_workflows)
            
            print(f"📊 Average workflow time: {avg_time:.2f}s")
            print(f"🔧 Total tool iterations: {total_iterations}")
            print(f"🔄 Average iterations per workflow: {avg_iterations:.1f}")
        
        print("\n📈 Workflow Performance:")
        for result in results:
            status = "✅" if result.get("success", False) else "❌"
            workflow = result.get("workflow", "Unknown")
            time_taken = result.get("execution_time", 0)
            iterations = result.get("iterations", 0)
            print(f"{status} {workflow}: {time_taken:.2f}s ({iterations} iterations)")
        
        # Save comprehensive report
        report = {
            "summary": {
                "total_workflows": len(results),
                "successful_workflows": len(successful_workflows),
                "failed_workflows": len(failed_workflows),
                "total_time": total_time,
                "average_time": avg_time if successful_workflows else 0,
                "total_tool_iterations": total_iterations if successful_workflows else 0,
                "average_iterations": avg_iterations if successful_workflows else 0
            },
            "benchmark_comparison": {
                "tau2_retail_expected": "70.6%",
                "acebench_expected": "76.5%",
                "claude_sonnet_4_tau2": "75.0%",
                "claude_sonnet_4_acebench": "76.2%"
            },
            "results": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs("reports", exist_ok=True)
        report_file = f"reports/kimi_k2_agentic_demo_{int(time.time())}.json"
        
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
        print("\n🎉 Agentic demo complete! Check agentic_outputs/ for workflow results.")

def main():
    """Main execution function"""
    demo = KimiK2AgenticDemo()
    demo.run_agentic_demo()

if __name__ == "__main__":
    main() 