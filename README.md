<div align="center">
  <h1>🏥 VisiHealth AI</h1>
  <p><strong>A Multimodal Explainable Medical Visual Question Answering System</strong></p>
  <p><i>Powered by ResNet50 · BioLinkBERT · Real Cross-Attention Fusion · Medical Knowledge Graph</i></p>
</div>

<br/>

---

## 🌟 Overview

VisiHealth AI is a full-stack Medical Visual Question Answering (VQA) system built as a final-year project. A user uploads a radiology image (X-ray, MRI, or CT scan) and asks a free-text question about it. The system returns:

- ✅ **A precise clinical answer** from 202 normalised answer classes
- 📊 **A confidence score** with colour-coded level (high / medium / low)
- 🎯 **Top alternative predictions** ranked by softmax probability
- 🗺️ **A Region-of-Interest (ROI) label** identifying which of 39 anatomical regions the model focused on
- 🔥 **An attention-map heatmap** (Grad-CAM style) overlaid on the original scan
- 💡 **A human-readable medical rationale** derived from a 4,444-triplet Medical Knowledge Graph

The entire pipeline—model training, Flask REST API, and a Next.js web application—lives in this repository.

---

## 🚀 Key Features

| Feature | Detail |
|---|---|
| **Real Multi-Token Cross-Attention** | Each BioLinkBERT question token independently attends over all 49–100 ResNet50 spatial patches. The word "lung" activates different image regions than "brain". |
| **Dual-Head Predictor** | CLOSED questions (yes / no) and OPEN questions (organ names, disease labels) are routed to dedicated classifier heads, reducing cross-category confusion. |
| **Question-Type Auxiliary Loss** | A lightweight binary classifier (CLOSED=0, OPEN=1) is trained jointly, contributing 10 % of the total loss to guide routing. |
| **Focal Loss + Class Weights** | `FocalLoss(γ=2.0)` down-weights easy examples so the model focuses on rare answer classes. Per-class inverse-frequency weights are capped at 10× to prevent extreme gradients. |
| **Answer Normalisation** | A `_normalize_answer()` function eliminates SLAKE typos (`barin→brain`), punctuation variants, and arbitrary ordering of multi-entity answers before building the vocabulary, reducing classes from 221 to 202. |
| **Explainable AI** | Attention maps are rendered as overlaid heatmaps. KG rationales follow the template `"Detected {roi}. Knowledge Graph indicates: {kg_fact}. Therefore, the answer is {prediction}."` |
| **74.36 % Validation Accuracy** | Achieved on SLAKE 1.0 (English subset) after 63 epochs with the latest fixed architecture. |
| **Complete Next.js Web App** | Four fully implemented pages (Home, Analyze, History, About) with Framer Motion animations, Three.js 3D components, and localStorage history with canvas thumbnail compression. |

---

## 💻 Tech Stack

### Backend — Python / Flask
| Component | Library / Version |
|---|---|
| Web framework | Flask |
| Deep learning | PyTorch |
| Image encoder | `torchvision` ResNet50 (ImageNet pretrained) |
| Text encoder | HuggingFace `transformers` — `michiyasunaga/BioLinkBERT-base` |
| Image processing | Pillow, torchvision transforms |
| Config management | PyYAML |
| CORS | Flask-CORS |

### Frontend — Next.js / React
| Component | Library / Version |
|---|---|
| Framework | **Next.js 16** (App Router, React Compiler enabled) |
| Language | TypeScript 5 |
| Styling | Tailwind CSS 4 |
| Animations | Framer Motion 11 |
| 3D graphics | Three.js + `@react-three/fiber` + `@react-three/drei` |
| State management | Zustand 4 (with `persist` middleware) |
| HTTP client | Axios 1.6 |
| Upload handling | Native drag-and-drop (no extra library) |
| Notifications | React Hot Toast 2.4 |
| Charts | Recharts 2.10 |

---

## 📂 Project Structure

