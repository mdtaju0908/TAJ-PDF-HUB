# Smart PDF Tools Backend (FastAPI)

Production-ready FastAPI backend for a Next.js Smart PDF Tools app. Supports async processing, CORS, streaming downloads, rate limiting, and API key security.

## Features
- Merge, Split, Compress, Rotate, Watermark, Page Numbers, Protect/Unlock
- Convert: PDF↔Word, JPG↔PDF, PDF→JPG
- OCR: Create searchable PDFs using Tesseract
- Async endpoints, background cleanup of temp files
- CORS for Next.js, API Key security, simple rate limiting

## Environment
Create `.env` based on `.env.example`:
```
API_KEYS=your-api-key
ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_REQUESTS_PER_MINUTE=120
TMP_DIR=./backend/tmp
```

## Install & Run (Local)
```
cd backend
python -m venv .venv && . .venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker
```
cd backend
docker compose up --build
```

## Endpoints
- Health: `GET /health`
- Download: `GET /api/download/{file_id}`
- Merge: `POST /api/merge` (files: PDFs[])
- Split: `POST /api/split` (file: PDF, body: { ranges })
- Compress: `POST /api/compress` (file: PDF, body: { quality })
- Convert:
  - `POST /api/pdf-to-word` (file: PDF, body: { include_page_breaks })
  - `POST /api/word-to-pdf` (file: DOCX, body: { font_name, font_size, line_height })
  - `POST /api/jpg-to-pdf` (files: images[])
  - `POST /api/pdf-to-jpg` (file: PDF)
- Edit:
  - `POST /api/rotate` (file: PDF, body: { degrees })
  - `POST /api/add-page-numbers` (file: PDF, body: { position, start, font_size })
  - `POST /api/add-watermark` (file: PDF, body: { text, opacity, font_size })
  - `POST /api/protect` (file: PDF, body: { user_password, owner_password? })
  - `POST /api/unlock` (file: PDF, body: { password })
- OCR: `POST /api/ocr` (file: PDF, body: { language })

All requests must include header `X-API-Key: <your key>` if API keys are configured.

## Example curl
Merge PDFs:
```
curl -X POST "http://localhost:8000/api/merge" \
  -H "X-API-Key: your-api-key" \
  -F "files=@/path/a.pdf" -F "files=@/path/b.pdf"
```

Split PDF:
```
curl -X POST "http://localhost:8000/api/split" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -H "Content-Type: multipart/form-data" \
  -F 'options={"ranges":"1-3,5"}'
```

Compress PDF:
```
curl -X POST "http://localhost:8000/api/compress" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -F 'options={"quality":"screen"}'
```

PDF to Word:
```
curl -X POST "http://localhost:8000/api/pdf-to-word" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -F 'options={"include_page_breaks":true}'
```

Word to PDF:
```
curl -X POST "http://localhost:8000/api/word-to-pdf" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.docx" \
  -F 'options={"font_name":"Helvetica","font_size":12,"line_height":1.2}'
```

JPG to PDF:
```
curl -X POST "http://localhost:8000/api/jpg-to-pdf" \
  -H "X-API-Key: your-api-key" \
  -F "files=@/path/img1.jpg" -F "files=@/path/img2.png"
```

PDF to JPG:
```
curl -X POST "http://localhost:8000/api/pdf-to-jpg" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf"
```

Rotate PDF:
```
curl -X POST "http://localhost:8000/api/rotate" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -F 'options={"degrees":90}'
```

Add Watermark:
```
curl -X POST "http://localhost:8000/api/add-watermark" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -F 'options={"text":"CONFIDENTIAL","opacity":0.2,"font_size":36}'
```

Protect PDF:
```
curl -X POST "http://localhost:8000/api/protect" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/sample.pdf" \
  -F 'options={"user_password":"1234"}'
```

Unlock PDF:
```
curl -X POST "http://localhost:8000/api/unlock" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/protected.pdf" \
  -F 'options={"password":"1234"}'
```

OCR:
```
curl -X POST "http://localhost:8000/api/ocr" \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/scanned.pdf" \
  -F 'options={"language":"eng"}'
```

## Notes
- Ghostscript, Tesseract, and Poppler are installed in the Docker image.
- For Windows local dev, install Ghostscript and Tesseract, and set them in PATH.

