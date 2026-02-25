import torch
from torch.utils.data import DataLoader
from src.datasets.sop import TripletDataset
from src.datasets.transforms import get_train_transforms
from src.models.embedder import ResNetEmbedder
from src.training.loss import TripletLoss

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    dataset = TripletDataset(
        csv_path="data/splits/gallery.csv",
        transform=get_train_transforms()
    )

    loader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=True,
        num_workers=2
    )

    model = ResNetEmbedder(embedding_dim=256).to(device)
    criterion = TripletLoss(margin=0.3)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    model.train()

    for batch_idx, (anchor, positive, negative) in enumerate(loader):
        anchor = anchor.to(device)
        positive = positive.to(device)
        negative = negative.to(device)

        anchor_emb = model(anchor)
        pos_emb = model(positive)
        neg_emb = model(negative)

        loss = criterion(anchor_emb, pos_emb, neg_emb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Batch {batch_idx} | Loss: {loss.item():.4f}")

        if batch_idx == 5:
            break

    # ✅ Save Model
    torch.save(model.state_dict(), "artifacts/embedding_model.pt")
    print("Model saved to artifacts/embedding_model.pt")


if __name__ == "__main__":
    main()