```text
VisiHealthAI/
│
├── backend/                        Flask REST API
│   ├── app.py                      Application factory, eager model load
│   ├── config.py                   CORS origins, upload limits, model paths
│   ├── requirements.txt            Python dependencies
│   ├── start_server.sh             Linux/macOS convenience launcher
│   ├── start_server.bat            Windows convenience launcher
│   ├── api/
│   │   └── routes.py               All 6 REST endpoints
│   ├── services/
│   │   └── model_service.py        Singleton model loader + inference
│   ├── middleware/
│   │   └── cors.py                 CORS setup
│   ├── utils/
│   │   └── validators.py           File-type, size, and question validation
│   └── uploads/                    Temporary image storage (gitignored)
│
├── models/                         PyTorch model modules
│   ├── __init__.py                 Exports get_cnn_model, get_bert_model, build_visihealth_model
│   ├── cnn_model.py                ResNet50 + ROI attention + segmentation head + spatial patches
│   ├── bert_model.py               BioLinkBERT loader with partial freezing and projection head
│   └── fusion_model.py             CrossAttentionFusion + DualHeadAnswerPredictor + QType classifier
│
├── data/                           SLAKE 1.0 dataset (gitignored — download separately)
│   └── Slake/Slake1.0/
│       ├── train.json
│       ├── validate.json
│       ├── test.json
│       ├── imgs/
│       └── masks/
│
├── scripts/
│   ├── train.py                    Full training pipeline (FocalLoss, early stopping, TensorBoard)
│   ├── demo.py                     Single-image inference demo with attention visualisation
│   ├── eval_diag.py                Evaluate checkpoint accuracy on the test set
│   ├── hf_diag.py                  Verify HuggingFace BioLinkBERT download
│   ├── refresh_model_artifacts.py  Regenerate results/*.json from a checkpoint
│   └── run_refresh_with_status.py  Wrapper that writes a status JSON after refresh
│
├── utils/
│   ├── __init__.py
│   └── knowledge_graph.py          KG loader (tab-delimited or JSON), RationaleGenerator
│
├── visihealth-frontend/            Next.js 16 web application
│   ├── app/
│   │   ├── layout.tsx              Root layout — Header, Footer, Toaster
│   │   ├── globals.css             Tailwind + blob animation keyframes
│   │   ├── page.tsx                Home page
│   │   ├── analyze/page.tsx        Image upload + question + results
│   │   ├── history/page.tsx        localStorage history with search/sort/export
│   │   └── about/page.tsx          Architecture, dataset, and disclaimer
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx          Sticky nav with active-link highlighting
│   │   │   └── Footer.tsx          Branding, links, GitHub icon
│   │   ├── home/
│   │   │   ├── Hero.tsx            Animated floating Brain icon + stat counters
│   │   │   ├── Features.tsx        6-card feature grid with hover-3D cards
│   │   │   └── HowItWorks.tsx      3-step connector diagram
│   │   ├── analyzer/
│   │   │   ├── ImageUploader.tsx   Drag-and-drop with AnimatePresence preview
│   │   │   ├── QuestionInput.tsx   Textarea + 6 suggested-question chips
│   │   │   └── ResultsDisplay.tsx  Answer + confidence bar + top predictions + ROI + rationale + attention map
│   │   ├── history/
│   │   │   ├── HistoryCard.tsx     80×80 px JPEG thumbnail, confidence badge, question/answer preview
│   │   │   ├── SearchBar.tsx       Controlled search input with clear button
│   │   │   └── DetailModal.tsx     Full-screen modal with all stored fields
│   │   ├── 3d/
│   │   │   ├── ParticleBackground.tsx  Three.js: 1,500 blue particles + 40 connecting lines (R3F)
│   │   │   └── ConfidenceGauge3D.tsx   Three.js: animated torus progress ring with colour coding
│   │   └── ui/
│   │       ├── Button.tsx          5 variants + loading spinner
│   │       ├── Card.tsx            Optional 3D hover lift effect
│   │       ├── Badge.tsx           5 semantic colour variants
│   │       └── Progress.tsx        Animated fill bar with optional label
│   ├── lib/
│   │   ├── api.ts                  Axios client: health, modelInfo, predict, visualizeAttention, predictBatch, getVocabulary
│   │   ├── store.ts                Zustand store persisting history to localStorage
│   │   └── utils.ts                cn(), formatConfidence(), getConfidenceColor(), validateImageFile()
│   ├── types/
│   │   └── api.ts                  PredictionResponse, AnalysisHistory, AnalyzerState, …
│   ├── package.json
│   ├── next.config.ts              reactCompiler: true
│   ├── tsconfig.json
│   ├── tailwind.config (inline)
│   └── postcss.config.mjs
│
├── checkpoints/                    Trained weights (gitignored — ~1.3 GB)
│   ├── best_checkpoint.pth         Best validation checkpoint
│   └── last_checkpoint.pth         Most recent epoch
│
├── results/
│   ├── VisiHealth_Model_Info.json  num_classes, answer_vocab, image_size, val_acc — used by backend
│   └── VisiHealth_Results.json     High-level accuracy summary for reporting
│
├── config.yaml                     Master training + model + runtime configuration
├── kg.txt                          4,444 tab-delimited medical knowledge triplets
├── requirements.txt                Root Python requirements (training + backend)
├── .gitignore
│
└── Docs/
    ├── REPORT_WRITING_MASTER_GUIDE.md   Full academic architecture blueprint
    ├── THREE_MODEL_COMPARISON.md        Three-model evolution and bug analysis
    ├── FRONTEND_PLAN.md                 Original frontend design specification
    ├── PROJECT_SUMMARY.md               Project overview and component explanation
    └── START_GUIDE.md                   Quick-start and troubleshooting reference
```

