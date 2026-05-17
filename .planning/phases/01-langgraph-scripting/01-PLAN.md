# Phase 1: LangGraph & Scripting - Plan

**Status:** Planned
**Mode:** MVP

## Goal
Setup LangGraph state and Agent 1 to generate scripts.

## Requirements Covered
- **GEN-01**: Agent 1 generates a 1-minute reflective/philosophical script using Gemini Pro.
- **GEN-05**: The LangGraph orchestrator manages the state and flow between all four generation agents.

## Tasks

- [ ] **Task 1: Setup project structure and dependencies**
  - Create standard Python project layout (`src/`, `tests/`, `requirements.txt`).
  - Add `langgraph`, `langchain-google-genai`, `python-dotenv`.
- [ ] **Task 2: Define State Schema**
  - Create `src/state.py`.
  - Define `VideoState` as a `TypedDict` with fields: `script`, `audio_path`, `video_path`, `final_video_path`, `status`.
- [ ] **Task 3: Implement Agent 1 (Scriptwriter)**
  - Create `src/agents/scriptwriter.py`.
  - Use `ChatGoogleGenerativeAI` (Gemini Pro).
  - Define prompt: "Write a 1-minute reflective, philosophical script (Shortsophy style) about {topic}."
- [ ] **Task 4: Implement Orchestrator (LangGraph)**
  - Create `src/graph.py`.
  - Initialize `StateGraph` with `VideoState`.
  - Add `scriptwriter` node.
  - Set entry point to `scriptwriter` and add an edge from `scriptwriter` to END.
  - Compile the graph.
- [ ] **Task 5: Create Entry Point**
  - Create `src/main.py`.
  - Allow running the graph with a test topic.

## Verification
- Run `python src/main.py` and verify that the output state contains a populated `script` string that matches the "Shortsophy" length and tone constraints.
