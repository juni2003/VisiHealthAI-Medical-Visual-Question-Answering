# VisiHealth AI - Master Guide for Final Report Writing

This document is a project-specific reference you can give to any report-writing AI or human writer.
It contains structured details for every chapter, recommended diagrams, data points, file-level implementation mapping, testing tables, formulas, and future scope guidance.

Use this as source material for writing a full professional Final Year Project report.

---

## 1. Project Snapshot (Use in Abstract/Executive Summary)

- Project name: VisiHealth AI - Medical Visual Question Answering System
- Core purpose: Answer medical-image questions using multimodal AI and provide explainability outputs.
- Input: Medical image + natural language question
- Output:
  - Predicted answer
  - Confidence score
  - Top predictions
  - ROI (region of interest)
  - AI rationale (knowledge graph-based)
  - Attention map visualization
- Dataset: SLAKE 1.0 (English subset: 642 images, 9835 QA pairs)
- Model family:
  - Visual encoder: ResNet50 (336x336 input size)
  - Text encoder: BioLinkBERT (`michiyasunaga/BioLinkBERT-base`)
  - Fusion: Cross-Attention (Multi-token spatial attention)
  - Extra heads: Dual-head predictor (CLOSED yes/no vs OPEN descriptive)
- Knowledge graph: 4,444 triplets (`kg.txt`)
- Performance (Current Latest Model):
  - Validation accuracy: 74.36%
- Backend: Flask REST API
- Frontend: Next.js + React + TypeScript + Tailwind + Framer Motion

---

## 2. Ground-Truth Technical Facts (Use Exactly)

### 2.1 Backend
- Main entry: `backend/app.py`
- Configuration: `backend/config.py`
- API routes: `backend/api/routes.py`
- Model management service: `backend/services/model_service.py`
- Input validation: `backend/utils/validators.py`
- CORS middleware: `backend/middleware/cors.py`

### 2.2 Model and Training
- CNN module: `models/cnn_model.py`
- BERT module: `models/bert_model.py`
- Fusion module: `models/fusion_model.py`
- Dataset loader: `data/dataset.py`
- Training script: `scripts/train.py`
- Demo script: `scripts/demo.py`
- Local model test script: `test_model.py`

### 2.3 Frontend
- Home route: `visihealth-frontend/app/page.tsx`
- Analyze route: `visihealth-frontend/app/analyze/page.tsx`
- History route: `visihealth-frontend/app/history/page.tsx`
- About route: `visihealth-frontend/app/about/page.tsx`
- API client: `visihealth-frontend/lib/api.ts`
- Types: `visihealth-frontend/types/api.ts`
- Header/Footer: `visihealth-frontend/components/layout/`
- Analysis components: `visihealth-frontend/components/analyzer/`
- History components: `visihealth-frontend/components/history/`

### 2.4 API Endpoints
- `GET /api/health`
- `GET /api/model/info`
- `POST /api/predict`
- `POST /api/predict/batch`
- `POST /api/visualize/attention`
- `GET /api/answers/vocabulary`

### 2.5 Important Runtime Behaviors
- Model is loaded once at startup (singleton pattern in `model_service.py`).
- Frontend stores analysis history in browser `localStorage` key: `visihealth_history`.
- Frontend communicates with backend using multipart form uploads for prediction.

---

## 3. Chapter-by-Chapter Writing Blueprint

## CHAPTER 1: INTRODUCTION

### 1.1 Project Background / Overview
Include:
- Digital healthcare demand and importance of medical imaging interpretation support.
- Need for AI-assisted question answering over medical scans.
- High-level system workflow: Upload image -> Ask question -> Receive explainable answer.
- Position project as a practical full-stack prototype, not only model experimentation.

Suggested paragraph direction:
- Start from healthcare burden and interpretation complexity.
- Introduce VQA as a multimodal AI task.
- Explain how VisiHealth AI combines vision, language, and explainability.

