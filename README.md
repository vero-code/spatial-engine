# Spatial Engine AI 💡

> **DeepTech Autonomous Agent for Optical Physics & Energy Optimization**
> *Powered by Gemini 3 Pro & Google GenAI SDK*

Spatial Engine is a multimodal AI agent designed to act as a **Senior Optical Physicist**. Unlike standard chatbots, it combines Generative AI's vision capabilities with a deterministic physics engine to audit rooms, calculate lighting deficits, and project energy ROI.

---

## 🚀 Key Features

### 1. The Physics Core (Deterministic)
The agent does not "guess" math. It delegates calculations to a rigorous Python engine.
- **Illuminance Calculation**: Uses the Inverse Square Law ($E = I/d^2$) and Beam Angle geometry to calculate exact Lux levels at specific points.
- **ROI & Energy Calculator**: Computes financial savings (USD) and CO2 reduction when switching lighting technologies (e.g., Incandescent to LED).
- **Unit Tested**: All physics formulas are covered by `unittest` to ensure 100% reliability.

### 2. The Vision System (Multimodal)
The agent can "see" and audit a room from a single photograph using **Gemini 3.0 Vision**.
- **3x3 Grid Analysis**: Mentally divides the image into sectors to pinpoint features (e.g., "Window in Sector 3").
- **Material Detection**: Analyzes wall textures (Concrete vs. Paint) to estimate Albedo (reflection coefficients).
- **Shadow Detection**: Identifies under-lit zones requiring optimization.
- **Scale Estimation**: Uses **Reference Object Inference** (e.g., comparing room width to standard door frames) to estimate floor area without user input.

### 3. Agentic Workflow
- **Tool Use**: Autonomous Function Calling (The agent decides when to calculate vs. when to analyze).
- **Streaming CLI**: Real-time "Thinking" logs showing Tool Calls and arguments in the terminal.

---

## 🛠️ Project Structure

```text
spatial-engine/
├── my_agent/
│   ├── agent.py            # The "Brain": System Prompt, Tool Binding, Vision Handler
│   ├── physics_engine.py   # The "Core": Pure Python math functions (No AI here)
│   └── search_tool.py      # (In Progress) Market analysis tools
├── tests/
│   └── test_physics.py     # Unit tests verifying the math formulas
├── .env                    # API Keys configuration
├── pyproject.toml          # Dependencies (uv managed)
└── README.md               # Documentation
```

## ⚡ Quick Start

### Prerequisites

-   Python 3.12+
    
-   `uv` (modern Python package manager)
    
-   Google Gemini API Key
    

### Installation

1.  **Clone & Sync:**
    
    ```
    git clone https://github.com/vero-code/spatial-engine.git
    cd spatial-engine
    uv sync
    ```
    
2.  Configure Environment:
    
    Create a .env file:
    
    ```
    GOOGLE_API_KEY=your_gemini_key_here
    ```
    
3.  **Run the Agent:**
    
    ```
    # Run with a test image for Vision Audit
    uv run my_agent/agent.py
    ```
    
4.  **Run Tests:**
    
    ```
    # Verify physics engine integrity
    uv run python -m unittest discover tests
    ```
----------

## 🗺️ Roadmap Status

### 🚩 Sprint 1: The Core (Completed)
> *Status: Fully Operational. 100% Test Coverage.*
- [x] **Infrastructure**: Environment setup (`uv`), Project structure, Basic ADK integration.
- [x] **Physics Engine**: Deterministic calculations for Illuminance ($E = I/d^2$) and Energy ROI.
- [x] **Reliability**: Pydantic typing for tools, `unittest` suite coverage, Chain of Thought logging.
- [x] **Persona**: Senior Optical Engineer system prompt configuration.

### 👁️ Sprint 2: The Vision (Completed)
> *Status: Implemented. Agent "sees" geometry and materials.*
- [x] **Multimodality**: Binary File Handler for image uploads.
- [x] **Visual Analysis**: 3x3 Grid decomposition, Shadow Detection, Material/Albedo identification.
- [x] **Spatial Reasoning**: Scale estimation via Reference Object Inference (no user input needed).
- [ ] **Advanced Features**: PDF Parser for blueprints, Persistent Spatial State class.

### 🛒 Sprint 3: The Market (In Progress)
> *Goal: Connect physics to real-world economics.*
- [ ] **Google Custom Search API**: Integration for real-time product pricing (Amazon/Home Depot).
- [ ] **Smart Logic**: Product parser (regex for lumens/price), Rate finder, ROI Calculator.
- [ ] **Standards**: Knowledge base for Smart Home protocols (Zigbee/Matter/ISO).
- [ ] **Fallback Mechanisms**: Offline mode with averaged market data.

### 🎨 Sprint 4: The Interface (Planned)
> *Goal: Generative UI and Data Visualization.*
- [ ] **Visualization**: Matplotlib/Heatmap Engine for Lux mapping on photos.
- [ ] **Reporting**: HTML/CSS Report generation with PDF export.
- [ ] **Generative UI**: Interactive widgets (e.g., Budget slider) and Visual Debugging.

### 🏆 Sprint 5: The Pitch (Planned)
> *Goal: Polish and Submission.*
- [ ] **Optimization**: Latency reduction, Error handling, End-to-End testing.
- [ ] **Documentation**: Architecture diagrams, Demo video script, Final submission text.
   
----------

_Built for the Gemini 3 Hackathon._