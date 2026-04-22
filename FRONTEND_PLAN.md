# 🎨 VisiHealth AI - Complete Frontend Development Plan

## 📋 **Technology Stack**

### **Core Framework**
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety

### **Styling & UI**
- **Tailwind CSS 3** - Utility-first CSS
- **Shadcn/ui** - Beautiful component library
- **Framer Motion** - Animations
- **Lucide React** - Modern icons

### **3D & Visualization**
- **Three.js** - 3D graphics library
- **React Three Fiber** - React renderer for Three.js
- **React Three Drei** - Useful helpers for R3F
- **GSAP** - Advanced animations

### **State Management & Data**
- **Zustand** - Lightweight state management
- **React Query** - Server state management
- **Axios** - HTTP client

### **Additional Features**
- **React Dropzone** - File upload
- **React Hot Toast** - Notifications
- **Chart.js / Recharts** - Data visualization
- **SWR** - Data fetching

---

## 🏗️ **Project Structure**

```
visihealth-frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   ├── analyze/
│   │   └── page.tsx             # Analysis page
│   ├── history/
│   │   └── page.tsx             # History page
│   ├── about/
│   │   └── page.tsx             # About page
│   ├── api/                     # API routes (if needed)
│   └── globals.css              # Global styles
│
├── components/                   # React components
│   ├── layout/
│   │   ├── Header.tsx           # Navigation header
│   │   ├── Footer.tsx           # Footer
│   │   └── Sidebar.tsx          # Sidebar navigation
│   │
│   ├── home/
│   │   ├── Hero3D.tsx           # 3D hero section
│   │   ├── Features.tsx         # Feature cards
│   │   ├── HowItWorks.tsx       # Process explanation
│   │   └── Stats.tsx            # Statistics display
│   │
│   ├── analyzer/
│   │   ├── ImageUploader.tsx    # Drag & drop uploader
│   │   ├── QuestionInput.tsx    # Question form
│   │   ├── PredictionResult.tsx # Result display
│   │   ├── AttentionMap.tsx     # Attention visualization
│   │   ├── ConfidenceGauge.tsx  # 3D confidence meter
│   │   └── ROIViewer.tsx        # Region of interest viewer
│   │
│   ├── 3d/
│   │   ├── Brain3D.tsx          # 3D brain model
│   │   ├── MedicalScan3D.tsx    # 3D scan visualization
│   │   ├── ParticleBackground.tsx # Particle effects
│   │   └── FloatingElements.tsx  # Animated elements
│   │
│   ├── ui/                       # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Badge.tsx
│   │   ├── Progress.tsx
│   │   └── Modal.tsx
│   │
│   └── shared/
│       ├── LoadingSpinner.tsx
│       └── ErrorBoundary.tsx
│
├── lib/                          # Utilities & helpers
│   ├── api.ts                   # API client
│   ├── store.ts                 # Zustand store
│   ├── utils.ts                 # Helper functions
│   └── constants.ts             # Constants
│
├── hooks/                        # Custom React hooks
│   ├── useAnalysis.ts           # Analysis logic
│   ├── useUpload.ts             # Upload handling
│   └── use3D.ts                 # Three.js helpers
│
├── types/                        # TypeScript types
│   ├── api.ts                   # API types
│   └── models.ts                # Data models
│
├── public/                       # Static assets
│   ├── models/                  # 3D models
│   ├── images/
│   └── textures/
│
├── styles/
│   └── animations.css           # Custom animations
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

---

## 📄 **Page Breakdown (4+ Pages)**

### **1. HOME PAGE** (`/`)

#### **Purpose:**
Landing page that introduces VisiHealth AI, showcases features, and drives users to analyze images.

#### **Sections:**

**A. Hero Section (3D Interactive)**
- **3D Element**: Rotating medical scan/brain model using Three.js
- **Headline**: "AI-Powered Medical Visual Question Answering"
- **Subheadline**: "Get instant answers to medical image questions with 74% accuracy"
- **CTA Buttons**: 
  - "Try Now" → Navigate to `/analyze`
  - "Learn More" → Scroll to features
- **Background**: Animated particle network (DNA helix or neural network)

**B. Features Section**
Grid of 6 feature cards:
1. 🧠 **Advanced AI** - BioBERT + ResNet50
2. 📊 **High Accuracy** - 74% validation accuracy
3. 🎯 **ROI Detection** - 39 organ regions
4. 💡 **Explainable AI** - Knowledge graph rationales
5. ⚡ **Real-time** - Instant predictions
6. 🔒 **Secure** - Privacy-focused

**C. How It Works**
3-step animated process:
1. **Upload** → Medical scan image
2. **Ask** → Type your question
3. **Analyze** → Get AI answer + explanation

**D. Statistics Dashboard**
Animated counters:
- 9,835 Training Samples
- 202 Answer Classes
- 4,444 Knowledge Triplets
- 74% Accuracy

**E. Sample Demo**
Interactive carousel showing example predictions with images

**F. CTA Section**
Large "Start Analyzing" button with 3D hover effect

---

### **2. ANALYZE PAGE** (`/analyze`)

#### **Purpose:**
Main application page where users upload images and ask questions.

#### **Layout:**

**A. Left Panel (40% width)**

1. **Image Upload Zone**
   - Drag & drop area with 3D drop animation
   - Or click to browse
   - Preview thumbnail with 3D card flip
   - Clear/Replace options

2. **Question Input**
   - Large text area
   - Character counter (max 500)
   - Suggested questions dropdown
   - Voice input button (optional)

3. **Action Button**
   - "Analyze Image" with loading animation
   - Disabled until image + question provided

**B. Right Panel (60% width)**

1. **Result Display** (shows after analysis)
   - **Answer Card** (3D elevated card)
     - Large answer text
     - 3D Confidence gauge (circular progress with Three.js)
     - Color-coded: Green (>70%), Yellow (40-70%), Red (<40%)
   
   2. **Top 3 Predictions**
     - Horizontal bar chart
     - Animated bars with percentages
   
   3. **Visual Attention Map**
     - Side-by-side: Original image | Attention overlay
     - Toggle switch
     - 3D depth effect on hover
   
   4. **ROI Information**
     - Detected region badge
     - 3D organ model preview (if available)
     - Confidence score
   
   5. **Explanation Section**
     - Knowledge graph rationale
     - Expandable/collapsible
     - Highlighted medical terms
   
   6. **Actions**
     - Download result as PDF
     - Save to history
     - Share (copy link)
     - Try another image

**C. Background**
Subtle 3D particle effect or floating geometric shapes

---

### **3. HISTORY PAGE** (`/history`)

#### **Purpose:**
View past analyses, compare results, manage saved scans.

#### **Features:**

**A. Header**
- Search bar (filter by date, answer, etc.)
- Sort options (newest, highest confidence)
- Filter by date range

**B. Analysis Cards Grid**
Each card shows:
- Thumbnail image (3D hover tilt effect)
- Question asked
- Answer given
- Confidence score
- Date/time
- Actions: View details, Delete, Export

**C. Detailed View Modal**
Click card to open full result in modal:
- All prediction details
- Attention map
- Full rationale
- Re-analyze option

**D. Statistics Panel**
- Total analyses
- Average confidence
- Most common questions
- Success rate over time (line chart)

**E. Empty State**
If no history:
- 3D illustration
- "No analyses yet"
- CTA to analyze page

---

### **4. ABOUT PAGE** (`/about`)

#### **Purpose:**
Explain the technology, team, dataset, and research behind VisiHealth AI.

#### **Sections:**

**A. Hero**
- 3D medical visualization
- "About VisiHealth AI"
- Mission statement

**B. Technology Stack**
Interactive cards showing:
1. **ResNet50** - Visual feature extraction
2. **BioLinkBERT** - Medical language understanding
3. **Knowledge Graph** - Medical reasoning
4. **Multimodal Fusion** - Combining vision & text

Each card has:
- 3D icon/model
- Brief description
- "Learn More" expand

**C. Dataset Information**
- SLAKE 1.0 details
- Sample images showcase
- Training statistics
- Performance metrics

**D. Model Performance**
- Accuracy charts
- Confusion matrix preview
- Performance by question type
- Comparison with baselines

**E. Team Section** (if applicable)
- Team members
- Research affiliations
- Contact information

**F. FAQ**
Accordion-style common questions

**G. Citation & Research**
- How to cite
- Published papers
- GitHub repository

---

## 🎨 **Design System**

### **Color Palette**

```css
/* Primary - Medical Blue */
--primary-50: #eff6ff
--primary-500: #3b82f6  /* Main blue */
--primary-700: #1d4ed8
--primary-900: #1e3a8a

