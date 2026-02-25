import torch
import numpy as np
from torch.utils.data import DataLoader
from src.datasets.sop import SOPDataset
from src.datasets.transforms import get_eval_transforms
from src.models.embedder import ResNetEmbedder
from tqdm import tqdm

def extract(csv_path, model, device):
    dataset = SOPDataset(csv_path, transform=get_eval_transforms())
    loader = DataLoader(dataset, batch_size=64, shuffle=False, num_workers=2)

    embeddings = []
    labels = []

    model.eval()
    with torch.no_grad():
        for images, product_ids in tqdm(loader):
            images = images.to(device)
            emb = model(images)
            embeddings.append(emb.cpu().numpy())
            labels.extend(product_ids)

    return np.vstack(embeddings), labels

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = ResNetEmbedder(256).to(device)
    model.load_state_dict(torch.load("artifacts/embedding_model.pt", map_location=device))

    gallery_emb, gallery_labels = extract("data/splits/gallery.csv", model, device)
    query_emb, query_labels = extract("data/splits/query.csv", model, device)

    np.save("artifacts/gallery_embeddings.npy", gallery_emb)
    np.save("artifacts/query_embeddings.npy", query_emb)
    np.save("artifacts/gallery_labels.npy", np.array(gallery_labels))
    np.save("artifacts/query_labels.npy", np.array(query_labels))