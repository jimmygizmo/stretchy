
import os
from flask import Flask, request, jsonify
from diffusers import StableDiffusionPipeline
import torch

app = Flask(__name__)


model_path = "/app/models/v2-1_768-ema-pruned.safetensors"

# pipe = StableDiffusionPipeline.from_pretrained(
#         model_path,
#         use_auth_token=False
#     ).to("cuda" if torch.cuda.is_available() else "cpu")


# Load the model from the safetensors file
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    custom_weights_format="safetensors",  # Indicate safetensors format
    torch_dtype=torch.float32,  # Ensure correct data type (use float16 if needed)
    local_files_only=True  # Avoid fetching from the hub
)


# Use the pipeline
pipe.to("cuda")  # If you're using a GPU


@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Generate the image
        image = pipe(prompt).images[0]

        # Save the generated image
        image_path = "/tmp/generated_image.png"
        image.save(image_path)

        return jsonify({"image_url": image_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

