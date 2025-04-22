# STORM FastAPI Wrapper with Gemini

A production-ready FastAPI wrapper for the [STORM](https://github.com/stanford-oval/storm) research framework from Stanford OVAL Lab. This API allows users to input a query and receive a structured, Wikipedia-style article generated using curated knowledge and LLM reasoning pipelines, now powered by Google's Gemini.

---

## 🚀 Features

- ✨ **Google Gemini Integration** using `google-generativeai` (supports `gemini-1.0-pro`, `gemini-1.5-pro`, and `gemini-2.0-flash-lite-001`)
- 🧠 Full STORM pipeline (knowledge curation, outline, draft, polish)
- 🔄 **Streaming support** with `stream=true`
- ✅ Pydantic request validation
- 📦 In-memory output (no disk writes)
- 🧪 Plug-in friendly for custom retrievers (uses mock retriever by default)
- 🐳 Docker-ready with secure API key handling

---

## 📁 Project Structure

```
storm_fastapi_wrapper/
├── api/
│   ├── routes.py         # FastAPI routes
│   └── schemas.py        # Request/response models
├── core/
│   └── storm_interface.py # STORM pipeline integration
├── utils/
│   ├── mock_retriever.py  # Dummy retriever for local/dev testing
│   └── patch_file_writes.py # Prevent file writes to disk
└── main.py
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/storm-api-wrapper.git
cd storm-api-wrapper
```

### 2. Create and activate virtual environment (recommended)
```bash
conda create -n storm-env python=3.10
conda activate storm-env
```

### 3. Install Poetry (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or via pipx:
```bash
pipx install poetry
```

### 4. Install dependencies
```bash
poetry install
```

### 5. Set your Gemini API key

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-lite-001  # or gemini-1.0-pro
GOOGLE_API_REGION=us-central1  # optional
```

Or export manually:
```bash
export GEMINI_API_KEY=your_api_key_here
export GEMINI_MODEL=gemini-2.0-flash-lite-001
```

---

## 📦 Dependency Management

This project uses [**Poetry**](https://python-poetry.org/) for dependency and virtual environment management.

### 🛠️ Requirements
- Python `3.10+`
- Poetry `>=1.3.0`
- Google Generative AI SDK `>=0.3.0`

### 📄 Key Files

| File              | Purpose                                    |
|-------------------|--------------------------------------------|
| `pyproject.toml`  | Declares project metadata and dependencies |
| `poetry.lock`     | Locks exact versions for reproducibility   |

### 📅 Installing Dependencies

To install all dependencies in a reproducible environment:
```bash
poetry install
```

### 📅 Installing STORM

Clone the official [STORM repo](https://github.com/stanford-oval/storm):
```bash
git clone https://github.com/stanford-oval/storm.git
```
Then add the path to `PYTHONPATH`:
```bash
export PYTHONPATH="$PYTHONPATH:/path/to/storm"
```
Or in Windows:
```powershell
$env:PYTHONPATH = "C:\path\to\storm"
```

Ensure it is imported correctly by your `storm_interface.py`.

---

## 🧪 Running the App

```bash
uvicorn api.main:app --reload
```
Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📄 API Usage

### POST `/query`
Generates an article based on a given query using Gemini.

**Request Body:**
```json
{
  "query": "What is quantum computing?",
  "stream": false,
  "temperature": 0.7,
  "model": "gemini-2.0-flash-lite-001"  # optional override
}
```

**Response (stream = false):**
```json
{
  "status": "success",
  "output": "# Summary\nQuantum computing...",
  "model_used": "gemini-2.0-flash-lite-001"
}
```

**Response (stream = true):**
- Returns `text/plain` streaming chunks as they are generated.

### GET `/models`
Lists available Gemini models:
```json
{
  "models": [
    "gemini-1.0-pro",
    "gemini-1.5-pro",
    "gemini-2.0-flash-lite-001"
  ]
}
```

---

## 🐳 Docker Usage

### Build the Docker image
```bash
docker build --build-arg GEMINI_API_KEY=your_real_key -t storm-dev .
```
This reads the Dockerfile in current directory (.)

Creates an image named storm-dev

### Run the container
```bash
docker run -p 8000:8000 -v ./:/app/storm_fastapi_wrapper storm-dev
```
-v ./:/app/storm_fastapi_wrapper connects your local folder to the container

-p 8000:8000 exposes the FastAPI port

### File Structure In Docker Container
```
/app
├── storm/               # STORM (installed in editable mode)
└── storm_fastapi_wrapper/  # Your FastAPI app (live-reloaded)

```
### Available Environment Variables
| Variable          | Default                     | Description                     |
|-------------------|-----------------------------|---------------------------------|
| GEMINI_API_KEY    | -                           | Required API key                |
| GEMINI_MODEL      | gemini-2.0-flash-lite-001   | Model version                   |
| GOOGLE_API_REGION | us-central1                 | Optional regional endpoint      |

---

## 🔐 Security Notes

- API keys are never written to disk
- All file writes are blocked by security patch
- Uses mock retriever by default (swap with real retriever in production)
- Container runs with non-root user

---

## 🧠 Credits

Built on top of:
- [STORM project](https://github.com/stanford-oval/storm) by Stanford OVAL Lab
- [Google's Gemini API](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/) framework

---

## 📄 License
MIT License

