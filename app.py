import time
import csv
from datetime import datetime
from pathlib import Path

import os
import torch
import psutil
try:
    import GPUtil
except ImportError:
    GPUtil = None

import gradio as gr
from PIL import Image

import webbrowser
import threading

MODEL_NAME = "yolov5n"
LOG_PATH = Path("yolo_app/logs") / "perf_log.csv"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
APP_MODE = os.getenv("APP_MODE", "student").lower()

device = "cuda" if torch.cuda.is_available() else "cpu"

BASE_DIR = Path(__file__).resolve().parent
YOLOV5_DIR = BASE_DIR / "yolov5"
WEIGHTS = BASE_DIR / "weights" / "yolov5n.pt"

model = torch.hub.load(str(YOLOV5_DIR), "custom", path=str(WEIGHTS), source="local")
model.to(device)
model.eval()

# Hilfsfunktionen für Begrenzung der Bildgröße
def get_vram_mb():
    if not torch.cuda.is_available():
        return None
    props = torch.cuda.get_device_properties(0)
    return props.total_memory / (1024 * 1024)

def choose_max_side(vram_mb: float | None) -> int:
    if vram_mb is None:
        return 640
    if vram_mb < 4500:
        return 640
    if vram_mb < 7000:
        return 960
    return 1280

def resize_max_side(image: Image.Image, max_side: int) -> Image.Image:
    w, h = image.size
    m = max(w, h)
    if m <= max_side:
        return image
    scale = max_side / m
    new_w = int(w * scale)
    new_h = int(h * scale)
    return image.resize((new_w, new_h))

# Leistungsmetriken
def get_gpu_metrics():
    data = {
        "gpu_name": None,
        "gpu_load_pct": None,
        "gpu_temp_c": None,
        "gpu_mem_used_mb": None,
        "gpu_mem_total_mb": None,
    }
    if GPUtil is None:
        return data

    gpus = GPUtil.getGPUs()
    if not gpus:
        return data

    gpu = gpus[0]
    data.update({
        "gpu_name": gpu.name,
        "gpu_load_pct": round(gpu.load * 100, 1),
        "gpu_temp_c": gpu.temperature,
        "gpu_mem_used_mb": round(gpu.memoryUsed, 1),
        "gpu_mem_total_mb": round(gpu.memoryTotal, 1),
    })
    return data


def append_log_row(row: dict):
    write_header = not LOG_PATH.exists()

    fieldnames = list(row.keys())
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# Objekterkennung
def detect(image: Image.Image) -> Image.Image:
    if image is None:
        raise gr.Error("Bitte ein Bild hochladen.")

    vram_mb = get_vram_mb()
    max_side = choose_max_side(vram_mb)
    image = resize_max_side(image, max_side)


    ram = psutil.virtual_memory()
    ram_used_mb = (ram.total - ram.available) / (1024 * 1024)
    ram_total_mb = ram.total / (1024 * 1024)

    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()

    start = time.perf_counter()

    results = model(image)

    if device == "cuda":
        torch.cuda.synchronize()

    end = time.perf_counter()
    infer_ms = (end - start) * 1000

    rendered = results.render()[0]
    out_img = Image.fromarray(rendered)

    vram_peak_mb = None
    if device == "cuda":
        vram_peak_mb = torch.cuda.max_memory_allocated() / (1024 * 1024)

    gpu_metrics = get_gpu_metrics()

    log_row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device": device,
        "model": MODEL_NAME,
        "infer_ms": round(infer_ms, 2),
        "vram_peak_mb": round(vram_peak_mb, 1) if vram_peak_mb is not None else None,
        "ram_used_mb": round(ram_used_mb, 1),
        "ram_total_mb": round(ram_total_mb, 1),
        **gpu_metrics,
    }
    append_log_row(log_row)

    return out_img

# Interface mit Gradio
with gr.Blocks(title="Objekterkennung (YOLOv5)") as demo:
    gr.Markdown(
        """
# Objekterkennung (YOLOv5)
**So funktioniert's:** Bild hochladen → **Detect** → Ergebnis ansehen.

"""
    )

    with gr.Row():
        inp = gr.Image(type="pil", label="Eingabebild")
        out = gr.Image(type="pil", label="Ergebnis (Bounding Boxes)")

    btn = gr.Button("Detect")
    btn.click(fn=detect, inputs=inp, outputs=out)

    gr.Markdown("Hinweis: Bitte keine personenbezogenen Bilder verwenden, sofern keine Einwilligung vorliegt.")

def open_browser():
    webbrowser.open("http://127.0.0.1:7860")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=False, share=False, prevent_thread_lock=False)