### 1.2 Problem Description
Define:
- Manual interpretation depends heavily on specialists and time.
- Traditional AI classifiers do not handle free-form medical questions.
- Many systems are not explainable and are difficult to trust.
- Lack of integrated user-facing systems in student/research prototypes.

### 1.3 Project Objectives
Use measurable/technical objectives:
- Develop an end-to-end medical VQA system for image + question inference.
- Integrate ResNet50 and BioLinkBERT for multimodal learning.
- Provide explainable outputs (attention map, ROI, rationale).
- Build REST APIs and a browser-based UI.
- Achieve and report measurable performance (74.36% validation accuracy).

### 1.4 Project Scope
In scope:
- Research-grade medical QA support tool.
- SLAKE dataset-based training/evaluation.
- Frontend + backend integration.

Out of scope:
- Hospital deployment, regulatory approval, EHR/PACS integration.
- Production-grade security and multi-tenant cloud ops.

Constraints/limitations to mention:
- Large class space (202 normalized answers) impacts confidence.
- History storage is local browser only.
- Performance differs CPU vs GPU.

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Overview of Core Domain Technology
Cover:
- Medical image understanding with CNNs.
- NLP understanding with Transformer/BERT families.
- Multimodal fusion in VQA systems.

### 2.2 Related Techniques / Hybrid Systems
Discuss:
- CNN + Transformer hybrids.
- Attention and explainability methods in medical AI.
- Knowledge-graph-assisted reasoning.

### 2.3 AI / Algorithms / Technologies Used
Map prior work to your implementation:
- Transfer learning with ResNet50.
- Medical-language encoding with BioLinkBERT.
- Cross-Attention multimodal fusion.
- ROI localization and attention extraction.
- KG-based rationale generation.

### 2.4 Challenges and Limitations in Existing Work
Mention:
- Imbalanced medical datasets.
- Noisy labels / synonym-rich answers.
- Explainability is often weak or absent.
- Limited end-to-end deployment in many papers.

### 2.5 Summary of Findings and Research Gap
State your gap clearly:
- Most works stop at offline metrics.
- Your project addresses full pipeline: model + API + web app + explainability.
- Remaining research gap: confidence calibration and stronger answer normalization.

---

## CHAPTER 3: REQUIREMENT SPECIFICATIONS

### 3.1 Introduction
Explain requirements as the bridge from problem statement to implementable design.

### 3.2 Existing System
Describe current alternatives:
- Manual expert interpretation
- Generic classification-only AI
- Non-integrated research code

### 3.3 Proposed System
High-level description:
- A multimodal explainable Medical VQA web platform with inference APIs and interactive frontend.

### 3.4 Requirement Specifications

### 3.4.1 Functional Requirements
- Upload medical image via UI.
- Enter natural-language question.
- Validate file type/size and question length.
- Trigger AI prediction and return structured response.
- Show answer, confidence, top predictions, ROI, rationale.
- Render attention visualization.
- Save analysis to history and allow export.

### 3.4.2 Non-Functional Requirements
- Usability: clear interface and navigation.
- Performance: acceptable response time for single-image inference.
- Reliability: robust error handling and model initialization checks.
- Maintainability: modular code organization.
- Security: request validation and CORS policy.
- Compatibility: local development on Windows.

### 3.5 Use Case Model
Actors:
- End User (primary)
- Developer/Admin (secondary)

Recommended use cases:
- Perform analysis
- View result details
- View/search history
- Export history
- Check system health/model info
- Handle invalid upload/request

### 3.5.1 Individual Use Case Template
For each use case include:
- Actor
- Description
- Preconditions
- Main Flow
- Alternate/Exception Flow
- Postconditions
- Assumptions

### 3.6 Summary
Summarize key requirements and transition to architecture/design.

---

## CHAPTER 4: DESIGN

### 4.1 System Architecture
Describe layered structure:
- UI layer (Next.js pages/components)
- API layer (Flask routes)
- Inference layer (ModelService)
- Data/config layer (checkpoint/config/vocab/KG)

### 4.2 Design Constraints

