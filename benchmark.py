import time
import requests

def run_benchmark():
    url = "http://localhost:8000/api/v1/verify/bidder/bidder-delta-004/tender/tender-sih-2026"
    iterations = 50
    latencies = []

    print(f"Running latency benchmark on {url} for {iterations} iterations...")
    
    for i in range(iterations):
        start_time = time.perf_counter()
        response = requests.post(url)
        end_time = time.perf_counter()
        
        if response.status_code == 200:
            latencies.append((end_time - start_time) * 1000) # Convert to ms
        else:
            print(f"Request failed on iteration {i}")
            
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        
        print("\n--- BENCHMARK RESULTS ---")
        print(f"Average Latency: {avg_latency:.2f} ms")
        print(f"Min Latency: {min_latency:.2f} ms")
        print(f"Max Latency: {max_latency:.2f} ms")
        print("-------------------------")
        print("SRD Target: < 1000ms")
        print(f"Pass: {avg_latency < 1000}")

if __name__ == "__main__":
    run_benchmark()
