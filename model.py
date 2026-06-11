import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

# Load model (UPDATED - no warning)
from torchvision.models import resnet18, ResNet18_Weights

model = resnet18(weights=ResNet18_Weights.DEFAULT)
model = models.resnet18(weights=weights)
model.eval()

# Load labels
with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

# Transform
transform = weights.transforms()

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)

    # Get top prediction
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_class = torch.max(probabilities, 0)

    return {
        "class": labels[top_class],
        "confidence": float(top_prob)
    }