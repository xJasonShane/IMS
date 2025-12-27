import asyncio
import httpx
import time
from typing import List, Dict, Any

# 测试配置
BASE_URL = "http://localhost:8000/api/v1"
NUM_REQUESTS = 100  # 总请求数
CONCURRENCY = 10  # 并发请求数

# 测试函数
async def test_api_endpoint(client: httpx.AsyncClient, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> float:
    """测试单个API端点的响应时间"""
    start_time = time.time()
    try:
        if method == "GET":
            response = await client.get(endpoint)
        elif method == "POST":
            response = await client.post(endpoint, json=data)
        elif method == "PUT":
            response = await client.put(endpoint, json=data)
        elif method == "DELETE":
            response = await client.delete(endpoint)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # 确保请求成功
        response.raise_for_status()
        
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")
        return float("inf")

async def run_concurrent_tests(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> List[float]:
    """运行并发测试"""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 创建测试任务
        tasks = [
            test_api_endpoint(client, endpoint, method, data)
            for _ in range(NUM_REQUESTS)
        ]
        
        # 并发执行任务
        results = await asyncio.gather(*tasks)
        return results

async def main():
    """主测试函数"""
    print(f"开始性能测试，共发送 {NUM_REQUESTS} 个请求，并发数 {CONCURRENCY}")
    print("=" * 60)
    
    # 测试端点列表
    test_endpoints = [
        ("/users", "GET"),
    ]
    
    for endpoint, method in test_endpoints:
        print(f"测试 {method} {endpoint}...")
        
        # 运行测试
        results = await run_concurrent_tests(endpoint, method)
        
        # 计算统计信息
        valid_results = [r for r in results if r != float("inf")]
        if not valid_results:
            print("  所有请求都失败了")
            continue
        
        min_time = min(valid_results)
        max_time = max(valid_results)
        avg_time = sum(valid_results) / len(valid_results)
        p95_time = sorted(valid_results)[int(len(valid_results) * 0.95)]
        p99_time = sorted(valid_results)[int(len(valid_results) * 0.99)]
        success_rate = len(valid_results) / len(results) * 100
        
        # 打印结果
        print(f"  请求总数: {NUM_REQUESTS}")
        print(f"  成功请求: {len(valid_results)}")
        print(f"  成功率: {success_rate:.2f}%")
        print(f"  最小响应时间: {min_time:.4f}s")
        print(f"  最大响应时间: {max_time:.4f}s")
        print(f"  平均响应时间: {avg_time:.4f}s")
        print(f"  95% 响应时间: {p95_time:.4f}s")
        print(f"  99% 响应时间: {p99_time:.4f}s")
        print(f"  吞吐量: {NUM_REQUESTS / sum(valid_results):.2f} 请求/秒")
        print()
    
    print("性能测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
