# 🎥 Video Transcript RAG AI Assistant

An AI-powered system that allows users to ask questions about video content and get **timestamped, context-aware answers** using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features
- 🔍 Semantic search over video transcripts
- ⏱ Timestamp-based answers
- 🎙 Whisper-based speech-to-text (Hindi → English)
- 🧠 Embeddings + cosine similarity retrieval
- 🤖 LLM-based contextual response generation

---

## 🧠 System Architecture

User Query → Embedding → Vector Search → Top-K Chunks → LLM → Answer with Timestamp

---

## 🛠 Tech Stack
- Python
- Whisper (Speech-to-text)
- BGE-M3 (Embeddings)
- LLaMA 3.2 (LLM)
- Pandas / NumPy

---

## 📸 Demo
(Add screenshots OR video)

---

## ⚡ How to Run
```bash
git clone https://github.com/adarsh-verse/video-transcript-rag
cd video-transcript-rag
pip install -r requirements.txt
python main.py
