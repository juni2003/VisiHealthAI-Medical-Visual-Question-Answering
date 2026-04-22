# VisiHealth AI - Flask Backend

## 📁 Project Structure

```
backend/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── api/
│   ├── __init__.py
│   └── routes.py          # API endpoints
├── services/
│   ├── __init__.py
│   └── model_service.py   # Model management
├── middleware/
│   ├── __init__.py
│   └── cors.py            # CORS configuration
├── utils/
│   ├── __init__.py
│   └── validators.py      # Input validation
└── uploads/               # Temporary image storage
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

**Development:**
```bash
python app.py
```

**Production:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```
GET /api/health
```
Returns server health status.

### Get Model Info
```
GET /api/model/info
```
Returns model configuration and status.

### Single Prediction
```
POST /api/predict

Form Data:
  - image: Image file (jpg, png, etc.)
  - question: Question text

Response:
{
  "success": true,
  "data": {
    "answer": "yes",
    "confidence": 0.856,
    "top_predictions": [...],
    "roi": {...},
    "rationale": "Detected liver region..."
  }
}
```

### Batch Prediction
```
POST /api/predict/batch

Form Data:
  - images: Multiple image files
  - questions: Array of questions

Response:
{
  "success": true,
  "data": [...]
}
```

### Attention Visualization
```
POST /api/visualize/attention

Form Data:
  - image: Image file
  - question: Question text

Response:
{
  "success": true,
  "data": {
    "visualization": "base64_encoded_image",
    "answer": "yes",
    "confidence": 0.856
  }
}
```

### Get Answer Vocabulary
```
GET /api/answers/vocabulary

Response:
{
  "success": true,
  "data": {
    "vocabulary": ["yes", "no", "liver", ...],
    "total": 202
  }
}
```

## 🔧 Configuration

Edit `config.py` to customize:

- **CORS_ORIGINS**: Allowed frontend origins
- **MAX_CONTENT_LENGTH**: Maximum upload size
- **UPLOAD_FOLDER**: Temporary storage path
- **MODEL paths**: Checkpoint and config locations

## 🔒 Security

- Input validation on all endpoints
- File type checking
- Size limits (16MB max)
- CORS protection
- Sanitized filenames

## 🧪 Testing with cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Prediction
curl -X POST http://localhost:5000/api/predict \
  -F "image=@path/to/image.jpg" \
  -F "question=Is there any disease?"
```

## 🐛 Debugging

Set environment variable:
```bash
export FLASK_DEBUG=True
```

## 📊 Architecture

### Model Service (Singleton)
- Loads model once at startup
- Caches model in memory
- Handles all inference requests
- Thread-safe for concurrent requests

### API Layer
- RESTful design
- JSON responses
- Error handling
- Input validation

### Middleware
- CORS for frontend integration
- Request logging
- Error handlers

## 🚀 Deployment

### Environment Variables

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
CORS_ORIGINS=https://your-frontend.com
```

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

## 📝 Notes

- First request takes longer (model loading)
- Use CPU by default (GPU if available)
- Upload folder auto-created
- Temporary files not auto-deleted (add cleanup if needed)