### 4.2.1 Hardware Requirements
- Development laptop/desktop (Windows in your setup)
- Sufficient RAM and storage for model/checkpoint/caches
- Optional GPU for faster training/inference

### 4.2.2 Software Requirements
- Python ecosystem (Flask, torch, transformers, PIL, matplotlib)
- JavaScript ecosystem (Next.js, React, TypeScript, Tailwind, Framer Motion)

### 4.2.3 Technical Limitations
- 202-class output space creates confidence spread.
- Answer label quality affects confidence and interpretability.
- Browser localStorage is not centralized persistence.

### 4.2.4 Assumptions
- Backend available at localhost:5000.
- Model artifacts available at configured paths.
- User inputs valid clinical image/question pairs.

### 4.3 Design Methodology
- Modular, layered design.
- Inference pipeline design with preprocessing, prediction, postprocessing, and explainability generation.

### 4.4 High Level Design
Include diagrams:
- Component architecture
- Request-response sequence (Analyze action)
- Deployment view (frontend-backend-artifacts)

### 4.5 Low Level Design
Include:
- Class-level view of CNN/BERT/Fusion/Service
- Activity diagram of prediction flow
- Data mapping: logits -> answer vocab -> response JSON

### 4.6 External Interfaces
- REST APIs
- File upload interface
- Browser localStorage interface
- Model artifact loading interface

---

## CHAPTER 5: SYSTEM IMPLEMENTATION

### 5.1 System Architecture (As Implemented)
Map design to actual files and modules (include exact paths from Section 2).

### 5.2 Tools and Technologies Used
Provide full stack table with purpose for each tool/library.

### 5.3 Development Environment
Document:
- OS, IDE, Python/Node versions
- Startup commands for backend and frontend
- Ports used and CORS setup

### 5.4 Processing Logic and Algorithms

### 5.4.1 Core Algorithm 1 (Prediction Pipeline)
- Read image and question
- Image transform and normalization
- Tokenization
- Model inference
- Softmax and top-k extraction

### 5.4.2 Core Algorithm 2 (Explainability Pipeline)
- ROI extraction from ROI head
- Attention map extraction and visualization generation
- Rationale generation using KG

### 5.4.3 Decision Fusion / Control Logic
- Fusion network combines visual + textual embeddings
- Classifier predicts final answer distribution

### 5.4.4 Safety / Exception Handling
- Input validation logic
- API try/except paths and HTTP code handling
- Frontend error toasts and fallback behavior

### 5.5 Implementation Example
Add short snippets from:
- `/api/predict` handler
- `model_service.predict`
- frontend analyze call + response rendering

### 5.6 Integration Workflow
Describe full integration:
- model load -> API ready -> frontend request -> response render -> history store

### 5.7 Testing and Calibration
Mention endpoint tests, manual inference tests, confidence interpretation thresholds.

### 5.8 Deployment and Execution
Describe local deployment steps and startup order.

### 5.9 Summary
Recap implementation outcomes.

---

## CHAPTER 6: SYSTEM TESTING AND EVALUATION

### 6.1 Test Strategy
- API endpoint testing
- Integration testing (frontend-backend)
- Functional UI tests
- Error and boundary tests

### 6.2 Test Environment
Specify machine environment, OS, ports, dependencies, artifact sizes.

### 6.3 Acceptance Criteria
Examples:
- API endpoints return expected payload structure.
- Analyze flow completes without failure.
- History save/export functions work.
- Explainability outputs render when available.

### 6.4 Functional Test Cases
Create table with:
- Test ID
- Input
- Expected output
- Actual output
- Pass/Fail

Suggested cases:
- Valid image + valid question
- Invalid image type
- Empty question
- Missing model artifacts
- Oversized file

### 6.5 Performance Testing
Track:
- Backend startup time
- Inference latency
- API response time
- CPU/RAM usage (if measured)

### 6.6 Accuracy Evaluation
Report:
- Validation and test accuracy
- Optional per-class/per-question-type analysis
- If available, precision/recall/F1

