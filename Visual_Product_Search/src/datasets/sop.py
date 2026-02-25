import random
from PIL import Image
from torch.utils.data import Dataset
import pandas as pd

class SOPDataset(Dataset):
    """
    Used for evaluation / inference.
    Returns (image, product_id)
    """
    def __init__(self, csv_path, transform=None):
        self.data = pd.read_csv(csv_path)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        image = Image.open(row["image_path"]).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, row["product_id"]


class TripletDataset(Dataset):
    """
    Used for training with triplet loss.
    Returns (anchor, positive, negative)
    """
    def __init__(self, csv_path, transform=None):
        self.data = pd.read_csv(csv_path)
        self.transform = transform

        # group indices by product_id
        self.product_to_indices = {}
        for idx, pid in enumerate(self.data["product_id"]):
            self.product_to_indices.setdefault(pid, []).append(idx)

        self.product_ids = list(self.product_to_indices.keys())

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        anchor_row = self.data.iloc[idx]
        anchor_pid = anchor_row["product_id"]

        # positive: same product_id, different image
        pos_idx = idx
        while pos_idx == idx:
            pos_idx = random.choice(self.product_to_indices[anchor_pid])

        # negative: different product_id
        neg_pid = random.choice(self.product_ids)
        while neg_pid == anchor_pid:
            neg_pid = random.choice(self.product_ids)
        neg_idx = random.choice(self.product_to_indices[neg_pid])

        anchor_img = Image.open(anchor_row["image_path"]).convert("RGB")
        positive_img = Image.open(self.data.iloc[pos_idx]["image_path"]).convert("RGB")
        negative_img = Image.open(self.data.iloc[neg_idx]["image_path"]).convert("RGB")

        if self.transform:
            anchor_img = self.transform(anchor_img)
            positive_img = self.transform(positive_img)
            negative_img = self.transform(negative_img)

        return anchor_img, positive_img, negative_img