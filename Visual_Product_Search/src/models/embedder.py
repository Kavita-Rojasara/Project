import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

from src.utils.config import load_config


class ResNetEmbedder(nn.Module):
    def __init__(self, embedding_dim=256):
        super().__init__()

        config = load_config()
        backbone_name = config["model"]["backbone"]

        if backbone_name == "resnet18":
            backbone = models.resnet18(
                weights=models.ResNet18_Weights.IMAGENET1K_V1
            )
        elif backbone_name == "resnet50":
            backbone = models.resnet50(
                weights=models.ResNet50_Weights.IMAGENET1K_V1
            )
        else:
            raise ValueError(f"Unsupported backbone: {backbone_name}")

        # Remove classification head
        self.backbone = nn.Sequential(*list(backbone.children())[:-1])

        # Embedding projection
        self.embedding = nn.Linear(
            backbone.fc.in_features,
            embedding_dim
        )

    def forward(self, x):
        x = self.backbone(x)
        x = x.view(x.size(0), -1)
        x = self.embedding(x)

        # L2 normalization for metric learning
        x = F.normalize(x, p=2, dim=1)
        return x