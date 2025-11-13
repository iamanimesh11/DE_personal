import subprocess
import platform
import psutil
import json
import shutil

def check_ollama_server():
    """Check if Ollama server is running"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, result.stdout
    except Exception as e:
        return False, str(e)


def get_gpu_info():
    """Check GPU and VRAM"""
    gpu_info = {"gpu": None, "vram_gb": 0}

    # NVIDIA GPU check
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.check_output(["nvidia-smi", "--query-gpu=gpu_name,memory.total",
                                              "--format=csv,noheader,nounits"])
            name, mem = result.decode().strip().split(",")
            gpu_info["gpu"] = name.strip()
            gpu_info["vram_gb"] = int(mem.strip())
            return gpu_info
        except:
            pass

    # Windows WMI fallback for integrated GPUs (Intel/AMD)
    try:
        import wmi
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            name = gpu.Name
            if name:
                gpu_info["gpu"] = name
                if gpu.AdapterRAM:
                    gpu_info["vram_gb"] = round(gpu.AdapterRAM / (1024**3))
                return gpu_info
    except:
        pass

    return gpu_info


def choose_model(ram_gb, vram_gb):
    """Select best-fitting model based on available memory"""
    # MODEL DECISION LOGIC
    if ram_gb <= 6:
        return "llama3.2:1b", "Very low RAM detected. Using 1B which never OOMs."
    if ram_gb <= 10:
        return "llama3.2:3b", "Moderate RAM. 3B is safe & fast."
    
    # For high RAM systems
    if vram_gb >= 6:
        return "mistral:7b-instruct-q4_K_M", "Your GPU can offload 7B safely."
    if ram_gb >= 16:
        return "mistral:7b-instruct-q4_K_M", "Enough RAM for 7B even without GPU."

    return "llama3.2:3b", "Fallback to 3B to avoid OOM."


def main():
    print("\n🔍 **Ollama Diagnostic Tool (Windows)**\n")

    # 1. OS
    print(f"🖥️ OS: {platform.system()} {platform.release()}")

    # 2. RAM
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    print(f"💾 System RAM Detected: {ram_gb:.2f} GB")

    # 3. GPU
    gpu = get_gpu_info()
    print(f"🎮 GPU: {gpu['gpu'] or 'No GPU detected'}")
    print(f"📦 VRAM: {gpu['vram_gb']} GB")

    # 4. Ollama service
    running, details = check_ollama_server()
    if running:
        print("🟢 Ollama is running.")
    else:
        print("🔴 Ollama is NOT running!")
        print(details)
        print("\nFix: Start Ollama Desktop or run `ollama serve`.")
        return

    # 5. Pick best model
    model, reason = choose_model(ram_gb, gpu["vram_gb"])
    print(f"\n🤖 Recommended Model: **{model}**")
    print(f"📌 Reason: {reason}")

    # 6. Additional warnings
    if ram_gb < 8:
        print("\n⚠️ Warning: Low RAM — avoid 7B models to prevent crashes.")
    if gpu["gpu"] is None:
        print("⚠️ No GPU detected — all models will run on CPU only (slower).")
    if gpu["gpu"] and gpu["vram_gb"] < 6:
        print("⚠️ Low VRAM — Ollama may not be able to offload 7B models to GPU.")

    # 7. Show helpful environment suggestions
    print("\n🔧 Recommended Environment Variables for Windows:")
    print("  OLLAMA_FLASH_ATTENTION=1")
    print("  OLLAMA_KV_CACHE_TYPE=q8_0")
    print("  OLLAMA_MAX_LOADED_MODELS=1")
    print("  OLLAMA_NUM_PARALLEL=1")
    print("  OLLAMA_KEEP_ALIVE=0")

    print("\n✅ Diagnostic complete.\n")


if __name__ == "__main__":
    main()