<div align="center">
  <h1>🏥 VisiHealth AI</h1>
  <p><strong>A Multimodal Explainable Medical Visual Question Answering System</strong></p>
  <p><i>Powered by ResNet50, BioLinkBERT, and Cross-Attention Fusion</i></p>
</div>

<br/>

## 🌟 Overview
VisiHealth AI is a state-of-the-art medical Visual Question Answering (VQA) system designed for final year project research. It allows users to upload medical images (X-rays, MRIs, CT scans) and ask natural language questions about them. The AI provides an accurate answer, a confidence score, the Region of Interest (ROI), an attention map visualization, and a human-readable medical rationale generated from a medical knowledge graph.

## 🚀 Key Features
* **Cross-Attention Fusion:** Uses true multi-token cross-attention to let ResNet50 spatial patches attend to BioLinkBERT text tokens.
* **Dual-Head Predictor:** Custom architecture that routes CLOSED questions (Yes/No) and OPEN questions (Descriptive) to specialized heads.
* **Explainable AI:** Generates medical rationales from a 4,444-triplet Knowledge Graph (`kg.txt`) and renders visual attention maps for interpretability.
* **High Performance:** Achieves **74.36% validation accuracy** across 202 normalized clinical classes on the SLAKE 1.0 dataset.
* **Beautiful 3D UI:** A Next.js frontend featuring Three.js 3D models, smooth framer-motion animations, and local history storage using canvas thumbnail compression.

## 💻 Tech Stack
### **Backend (Python / Flask)**
* **Core:** PyTorch, Flask, Transformers (HuggingFace)
* **Models:** ResNet50 (Visual), BioLinkBERT (Text)
* **API:** RESTful architecture with CORS enabled
* **Capabilities:** Image tensor normalization, tokenization, real-time inference, softmax scaling

### **Frontend (Next.js / React)**
* **Framework:** Next.js 14 App Router, React, TypeScript
* **Styling:** Tailwind CSS
* **Animations & 3D:** Framer Motion, Three.js, React Three Fiber
* **Features:** Drag-and-drop uploads, history storage, interactive 3D visualizations

## 📂 Project Structure
```text
VISIHEALTH CODE/
├── backend/                  # Flask REST API backend
│   ├── app.py                # Main server entrypoint
│   ├── api/routes.py         # Endpoints definition
│   └── services/             # Model loading and inference service
├── visihealth-frontend/      # Next.js web application
│   ├── app/                  # Pages (Home, Analyze, History, About)
│   ├── components/           # UI, 3D, and Layout components
│   └── lib/                  # API client and state management
├── models/                   # PyTorch Model Architectures
│   ├── cnn_model.py          # ResNet50 vision extraction
│   ├── bert_model.py         # BioLinkBERT text extraction
│   └── fusion_model.py       # Cross-attention fusion network
├── checkpoints/              # Pretrained model weights (GitIgnored)
├── data/                     # SLAKE 1.0 Dataset (GitIgnored)
├── results/                  # Inference metadata and info JSON
├── config.yaml               # Master model configuration
└── kg.txt                    # Medical Knowledge Graph triplets
```

## ⚙️ Installation & Setup

> **Note:** The trained PyTorch model weights (`best_checkpoint.pth` ~1.3GB) and the dataset are intentionally excluded from this repository via `.gitignore` due to size limitations.

### 1. Backend Setup
```bash
# Navigate to the root directory
# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend
cd backend

# Run the Flask server
python app.py
```
*The API will be available at `http://localhost:5000`*

### 2. Frontend Setup
```bash
# Open a new terminal and navigate to frontend
cd visihealth-frontend

# Install Node dependencies
npm install

# Start the Next.js development server
npm run dev
```
*The web app will be available at `http://localhost:3000`*

## 🧪 API Endpoints Reference
| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Check backend server status |
| `/api/model/info` | GET | Retrieve model configuration and loaded state |
| `/api/predict` | POST | Send an image + question for AI inference |
| `/api/visualize/attention` | POST | Generate a heat-map overlay over the medical scan |

## 🎓 Academic Documentation
If you are viewing this project for academic purposes, please refer to the provided `.md` files in the repository for deep technical insights:
* `REPORT_WRITING_MASTER_GUIDE.md` - Complete architectural blueprint
* `THREE_MODEL_COMPARISON.md` - Analysis of architectural iterations and accuracy improvements
* `START_GUIDE.md` - Overview of system states and UI components

---
**Disclaimer:** VisiHealth AI is a research prototype built for academic purposes. It should **not** be used for actual medical diagnosis. Always consult a qualified healthcare professional.
