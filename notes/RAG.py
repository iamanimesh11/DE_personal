import subprocess
import time
import psutil
import json
import platform

# ----------------------------------------
# CONFIG: Models to benchmark
# ----------------------------------------
MODELS = [
    "llama3.2:1b",
    "llama3.2:3b",
    "mistral:7b-instruct-q4_K_M"
]

TEST_PROMPT = "Explain what a computer is in one short sentence."


def get_ram_gb():
    return psutil.virtual_memory().available / (1024 ** 3)


def run_ollama(model, prompt):
    """Run Ollama using `ollama run <model>`."""
    try:
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send prompt
        output, err = process.communicate(prompt, timeout=60)
        return output, err

    except subprocess.TimeoutExpired:
        process.kill()
        return None, "Timeout"


def benchmark_model(model_name):
    print(f"\n🔍 Benchmarking: {model_name}")
    result = {
        "model": model_name,
        "load_time_sec": None,
        "inference_time_sec": None,
        "tokens_per_sec": None,
        "ram_before_gb": None,
        "ram_after_gb": None,
        "status": "OK"
    }

    # RAM before
    ram_before = get_ram_gb()
    result["ram_before_gb"] = round(ram_before, 2)

    # --------------------------
    # Measure load + inference
    # --------------------------
    start_time = time.time()
    output, err = run_ollama(model_name, TEST_PROMPT)
    end_time = time.time()

    if output is None:
        result["status"] = f"Failed: {err}"
        return result

    total_time = end_time - start_time
    result["inference_time_sec"] = round(total_time, 2)

    # Simple token count (approx)
    tokens = len(output.split())
    if total_time > 0:
        result["tokens_per_sec"] = round(tokens / total_time, 2)

    # RAM after
    ram_after = get_ram_gb()
    result["ram_after_gb"] = round(ram_after, 2)

    # When model loads, inference time ~ load time + response
    if total_time > 0:
        result["load_time_sec"] = round(total_time * 0.40, 2)  # approx

    return result


def main():
    print("\n🚀 OLLAMA BENCHMARK TOOL (Windows)\n")
    print(f"🖥️ OS: {platform.system()} {platform.release()}")

    overall_ram = psutil.virtual_memory().total / (1024 ** 3)
    print(f"💾 Total RAM: {overall_ram:.2f} GB")

    benchmark_results = []

    for model in MODELS:
        res = benchmark_model(model)
        benchmark_results.append(res)

    # ----------------------------------------
    # Print Summary
    ----------------------------------------
    print("\n=================================")
    print("📊 BENCHMARK RESULTS SUMMARY")
    print("=================================")

    for r in benchmark_results:
        print(f"\nModel: {r['model']}")
        print(f"  Status: {r['status']}")
        print(f"  RAM Before: {r['ram_before_gb']} GB")
        print(f"  RAM After: {r['ram_after_gb']} GB")
        print(f"  Load Time (est): {r['load_time_sec']} sec")
        print(f"  Inference Time: {r['inference_time_sec']} sec")
        print(f"  Tokens/sec: {r['tokens_per_sec']}")

    # Save JSON summary
    with open("ollama_benchmark_results.json", "w") as f:
        json.dump(benchmark_results, f, indent=4)

    print("\n💾 JSON saved → ollama_benchmark_results.json")
    print("\n✅ Benchmark complete!\n")


if __name__ == "__main__":
    main()