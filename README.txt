Automated CV Intelligence System
Local OCR + RAG Pipeline for Skill Extraction and Labor-Market Analysis


TL;DR

A fully local, deterministic OCR pipeline for CVs, extended with embedding-based
semantic retrieval and LLM-powered Retrieval-Augmented Generation (RAG) to enable
grounded, searchable document understanding — without cloud dependencies.


Development Environment

The project is currently developed and tested on Windows.
A Linux (Ubuntu) environment is planned for future versions to support
GPU-accelerated OCR, embeddings, and local LLM inference.


Overview

This project implements a production-oriented pipeline that converts CVs
(PDF, PNG, JPEG, JPG) into structured, searchable knowledge using OCR,
deterministic text cleaning, embeddings, semantic retrieval, and
retrieval-augmented LLMs.

The system is designed to be offline-first, modular, and automation-ready.
Its goal is not free-form text generation, but reliable document understanding
and retrieval as a foundation for automated CV intelligence and labor-market
analysis.


Why This Project Exists

Most CV processing systems today are either:
- Cloud-dependent and opaque
- Script-based OCR pipelines without retrieval guarantees
- End-to-end ML systems that mix extraction, interpretation, and scoring

This project explores a different approach:
- Fully local execution (OCR, embeddings, retrieval, LLM)
- Deterministic preprocessing and cleaning
- Embedding-based semantic retrieval
- Retrieval-Augmented Generation (RAG), not hallucination-prone generation
- Clear separation between extraction, retrieval, and interaction

The focus is on building a strong document and retrieval foundation
before adding higher-level analytics.


High-Level Architecture (Actual Implementation)

PDF CV
→ Step 1: PDF/Picture CV file format → PNG Preprocessing
→ Step 2: OCR (PaddleOCR)
→ Step 3: Light OCR Cleaning (No Semantics)
→ Step 4: RAG Block Preparation (Paragraph-Level Text)
→ Step 5: Embeddings + Vector Store (Chroma)
→ Step 6: Semantic Retrieval (Query ↔ Vector Database)
→ Step 7: LLM Answering (RAG)


Core RAG Flow

The pipeline follows a strict Retrieval-Augmented Generation (RAG) architecture.

Knowledge is built once:
- OCR text is cleaned deterministically
- Cleaned text is converted into dense, paragraph-level RAG blocks
- RAG blocks are embedded using a pre-trained embedding model
- Embeddings are stored persistently in a vector database (Chroma)

Every user query follows the same runtime flow:
Question
→ Step 6: Embed query and retrieve relevant text blocks
→ Step 7: LLM generates an answer using retrieved context only

The LLM never accesses raw CV files, JSON artifacts, or the vector database
directly. All grounding is enforced through retrieval.


Core Design Principles

- Fully local execution (OCR, embeddings, retrieval, LLM)
- Deterministic preprocessing (no semantics before embeddings)
- JSON as the canonical intermediate format
- Clear separation between ingestion, retrieval, and reasoning
- Retrieval first, generation second (RAG, not free generation)
- Embedding models handle tokenization internally (model-specific)


Folder Structure

ocr-pipeline/
├── step1_preprocess/
│   ├── step1_preprocess_pdf.py
│   └── output/
├── step2_ocr/
│   ├── step2_ocr_paddle.py
│   └── output/
│       └── cv_ocr_raw.json
├── step3_lightclean/
│   ├── step3_light_clean.py
│   └── output/
│       └── cv_ocr_cleaned.json
├── step4_rag/
│   ├── step4_rag_prepare.py
│   └── output/
│       └── cv_rag_blocks.json
├── step5_embeddings/
│   ├── step5_embeddings.py
│   └── step5_output/        (Chroma persistent store)
├── step6_retrieval/
│   ├── step6_retrieval.py
├── step7_llm/
│   └── step7_llm_answering.py
└── callers/
    ├── calling_script.py
    └── batch_callers.py


Pipeline Stages

Step 1 — PDF/IMG Preprocessing  
Converts PDF/IMG pages into normalized PNG images while preserving page order
and resolution.

Step 2 — OCR (PaddleOCR)  
Extracts raw text with layout and confidence metadata.
No semantic interpretation is performed at this stage.

Step 3 — Light OCR Cleaning (Pre-RAG)  
Deterministic cleanup only:
- Remove low-confidence lines
- Normalize whitespace and casing
- Normalize accents
- Preserve reading order

The output is embedding-ready, not semantically interpreted.

Step 4 — RAG Block Preparation  
- Merge OCR lines into dense, paragraph-level blocks
- Absorb CV layout fragmentation (titles, bullets, line breaks)
- No semantic interpretation
- No LLM usage

Output:
- cv_rag_blocks.json

Step 5 — Embeddings & Vector Store (Chroma)  
- Convert RAG blocks into semantic vectors using a pre-trained embedding model
- Tokenization and embeddings are handled internally by the model
- Store embeddings and metadata persistently in Chroma

This step runs once per data update and survives system restarts.

Step 6 — Semantic Retrieval  
- Embed user queries using the same embedding model
- Perform vector similarity search against the Chroma database
- Retrieve the most relevant text blocks

This step:
- Runs for every query
- Does not write files
- Does not modify the vector store

Step 7 — LLM Answering (RAG)  
- Build a prompt from retrieved text blocks and the user question
- Generate answers grounded strictly in retrieved OCR content
- Prevent hallucinations by enforcing retrieval-first answering


Example Usage (RAG)

Query:
What experience does the candidate have in data science?

Retrieved Context:
- Training in Data Science and Machine Learning
- Python and Pandas usage
- Related projects and education

LLM Answer:
The candidate has experience in data science through formal training in
machine learning, hands-on projects, and the use of Python and Pandas.

All answers are generated strictly from retrieved OCR text.


Intended Applications

While the current focus is on building a reliable OCR → Retrieval → RAG pipeline,
the broader motivation is automated CV intelligence, including:

- Skill extraction from unstructured CVs
- Structured querying of candidate profiles
- Resume-to-job matching (future work)
- Aggregated skill statistics across CV corpora
- Labor-market and workforce analysis

This repository focuses on the document and retrieval foundations
required for these applications, rather than downstream analytics.


Automation Strategy

- Each step is stateless and independently callable
- Embeddings are rebuilt only when data changes
- Retrieval and LLM answering run at query time
- Designed for debugging, automation, and scaling


Project Status

- OCR pipeline: stable
- RAG block preparation: stable
- Embeddings & retrieval: stable (Chroma)
- LLM answering: integration-ready
- Frontend & API: early stage

The project prioritizes correctness and clarity before optimization.


Non-Goals (Current Scope)

- Cloud-based OCR or hosted LLMs
- Semantic interpretation during OCR cleaning
- End-to-end ML training pipelines
- Automated hiring decisions or candidate scoring


Final Notes

This project is intentionally:
- Offline-first
- Modular
- Deterministic
- Retrieval-driven
- Production-oriented
