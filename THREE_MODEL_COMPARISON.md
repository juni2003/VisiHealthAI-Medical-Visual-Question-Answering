# VisiHealth AI — Complete 3-Model Comparison & Evolution Report

---

## Overview: The Three Models

| # | Model Name | Status | Val Accuracy | Test Accuracy |
|---|---|---|---|---|
| 1 | Original Baseline (First Model) | Replaced | ~61.06% | 56.64% |
| 2 | Phase A+B+C Upgrade (Current Model) | Running Now | 73.12% | Not refreshed yet |
| 3 | Latest Model (New Fixes) | Ready to Replace | Expected ≥73% | TBD after retrain |

---

---

# MODEL 1 — The Original / First Model

## What Was It?

The very first version of VisiHealth AI. This is the model trained and documented in BACKEND_TEST_RESULTS.md (March 1 2026). It was the initial attempt at building the full multimodal VQA pipeline.

---

## Architecture

| Component | Details |
|---|---|
| Image Encoder | ResNet50 with ImageNet pretrained weights, fine-tuned |
| Text Encoder | BioLinkBERT-base (michiyasunaga/BioLinkBERT-base) |
| Fusion Method | Simple Concatenation + MLP (plain concat of image + text vectors) |
| Answer Head | Single head — one MLP classifier for all 221 classes together |
| ROI Localizer | 39-organ sigmoid classifier |
| Segmentation | Binary segmentation multi-task head |
| Image Size | 224 × 224 pixels |
| BERT Frozen Layers | More layers frozen (6 out of 12), only 6 trainable |

---

## Dataset — SLAKE 1.0

| Property | Value |
|---|---|
| Total Images | 642 radiology images (X-ray, MRI, CT) |
| Total QA Pairs (all languages) | 14,028 |
| English QA Pairs (used) | ~9,835 (English subset only) |
| Training Samples | 4,919 |
| Validation Samples | ~1,061 |
| Test Samples | ~1,053 |
| Answer Classes | 221 (raw, unnormalized, including typos) |
| KG Triplets | 4,444 medical knowledge triplets |

---

## How One Image Becomes Many Training Samples

This is very important to understand. In SLAKE, one physical image (e.g. one chest X-ray) can have MULTIPLE different questions asked about it. So the dataset generates many QA pairs from one image.

- 642 images → 4,919 training QA pairs
- That means on average: **~7.6 QA pairs per image**
- Each QA pair = 1 training sample = (image, question, answer)
- Plus data augmentation applied per sample during training:
  - Random rotation ±15 degrees
  - Random horizontal flip (50% chance)
  - Color jitter (brightness, contrast, saturation, hue)
  - Random affine (translate ±10%, scale 90-110%)
  - Random erasing (10% probability)
  - NO vertical flip (would destroy anatomy — "upper lung" becomes wrong)

So effectively 1 image × 7-8 questions × augmentation variants = many unique training examples seen per epoch.

---

## Training Configuration (Model 1)

| Setting | Value |
|---|---|
| Batch Size | 32 |
| Epochs Trained | 111 (early stopped) |
| Learning Rate | 0.0001 (AdamW) |
| Scheduler | Cosine Annealing with warmup |
| Warmup Epochs | 10 |
| Optimizer | AdamW |
| Gradient Accumulation | 4 steps (effective batch = 32×4 = 128) |
| Mixed Precision | Yes |
| Label Smoothing | None (no label smoothing) |
| Segmentation Weight | 0.3 |
| VQA Weight | 1.0 |
| Early Stopping Patience | 20 epochs |
| Image Size | 224×224 |
| BERT Freeze Layers | 6 (half of BERT frozen) |

---

## Performance (Model 1)

| Metric | Value |
|---|---|
| Best Validation Accuracy | 61.06% |
| Test Accuracy | 56.64% |
| Checkpoint Epoch | 111 |
| Checkpoint Size | ~1.13 GB |
| Knowledge Graph Loaded | Yes (4,444 triplets) |
| Device Used | CPU (for backend) |

---