> **⚠️ Not in this repository:** `checkpoints/*.pth` (~1.3 GB), `data/` (SLAKE 1.0), and `colab_notebooks/` are all excluded via `.gitignore` due to file-size constraints.

---

## 🧠 Model Architecture

VisiHealth AI went through three architectural generations. The current checkpoint uses **Model 3**.

### How inference works (Model 3)

```
Medical Image (336×336)
      │
  ResNet50 backbone
      ├── Pooled vector  [B, 512]          → ROI attention head (39-class sigmoid)
      └── Spatial tokens [B, ≈100, 2048]  → projected to [B, ≈100, 512]
                                                     │
                                          ┌──────────┘
Question text (up to 128 tokens)         │
      │                                  │
  BioLinkBERT (10 of 12 layers trainable)│
      └── Token embeddings [B, L, 768]   │
                │                        │
                └──────────CrossAttentionFusion──────────
                           Each question token attends
                           over all image spatial patches
                                     │
                          Gated blend + mean pool → [B, 512]
                                     │
                          ┌──────────┴──────────┐
                     QType classifier     Dual Answer Head
                      (CLOSED / OPEN)    ┌────────────────┐
                                         │ CLOSED head     │ → yes/no/none/…
                                         │ OPEN head       │ → organ/disease/…
                                         └────────────────┘
                                     │
                              Final answer logits
                                     │
                          Segmentation head (binary, multi-task)
```

### Three-model evolution

| | Model 1 | Model 2 | **Model 3 (current)** |
|---|---|---|---|
| Image size | 224 × 224 | 336 × 336 | **336 × 336** |
| Spatial tokens for attention | ✗ | ✗ (bug: length-1 sequence) | **✅ ~100 real patches** |
| Fusion | Plain concat + MLP | Fake cross-attention | **✅ Real multi-token cross-attention** |
| Answer head | Single (221 classes) | Dual CLOSED / OPEN | **Dual CLOSED / OPEN** |
| QType classifier | ✗ | ✅ | **✅** |
| Answer normalisation | ✗ | ✅ | **✅ (202 clean classes)** |
| Shared train/val vocab | ✗ (index mismatch bug) | Partially fixed | **✅ Hard assertion** |
| Loss | CrossEntropy | CrossEntropy + class weights | **FocalLoss (γ=2) + class weights** |
| Label smoothing | ✗ | 0.1 | **0.05** |
| CLOSED oversampling | ✗ | ✗ | **✅ WeightedRandomSampler 2×** |
| BERT trainable layers | 6 / 12 | 9 / 12 | **10 / 12** |
| **Val accuracy** | 61.06 % | 73.12 % | **74.36 %** |
| **Test accuracy** | 56.64 % | TBD | TBD |

See `THREE_MODEL_COMPARISON.md` for a detailed bug-by-bug breakdown.

---

## 📊 Dataset — SLAKE 1.0

| Property | Value |
|---|---|
| Total radiology images | 642 (chest X-ray, MRI, CT) |
| Total QA pairs (bilingual) | 14,028 |
| English QA pairs (used) | ~9,835 |
| Training samples | 4,919 |
| Validation samples | ~1,061 |
| Test samples | ~1,053 |
| Answer classes (raw) | 221 (includes typos, duplicates) |
| Answer classes (normalised) | **202** |
| Avg QA pairs per image | ~7.6 |

**Training augmentation** (applied per sample):
- Random rotation ±15°
- Random horizontal flip (50 %)
- Colour jitter (brightness 0.2, contrast 0.2)
- Random affine (translate ±10 %, scale 90–110 %)
- Random erasing (10 % probability)
- **No vertical flip** — would destroy anatomical semantics (e.g. "upper lung" becomes wrong)

**Question types in SLAKE:**
- CLOSED (yes / no): abnormality presence, laterality
- OPEN (descriptive): organ identification, disease classification, imaging modality, anatomical plane, location queries

