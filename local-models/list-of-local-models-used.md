# Local Models Reference Guide 🏠💻

This document lists the specific local Large Language Models (LLMs) used in the Winter School 2026 workshop. These models were selected to demonstrate that efficient, private, and capable AI can run on consumer hardware (like Apple Silicon or standard GPUs) without relying on external APIs.

## 🌟 Featured Models

### 1. TinyLlama 1.1B (Quantized)
* **Full Name:** `tinyllama1.1b-llm-quantized`
* **Size:** ~668 MB
* **Architecture:** Llama-based (scaled down)
* **Best For:**
    * [cite_start]**Few-Shot Prompting:** Extremely fast inference for simple classification tasks when provided with examples[cite: 107].
    * **Edge Devices:** Runs on almost any hardware due to its sub-1GB footprint.
* **Limitations:**
    * **Reasoning:** struggles with complex logic or "thinking through" problems without heavy guidance.
    * [cite_start]**Hallucinations:** Prone to making up facts if not strictly constrained by the prompt[cite: 146].
* [cite_start]**Workshop Use Case:** Sentiment classification (Positive/Negative/Neutral) using few-shot examples[cite: 112].

---

### 2. Phi-2 (MLX Optimized)
* **Full Name:** `phi-2-mlx-4bit`
* **Owner:** Microsoft (optimized for Apple Silicon by MLX Community)
* **Size:** ~1.57 GB
* **Architecture:** Transformer-based (specialized training on textbook-quality data)
* **Best For:**
    * [cite_start]**Reasoning (CoT):** punchy performance for its size on logic puzzles and arithmetic[cite: 169].
    * [cite_start]**Creative Writing/Roleplay:** Good at adopting personas (e.g., "Professional Poet")[cite: 234].
* **Limitations:**
    * **Context Window:** Smaller context compared to newer models.
    * **Safety/Refusal:** Can be overly cautious or verbose in refusals depending on the fine-tune.
* [cite_start]**Workshop Use Case:** Solving the "pen and notebook" math puzzle using Chain of Thought [cite: 176][cite_start]; explaining concepts as a Ukrainian poet[cite: 230].

---

### 3. Qwen 2.5 (1.5B Instruct)
* **Full Name:** `qwen2.5-1.5b-instruct`
* **Owner:** Alibaba Cloud (Qwen Team)
* **Size:** ~1.4 GB
* **Architecture:** Transformer (highly optimized for instruction following)
* **Best For:**
    * [cite_start]**Instruction Following:** Excellent at adhering to complex formatting rules (JSON, lists, etc.)[cite: 340].
    * [cite_start]**Prompt Chaining:** Reliable enough to handle multi-step pipelines (Summarize $\to$ Extract $\to$ Post)[cite: 344].
    * [cite_start]**Tool Use (ReAct):** Can simulate reasoning and acting loops (e.g., checking weather)[cite: 523].
* [cite_start]**Workshop Use Case:** Summarizing AI trends, generating LinkedIn posts, and performing Tree-of-Thought marketing strategy brainstorming[cite: 444].

---

### 4. Qwen 3 VL (4B)
* **Full Name:** `qwen/qwen3-vl-4b`
* **Owner:** Alibaba Cloud
* **Size:** ~3.11 GB
* **Type:** Vision-Language Model (Multimodal)
* **Best For:**
    * [cite_start]**Multimodal Tasks:** Can process and understand images along with text[cite: 246].
    * [cite_start]**Complex Creative Nuance:** Better at capturing subtle stylistic instructions (e.g., "Ukrainian soul" in poetry) than smaller models[cite: 261].
* [cite_start]**Workshop Use Case:** Meta-prompting example to generate poetry about Prompt Engineering with deep cultural context[cite: 274].

---

## 🛠️ Management Tools

### Ollama
* **Type:** CLI & Background Service
* **Platform:** macOS, Linux, Windows
* **Key Features:**
    * Easiest setup ("one-click" experience).
    * Model library accessibility (similar to Docker hub).
    * [cite_start]Great for scripting and automation via API[cite: 624].
* **Command:** `ollama run llama3`

### LM Studio
* **Type:** GUI Application
* **Platform:** All OS
* **Key Features:**
    * Visual interface for chatting and configuration.
    * Native support for **GGUF** models from Hugging Face.
    * [cite_start]Visualizes system prompts and chat history clearly[cite: 651].
* **Best For:** Experimenting with different system prompts and parameters (temperature, context window) without writing code.

---

## 📊 Comparison Table

| Model Name | Size | Optimized For | Best Use Case |
| :--- | :--- | :--- | :--- |
| **TinyLlama 1.1B** | 668 MB | Speed & Efficiency | Simple classification, formatting |
| **Phi-2 (MLX)** | 1.57 GB | Logic & Reasoning | Math puzzles, step-by-step logic |
| **Qwen 2.5 (1.5B)** | 1.4 GB | Instruction Following | RAG, summarization, structured output |
| **Qwen 3 VL (4B)** | 3.11 GB | Multimodal & Nuance | Vision tasks, complex creative writing |