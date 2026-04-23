# High-Level Architecture for AI Copilot in Langflow

Files:

- [architecture_high_level.mmd](/C:/Users/evgen/Downloads/project1/langflow_copilot_seed/architecture_high_level.mmd)
- [architecture_high_level.png](/C:/Users/evgen/Downloads/project1/langflow_copilot_seed/architecture_high_level.png)
- [architecture_high_level.jpg](/C:/Users/evgen/Downloads/project1/langflow_copilot_seed/architecture_high_level.jpg)

## Key idea

The architecture is centered around an internal canonical workflow representation.

- In **edit mode**, the incoming Langflow workflow JSON is first converted into the internal representation.
- The Copilot performs planning, editing, validation, and explanation over that internal representation.
- On output, the updated internal representation is converted back into Langflow-compatible JSON.

## Mermaid

```mermaid
flowchart LR
  USER["Business User"] --> UX["Copilot UX in Langflow"]
  UX --> ORCH["AI Copilot Orchestrator"]

  EDIT_JSON["Existing Langflow Workflow JSON\n(edit mode input)"] --> IN_ADAPTER["Input Adapter\nLangflow JSON -> Internal Representation"]
  IN_ADAPTER --> IR["Canonical Workflow IR\ncompact graph JSON preserving structure"]

  ORCH --> IR
  ORCH --> SKILLS
  ORCH --> CONTEXT
  ORCH --> GOVERNANCE

  subgraph SKILLS["Skill Layer"]
    INTAKE["Requirement Intake"]
    PLAN["Workflow Planner"]
    EDITOR["Graph Builder / Editor"]
    VALIDATE["Validator / Repair"]
    EXPLAIN["Explainer"]
  end

  subgraph CONTEXT["Context Layer"]
    RAG["RAG\ncomponent catalog\nbank policies\nworkflow templates"]
    STATE["State and Versioning\ndialog history\nworkflow snapshot\nchange diff"]
  end

  subgraph GOVERNANCE["Governance Layer"]
    POLICY["Policy Engine\nallow-lists\napproval for risky actions"]
    AUDIT["Audit Trail\nevents\ndecisions\nversions\ntrace"]
  end

  IR --> EDITOR
  IR --> VALIDATE
  IR --> EXPLAIN

  RAG --> SKILLS
  STATE --> SKILLS
  POLICY --> SKILLS

  EDITOR --> OUT_ADAPTER["Output Adapter\nInternal Representation -> Langflow JSON"]
  VALIDATE --> OUT_ADAPTER
  OUT_ADAPTER --> LF_JSON["Langflow Workflow JSON\n(output envelope)"]
  LF_JSON --> STORE["Langflow Canvas / Flow Store"]

  STORE --> COMPONENTS["Approved Components"]
  STORE --> MODELS["Approved Models"]

  EXPLAIN --> UX
  VALIDATE --> UX
  AUDIT --> UX
```
