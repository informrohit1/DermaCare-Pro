import torch
import torchvision.transforms as transforms
from PIL import Image
from mymodel import SkinDiseaseCNN

# ===============================
# Hardcoded Class Labels (Production Safe)
# ===============================
class_names = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]

# Load Trained Model
num_classes = len(class_names)
model = SkinDiseaseCNN(num_classes)
model.load_state_dict(torch.load("skin_disease_cnn.pth", map_location=torch.device("cpu")))
model.eval()

# Image Transformations (Same as training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5],
                         std=[0.5, 0.5, 0.5])
])

def predict(image_path):
    """Predict disease from an input image."""
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    class_id = predicted.item()
    return class_id, class_names[class_id]
