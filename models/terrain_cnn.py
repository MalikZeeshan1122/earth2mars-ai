"""
Earth2Mars AI - Terrain CNN Model
Convolutional Neural Network for terrain classification from satellite imagery.
Classifies terrain patches into analog categories matching Moon/Mars surface types.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TerrainCNN(nn.Module):
    """
    CNN model for classifying satellite image patches into terrain types
    that correspond to planetary analog categories.

    Input: Multi-band satellite image patch (e.g., 13-band Sentinel-2, 64x64 pixels)
    Output: Probability distribution over terrain classes

    Terrain Classes:
        0: Basaltic lava flow (Lunar maria / Martian volcanic plains)
        1: Impact crater terrain (Shattered rock, breccia)
        2: Sandy desert / dune field (Regolith analog)
        3: Polar permafrost (Cold trap / cryogenic analog)
        4: Iron-oxide rich terrain (Red desert / Martian soil)
        5: Hydrothermal / acidic terrain (Astrobiology analog)
        6: Volcanic tube / cave terrain (Lava tube habitat analog)
        7: Other
    """

    NUM_CLASSES = 8

    def __init__(self, in_channels: int = 13, num_classes: int = NUM_CLASSES):
        super().__init__()

        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.25),

            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.25),

            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4)),
            nn.Dropout2d(0.25),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return x

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        """Return softmax probabilities."""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            return F.softmax(logits, dim=1)


TERRAIN_LABELS = {
    0: "Basaltic Lava Flow",
    1: "Impact Crater Terrain",
    2: "Sandy Desert / Dune Field",
    3: "Polar Permafrost",
    4: "Iron-Oxide Rich Terrain",
    5: "Hydrothermal / Acidic",
    6: "Volcanic Tube / Cave",
    7: "Other",
}