---

## 💡 Knowledge Graph (`kg.txt`)

`kg.txt` contains exactly **4,444 tab-delimited medical knowledge triplets** in the form:

```
entity_A\trelation\tentity_B
brain\thas_condition\tbrain edema
lung\thas_disease\tpneumonia
...
```

At inference time `RationaleGenerator` (`utils/knowledge_graph.py`) retrieves the most relevant triplet for the predicted ROI and answer, then fills the template:

```
"Detected {roi}. Knowledge Graph indicates: {kg_fact}. Therefore, the answer is {prediction}."
```

---

## ⚙️ Installation & Setup

### Prerequisites

| Tool | Minimum version |
|---|---|
| Python | 3.9 |
| pip | 21 |
| Node.js | 20 |
| npm | 9 |
| CUDA (optional) | 11.8+ for GPU training / inference |

### Step 0 — Obtain weights and dataset

The model checkpoint and SLAKE dataset are **not** included in this repository.

1. **Checkpoint** — place `best_checkpoint.pth` (~1.3 GB) at `checkpoints/best_checkpoint.pth`
2. **Dataset** — download SLAKE 1.0 from the [official source](https://www.med-vqa.com/slake/) and extract to `data/Slake/Slake1.0/`
3. `results/VisiHealth_Model_Info.json` is included and pre-populated with the answer vocabulary — the backend reads this at startup.

### Step 1 — Backend

```bash
# From the project root, install Python dependencies
pip install -r requirements.txt

# Start the Flask server (development mode)
cd backend
python app.py
```

**Or use the convenience launcher:**
```bash
# Linux / macOS
bash backend/start_server.sh

# Windows
backend\start_server.bat
```

The API will be available at **`http://localhost:5000`**.
On first start the model checkpoint is loaded (~15 s). Confirm readiness with:
```
GET http://localhost:5000/api/health
→ {"status": "healthy", "service": "VisiHealth AI", "version": "1.0.0"}
```

**For production (gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

**Environment variables** recognised by the backend:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
CORS_ORIGINS=https://your-frontend.com   # defaults to http://localhost:3000
```

### Step 2 — Frontend

```bash
cd visihealth-frontend
npm install
npm run dev
```

The web app will be available at **`http://localhost:3000`**.

To point the frontend at a non-default backend URL, set the environment variable before running:
```bash
NEXT_PUBLIC_API_URL=http://your-backend:5000/api npm run dev
```

---

## 🌐 API Reference

All endpoints are under the `/api` prefix. The backend enforces a **16 MB** file-size limit and validates MIME types (jpg, png, gif, bmp, webp, dcm). Questions must be 3–500 characters.

### `GET /api/health`
Returns server health. Use this to confirm the backend is up.

```json
{ "status": "healthy", "service": "VisiHealth AI", "version": "1.0.0" }
```

### `GET /api/model/info`
Returns model load status and configuration.

```json
{ "model_loaded": true, "device": "cuda", "num_classes": 202, "kg_enabled": true }
```

### `POST /api/predict`
Main inference endpoint. Accepts `multipart/form-data`.

| Field | Type | Description |
|---|---|---|
| `image` | File | Medical scan image (jpg / png / bmp / dcm) |
| `question` | string | Natural-language question (3–500 chars) |

```json
{
  "success": true,
  "data": {
    "answer": "brain edema",
    "confidence": 0.712,
    "top_predictions": [
      { "answer": "brain edema", "confidence": 0.712 },
      { "answer": "brain tumor", "confidence": 0.198 },
      { "answer": "no",          "confidence": 0.043 }
    ],
    "roi": { "top_region": 12, "confidence": 0.631, "region_name": "brain" },
    "rationale": "Detected brain. Knowledge Graph indicates: brain has_condition brain edema. Therefore, the answer is brain edema.",
    "attention_map": "<base64-encoded PNG heatmap>"
  }
}
```

### `POST /api/predict/batch`
Accepts multiple images and questions in a single request (same `multipart/form-data` schema, repeated fields).

### `POST /api/visualize/attention`
Returns the Grad-CAM-style attention map as a base64-encoded PNG, plus the answer and confidence.

### `GET /api/answers/vocabulary`
Returns the full list of 202 normalised answer strings.

```json
{ "success": true, "data": { "total": 202, "vocabulary": ["yes", "no", "brain", ...] } }
```

---

## 🖥️ Frontend Pages

All four pages are fully implemented.

### Home (`/`)
- Animated hero section with a floating `Brain` icon, pulsing rings, and 8 floating particles (Framer Motion)
- Three blob animations in the background (CSS keyframes)
- Stat counters: 9,835 training samples · 202 answer classes · 74 % val accuracy
- **Features grid** (6 cards): Cross-Attention Fusion · High Accuracy · ROI Detection · Explainable AI · Real-time Analysis · Privacy Focused
- **How It Works** 3-step connector diagram

### Analyze (`/analyze`)
- **Image uploader** with drag-and-drop (`onDrop` handler) and click-to-browse; AnimatePresence flip between upload zone and preview thumbnail with file name and size overlay
- **Question input** with 6 pre-written suggested question chips
- **Analyze button** disabled until both inputs are present; shows spinner during inference
- After inference, fetches attention map from `/visualize/attention` as a fallback if `/predict` does not return one
- **Results panel**: primary answer with animated confidence fill bar (green ≥70 % / yellow ≥40 % / red <40 %), alternative predictions (ranked bar chart), ROI label, knowledge-graph rationale, attention map heatmap
- History auto-saved to `localStorage` key `visihealth_history`; thumbnails are canvas-compressed to 80×80 px JPEG at 30 % quality (~3–5 KB); QuotaExceededError is caught and handled gracefully (strips thumbnails, trims to 10 entries, or clears if still full)
- **New Analysis** button to reset all state

### History (`/history`)
- Loads and migrates entries from localStorage on mount (strips large legacy `imageUrl`/`attentionMap` fields)
- Searchable by question, answer, or alternative predictions
- Sortable by most recent or highest confidence
- Grid of `HistoryCard` components with 80×80 compressed thumbnail (or Brain icon placeholder), confidence badge, question, answer, two alternative predictions, and timestamp
- **Export** button downloads `visihealth-history-<timestamp>.json`
- **Clear All** button with confirmation dialog
- `DetailModal` shows the full stored record in a scrollable overlay

### About (`/about`)
- Model architecture card (accuracy, parameters, encoders, fusion method, training data)
- Four key-feature cards (Multi-Modal Fusion, Attention Mechanism, Knowledge Graph, Transfer Learning)
- Technology stack panel (Frontend / Backend / Model columns)
- SLAKE 1.0 dataset facts (642 images, 9,835 English QA pairs, 202 classes, 4,444 KG triplets, 6 question types)
- Medical disclaimer banner

---

## 🏋️ Training Your Own Model

### Prerequisites
- SLAKE 1.0 dataset at `data/Slake/Slake1.0/`
- A CUDA GPU is strongly recommended (training was performed on a Kaggle T4)

### Run training
```bash
python scripts/train.py --config config.yaml
```

Resume from checkpoint:
```bash
python scripts/train.py --config config.yaml --resume
# or specify a checkpoint explicitly:
python scripts/train.py --config config.yaml --checkpoint checkpoints/last_checkpoint.pth
```

Training will:
1. Build a normalised answer vocabulary from the training split and share it with validation
2. Apply `WeightedRandomSampler` to oversample CLOSED questions 2× per epoch
3. Compute inverse-frequency class weights (capped at 10×)
4. Train with `FocalLoss(γ=2.0, label_smoothing=0.05)` and AdamW differential learning rates (BERT 10× lower than CNN/fusion heads)
5. Log train loss, train accuracy, val loss, val accuracy, CLOSED accuracy, and OPEN accuracy to TensorBoard under `logs/`
6. Save periodic checkpoints every 20 epochs (keep latest 3), `last_checkpoint.pth`, and `best_checkpoint.pth`
7. Stop early if validation loss does not improve for 30 consecutive epochs
8. Write `results/VisiHealth_Model_Info.json` with the clean normalised vocabulary on completion

Monitor training:
```bash
tensorboard --logdir logs/
```

### Key training hyperparameters (`config.yaml`)

| Parameter | Value | Notes |
|---|---|---|
| `image.size` | 336 | Produces ~100 spatial tokens for cross-attention |
| `training.batch_size` | 8 | × 8 gradient accumulation = effective batch 64 |
| `training.num_epochs` | 200 | Early stopping patience 30 |
| `training.learning_rate` | 1e-4 | BERT group gets 1e-5 (10× lower) |
| `training.optimizer` | AdamW | weight_decay = 1e-4 |
| `training.scheduler` | ReduceLROnPlateau | factor 0.5, halves LR on val-loss plateau |
| `training.use_focal_loss` | true | gamma = 2.0 |
| `training.label_smoothing` | 0.05 | Prevents over-confident wrong predictions |
| `model.bert.freeze_layers` | 2 | Bottom 2 frozen; 10 / 12 layers trainable |
| `model.cnn.dropout` | 0.25 | |
| `model.bert.dropout` | 0.1 | |
| `training.multitask.segmentation_weight` | 0.2 | VQA is primary (weight 1.0) |

---

## 🔑 Key Scripts

| Script | Purpose |
|---|---|
| `scripts/train.py` | End-to-end training pipeline |
| `scripts/demo.py` | Run inference on a single image from the command line with optional attention visualisation |
| `scripts/eval_diag.py` | Evaluate a checkpoint on the test set and print accuracy |
| `scripts/refresh_model_artifacts.py` | Regenerate `results/*.json` metadata from a checkpoint + dataset |
| `scripts/run_refresh_with_status.py` | Wrapper around refresh that also writes a status JSON |
| `scripts/hf_diag.py` | Verify BioLinkBERT is accessible from HuggingFace Hub |

---

## 📈 Performance

| Metric | Value |
|---|---|
| Best validation accuracy | **74.36 %** (epoch 63) |
| Answer vocabulary size | 202 normalised classes |
| Model checkpoint size | ~1.3 GB |
| Backend model load time | ~15 seconds |
| Per-request inference time | ~2–3 seconds (CPU) |
| Frontend initial load | ~3 seconds |

> Test-set accuracy is pending a fresh evaluation run (`python scripts/eval_diag.py`). The last known figure of 56.64 % is from Model 1 (superseded).

---

## 🔒 Security & Privacy

- All uploaded images are processed **in memory** and never persisted to disk by the inference pipeline.
- Input validation rejects unsupported file types and questions shorter than 3 characters.
- File size is capped at **16 MB** server-side.
- CORS is restricted to configured origins (`http://localhost:3000` by default; override via `CORS_ORIGINS` env var).
- History is stored only in the **browser's localStorage** — no user data reaches the server beyond the prediction request itself.

---

## 🔧 Troubleshooting

### Backend not starting
```bash
python --version                  # confirm Python ≥ 3.9
pip install -r requirements.txt   # reinstall if import errors
```

### Model fails to load
- Confirm `checkpoints/best_checkpoint.pth` exists (~1.3 GB).
- Confirm `results/VisiHealth_Model_Info.json` exists (included in the repo).
- If you retrained, the checkpoint vocabulary must match `VisiHealth_Model_Info.json`; the training script auto-regenerates this file on completion.

### Frontend not starting
```bash
node --version            # confirm Node ≥ 20
cd visihealth-frontend
npm install               # reinstall if module errors
rm -rf .next && npm run dev
```

### Port conflicts
```bash
# Linux / macOS — find and kill process on port 5000
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### API calls fail from frontend
- Ensure the backend server is running before using the Analyze page.
- Set `NEXT_PUBLIC_API_URL` if the backend is not on `localhost:5000`.
- Check the browser Network tab and the backend terminal for error details.

### Training — CUDA out of memory
- Reduce `batch_size` to 4 or 2 in `config.yaml` and increase `gradient_accumulation_steps` proportionally to keep the effective batch size at 64.

---

## 🚀 Deployment Notes

### Backend
```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers and a 120-second timeout (inference can be slow on first request)
FLASK_ENV=production \
CORS_ORIGINS=https://your-frontend.vercel.app \
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Frontend
The Next.js app can be deployed to Vercel in one command:
```bash
cd visihealth-frontend
npx vercel --prod
```
Set the `NEXT_PUBLIC_API_URL` environment variable in the Vercel dashboard to point to your deployed backend.

---

## 🎓 Academic Documentation

| Document | Contents |
|---|---|
| `REPORT_WRITING_MASTER_GUIDE.md` | Complete architectural blueprint and academic write-up guide |
| `THREE_MODEL_COMPARISON.md` | Deep dive into all three model iterations, bug analysis, and accuracy progression |
| `FRONTEND_PLAN.md` | Original frontend design specification |
| `PROJECT_SUMMARY.md` | High-level system overview with component explanations and sample backend↔frontend JSON exchange |
| `START_GUIDE.md` | Component inventory, troubleshooting, and performance benchmarks |

---

> **⚕️ Medical Disclaimer:** VisiHealth AI is a research prototype built for academic purposes only. It is **not** validated for clinical use and must **not** be used to make or inform actual medical diagnoses. Always consult a qualified healthcare professional.
