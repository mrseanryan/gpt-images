import torch
from diffusers import FluxPipeline

# note: you need to log in to Hugging Face and have access to the model to run this code.
# (get token from: https://huggingface.co/settings/tokens)
# uv add huggingface_hub --index-strategy unsafe-best-match
# uv run hf auth login
# - you can say 'y' to git credentials, as it may help pull/push models later
# - make sure it has at least “read” permissions
# - check with: uv run hf auth whoami

pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()  # Keep peak VRAM lower by moving model chunks to CPU between steps; this increases CPU usage by design.

prompt = "a dark sci-fi corridor, space hulk style, cinematic lighting"
image = pipe(
    prompt,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cpu").manual_seed(0)  # Seed RNG on CPU for reproducible results; this does not force the denoising model to run on CPU.
).images[0]
# Save the image
output_path = "output/local_gpu_output.png"
print(f"Saving image to {output_path}")
image.save(output_path)
