import sys
import torch
from diffusers import FluxPipeline

# To be safe, install via:
# uv sync --index-strategy unsafe-best-match

# Tested with GPU: RTX 5070. CUDA 13
#
# note: you need to log in to Hugging Face and have access to the model to run this code.
# (get token from: https://huggingface.co/settings/tokens)
# uv add huggingface_hub --index-strategy unsafe-best-match
# uv run hf auth login
# - you can say 'y' to git credentials, as it may help pull/push models later
# - make sure it has at least “read” permissions
# - check with: uv run hf auth whoami
if torch.cuda.is_available():
    print(f"[CUDA] Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
    torch.cuda.empty_cache()
    print("[CUDA] Cache cleared")
# Determine device and load model
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.float16)  # float32 segfaults on load (too large); float16 halves memory vs float32.
pipe.enable_sequential_cpu_offload()  # More aggressive than enable_model_cpu_offload: moves each submodel to CPU after use, minimising peak VRAM.

print(f"[Device] CUDA available: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")

if len(sys.argv) < 2:
    print("Usage: python generate_via_local_2.py <prompt>")
    sys.exit(1)

prompt = sys.argv[1]
print(f"[Prompt] {prompt}")
image = pipe(
    prompt,
    height=512,
    width=512,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cuda" if torch.cuda.is_available() else "cpu").manual_seed(0)  # Seed RNG on target device; this does not force the denoising model to run on CPU.
).images[0]

# Save the image
output_path = "output/local_gpu_output.png"
print(f"Saving image to {output_path}")
image.save(output_path)
