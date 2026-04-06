from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image
import torch

model_path = "/models--vikhyatk--moondream2"

processor = AutoProcessor.from_pretrained(
    model_path,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    device_map="auto"
).eval()