### 6.7 User Evaluation
Collect feedback on usability, clarity, trust in outputs.

### 6.8 Reliability and Safety Testing
Run repeated requests, invalid input stress, and failure handling scenarios.

### 6.9 Quality Metrics and Formulas
Use formulas:
- Accuracy = (TP + TN) / (TP + TN + FP + FN)
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 = 2 * (Precision * Recall) / (Precision + Recall)
- Mean response time = sum(latency) / N

### 6.10 Discussion
Interpret strengths and weaknesses:
- Strengths: integrated, explainable, deployable prototype
- Weaknesses: confidence spread, label noise, local history limits

### 6.11 Conclusion
State readiness level: strong academic prototype, not clinical product.

---

## CHAPTER 7: CONCLUSIONS

### 7.1 Conclusion
Summarize complete pipeline achievement and evaluation outcomes.

### 7.2 Future Scope
Practical improvements:
- Better answer normalization and synonym merging
- Confidence calibration (temperature scaling)
- Advanced fusion/attention methods
- DB-backed history and auth
- Dockerized deployment and CI/CD
- Broader dataset and external validation

---

## 4. Diagram Checklist (Strongly Recommended)

Create these diagrams for a professional report:
- Problem context diagram
- Proposed solution block diagram
- UML use case diagram
- Use case narrative tables
- High-level component architecture
- Sequence diagram: Analyze request (`/api/predict`)
- Sequence diagram: History workflow (save/read/export)
- Activity diagram: end-to-end prediction pipeline
- Data flow diagram (DFD)
- Class diagram (ModelService + model blocks)
- API contract diagram
- Deployment diagram (local setup)
- UI navigation flow diagram
- Testing workflow diagram
- Performance/accuracy charts
- Failure handling flowchart
- Future roadmap diagram

---

## 5. Suggested Tables to Include in Final Report

- System requirements table (hardware/software)
- API endpoint specification table
- Functional requirement table
- Non-functional requirement table
- Dataset statistics table
- Model architecture configuration table
- Testing matrix (expected vs actual)
- Performance benchmark table
- Risk and mitigation table
- Future enhancement prioritization table

---

## 6. Ready Prompts for Another AI Writer

Use these prompts with another AI tool.

Prompt A (Full Chapter Expansion):
"Using the provided VisiHealth AI guide, write Chapter [X] in formal academic style for a final year project report. Use project-specific details only. Include introduction, technical explanation, tables where appropriate, and transitions to next sections."

Prompt B (Diagram Content Draft):
"Using this project guide, generate precise text content for the [diagram name], including actors/components, arrows, labels, and short explanation paragraph."

Prompt C (Testing Section):
"Generate Chapter 6 testing and evaluation with realistic test case tables, acceptance criteria, formulas, and analytical discussion based on the VisiHealth AI project facts."

Prompt D (Implementation with File Mapping):
"Write Chapter 5 implementation with explicit mapping to file paths and module responsibilities from the provided project guide."

---

## 7. Important Consistency Rules for Final Report

- Always use one project title format consistently.
- Keep metric values consistent across all chapters.
- Clearly distinguish design proposal vs implemented reality.
- Avoid claiming clinical deployment or regulatory compliance.
- Mention limitations honestly and propose realistic future scope.
- Ensure diagrams and text use the same module names.

---

## 8. Optional Appendices You Can Add

- Appendix A: API request/response samples
- Appendix B: Configuration file snapshot (`config.yaml`)
- Appendix C: Key code snippets
- Appendix D: Additional test logs
- Appendix E: User guide / operating steps

---

## 9. Final Notes for Professional Quality

- Prefer concise, technical, evidence-based writing.
- Use chapter opening and closing paragraphs to improve flow.
- Include at least one figure or table every 1-2 pages in technical chapters.
- Cross-reference figures/tables in text.
- Use uniform tense and terminology throughout the report.

This guide is intentionally detailed so a new writer (human or AI) can produce a complete professional report without direct codebase access.
