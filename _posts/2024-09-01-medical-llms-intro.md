---
title: "Introduction to Large Language Models in Medicine"
date: 2024-09-01
categories: [AI in Medicine, Digital Health]
tags: [llm, medical-ai, generative-ai, clinical-nlp, gpt]
---

Large Language Models (LLMs) have moved from research curiosity to clinical conversation in a remarkably short time. From GPT-4 passing the USMLE to Med-PaLM 2 matching clinician-level performance on medical QA benchmarks, the question is no longer *can* AI understand medical language — it's *how* we deploy it safely.

This post is my attempt to lay a practical foundation: what LLMs actually are, where they show promise in healthcare, and where the hard problems remain.

---

## What is a Large Language Model?

An LLM is a neural network trained on vast amounts of text to predict the next token in a sequence. At scale, this simple objective produces models capable of reasoning, summarisation, translation, and question answering — without being explicitly programmed to do any of those things.

The architecture underlying most modern LLMs is the **Transformer** (Vaswani et al., 2017), which processes input as sequences of tokens and learns relationships between them via attention mechanisms. What makes today's models notable isn't just the architecture — it's the scale of training data and parameters (billions to hundreds of billions).

**Key milestones in medical LLMs:**

| Model | Organisation | Highlight |
|---|---|---|
| BioGPT | Microsoft | Pre-trained on PubMed for biomedical NLP tasks |
| Med-PaLM 2 | Google | Expert-level on MedQA; published in *Nature* |
| PMC-LLaMA | Meta (fine-tuned) | Open-weight model on medical literature |
| MedAlpaca | Stanford | Instruction-tuned for clinical conversations |
| GPT-4 | OpenAI | Passed USMLE Step 1–3 without fine-tuning |

---

## Where LLMs Show Real Promise

### 1. Clinical Documentation
The biggest immediate win. LLMs can transcribe and structure clinical conversations into SOAP notes, reduce documentation burden, and generate discharge summaries. Tools like Nuance DAX and Nabla Copilot are already deployed in hospitals.

The appeal is clear: physicians spend nearly **2 hours on documentation for every 1 hour of patient contact** (Sinsky et al., 2016). Any reduction has direct impact on burnout and time-to-care.

### 2. Clinical Decision Support
LLMs can surface relevant differential diagnoses, drug interactions, or guideline-concordant recommendations. Unlike rule-based systems, they can handle free-text inputs and reason across ambiguous presentations.

Important caveat: these systems should augment, not replace, clinical reasoning. Blind trust is dangerous.

### 3. Patient-Facing Communication
Explaining complex diagnoses in plain language, answering FAQs about medications, and triaging symptoms. LLMs can personalise communication at scale — something previously impossible.

### 4. Medical Research Acceleration
Literature synthesis, hypothesis generation, extraction of structured data from unstructured trial reports. This is where I spend most of my research time.

---

## Where the Hard Problems Remain

### Hallucination
LLMs confabulate — they generate plausible-sounding but factually wrong statements with confidence. In medicine, this is not a UX problem; it is a patient safety problem.

Hallucination rates vary by task and model but are non-zero in all current systems. Retrieval-Augmented Generation (RAG) helps by grounding responses in verified documents, but doesn't eliminate the problem.

### Calibration
A well-calibrated model expresses uncertainty proportional to its actual accuracy. Current LLMs are often overconfident. In clinical contexts, knowing *when the model doesn't know* matters as much as what it does know.

### Bias and Equity
LLMs trained predominantly on English-language, Western biomedical literature encode the gaps and biases of that literature. Models may perform differently across patient populations, languages, and health systems — a critical issue for global health.

### Regulatory and Liability Gaps
Most medical LLM deployments exist in a regulatory grey zone. The FDA has frameworks for AI/ML-based Software as a Medical Device (SaMD), but LLMs with general-purpose outputs challenge these boundaries. Liability when an AI-assisted decision leads to harm remains legally unresolved in most jurisdictions.

---

## A Framework for Evaluation

When evaluating an LLM for clinical use, I find it useful to ask:

1. **Task definition**: Is the task narrow and well-defined (e.g., ICD coding) or open-ended (e.g., clinical reasoning)?
2. **Grounding**: Does the system retrieve from verified sources (RAG), or purely generate from parametric memory?
3. **Human oversight**: Where does the human stay in the loop? For high-stakes decisions, the loop must be tight.
4. **Evaluation dataset**: Was performance measured on held-out data from the target population and clinical setting?
5. **Failure modes**: Has the system been red-teamed for the specific failure modes relevant to the clinical context?

---

## Looking Ahead

The next frontier isn't bigger models — it's better integration. LLMs need to talk to EHR systems (ideally via FHIR APIs), reason over structured clinical data alongside unstructured notes, and operate within clear accountability frameworks.

The models are impressive. The infrastructure, governance, and clinical workflow integration are the bottlenecks.

In future posts, I'll explore RAG architectures for clinical knowledge bases, the role of knowledge graphs in making LLMs more reliable, and what truly "clinical-grade" AI evaluation should look like.

---

*References:*
- *Singhal K, et al. (2023). Large language models encode clinical knowledge. Nature.*
- *Sinsky C, et al. (2016). Allocation of physician time in ambulatory practice. Annals of Internal Medicine.*
- *Vaswani A, et al. (2017). Attention is all you need. NeurIPS.*
