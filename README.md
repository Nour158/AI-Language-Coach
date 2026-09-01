# AI Language Coach

AI Language Coach is a graduation project combining **Generative AI,
NLP, Retrieval-Augmented Generation (RAG), Speech-to-Text, fine-tuning,
and model optimization** to create a personalized English
conversation-learning experience.

Learners practice through natural, open-ended conversations by **text or
voice**. Instead of interrupting every sentence with corrections, the
assistant preserves conversational flow and analyzes the learner when
the session ends.

## Project Team

-   **Nourallah Ghonim**
-   **Mariam Eladawy**
-   **Zeyna Nader**
-   **Jalsim Mohamed**

## Project Idea

The project has two main stages.

### 1. Natural Conversation

The learner can communicate with the AI about different topics using
text or voice. The system should:

-   Maintain natural dialogue.
-   Remember conversation context.
-   Ask relevant follow-up questions.
-   Encourage the learner to communicate.
-   Avoid unnecessary correction during every turn.
-   Use RAG when educational knowledge or guidance is useful.

### 2. Personalized Session Assessment

After **End Session**, the system analyzes only the learner's messages
and produces a personalized report.

Evaluation areas include:

-   Grammar
-   Vocabulary
-   Fluency / Naturalness
-   Coherence
-   Sentence Structure
-   Repeated Mistakes

Feedback can include strengths, weaknesses, original mistakes, corrected
versions, more natural alternatives, explanations, repeated patterns,
and personalized exercises.

> CEFR/proficiency scoring should only be presented as calibrated when
> supported by the selected assessment data and evaluation methodology.

## Main Features

-   Natural AI-powered English conversation
-   Text and voice interaction
-   Whisper/equivalent Speech-to-Text
-   Conversation history
-   Prompt engineering
-   Retrieval-Augmented Generation
-   Open-source LLM
-   Fine-tuned model
-   LoRA / QLoRA
-   Quantization / model optimization
-   Base vs. fine-tuned model comparison
-   Session-level English assessment
-   Personalized corrections and exercises
-   React frontend
-   FastAPI backend
-   Optional Text-to-Speech

## AI Pipeline

``` text
Voice / Text
     |
     v
Speech-to-Text (when voice is used)
     |
     v
Prompt Engineering
     |
     v
RAG
     |
     v
Fine-Tuned & Optimized Open-Source LLM
     |
     v
AI Response
     |
     v
Optional TTS
```

Conversation history is maintained throughout the session and later
passed to the assessment system.

## Technology Stack

**AI / ML:** Python, open-source LLM, Hugging Face/Transformers, PEFT,
LoRA/QLoRA, quantization, Whisper/equivalent, LangChain/equivalent,
FAISS/Chroma/Qdrant, embedding models.

**Backend:** FastAPI, Pydantic, Python.

**Frontend:** React, JavaScript, Vite.

**Development:** Git, GitHub, Pull Requests, feature-branch workflow.

## Repository Structure

``` text
AI-Language-Coach/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── chat_routes.py
│   │   ├── voice_routes.py
│   │   ├── assessment_routes.py
│   │   └── health_routes.py
│   ├── schemas/
│   └── services/
├── ai/
│   ├── config.py
│   ├── llm/
│   ├── prompts/
│   ├── rag/
│   ├── assessment/
│   ├── feedback/
│   └── speech/
├── training/
│   ├── prepare_data.py
│   ├── train.py
│   ├── lora_train.py
│   ├── qlora_train.py
│   ├── inference.py
│   └── training_config.py
├── evaluation/
│   ├── evaluate_base.py
│   ├── evaluate_finetuned.py
│   ├── compare_models.py
│   ├── evaluate_rag.py
│   ├── evaluate_assessment.py
│   └── metrics.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── knowledge_base/
│   └── vector_db/
├── models/
│   ├── base/
│   ├── adapters/
│   └── optimized/
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── tests/
├── scripts/
└── docs/
```

## Git Branch Strategy

``` text
main
  ↑
develop
  ↑
  ├── feature/conversation-rag
  ├── feature/assessment-feedback
  ├── feature/training-optimization
  └── feature/frontend-backend
```

### `main`

Stable, demo-ready versions only.

### `develop`

Integration branch where completed feature work is combined and tested.

### `feature/conversation-rag`

LLM loading/generation, prompt engineering, embeddings, vector store,
retrieval, RAG, and conversation context.

### `feature/assessment-feedback`

