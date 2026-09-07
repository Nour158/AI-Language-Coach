<p align="center">
  <img src="assets/ai-language-coach-logo.png" alt="AI Language Coach Logo" width="220"/>
</p>

<h1 align="center">AI Language Coach</h1>

<p align="center">
  <b>AI-Powered English Conversation & Personalized Learning Platform</b>
</p>

<p align="center">
  Graduation Project • Artificial Intelligence • NLP • RAG • LLM
</p>

---

## 📖 Overview

**AI Language Coach** is an AI-powered English learning platform designed to help learners improve their English through natural, interactive conversations.

Unlike a traditional chatbot, AI Language Coach combines conversational AI, Retrieval-Augmented Generation (RAG), learner assessment, personalized feedback, and speech technologies to create an adaptive learning experience.

The system can:

- Hold natural English conversations
- Understand conversation context
- Retrieve relevant English-learning knowledge
- Provide grammar and vocabulary guidance
- Analyze learner performance
- Detect recurring mistakes
- Generate personalized feedback and exercises
- Support text and voice interaction

---

## 🎯 Project Goal

The goal of AI Language Coach is to create an intelligent English-learning assistant that behaves naturally during conversation while continuously understanding the learner's needs.

Instead of correcting every sentence immediately, the system focuses on maintaining a natural conversation and uses the learner's session history to provide useful assessment and personalized learning recommendations.

---

## ✨ Main Features

### 💬 Intelligent Conversation

Natural English conversations powered by **Qwen2.5-7B-Instruct** with conversation history and contextual prompting.

### 🧠 Advanced Hybrid RAG

The system uses a history-aware conversational hybrid RAG architecture combining:

- Dense semantic retrieval
- Sparse lexical retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Conditional retrieval
- History-aware query rewriting

### 📚 Educational Knowledge Base

The RAG knowledge base contains English-learning resources covering areas such as:

- Grammar
- Vocabulary
- CEFR learning material
- Natural English usage
- Learner mistakes
- Coaching guidance

### 📊 Assessment & Feedback

After a learning session, the system can analyze the learner's conversation and evaluate areas such as:

- Grammar
- Vocabulary
- Fluency
- Coherence
- Repeated mistakes
- Areas for improvement

The system then generates personalized feedback and learning recommendations.

### 🧠 Conversation Memory

The platform uses:

- Recent conversation history
- Session summaries
- Learner goals
- Recurring difficulties
- Learning preferences

This allows the assistant to maintain context without repeatedly sending the entire conversation.

### 🎙️ Speech Support

The architecture supports voice-based interaction using Speech-to-Text and Text-to-Speech components.

---

# 🏗️ System Architecture

```text
                    USER
                      │
              Text / Voice Input
                      │
                      ▼
              Speech-to-Text
                (if voice)
                      │
                      ▼
             Conversation History
                      │
                      ▼
              Context Understanding
                      │
                      ▼
                Need RAG?
                 /       \
               YES        NO
                │          │
                ▼          │
       History-Aware Query │
            Rewriting      │
                │          │
                ▼          │
       ┌─────────────────┐ │
       │ Hybrid Retrieval│ │
       └─────────────────┘ │
          │           │    │
          ▼           ▼    │
     Dense Search  Sparse Search
        BGE          SPLADE
          │           │
          └─────┬─────┘
                ▼
        Reciprocal Rank
          Fusion (RRF)
                │
                ▼
             Top 10
                │
                ▼
          Cross-Encoder
            Reranker
                │
                ▼
         Top 3–5 Chunks
                │
                └──────────┐
                           ▼
                  Prompt Construction
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       System          Conversation      Retrieved
       Prompt            Memory          Context
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  Qwen2.5-7B-Instruct
                           │
                           ▼
                    AI Response
                           │
                           ▼
                   Structured JSON
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                       Frontend