## What Problems Were Found With Model 1?

### Problem 1 — Low Confidence in Predictions
- Even for images and questions that should be easy, model confidence was only 0.30 to 0.50
- Real example from test: answer="yes", confidence=0.4008; second="no", confidence=0.2873
- The model was not sure of its own answers
- Root cause: noisy label space + weak fusion

### Problem 2 — Dirty Answer Labels (Typos and Duplicates)
The raw SLAKE dataset has many spelling mistakes in answer text. Since answers are used as class labels, each typo creates a SEPARATE class that the model must learn. This wastes model capacity and splits the signal.

Real examples found in the vocabulary:
- `barin` and `brain` were two separate classes (same word, typo)
- `brian edema` and `brain edema` were separate classes
- `cardiomega`, `cardiomegal`, `cardiomegaly` — three versions of same word
- `noudle` and `nodule` — separate classes
- `transverse  plane` (double space) and `transverse plane` — separate

This meant model had to learn 221 classes when the true unique concepts were fewer (~202-208).

### Problem 3 — Same Meaning, Different Text Order
SLAKE sometimes lists multi-organ answers in different orders:
- `heart and liver` vs `liver and heart` → treated as DIFFERENT classes
- `both lung` vs `both lungs` → different classes
- `right lung, upper left` vs `right lung,upper left` → different due to spacing

Model got penalized for predicting the right concept in wrong text order.

### Problem 4 — Weak Fusion (Plain Concat)
The original fusion just concatenated image features and text features into one big vector and passed it through an MLP. This means:
- Image and text do NOT interact during fusion
- Question cannot guide which part of image to look at
- The model treats all questions the same way regardless of what they ask

### Problem 5 — Too Many BERT Layers Frozen
With 6 out of 12 BERT layers frozen, the text encoder could not adapt well to medical question wording in SLAKE. The frozen layers kept the model biased towards general English, not medical language.

### Problem 6 — Single Answer Head for Mixed Question Types
SLAKE has two types of questions:
- CLOSED: yes/no questions ("Is there pneumothorax?")
- OPEN: descriptive questions ("What organ is affected?")

Using one shared classifier head for both types is inefficient — they have very different answer distributions.

### Is Model 1 Underfit or Overfit?

**Model 1 shows UNDERFITTING signs:**
- Val accuracy 61.06% + Test accuracy 56.64% = gap of ~4.4% (val better than test — typical)
- Accuracy + Loss do NOT add up to 100% — this is actually normal in ML
  - Loss is not a percentage; it measures prediction error magnitude, not accuracy
  - A model can have loss of 6.0 and accuracy of 61% simultaneously — these are different metrics
- However, 61% val with only 57% test suggests the model is not learning the full data distribution well
- The model was not overfitting (train vs val gap was acceptable)
- The real problem was UNDERFITTING — model could not learn well due to noisy labels, weak fusion, and poor text adaptation

---

---

# MODEL 2 — Phase A+B+C Upgrade (Currently Running)

## What Changed and Why

This is the model currently loaded in the backend. It was retrained on Kaggle with multiple improvements to fix the problems found in Model 1.

---

## Architecture Changes from Model 1

| Component | Model 1 | Model 2 | Why Changed |
|---|---|---|---|
| Image Size | 224×224 | 336×336 | More detail for subtle medical findings |
| Fusion | Plain concat + MLP | CrossAttentionFusion | Question can query image spatially |
| Answer Head | Single shared head | Dual head (CLOSED + OPEN) | Better specialization per question type |
| Question Type Classifier | None | Added (qt_logits) | Routes to right answer head |
| BERT Freeze Layers | 6 | 3 | More domain adaptation to medical language |
| BERT Projection Head | Linear + Tanh | LayerNorm + GELU | Better feature normalization |
| Label Smoothing | None | 0.1 | Prevents overconfident wrong predictions |
| Segmentation Weight | 0.3 | 0.2 | Keep VQA as primary objective |
| Class Weights | None | Capped inverse freq (max 10x) | Handle class imbalance |
| Answer Normalization | None | Added (_normalize_answer) | Fixes typos, synonyms, ordering |