Grammar, vocabulary, fluency/naturalness, coherence, sentence structure,
repeated mistakes, scoring, corrections, explanations, natural
alternatives, and personalized exercises.

### `feature/training-optimization`

Dataset processing, fine-tuning, LoRA/QLoRA, quantization, inference,
base-model evaluation, fine-tuned evaluation, and model comparison.

### `feature/frontend-backend`

FastAPI, React, API integration, conversation history, Whisper/STT,
voice interaction, report UI, end-to-end integration, and optional TTS.

## Git Workflow

``` text
Feature Branch
      |
      v
Commit + Test
      |
      v
Pull Request
      |
      v
develop
      |
      v
Integration Testing
      |
      v
Pull Request
      |
      v
main
```

Avoid routine direct development on `main`.

## Dataset Strategy

  -----------------------------------------------------------------------
  Dataset                 Status                  Intended Role
  ----------------------- ----------------------- -----------------------
  ErAConD                 Selected                Learner conversational
                                                  English and error
                                                  patterns

  JFLEG                   Selected                Grammar correction,
                                                  fluency, natural
                                                  reformulation

  TSCC v2                 **Processing**          Teacher-student
                                                  tutoring, corrective
                                                  feedback, scaffolding

  Assessment /            In Progress             Proficiency / CEFR /
  Proficiency Dataset                             session-level
                                                  assessment grounding
  -----------------------------------------------------------------------

### ErAConD

Used for authentic learner conversational language and common learner
mistake patterns.

### JFLEG

Used as supplementary data for grammatical correction, fluency
improvement, and natural reformulation.

### TSCC v2

Access has been received. The dataset is currently being inspected and
processed before final transformation rules are implemented.

### Assessment Dataset

Selection is still in progress. Its intended purpose is stronger
grounding for proficiency and CEFR-related assessment.

## Data Processing Workflow

``` text
Raw Dataset
    ↓
Schema & License Inspection
    ↓
Cleaning
    ↓
Task-Specific Transformation
    ↓
Leakage-Aware Train / Validation / Test Split
    ↓
Training / Evaluation Data
```

Important rules:

-   Preserve meaningful learner errors.
-   Handle duplicates and empty records carefully.
-   Preserve dataset source and task type.
-   Avoid train/test leakage.
-   Inspect real schemas before assuming columns or annotations.
-   Respect dataset redistribution licenses.

## Fine-Tuning & Optimization

The project will evaluate the pretrained base model before and after
fine-tuning.

Candidate techniques:

-   LoRA
-   QLoRA
-   4-bit quantization
-   8-bit quantization

Comparison should include:

-   Response quality
-   Model/storage size where applicable
-   Memory usage
-   Inference latency/speed

All reported results must come from actual experiments.

## Planned API

``` text
GET  /health
POST /chat
POST /voice/transcribe
POST /session/evaluate
```

Suggested internal interfaces:

``` python
generate_response(user_message, conversation_history)
```

``` python
evaluate_session(conversation_history)
```

## Development Rules

-   Work on the assigned feature branch.
-   Merge completed work into `develop` through Pull Requests.
-   Test integration before merging `develop` into `main`.
-   Never commit secrets or API keys.
-   Document environment variables in `.env.example`.
-   Avoid committing large model weights.
-   Respect model and dataset licenses.
-   Keep modules reusable and replaceable.
-   Use structured JSON between AI, backend, and frontend.
-   Add meaningful tests and error handling.
-   Never fabricate model, assessment, or optimization results.

## Current Status

-   [x] Project idea defined
-   [x] Initial architecture defined
-   [x] GitHub repository created
-   [x] `main` branch created
-   [x] `develop` branch created
-   [x] Four feature branches created
-   [x] Initial dataset strategy defined
-   [x] TSCC v2 access received
-   [ ] TSCC v2 processing completed
-   [ ] Assessment dataset finalized
-   [ ] RAG pipeline completed
-   [ ] Assessment pipeline completed
-   [ ] Fine-tuning completed
-   [ ] Optimization completed
-   [ ] Base vs. fine-tuned evaluation completed
-   [ ] Voice pipeline completed
-   [ ] Frontend/backend integration completed
-   [ ] Final end-to-end demo completed

## Team Members

  Member
  ------------------
  Nourallah Ghonim
  Mariam Eladawy
  Zeyna Nader
  Jalsim Mohamed

## License

Project licensing and third-party dataset/model licensing will be
documented before final release. Individual datasets and pretrained
models remain subject to their respective licenses.
