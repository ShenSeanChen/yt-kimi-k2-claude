#!/usr/bin/env python3
"""
Kimi K2 Coding Capabilities Demo
Directory: /Users/shenseanchen/Desktop/Dev/claude-code/examples/

This script demonstrates Kimi K2's exceptional coding abilities:
- LiveCodeBench performance: 53.7% (beats GPT-4.1's 44.7%)
- SWE-bench Verified: 65.8% (competitive with top models)
- Complex algorithmic problem solving
- Code generation, debugging, and optimization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.kimi_k2_setup import KimiK2Client, KimiK2Config
import json
import time

class KimiK2CodingDemo:
    """Demonstration of Kimi K2's coding capabilities"""
    
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
    
    def test_algorithm_implementation(self):
        """Test complex algorithm implementation"""
        print("🧮 Testing Algorithm Implementation...")
        
        prompt = """
        Implement a highly optimized solution for the following problem:
        
        **Problem**: Given a string, find the longest palindromic substring.
        
        Requirements:
        1. Implement using Manacher's algorithm for O(n) time complexity
        2. Include comprehensive unit tests
        3. Add detailed comments explaining the algorithm
        4. Handle edge cases (empty string, single character, etc.)
        5. Provide time and space complexity analysis
        
        Make this production-ready code with proper error handling.
        """
        
        return self._execute_coding_task("Algorithm Implementation", prompt)
    
    def test_data_structures(self):
        """Test advanced data structure implementation"""
        print("🏗️  Testing Data Structure Implementation...")
        
        prompt = """
        Implement a thread-safe LRU (Least Recently Used) Cache with the following features:
        
        1. Generic type support (works with any key-value types)
        2. Thread-safe operations using appropriate locking mechanisms
        3. O(1) get and put operations
        4. Configurable maximum capacity
        5. Optional TTL (Time To Live) for cache entries
        6. Statistics tracking (hit rate, miss rate, etc.)
        7. Comprehensive unit tests with concurrent access scenarios
        
        Include proper documentation and usage examples.
        """
        
        return self._execute_coding_task("Data Structure Implementation", prompt)
    
    def test_system_design_coding(self):
        """Test system design implementation"""
        print("🏛️  Testing System Design Implementation...")
        
        prompt = """
        Design and implement a distributed rate limiter system with the following requirements:
        
        1. Support multiple rate limiting algorithms (Token Bucket, Sliding Window)
        2. Distributed architecture using Redis for shared state
        3. Configurable rate limits per user/IP/API key
        4. Graceful degradation when Redis is unavailable
        5. Monitoring and metrics collection
        6. REST API endpoints for configuration
        7. Docker containerization
        8. Unit and integration tests
        
        Provide a complete implementation with:
        - Main application code
        - Configuration management
        - Docker files
        - API documentation
        - Performance benchmarks
        """
        
        return self._execute_coding_task("System Design Implementation", prompt)
    
    def test_debugging_skills(self):
        """Test debugging and code analysis skills"""
        print("🐛 Testing Debugging Skills...")
        
        buggy_code = '''
        def binary_search(arr, target):
            left, right = 0, len(arr)
            
            while left < right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    return mid
                elif arr[mid] < target:
                    left = mid
                else:
                    right = mid - 1
            
            return -1
        
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            
            pivot = arr[0]
            less = [x for x in arr[1:] if x <= pivot]
            greater = [x for x in arr[1:] if x > pivot]
            
            return quicksort(less) + [pivot] + quicksort(greater)
        
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        '''
        
        prompt = f"""
        Analyze the following code and identify all bugs, inefficiencies, and potential issues:
        
        ```python
        {buggy_code}
        ```
        
        For each function:
        1. Identify specific bugs and explain why they're problematic
        2. Provide corrected versions
        3. Suggest optimizations
        4. Add proper error handling
        5. Include unit tests for the corrected versions
        6. Analyze time/space complexity before and after fixes
        
        Be thorough and explain your reasoning for each change.
        """
        
        return self._execute_coding_task("Code Debugging", prompt)
    
    def test_competitive_programming(self):
        """Test competitive programming problem solving"""
        print("🏆 Testing Competitive Programming...")
        
        prompt = """
        Solve this competitive programming problem efficiently:
        
        **Problem**: Maximum Subarray Sum with At Most K Deletions
        
        Given an array of integers and an integer k, you can delete at most k elements 
        from the array. Find the maximum possible sum of a contiguous subarray after 
        performing the deletions optimally.
        
        Constraints:
        - 1 ≤ n ≤ 10^5
        - 1 ≤ k ≤ min(n, 100)
        - -10^9 ≤ arr[i] ≤ 10^9
        
        Requirements:
        1. Implement an efficient solution (consider DP approaches)
        2. Analyze time and space complexity
        3. Handle edge cases
        4. Provide multiple test cases
        5. Explain the algorithm strategy
        
        Example:
        arr = [-1, 3, -2, 4, -5], k = 2
        Output: 7 (delete -1 and -5, subarray [3, -2, 4] becomes [3, 4] = 7)
        """
        
        return self._execute_coding_task("Competitive Programming", prompt)
    
    def test_ml_implementation(self):
        """Test machine learning algorithm implementation"""
        print("🤖 Testing ML Implementation...")
        
        prompt = """
        Implement a neural network from scratch with the following specifications:
        
        1. **Architecture**: Multi-layer perceptron with configurable layers
        2. **Features**:
           - Forward propagation
           - Backpropagation with gradient descent
           - Support for different activation functions (ReLU, Sigmoid, Tanh)
           - Batch processing
           - Learning rate scheduling
           - Regularization (L1, L2)
           - Early stopping
        
        3. **Implementation Requirements**:
           - Use only NumPy (no ML frameworks)
           - Vectorized operations for efficiency
           - Proper weight initialization (Xavier/He)
           - Gradient checking for verification
           - Comprehensive logging and visualization
        
        4. **Testing**:
           - Train on a simple dataset (XOR or Iris)
           - Plot training/validation curves
           - Compare with sklearn implementation
           - Unit tests for each component
        
        Make it educational but production-quality code.
        """
        
        return self._execute_coding_task("ML Implementation", prompt)
    
    def _execute_coding_task(self, task_name: str, prompt: str) -> dict:
        """Execute a coding task and return results"""
        if not self.client:
            return {"error": "No API client available"}
        
        print(f"\n📝 Executing: {task_name}")
        print("-" * 60)
        
        start_time = time.time()
        
        messages = [
            {
                "role": "system", 
                "content": """You are Kimi K2, an exceptional coding AI with state-of-the-art performance:
                - LiveCodeBench: 53.7% (beats GPT-4.1's 44.7%)
                - SWE-bench Verified: 65.8% (competitive with Claude Sonnet 4)
                - Expert in algorithms, data structures, system design, and debugging
                
                Provide complete, production-ready code with:
                1. Clean, well-commented implementation
                2. Comprehensive error handling
                3. Unit tests
                4. Performance analysis
                5. Clear explanations of your approach
                
                Focus on correctness, efficiency, and maintainability."""
            },
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat_completion(messages)
        execution_time = time.time() - start_time
        
        result = {
            "task": task_name,
            "execution_time": execution_time,
            "response": response,
            "success": "error" not in response
        }
        
        if result["success"]:
            print(f"✅ {task_name} completed in {execution_time:.2f}s")
            print(f"📊 Tokens used: {response.get('usage', {}).get('total_tokens', 'N/A')}")
            
            # Save the response for analysis
            output_file = f"outputs/{task_name.lower().replace(' ', '_')}_output.md"
            os.makedirs("outputs", exist_ok=True)
            
            with open(output_file, "w") as f:
                f.write(f"# {task_name}\n\n")
                f.write(f"**Execution Time**: {execution_time:.2f}s\n")
                f.write(f"**Tokens Used**: {response.get('usage', {}).get('total_tokens', 'N/A')}\n\n")
                f.write("## Response\n\n")
                f.write(response.get('content', 'No content'))
            
            print(f"💾 Output saved to: {output_file}")
        else:
            print(f"❌ {task_name} failed: {response.get('error', 'Unknown error')}")
        
        return result
    
    def run_comprehensive_demo(self):
        """Run all coding demonstrations"""
        print("🚀 Kimi K2 Comprehensive Coding Demo")
        print("=" * 60)
        print("Testing state-of-the-art coding capabilities...")
        print("Expected performance based on benchmarks:")
        print("- LiveCodeBench v6: 53.7% (vs GPT-4.1: 44.7%)")
        print("- SWE-bench Verified: 65.8% (vs GPT-4.1: 54.6%)")
        print("=" * 60)
        
        if not self.client:
            print("❌ Cannot run demo without API access")
            return
        
        # Run all tests
        tests = [
            self.test_algorithm_implementation,
            self.test_data_structures,
            self.test_debugging_skills,
            self.test_competitive_programming,
            self.test_ml_implementation,
            self.test_system_design_coding
        ]
        
        results = []
        total_start_time = time.time()
        
        for test in tests:
            try:
                result = test()
                results.append(result)
                print("\n" + "="*40 + "\n")
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results.append({"error": str(e), "success": False})
        
        total_time = time.time() - total_start_time
        
        # Generate summary report
        self._generate_summary_report(results, total_time)
    
    def _generate_summary_report(self, results: list, total_time: float):
        """Generate a comprehensive summary report"""
        print("\n🎯 KIMI K2 CODING DEMO SUMMARY")
        print("=" * 60)
        
        successful_tests = [r for r in results if r.get("success", False)]
        failed_tests = [r for r in results if not r.get("success", False)]
        
        print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
        print(f"❌ Failed tests: {len(failed_tests)}")
        print(f"⏱️  Total execution time: {total_time:.2f}s")
        
        if successful_tests:
            avg_time = sum(r["execution_time"] for r in successful_tests) / len(successful_tests)
            print(f"📊 Average response time: {avg_time:.2f}s")
        
        print("\n📈 Performance Analysis:")
        for result in results:
            status = "✅" if result.get("success", False) else "❌"
            task = result.get("task", "Unknown")
            time_taken = result.get("execution_time", 0)
            print(f"{status} {task}: {time_taken:.2f}s")
        
        # Save detailed report
        report = {
            "summary": {
                "total_tests": len(results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "total_time": total_time,
                "average_time": avg_time if successful_tests else 0
            },
            "results": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs("reports", exist_ok=True)
        report_file = f"reports/kimi_k2_coding_demo_{int(time.time())}.json"
        
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
        print("\n🎉 Demo complete! Check the outputs/ directory for detailed responses.")

def main():
    """Main execution function"""
    demo = KimiK2CodingDemo()
    demo.run_comprehensive_demo()

if __name__ == "__main__":
    main() 