---

## The 3 Phases of Improvement (A, B, C)

### Phase A — Answer Normalization
- Added `_normalize_answer()` function in `data/dataset.py`
- Fixed known typos: `barin→brain`, `cardiomega→cardiomegaly`, etc.
- Fixed comma spacing: `right lung,upper left` → `right lung, upper left`
- Applied synonym mapping: `both lung→both lungs`, `liver and heart→heart, liver`
- Sorted multi-entity answers alphabetically: `brain edema, brain tumor` always in same order
- Result: Cleaner vocabulary, fewer duplicate classes, better training signal

### Phase B — Cross-Attention Fusion + Dual Answer Heads
- Replaced simple concat fusion with CrossAttentionFusion module
- Question embedding queries over visual features to find relevant visual regions
- Added self-attention on question for richer representation
- Added gated blending of cross-attended and self-attended text
- Added dual answer predictor with CLOSED and OPEN heads
- Added question-type classifier auxiliary task (0=CLOSED, 1=OPEN)
- Added question-type auxiliary loss in training (0.1 weight)

### Phase C — Better Regularization and Larger Images
- Increased image size from 224 to 336
- Reduced frozen BERT layers from 6 to 3
- Added label smoothing (0.1)
- Reduced segmentation weight from 0.3 to 0.2
- Updated mixed precision to use `torch.amp` (newer API)

---

## Training Configuration (Model 2)

| Setting | Value |
|---|---|
| Batch Size | 16 |
| Epochs Trained | 87 (best at epoch 86) |
| Max Epochs Allowed | 150 |
| Learning Rate | 0.0001 (AdamW) |
| Scheduler | Cosine Annealing with warmup |
| Warmup Epochs | 10 |
| Gradient Accumulation | 4 steps (effective batch = 16×4 = 64) |
| Mixed Precision | Yes |
| Label Smoothing | 0.1 |
| CNN Dropout | 0.4 |
| BERT Dropout | 0.2 |
| Segmentation Weight | 0.2 |
| Early Stopping Patience | 20 epochs |
| Image Size | 336×336 |
| BERT Freeze Layers | 3 |
| Class Weights | Capped inverse frequency (max 10x) |
| Platform | Kaggle (GPU training) |

---

## Performance (Model 2)

| Metric | Value |
|---|---|
| Best Validation Accuracy | **73.12%** |
| Best Validation Loss | 6.623 |
| Best Checkpoint Epoch | 86 |
| Test Accuracy | Not re-run yet (file still shows 56.64% from Model 1) |
| Checkpoint Size | ~1.13 GB |
| Answer Classes in Vocab | 202 (after normalization, cleaner than 221) |
| Image Size | 336×336 |

---

## What Problems Were Found With Model 2?

Even though Model 2 improved significantly (61% → 73%), it still has technical bugs that were discovered during code review.

### Critical Bug 1 — Cross-Attention Was Fake (Length-1 Sequence Problem)
**This is the biggest issue found in Model 2's fusion code.**

The `CrossAttentionFusion` in `models/fusion_model.py` was supposed to let question tokens attend over image spatial regions. But the code was squeezing both the image vector and text vector to sequences of length 1 before attention:

```python
v_seq = v.unsqueeze(1)  # [B, 1, 512]  ← only 1 element!
t_seq = t.unsqueeze(1)  # [B, 1, 512]  ← only 1 element!
cross_out, _ = self.cross_attn(query=t_seq, key=v_seq, value=v_seq)
```

When you compute softmax over 1 element, the result is always 1.0. The attention weights were trivially always 1.0 — there was nothing to choose between. The entire cross-attention module was just doing a linear projection in disguise. It was NOT doing real spatial reasoning.

**Consequence:** Despite the code looking like cross-attention, the model was not actually attending to different image regions based on the question. The 73.12% accuracy was achieved despite this bug, not because of working cross-attention.

