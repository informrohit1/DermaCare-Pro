import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
import os
import sys
import pandas as pd
import numpy as np
from collections import Counter

# Add the current directory to the system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import custom modules
from mymodel import SkinDiseaseCNN, get_vgg16_model
from builddataset import SkinDiseaseDataset

def compute_class_weights(metadata_path):
    df = pd.read_csv(metadata_path)
    label_column = 'dx'  # Change this if your label column has a different name

    class_counts = Counter(df[label_column])
    classes = sorted(class_counts.keys())  # Ensure consistent order

    class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
    total_samples = sum(class_counts.values())

    class_weights = []
    for cls in classes:
        freq = class_counts[cls]
        weight = total_samples / (len(classes) * freq)
        class_weights.append(weight)

    weights_tensor = torch.tensor(class_weights, dtype=torch.float)
    return weights_tensor, class_to_idx

def main():
    # Paths
    image_dir = r"C:\Users\infor\Programming\DataScience\skindisease\HAM"
    metadata_path = r"C:\Users\infor\Programming\DataScience\skindisease\HAM10000_metadata.csv"
    batch_size = 32
    num_classes = 7
    epochs = 10 # Adjust as needed
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    # Load class weights
    class_weights, class_to_idx = compute_class_weights(metadata_path)
    class_weights = class_weights.to(device)

    # Load Dataset
    dataset = SkinDiseaseDataset(image_dir, metadata_path)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

    # Choose model (CNN or Transfer Learning)
    model = SkinDiseaseCNN(num_classes).to(device)  # Use CNN
    # model = get_vgg16_model(num_classes).to(device)  # Uncomment for VGG16

    # Loss and Optimizer (use class weights here)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training Loop
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}")

    # Save Model
    torch.save(model.state_dict(), "skin_disease_cnn.pth")
    print("Training Complete. Model Saved.")

if __name__ == '__main__':
    main()