/* Accent - Success Green */
--accent-500: #10b981

/* Warning - Amber */
--warning-500: #f59e0b

/* Error - Red */
--error-500: #ef4444

/* Neutral */
--gray-50: #f9fafb
--gray-900: #111827

/* Background */
--bg-primary: #ffffff
--bg-secondary: #f3f4f6
--bg-dark: #0f172a
```

### **Typography**

```css
/* Headings */
font-family: 'Inter', sans-serif;
H1: 3rem (48px) - font-bold
H2: 2.25rem (36px) - font-semibold
H3: 1.875rem (30px) - font-semibold

/* Body */
font-family: 'Inter', sans-serif;
Body: 1rem (16px) - font-normal
Small: 0.875rem (14px) - font-normal
```

### **3D Elements**

1. **Particle Background** (Home page)
   - Floating DNA helix or neural network
   - Interactive on mouse move
   - Blue/white gradient

2. **3D Brain Model** (Home & About)
   - Rotating brain scan
   - Click to explore different angles
   - Highlight different regions

3. **Confidence Gauge** (Analyze page)
   - 3D circular progress ring
   - Animated fill based on confidence
   - Glow effect for high confidence

4. **Medical Scan Viewer** (Analyze page)
   - 3D volumetric rendering (future)
   - Layer by layer navigation
   - Zoom and rotate

5. **Floating Cards** (Throughout)
   - 3D transform on hover
   - Depth shadows
   - Parallax scrolling

---

## 🔄 **User Flow**

### **Primary Flow: Image Analysis**

```
1. User lands on HOME
   ↓