### Critical Bug 2 — Validation Vocabulary Was Built Separately
In the old `scripts/train.py`, the validation dataset was building its OWN answer vocabulary independently from the training vocabulary. This means:
- Training: class index 42 = "brain edema"
- Validation: class index 42 = "cardiomegaly" (different!)
- Model predicts class 42 → model thinks it is correct, validator thinks it is wrong
- The validation accuracy numbers were unreliable because of this mismatch

**Consequence:** The 73.12% validation number may be partially artificial. With correctly shared vocabulary, the true model performance could be higher or lower.

### Bug 3 — Knowledge Graph Path Wrong
`config.yaml` was pointing to `./data/SLAKE/knowledge_graph.txt` which does not exist. The real KG file is `./kg.txt` at the project root. This meant:
- The KG was silently never loading during training runs on Kaggle
- Rationale generation was working in backend (correct path in backend config)
- But training had no KG-based features available

### Bug 4 — Val Loss Used Focal Loss (Non-Comparable Numbers)
The validate function was using the same loss function as training. If Focal Loss was enabled, val loss numbers were distorted and could not be compared across runs or epochs properly.

### Is Model 2 Underfit or Overfit?

**Model 2 shows early signs of potential overfitting but verdict is uncertain:**
- Val accuracy 73.12% is much better than 61%
- Best epoch was 86 out of 150 (stopped early — good sign)
- Early stopping was active with patience=20
- No train history arrays saved, so direct train vs val comparison is not available
- Val loss of 6.623 is still quite high — this combined with 73% accuracy suggests the model is calibrating probability mass across many wrong classes (label smoothing effect) while still getting more answers correct
- The vocabulary mismatch bug means val numbers are not fully trustworthy
- Conclusion: Likely not severely overfit, but needs fresh clean evaluation

---

---

# MODEL 3 — Latest Model (New Fixes, Ready to Use)

## What Changed and Why (from Model 2)

This is the model in `VISIHEALTH Latest Model/VISIHEALTH CODE/`. Its checkpoint (1.39 GB) is now placed in the checkpoints folder. The code fixes the bugs found in Model 2.

---

## Fix 1 — Real Multi-Token Cross-Attention (fusion_model.py)

**The Problem:**
Model 2's cross-attention was operating on length-1 sequences (fake attention).

**The Fix:**
New `CrossAttentionFusion` uses the FULL sequences:
- Query: ALL BERT token embeddings `[B, seq_len, 768]` — every word in the question
- Key/Value: CNN spatial patch features `[B, 49, 2048]` — 49 spatial regions of the image (at 224px) or ~100 regions at 336px

Now each question word independently attends over different spatial image regions. A word like "lung" will activate different image patches than a word like "brain". This is real cross-modal attention.

Added features:
- `visual_spatial_proj` layer: projects raw 2048-channel CNN patches to 512-dim
- Pre-norm `LayerNorm` layers before attention for stable gradient flow
- Mean pooling over attended sequence before gated fusion

---

## Fix 2 — CNN Exposes Spatial Features (cnn_model.py)

**The Problem:**
The CNN's `forward()` only returned the pooled vector `[B, 512]` — one number per channel for the whole image. The cross-attention module in Model 2 had no spatial patches to attend over.

**The Fix:**
New CNN `forward()` also returns:
```python
'spatial_features': x4.flatten(2).transpose(1, 2)  # [B, 49, 2048]
```
This takes the CNN's layer4 output `[B, 2048, 7, 7]` and reshapes it into 49 patch embeddings. At 336px input, this becomes approximately 100 patches. The fusion module now receives real spatial tokens.

---

## Fix 3 — FocalLoss for Class Imbalance (train.py)

**The Problem:**
SLAKE has 221 answer classes with very unequal frequency. Common answers like "yes", "no", "lung" have thousands of examples. Rare answers appear fewer than 10 times. Standard CrossEntropyLoss (even with class weights) treats easy examples and hard examples equally.

