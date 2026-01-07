# Wedding Photo Face Recognition System

## Overview

This project is a **face recognition system** designed to help users find their photos from large wedding image collections. Given a selfie or query image, the system retrieves all matching photos from a preprocessed dataset using facial similarity.

The project was developed during an internship where responsibilities were **clearly scoped**:
- This repository contains the **face recognition pipeline and demo interface**
- The **production web/mobile application** was handled by a separate team

A lightweight Streamlit app is included **only for end-to-end validation and demonstration** of the core system.

---

## Problem Statement

Wedding albums often contain thousands of photos, making it difficult for guests to find images they appear in.

The goal of this system is to:
- Detect faces from large image collections
- Generate facial embeddings
- Allow users to upload a selfie
- Retrieve all photos containing matching faces

---

## My Responsibility

During the internship, my responsibility was to design and implement the **face recognition backend**, including:

- Face detection from images
- Face embedding generation
- Similarity matching logic
- Storage and retrieval of embeddings
- A demo interface to validate the pipeline

The **frontend application, cloud deployment, and user-facing product** were handled by a separate web team.

---

## System Architectur

1. **Offline Ingestion**
   - Wedding images are processed once
   - Faces are detected using RetinaFace
   - Embeddings are generated using FaceNet
   - Embeddings are stored in a database along with image references

2. **Online Query**
   - User uploads a selfie
   - Embeddings are generated in real time
   - Cosine similarity is used to match against stored embeddings
   - Matching images are returned

This separation ensures:
- Fast query performance
- No repeated processing of wedding images
- Scalable design for future deployment

---

## Technologies Used

- **Python**
- **DeepFace (FaceNet model)** – embedding generation
- **RetinaFace** – face detection
- **PostgreSQL** – embedding storage
- **NumPy** – similarity computation
- **Streamlit** – demo and validation interface

---

## Repository Structure

Photo_App/
├── app.py                     # Streamlit demo for face search
├── face_recognition_system.py # Offline embedding generation
├── event_management.py        # Event & QR demo module
├── config.py                  # Centralized path configuration
├── data/                      # Local demo/test data (gitignored)
├── utils/                     # Helper utilities
├── requirements.txt
└── README.md


---

## Data & Privacy

⚠️ **Important**

- Real wedding images, cropped faces, and embeddings are **not included** in this repository
- All biometric data used during development remains private
- The repository contains **only code and configuration**

The system is designed so that **any dataset can be plugged in locally or via cloud storage** without modifying core logic.

---

## Running the Demo Locally

### Prerequisites
- Python 3.9+
- PostgreSQL (running locally)
- Required Python dependencies installed

### Install dependencies
```bash
pip install -r requirements.txt