2. Clicks "Try Now"
   ↓
3. Arrives at ANALYZE page
   ↓
4. Uploads medical image
   ↓
5. Types question
   ↓
6. Clicks "Analyze"
   ↓
7. Loading animation (3D spinner)
   ↓
8. Results displayed with animations
   ↓
9. User explores:
   - View attention map
   - Read rationale
   - Check confidence
   ↓
10. Options:
    - Save to history
    - Try another image
    - Download result
```

### **Secondary Flow: View History**

```
1. User clicks "History" in nav
   ↓
2. Sees list of past analyses
   ↓
3. Clicks on analysis card
   ↓
4. Modal opens with full details
   ↓
5. Can delete, export, or re-analyze
```

---

## 🎬 **Animations & Interactions**

### **Page Transitions**
- Fade in/out with scale (Framer Motion)
- Page load: Staggered element entrance

### **Component Animations**

1. **Image Upload**
   - Drag over: Border pulse + glow
   - Drop: 3D flip animation
   - Preview: Scale up from center

2. **Analyze Button**
   - Hover: 3D lift + glow
   - Click: Ripple effect
   - Loading: Rotating 3D DNA helix

3. **Results**
   - Answer: Type-writer effect
   - Confidence gauge: Animated fill (0 → final%)
   - Predictions: Bars slide in sequentially
   - Attention map: Fade in with overlay

4. **3D Elements**
   - Brain: Continuous rotation
   - Particles: Follow mouse cursor
   - Cards: Tilt on mouse move (vanilla-tilt.js)

---

## 📡 **API Integration**

### **API Service (`lib/api.ts`)**

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const api = {
  // Health check
  health: () => axios.get(`${API_BASE}/health`),
  
  // Predict
  predict: (image: File, question: string) => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('question', question);
    return axios.post(`${API_BASE}/predict`, formData);
  },
  
  // Get attention visualization
  visualize: (image: File, question: string) => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('question', question);
    return axios.post(`${API_BASE}/visualize/attention`, formData);
  },
  
  // Get vocabulary
  vocabulary: () => axios.get(`${API_BASE}/answers/vocabulary`),
};
```

---

## 💾 **State Management (`lib/store.ts`)**