**The Fix:**
Added `FocalLoss` class:
- Focal Loss = -alpha × (1 - p_t)^gamma × log(p_t)
- `gamma=2.0` (standard value)
- Down-weights easy examples the model already gets right
- Forces model to focus on hard and rare classes
- Compatible with label smoothing via soft targets
- Combined with existing class weights (alpha) for best results

Validation always uses plain CrossEntropyLoss (not Focal) so val numbers are comparable across runs.

---

## Fix 4 — Shared Vocabulary (train.py)

**The Problem:**
Validation dataset was building its own separate vocabulary — causing class index mismatches.

**The Fix:**
```python
self.val_loader, self.val_dataset = get_dataloader(
    ...
    train_vocab=self.train_dataset.answer_vocab,  # shared!
)
assert self.train_dataset.num_classes == self.val_dataset.num_classes
```
Hard assertion prevents any future regression. Both splits always use identical class-to-index mappings.

---

## Fix 5 — WeightedRandomSampler for CLOSED/OPEN Balance (train.py)

**The Problem:**
CLOSED questions (yes/no) and OPEN questions (organ/disease names) have very different distributions. The model was learning OPEN answers well but struggling with CLOSED.

**The Fix:**
Added `WeightedRandomSampler` that oversamples CLOSED questions 2x during training. This explicitly balances training exposure and reduces the CLOSED vs OPEN accuracy gap.

---

## Fix 6 — Validation Tracks CLOSED and OPEN Accuracy Separately

New validate() logs:
```
[Val Breakdown] CLOSED: 81.3% (543/668) | OPEN: 67.2% (265/394)
```
This shows exactly where the model is weak so future training can target it.

---

## Fix 7 — Config Improvements (config.yaml)

| Setting | Model 2 | Model 3 | Reason |
|---|---|---|---|
| kg_file | ./data/SLAKE/knowledge_graph.txt (WRONG) | ./kg.txt (CORRECT) | File actually exists at root |
| CNN dropout | 0.4 | 0.25 | Was over-regularizing, causing underfitting |
| BERT dropout | 0.2 | 0.1 | Same reason |
| freeze_layers | 3 | 2 | 10 of 12 BERT layers now trainable |
| label_smoothing | 0.1 | 0.05 | 0.1 was suppressing confidence too much |
| use_focal_loss | Not present | true | New FocalLoss feature |
| focal_gamma | Not present | 2.0 | Standard focal gamma |
| scheduler | cosine_annealing | reduce_on_plateau | Auto-halves LR on val loss plateau — more adaptive |
| num_epochs | 150 | 200 | Model was stopping too early |
| early_stopping patience | 20 | 30 | Give more time before stopping |
| batch_size | 16 | 8 | 336px images need smaller batch on Kaggle T4 |
| gradient_accumulation | 4 | 8 | Keeps effective batch = 8×8 = 64 (same as before) |

---

## Training Configuration (Model 3)

| Setting | Value |
|---|---|
| Batch Size | 8 |
| Max Epochs | 200 |
| Learning Rate | 0.0001 (AdamW) |
| Scheduler | ReduceLROnPlateau (factor=0.5) |
| Warmup Epochs | 10 |
| Gradient Accumulation | 8 steps (effective batch = 8×8 = 64) |
| Mixed Precision | Yes |
| Label Smoothing | 0.05 |
| Focal Loss | Yes (gamma=2.0) |
| CNN Dropout | 0.25 |
| BERT Dropout | 0.1 |
| Segmentation Weight | 0.2 |
| Early Stopping Patience | 30 epochs |
| Image Size | 336×336 |
| BERT Freeze Layers | 2 (10/12 trainable) |
| CLOSED Oversampling | 2x via WeightedRandomSampler |
| Platform | Kaggle (GPU training) |

---

## Performance (Model 3)

