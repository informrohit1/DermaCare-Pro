import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class SkinDiseaseDataset(Dataset):
    def __init__(self, image_dir, metadata_path, transform=None):
        self.image_dir = image_dir

        # Load and preprocess metadata
        df = pd.read_csv(metadata_path)
        df.columns = df.columns.str.strip()
        df["image_id"] = df["image_id"].astype(str).str.strip().str.lower()

        # Get diagnosis column dynamically
        diagnosis_col = [col for col in df.columns if "dx" in col.lower()]
        if not diagnosis_col:
            raise ValueError("No diagnosis column found in metadata.")
        diagnosis_col = diagnosis_col[0]

        # Create label mapping and image-label dictionary
        self.label_mapping = {label: idx for idx, label in enumerate(df[diagnosis_col].unique())}
        self.image_labels = {row["image_id"]: self.label_mapping[row[diagnosis_col]] for _, row in df.iterrows()}
        self.image_filenames = list(self.image_labels.keys())

        # Image Transformations
        self.transform = transform if transform else transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        # Get image ID and path
        image_id = self.image_filenames[idx]
        image_path = os.path.join(self.image_dir, f"{image_id}.jpg")

        # Check if the image file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Load and preprocess the image
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        # Get the label
        label = self.image_labels[image_id]

        return image, label