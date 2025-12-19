
import io
import pathlib

import gradio as gr
import numpy as np
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def caption_image(input_image: np.ndarray | Image.Image | bytes | str):
    # Convert various input types to a PIL Image in RGB mode
    if isinstance(input_image, np.ndarray):
        raw_image = Image.fromarray(input_image).convert("RGB")
    elif isinstance(input_image, Image.Image):
        raw_image = input_image.convert("RGB")
    elif isinstance(input_image, (str, pathlib.Path)):
        raw_image = Image.open(input_image).convert("RGB")
    else:
        # assume bytes / file-like
        raw_image = Image.open(io.BytesIO(input_image)).convert("RGB")

    # You do not need a question for image captioning
    text = "the image of"
    inputs = processor(images=raw_image, text=text, return_tensors="pt")

    # Generate a caption for the image
    outputs = model.generate(**inputs, max_length=50)

    # Decode the generated tokens to text
    caption = processor.tokenizer.decode(outputs[0], skip_special_tokens=True)

    return caption


iface = gr.Interface(
    fn=caption_image,
    inputs=gr.Image(type="numpy"),
    outputs="text",
    title="Image Captioning",
    description="This is a simple web app for generating captions for images using a trained model."
)

iface.launch()