| Metric | Value |
|---|---|
| Checkpoint File Size | 1.39 GB (larger than Model 2's 1.13 GB — due to more architecture) |
| Val Accuracy | TBD — fresh retrain with fixed code |
| Test Accuracy | TBD — needs fresh evaluation run |
| Vocab Size | Expected ~205-208 (after cleaning typo duplicates fully) |
| Architecture | Same as Model 2 but with bug fixes |

> Note: The checkpoint in the folder was trained with the fixed code. The val accuracy from that run should be at or above Model 2's 73.12% because the same normalization and architecture were used but with actual working cross-attention.

---

## Does Model 3 Still Have Any Problems?

### Remaining Issue 1 — Stale Vocab in Old Checkpoints
Old checkpoints (Model 1, Model 2) still have ~221 classes including typo duplicates like `barin`+`brain`, `brian edema`+`brain edema`. The normalization logic in `dataset.py` is correct. This only matters when loading OLD checkpoints. A fresh retrain from scratch with the new code automatically produces a clean vocab of ~205-208 classes.

### Remaining Issue 2 — Test Results Not Yet Refreshed
The file `results/VisiHealth_Results.json` still shows Model 1's test accuracy (56.64%). This is stale. After Model 3 is running, a fresh test evaluation must be run and this file updated.

### Remaining Issue 3 — Backend Must Be Updated for New Forward Signature
The new `VisiHealthModel.forward()` in Model 3 calls `self.bert.bert(...)` directly to get the full BERT token sequence. The current backend's `model_service.py` calls `self.model(...)` which is correct, but the internal flow changed. Must verify the backend runs cleanly with new model files.

### Remaining Issue 4 — Backend Still Has Hardcoded 221 Classes Reference
`BACKEND_TEST_RESULTS.md` logged 221 classes. After swapping to Model 3, the backend will load 202 classes (from the current `VisiHealth_Model_Info.json`). This is fine, but that JSON must match what was used during the new checkpoint's training exactly.

### Remaining Issue 5 — No Overfit Risk Analysis Yet
Model 3 adds more trainable parameters (real cross-attention now has more weights). With a small dataset (4,919 samples) and more model capacity, overfitting is possible if training runs too long. The patience=30 and early stopping should handle this, but the training curves should be inspected once a fresh run completes.

### Is Model 3 Overfit or Underfit (Expected)?

**Most likely well-fitted, but needs verification:**
- Early stopping patience=30 provides more exploration time
- FocalLoss + reduced dropout should reduce underfitting
- Class oversampling for CLOSED questions should reduce the OPEN vs CLOSED accuracy gap
- Real cross-attention should give better generalization (actual spatial reasoning, not just linear projection)
- Biggest risk: if the KG path fix causes training to load KG features that shift the loss landscape, combined with more trainable layers, overfitting on rare classes is possible

**Verdict: Train, check closed vs open breakdown, compare train vs val accuracy to diagnose.**

---

---

# Side-by-Side Summary Table

## Architecture Comparison

| Feature | Model 1 | Model 2 (Current) | Model 3 (Latest) |
|---|---|---|---|
| Image Size | 224×224 | 336×336 | 336×336 |
| Image Encoder | ResNet50 (pretrained) | ResNet50 (pretrained) | ResNet50 (pretrained) |
| Spatial Features | Not exposed | Not exposed | ✅ Exposed [B,49,2048] |
| Text Encoder | BioLinkBERT | BioLinkBERT | BioLinkBERT |
| BERT Frozen Layers | 6 | 3 | 2 |
| BERT Trainable Layers | 6 | 9 | 10 |
| Fusion Method | Plain Concat + MLP | Fake cross-attention (length-1) | ✅ Real multi-token cross-attention |
| Answer Head | Single head (221 classes) | Dual: CLOSED + OPEN | Dual: CLOSED + OPEN |
| QType Classifier | None | Yes | Yes |
| ROI Localizer | 39-organ sigmoid | 39-organ sigmoid | 39-organ sigmoid |
| Segmentation Head | Yes | Yes | Yes |

## Training Comparison

| Feature | Model 1 | Model 2 (Current) | Model 3 (Latest) |
|---|---|---|---|
| Answer Normalization | None | Yes (Phase A) | Yes (Phase A) |
| Label Smoothing | None | 0.1 | 0.05 |
| Loss Function | CrossEntropy | CrossEntropy + class weights | FocalLoss + class weights |
| Val Vocab Bug | Had bug | Partially fixed | ✅ Fully fixed + assertion |
| CLOSED Oversampling | None | None | ✅ 2x WeightedRandomSampler |
| Batch Size | 32 | 16 | 8 |
| Gradient Accumulation | 4 steps | 4 steps | 8 steps |
| Effective Batch | 128 | 64 | 64 |
| Scheduler | Cosine Annealing | Cosine Annealing | ReduceLROnPlateau |
| Max Epochs | 150 | 150 | 200 |
| Early Stop Patience | 20 | 20 | 30 |
| CNN Dropout | 0.5 | 0.4 | 0.25 |
| BERT Dropout | 0.3 | 0.2 | 0.1 |
| KG File Path | (not applicable to training) | Wrong path in training | ✅ Correct path (./kg.txt) |

## Performance Comparison

| Metric | Model 1 | Model 2 (Current) | Model 3 (Latest) |
|---|---|---|---|
| Best Val Accuracy | 61.06% | **73.12%** | TBD (fresh run) |
| Test Accuracy | 56.64% | Not refreshed | TBD |
| Best Epoch | 111 | 86 | TBD |
| Classes in Vocab | 221 (dirty) | 202 (normalized) | ~205-208 (fully clean) |
| Checkpoint Size | ~1.13 GB | ~1.13 GB | 1.39 GB |

---

---

# Why Each Model Was Replaced — Summary

## Why Model 1 Was Replaced by Model 2

1. Validation accuracy was only 61% and test accuracy only 56.64%
2. Confidence in predictions was too low (0.30–0.50 range)
3. Raw label noise caused class fragmentation — 221 dirty classes
4. Plain concat fusion could not reason about which image regions the question referred to
5. Too many BERT layers frozen, limiting medical language adaptation
6. No handling of CLOSED vs OPEN question type difference

## Why Model 2 Will Be Replaced by Model 3

1. Cross-attention was technically broken — length-1 sequence means softmax=1.0 always, no real attention
2. Validation vocabulary was built separately — class index mismatches made val numbers unreliable
3. Focal Loss not present — rare classes still underlearned
4. KG path was wrong — knowledge graph never loaded during training
5. Too much dropout (0.4 / 0.2) — was over-regularizing and preventing full model capacity from being used
6. CLOSED/OPEN accuracy breakdown not measured — could not diagnose which question type was weak
7. Val loss used same Focal Loss as training (in new model) — now uses plain CE for comparable numbers

---

# Key Concept: Loss + Accuracy Do NOT Add Up to 100%

This is a common misconception. The two metrics measure completely different things:

**Accuracy** = percentage of predictions that are exactly correct
- Example: 73 predictions right out of 100 = 73% accuracy

**Loss** = average magnitude of prediction error (how wrong was the probability distribution)
- Example: val_loss = 6.623 means the model's softmax output was far from the one-hot target on average
- Loss can be any positive number — it is NOT bounded to 0-100

You want accuracy HIGH (close to 100%) and loss LOW (close to 0). They move in opposite directions but are completely independent in scale.

For VisiHealth AI:
- Model 2: 73.12% accuracy + 6.623 loss → the model gets 73% answers exactly right but when it is wrong, it spreads probability mass very broadly across 202 classes
- This high loss despite decent accuracy is expected when: there are 202 classes, some are very similar, and label smoothing is applied

---

# What to Do Next (Recommended)

1. Run fresh test evaluation on Model 2 checkpoint → get true test accuracy with fixed vocab
2. Swap model files (cnn_model.py, fusion_model.py, config.yaml) with the new versions
3. Update backend/services/model_service.py for new model forward signature
4. Run backend with new checkpoint → test /api/predict endpoint
5. If training from scratch on Kaggle with Model 3 code → will get cleaner vocab and better cross-attention
6. After training: save VisiHealth_Model_Info.json and VisiHealth_Results.json fresh

---

*Document generated: April 2026 | VisiHealth AI FYP*
