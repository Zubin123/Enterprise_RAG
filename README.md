# SEC RAG Intelligence System

Enterprise-grade Retrieval-Augmented Generation (RAG) system for querying SEC 10-K filings from Apple and Microsoft using natural language.

---

## Live Demo

**Try it now**: [Enterprise RAG on Render](https://enterprise-rag-cz5t.onrender.com)

---

##  What This System Does

This is not a basic vector search demo. It is a full document intelligence pipeline that:

- Automatically detects company and year from the query  
- Infers the correct SEC Part and Item  
- Retrieves the full section content  
- Anchors answers to official SEC sections  
- Prevents hallucinations by answering only from retrieved context  

---

##  Core Capabilities

### Intelligent Query Understanding
- Auto company detection (AAPL / MSFT)
- Auto year detection
- Auto section inference (Item 1A, Item 7, etc.)
- Works with vague or incomplete questions

### SEC-Aware Document Parsing
- Detects navigation & TOC pages
- Extracts SEC Part & Item structure
- Handles inconsistent PDF layouts (Apple vs Microsoft)
- Tracks section hierarchy across pages

### Enterprise Retrieval Pipeline
- Semantic search using FAISS + embeddings
- Metadata filtering (company, year, section)
- Full section expansion
- Section anchoring
- Semantic re-ranking

### Hallucination-Resistant Generation
- LLM answers only from retrieved context
- No external knowledge leakage
- Automatic fallback logic

---

##  Architecture

User Query
↓
Retriever (Hybrid RAG Engine)
├─ Semantic Search
├─ Auto Company & Year Detection
├─ Auto Section Inference
├─ Metadata Filtering
├─ Section Expansion
└─ Section Anchoring
↓
Context Builder
↓
LLM Generator
↓
Grounded Answer


---

##  Project Structure

```
Enterprise_RAG/
├── app/                          # Main application code
│   ├── core/                     # Core configuration and utilities
│   │   ├── config.py            # Application settings and environment variables
│   │   └── logger.py            # Logging configuration
│   ├── generation/               # LLM generation components
│   │   ├── context_builder.py   # Builds context from retrieved documents
│   │   ├── llm.py               # LLM generator wrapper
│   │   └── prompt.py            # Prompt templates
│   ├── ingestion/                # Document ingestion pipeline
│   │   ├── chunker.py           # Document chunking logic
│   │   ├── navigation_detector.py # Detects TOC/navigation pages
│   │   ├── run_ingestion.py     # Main ingestion script
│   │   ├── sec_grammar.py       # SEC document structure parsing
│   │   └── sec_loader.py        # PDF loader for SEC filings
│   ├── retrieval/                # Retrieval components
│   │   ├── retriever.py         # Main retriever with hybrid search
│   │   ├── vector_store.py      # FAISS vector store management
│   │   ├── test_retrieval.py    # Retrieval testing utilities
│   │   └── test_retriever.py    # Retriever testing utilities
│   ├── static/                   # Static web assets
│   │   └── style.css            # CSS styles
│   ├── templates/                # HTML templates
│   │   └── index.html           # Main UI template
│   ├── main.py                  # FastAPI application entry point
│   └── test_rag.py              # RAG system testing
├── data/                         # Data directory
│   ├── raw/                      # Raw SEC filing PDFs
│   │   ├── AAPL_2023_10K.pdf    # Apple 2023 10-K filing
│   │   └── MSFT_2023_10K.pdf    # Microsoft 2023 10-K filing
│   └── vectorstore/              # Vector database storage
│       ├── index.faiss          # FAISS index file
│       └── index.pkl            # FAISS index metadata
├── logs/                         # Application logs
│   └── app.log                  # Main application log file
├── Dockerfile                    # Docker container configuration
├── .dockerignore                 # Docker build exclusions
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project metadata and dependencies
└── uv.lock                      # Dependency lock file
```

---

##  Setup Guide

### Prerequisites

- **Python 3.11+** (required as per `pyproject.toml`)
- **pip** or **uv** package manager
- **OpenAI API Key** (for LLM generation)
- **Docker** (optional, for containerized deployment)

### Installation Steps

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd Enterprise_RAG
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv (if available):
   ```bash
   uv sync
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   > **Note**: The embedding model (`sentence-transformers/all-MiniLM-L6-v2`) runs locally and doesn't require an API key.

5. **Prepare data directory structure**:
   
   Ensure the following directories exist:
   ```bash
   mkdir -p data/raw
   mkdir -p data/vectorstore
   mkdir -p logs
   ```

6. **Ingest SEC filings**:
   
   Place your SEC 10-K PDF files in `data/raw/` directory, then run the ingestion script:
   ```bash
   python -m app.ingestion.run_ingestion
   ```
   
   This will:
   - Load and parse the PDF files
   - Extract SEC sections and structure
   - Chunk the documents
   - Build the FAISS vector store
   - Save the vector store to `data/vectorstore/`

   > **Note**: The ingestion process may take several minutes depending on the size of the PDF files.

7. **Run the application**:
   
   Start the FastAPI server:
   ```bash
   python -m app.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

8. **Access the web interface**:
   
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

### Docker Deployment

#### Build and Run Locally

1. **Build the Docker image**:
   ```bash
   docker build -t enterprise-rag .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env enterprise-rag
   ```
   
   Or with volume mounting for data persistence:
   ```bash
   docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data enterprise-rag
   ```

3. **Access the application**:
   ```
   http://localhost:8000
   ```

#### Deploy to Render

1. Push your repository to GitHub
2. Connect your GitHub repository to Render
3. Set the following configuration in Render:
   - **Build Command**: `pip install -r requirements.txt && python -m app.ingestion.run_ingestion`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Environment Variable**: Add `OPENAI_API_KEY` in Render dashboard

4. Deploy and access at your Render URL

### Quick Start Example

After setup, you can test the system with queries like:
- "What are Apple's main risk factors in 2023?"
- "Summarize Item 1A for Microsoft 2023"
- "Explain Part II of AAPL 10-K"
- "What does MSFT say about competition?"

### Troubleshooting

- **Vector store not found**: Make sure you've run the ingestion script first (`python -m app.ingestion.run_ingestion`)
- **OpenAI API errors**: Verify your API key is correctly set in the `.env` file
- **Import errors**: Ensure all dependencies are installed and your virtual environment is activated
- **Port already in use**: Change the port in `app/main.py` or use `--port` flag with uvicorn
- **Docker build fails**: Ensure Docker is installed and running; check `requirements.txt` is in the root directory

---

##  Key Optimizations

| Optimization | Benefit |
|-------------|---------|
Navigation filtering | Removes TOC/index noise |
SEC grammar parsing | Accurate section boundaries |
Section expansion | Prevents partial answers |
Hybrid retrieval | High recall + precision |
Semantic re-ranking | Best chunks first |
Auto inference | Zero-config querying |
Chunk overlap | Prevents context loss |
Metadata propagation | Perfect traceability |

---

##  Use Cases

- Financial research  
- Equity analysis  
- Risk assessment  
- Compliance review  
- Investor due diligence  
- AI research agents  


##  Author

Mohammed Zubin Essudeen
AI/ML Engineer — Applied RAG & Document Intelligence