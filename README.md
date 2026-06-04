# Production-Ready RAG Application

A production-grade Retrieval-Augmented Generation (RAG) system built using Python, LlamaIndex, Qdrant, and Inngest.

Unlike typical AI demos, this project focuses on real-world deployment considerations including observability, retries, rate limiting, concurrency controls, logging, and scalable document ingestion pipelines.

## 🚀 Features

* 📄 PDF document ingestion and processing
* ✂️ Intelligent document chunking
* 🧠 Embedding generation and vector indexing
* 🔍 Semantic search powered by Qdrant
* 🤖 Retrieval-Augmented Generation (RAG)
* ⚡ Event-driven workflows with Inngest
* 📊 Observability and structured logging
* 🔄 Automatic retries and failure handling
* 🚦 Rate limiting and throttling
* 🔒 Concurrency controls for production workloads
* 🌐 Frontend integration for user interaction
* ☁️ Deployment-ready architecture

---

## Architecture

```text
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Chunking Pipeline
      │
      ▼
Embedding Generation
      │
      ▼
Qdrant Vector Database
      │
      ▼
Semantic Retrieval
      │
      ▼
LLM Context Augmentation
      │
      ▼
Generated Response
```

### Tech Stack

| Component              | Technology               |
| ---------------------- | ------------------------ |
| Backend                | Python                   |
| RAG Framework          | LlamaIndex               |
| Vector Database        | Qdrant                   |
| Workflow Orchestration | Inngest                  |
| Embeddings             | OpenAI Embeddings        |
| LLM                    | OpenAI GPT Models        |
| Frontend               | Web UI                   |
| Observability          | Logging & Event Tracking |

---

## Project Structure

```bash
.
├── api/
│   ├── routes/
│   ├── services/
│   └── middleware/
│
├── ingestion/
│   ├── loaders/
│   ├── chunking/
│   └── embeddings/
│
├── workflows/
│   ├── inngest/
│   └── background_tasks/
│
├── vector_store/
│   └── qdrant/
│
├── frontend/
│
├── logs/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/production-rag-app.git

cd production-rag-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

INNGEST_EVENT_KEY=your_event_key
INNGEST_SIGNING_KEY=your_signing_key
```

---

## Running the Application

### Start API

```bash
python main.py
```

### Start Inngest Development Server

```bash
inngest dev
```

### Run Frontend

```bash
npm install

npm run dev
```

---

## Document Ingestion

Place PDF files inside:

```bash
data/documents/
```

Run ingestion:

```bash
python ingest.py
```

The pipeline will:

1. Load PDFs
2. Split documents into chunks
3. Generate embeddings
4. Store vectors in Qdrant

---

## Querying Documents

Example:

```python
response = query_engine.query(
    "What are the key findings from the report?"
)

print(response)
```

---

## Production Engineering Considerations

This project implements several production-grade patterns:

### Observability

* Structured logging
* Request tracing
* Workflow monitoring
* Error reporting

### Reliability

* Retry mechanisms
* Failure recovery
* Dead-letter handling
* Workflow durability

### Scalability

* Asynchronous processing
* Event-driven architecture
* Horizontal scaling support
* Distributed vector search

### Security

* Environment-based secrets
* API key management
* Input validation
* Request controls

### Performance

* Caching strategies
* Concurrent processing
* Optimized retrieval pipelines
* Rate limiting and throttling

---

## Example Use Cases

* Enterprise Knowledge Base
* Internal Documentation Assistant
* Research Assistant
* Customer Support Chatbot
* Compliance and Policy Search
* Technical Documentation Search

---

## Future Improvements

* Multi-tenant support
* Hybrid Search (BM25 + Vector Search)
* Advanced Evaluation Framework
* OpenTelemetry Integration
* Streaming Responses
* Multi-modal RAG
* Kubernetes Deployment

---

## Learning Resources

This project was inspired by and implemented while following:

Creator: Tech With Tim

---

## License

MIT License

---

## Author

Jigeesha Jain

Software Engineer | AI Engineer | Building scalable AI systems, RAG pipelines, and production-ready LLM applications.
