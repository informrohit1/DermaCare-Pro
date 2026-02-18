import torch
import torchvision.transforms as transforms
from PIL import Image
import pandas as pd
from mymodel import SkinDiseaseCNN  # Import model

# Load metadata to map class indices to labels
metadata = pd.read_csv("HAM10000_metadata.csv")
unique_labels = sorted(metadata['dx'].unique())
idx_to_class = {i: label for i, label in enumerate(unique_labels)}

# Load Trained Model
num_classes = len(unique_labels)
model = SkinDiseaseCNN(num_classes)
model.load_state_dict(torch.load("skin_disease_cnn.pth", map_location=torch.device("cpu")))
model.eval()

# Image Transformations (Same as training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def predict(image_path):
    """Predict disease from an input image."""
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    
    class_id = predicted.item()
    return class_id, idx_to_class[class_id]
