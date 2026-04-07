---
title: "Knowledge Graphs in Healthcare: Connecting the Dots"
date: 2025-02-01
categories: [AI in Medicine, Digital Health]
tags: [knowledge-graphs, medical-ai, ontology, graph-databases, clinical-reasoning]
---

Healthcare data is fundamentally relational. A diagnosis connects to symptoms, which connect to lab findings, which connect to treatment options, which connect to drug interactions, which connect to comorbidities. This web of relationships is exactly what **knowledge graphs** are designed to represent.

As I've been going deeper into this topic for my research, I've become convinced that knowledge graphs are one of the most underappreciated tools in the medical AI toolkit — and increasingly, the piece that makes LLMs genuinely reliable in clinical contexts.

---

## What is a Knowledge Graph?

A knowledge graph (KG) is a structured representation of real-world entities and the relationships between them, stored in a graph database. Formally:

- **Nodes (vertices)**: Entities — concepts, patients, drugs, genes, diseases
- **Edges**: Relationships between entities — *"metformin TREATS type-2 diabetes"*, *"BRCA1 ASSOCIATED_WITH breast cancer"*
- **Properties**: Attributes of nodes and edges — confidence scores, provenance, timestamps

The most common representation is **RDF triples**: Subject – Predicate – Object. For example:

```
<Metformin> <treates> <Type2Diabetes>
<Type2Diabetes> <hasSymptom> <Polydipsia>
<Metformin> <contraindicatedIn> <ChronicKidneyDisease>
```

Queried using SPARQL (for RDF graphs) or Cypher (for property graphs like Neo4j).

---

## Why Healthcare is a Natural Fit

Medicine has always been about navigating a complex network of relationships. Long before computers, physicians built mental models linking symptoms, pathophysiology, differentials, and treatments. Knowledge graphs make that implicit structure explicit and computable.

Several properties make KGs particularly well-suited for healthcare:

**Interpretability**: Unlike a neural network's hidden layers, a KG's reasoning is traceable. You can see *why* a system suggested a diagnosis — which connected entities led there.

**Knowledge integration**: Medical knowledge is distributed across thousands of sources — PubMed, clinical guidelines, drug databases, genomic databases. KGs can integrate heterogeneous sources under a common schema.

**Inference**: Using reasoning engines or graph neural networks, KGs can infer new knowledge — discovering drug repurposing candidates, predicting gene-disease associations, or identifying novel contraindications.

**Terminology grounding**: Linked to standard terminologies (SNOMED CT, MeSH, UMLS), KGs help resolve the ambiguity in natural language clinical text.

---

## Major Medical Knowledge Graphs

### UMLS (Unified Medical Language System)
The foundational metathesaurus from the US National Library of Medicine, integrating 200+ biomedical terminologies (SNOMED CT, ICD, MeSH, LOINC, etc.) into a unified concept network. Essential for NLP pipelines that need semantic normalisation.

### PrimeKG
A precision medicine knowledge graph integrating 20 biomedical databases — covering diseases, drugs, genes, pathways, and biological processes. Published in *Nature Scientific Data* (2023). Widely used for drug repurposing research and graph ML benchmarks.

### SPOKE (Scalable Precision Medicine Open Knowledge Engine)
Built at UCSF, SPOKE integrates biomedical data from 41 databases to create a 27-million-node, 54-million-edge graph. Used to identify COVID-19 drug candidates and in clinical decision support research.

### Hetionet
A heterogeneous network integrating data from 29 databases across 11 node types and 24 edge types. Open-access. Seminal work for graph-based drug repurposing.

### SNOMED CT as a Graph
SNOMED CT itself is a massive clinical terminology structured as a directed acyclic graph (DAG) — concepts are linked by hierarchical (Is-A) and non-hierarchical relationships. With ~350,000 concepts and ~1.5 million relationships, it's one of the largest clinical knowledge graphs in use.

---