```typescript
import create from 'zustand';

interface AnalysisState {
  currentImage: File | null;
  currentQuestion: string;
  result: PredictionResult | null;
  history: Analysis[];
  
  setImage: (file: File) => void;
  setQuestion: (q: string) => void;
  setResult: (r: PredictionResult) => void;
  addToHistory: (analysis: Analysis) => void;
  clearCurrent: () => void;
}

export const useStore = create<AnalysisState>((set) => ({
  currentImage: null,
  currentQuestion: '',
  result: null,
  history: [],
  
  setImage: (file) => set({ currentImage: file }),
  setQuestion: (q) => set({ currentQuestion: q }),
  setResult: (r) => set({ result: r }),
  addToHistory: (analysis) => set((state) => ({
    history: [analysis, ...state.history]
  })),
  clearCurrent: () => set({
    currentImage: null,
    currentQuestion: '',
    result: null
  }),
}));
```

---

## 🚀 **Development Phases**

### **Phase 1: Setup & Foundation** (Week 1)
- [ ] Initialize Next.js project
- [ ] Install dependencies (Tailwind, Three.js, etc.)
- [ ] Setup folder structure
- [ ] Configure TypeScript
- [ ] Setup API client
- [ ] Create basic layout (Header, Footer)

### **Phase 2: Core Pages** (Week 2)
- [ ] Build Home page
- [ ] Create Analyze page structure
- [ ] Implement image upload
- [ ] Connect to backend API
- [ ] Display basic results

### **Phase 3: 3D & Animations** (Week 3)
- [ ] Add Three.js scenes
- [ ] Create 3D brain model
- [ ] Implement particle backgrounds
- [ ] Add Framer Motion animations
- [ ] 3D confidence gauge

### **Phase 4: Advanced Features** (Week 4)
- [ ] Attention map visualization
- [ ] History page with storage
- [ ] About page
- [ ] Download functionality
- [ ] Responsive design

### **Phase 5: Polish & Deploy** (Week 5)
- [ ] Performance optimization
- [ ] Error handling
- [ ] Loading states
- [ ] SEO optimization
- [ ] Deploy to Vercel

---

## 📦 **Package.json Dependencies**

```json
{
  "dependencies": {
    "next": "^14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.3",
    
    "tailwindcss": "^3.4.0",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10",
    
    "three": "^0.160.0",
    "@react-three/fiber": "^8.15.13",
    "@react-three/drei": "^9.93.0",
    
    "framer-motion": "^10.16.16",
    "gsap": "^3.12.4",
    
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.17.9",
    "axios": "^1.6.5",
    "swr": "^2.2.4",
    
    "react-dropzone": "^14.2.3",
    "react-hot-toast": "^2.4.1",
    "lucide-react": "^0.303.0",
    
    "recharts": "^2.10.3",
    "chart.js": "^4.4.1",
    "react-chartjs-2": "^5.2.0",
    
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  }
}
```

---

## 🎯 **Key Features Summary**

### **Home Page**
- 3D rotating medical scan
- Particle background effect
- Feature showcase
- Statistics counter
- How it works section

### **Analyze Page**
- Drag & drop image upload with 3D effects
- Real-time question input
- 3D confidence gauge
- Attention map visualization
- ROI detection display
- Knowledge graph explanation

### **History Page**
- Save past analyses
- 3D card grid
- Search and filter
- Detailed view modal
- Statistics dashboard

### **About Page**
- Technology explanation with 3D models
- Dataset information
- Performance metrics
- Team & contact
- FAQ section

---

## 📱 **Responsive Design**

- **Desktop**: Full 3D effects, side-by-side layouts
- **Tablet**: Simplified 3D, stacked layouts
- **Mobile**: Minimal 3D, vertical flow, touch-optimized

---

## 🎨 **Sample 3D Component**

```typescript
// components/3d/Brain3D.tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

export function Brain3D() {
  const { scene } = useGLTF('/models/brain.glb');
  
  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} />
      <primitive object={scene} />
      <OrbitControls enableZoom={false} />
    </Canvas>
  );
}
```

---

This comprehensive plan provides a complete roadmap for building a modern, interactive, and visually stunning frontend for VisiHealth AI! 🚀