## Applications in Clinical AI

### Drug Repurposing
Graph traversal and link prediction algorithms can identify existing approved drugs likely to be effective for new indications. This has been validated in COVID-19, ALS, and cancer research. The KG provides the hypothesis space; wet lab or clinical trials validate.

### Clinical Decision Support
KG-backed CDS can explain its reasoning: *"Suggested checking renal function because patient is on metformin AND has documented heart failure, and metformin is contraindicated in severe renal impairment."* The path through the graph is the explanation.

### Automated Clinical Coding
Mapping free-text diagnoses to ICD or SNOMED codes is a KG problem — matching text to nodes in a clinical terminology graph, resolved via embedding similarity and graph traversal.

### Making LLMs More Reliable (Knowledge Graph + RAG)
This is where I'm most excited. LLMs hallucinate partly because they rely on parametric memory that may be outdated, incorrect, or uncalibrated. Grounding LLM reasoning in a KG — retrieving relevant subgraphs as context — significantly reduces hallucination for factual medical queries.

The architecture: user query → entity extraction → KG subgraph retrieval → LLM generates response grounded in retrieved facts. Known as **Graph RAG** or **KG-augmented generation**.

---

## Challenges

### Knowledge Currency
Medical knowledge evolves fast. A KG that encodes drug interactions from 2020 guidelines may be dangerous by 2025. Maintaining and versioning medical KGs requires sustained effort and governance.

### Incompleteness
No KG captures all medical knowledge. The **open-world assumption** — that absence of a fact in the KG doesn't mean the fact is false — is clinically important. Reasoning engines and users must understand what the KG doesn't know.

### Integrating Structured and Unstructured Data
~80% of clinical data is unstructured (notes, letters, reports). Extracting entities and relationships from text using NLP and adding them to a KG is powerful but introduces noise. Entity recognition, relation extraction, and coreference resolution all have error rates that compound in graph populations.

### Scalability for Patient-Level Data
Population-level KGs encode medical knowledge. Patient-level KGs encode individual patient history. The combination — personalised reasoning over a patient's graph in the context of a population-level knowledge base — is the frontier. Systems like SPOKE are beginning to attempt this.

---

## Getting Started

If you want to explore medical knowledge graphs hands-on:

**Datasets and graphs:**
- [PrimeKG](https://github.com/mims-harvard/PrimeKG) — clean, well-documented, open access
- [Hetionet](https://het.io) — open access, great for learning graph ML
- [SNOMED CT Browser](https://browser.ihtsdotools.org/) — explore the clinical ontology

**Graph databases:**
- Neo4j — property graph, Cypher query language, excellent tooling
- Apache Jena / Stardog — RDF/SPARQL, better for linked data
- Amazon Neptune — managed cloud graph DB

**Libraries:**
- `networkx` (Python) — graph algorithms, simple to start
- `PyKEEN` — knowledge graph embedding models (TransE, RotatE, ComplEx)
- `PyG` (PyTorch Geometric) — graph neural networks

---

## The Bigger Picture

Knowledge graphs represent a vision of medical knowledge that is explicit, queryable, updatable, and auditable. In a field where unexplainable decisions cost lives, that matters.

The most powerful medical AI systems of the next decade will almost certainly combine the language fluency of LLMs with the factual precision of knowledge graphs. The two are complementary, not competing.

Getting the knowledge graph right — well-curated, current, semantically rich — is foundational work. It may be less glamorous than fine-tuning the latest model, but it's the infrastructure that makes reliable clinical AI possible.

---

*References:*
- *Chandak P, et al. (2023). Building a knowledge graph to enable precision medicine. Nature Scientific Data.*
- *Nelson SJ, et al. (2011). Normalized names for clinical drugs: RxNorm at 6 years. JAMIA.*
- *Himmelstein DS, et al. (2017). Systematic integration of biomedical knowledge prioritizes drugs for repurposing. eLife.*
