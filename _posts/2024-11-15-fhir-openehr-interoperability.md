---
title: "HL7 FHIR vs OpenEHR: Making Sense of Health Data Standards"
date: 2024-11-15
categories: [Digital Health, Interoperability]
tags: [fhir, openehr, hl7, interoperability, health-data, standards]
---

If you've spent any time in Digital Health, you've encountered the alphabet soup: HL7, FHIR, CDA, SNOMED, ICD, LOINC, OpenEHR. For clinicians new to the field, this is genuinely confusing — and for good reason. These standards solve different problems, have different histories, and often coexist awkwardly in real-world health information systems.

Two of the most important — and most frequently confused — are **HL7 FHIR** and **OpenEHR**. Let me break them down.

---

## Why Health Data Standards Exist

Healthcare data is a mess. A patient record created in a German hospital, a lab result from a private clinic in India, a prescription from a GP in Australia — all represent the same kinds of information, but stored in formats so different they're functionally incompatible.

Health data standards are the attempt to create a shared language: agreed ways of representing clinical information so that systems can exchange, understand, and act on data from other systems.

The clinical importance of getting this right cannot be overstated. Incomplete or mis-communicated patient data is a leading contributor to adverse events. Interoperability isn't a technical nicety — it's a patient safety issue.

---

## HL7 FHIR: The API Standard

**FHIR** (Fast Healthcare Interoperability Resources) is a standard developed by Health Level 7 (HL7) and published in versions since 2014, with R4 (released 2019) now the dominant version.

### The core idea
FHIR models clinical and administrative data as **Resources** — discrete, addressable units of information accessible via RESTful APIs. Think of it like a well-designed web API, but for health data.

Each resource represents something clinical: a `Patient`, an `Observation`, a `MedicationRequest`, a `DiagnosticReport`. Resources have defined fields, data types, and relationships. They're encoded in JSON or XML and exchanged via standard HTTP methods.

```json
{
  "resourceType": "Observation",
  "id": "blood-glucose-001",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "2339-0",
      "display": "Glucose [Mass/volume] in Blood"
    }]
  },
  "valueQuantity": {
    "value": 6.3,
    "unit": "mmol/L"
  }
}
```

### What FHIR is good at
- **Integration and data exchange** between systems (EHR ↔ app ↔ lab ↔ payer)
- **API-first design** — built for the modern web
- **Wide industry adoption** — mandated in the US (21st Century Cures Act), Australia (My Health Record), UK (NHS), and increasingly in EU regulation
- **Implementation speed** — relative to older HL7 v2 and CDA, FHIR is much easier to implement

### What FHIR is less good at
FHIR's flexibility is also its weakness. Resources have many optional fields and the standard allows significant variation in how data is represented. Without additional profiling (via **Implementation Guides**), two FHIR-conformant systems may still fail to semantically interoperate.

FHIR is also primarily a transport and exchange standard. It doesn't prescribe how clinical knowledge should be structured or validated — that's where OpenEHR comes in.

---

## OpenEHR: The Clinical Knowledge Standard

**OpenEHR** is an open specification — not a product or a vendor — that defines how to model, store, and query clinical information. Its roots go back to the 1990s (the GEHR project, later Synapses and EHCR) and it has been actively developed since.

### The core idea
OpenEHR separates concerns cleanly into two levels:

1. **The Reference Model (RM)**: The stable, generic information model defining how any clinical record is structured — compositions, sections, entries, clusters, elements. This rarely changes.

2. **Archetypes**: Reusable, formal definitions of clinical concepts — what "blood pressure measurement" means, what fields it has, what value ranges are valid. Archetypes are written in ADL (Archetype Definition Language) and stored in the CKM (Clinical Knowledge Manager).

3. **Templates**: Combinations of archetypes assembled for specific clinical use cases (e.g., an anaesthesia pre-op assessment form = archetype for allergies + archetype for current medications + ...).

The key insight: **clinical knowledge is separated from the software**. A change in clinical best practice (e.g., new fields added to a sepsis screening tool) can be made in the archetype without rewriting the EHR software.

### What OpenEHR is good at
- **Semantic richness** — fine-grained, clinically validated data models
- **Queryability** — AQL (Archetype Query Language) allows complex cross-record queries regardless of which EHR product stored the data
- **Longitudinal records** — designed for a patient's lifelong record, not just episodic encounter data
- **Clinical knowledge governance** — the CKM enables international collaboration on archetype definitions
- **AI/ML readiness** — highly structured, semantically consistent data is gold for training medical AI models

### What OpenEHR is less good at
- **Steeper learning curve** — archetypes and ADL require investment to understand
- **Smaller ecosystem** — fewer off-the-shelf integrations compared to FHIR
- **Tooling** — while improving, the tooling ecosystem is less mature than FHIR's

---

## FHIR vs OpenEHR: Not a Competition

This is the key point most introductions miss: **FHIR and OpenEHR solve different problems and are increasingly used together**.

| Dimension | FHIR | OpenEHR |
|---|---|---|
| Primary purpose | Data exchange (API) | Clinical knowledge modelling & storage |
| Paradigm | Resources + REST | Archetypes + canonical records |
| Granularity | Coarser (flexible) | Finer (semantically rich) |
| Industry adoption | Very broad (especially US, UK) | Strong in Europe, AU, NZ, LATAM |
| Best for | Integration between systems | Longitudinal record, research, AI |
| Query language | FHIR Search / CQL | AQL |

A growing architecture pattern is **FHIR as the access layer** (APIs that external apps call) sitting on top of **OpenEHR as the persistence layer** (the structured, queryable clinical record). This gives you both: the ecosystem reach of FHIR and the semantic depth of OpenEHR.

Projects like the **Better FHIR Bridge** and work within the **EHR Foundation** are building exactly these translation layers.

---

## Practical Implications for Digital Health Projects

If you're building or evaluating a digital health solution, here are the questions I'd ask:

**"What data exchange standard do you support?"**
If the answer is FHIR R4 with a published Implementation Guide, that's a good sign. Ask which Implementation Guide (US Core? IPS? local national profile?) — the details matter.

**"How is clinical data modelled internally?"**
FHIR says nothing about internal storage. Some systems store FHIR natively; others store in proprietary formats and generate FHIR on the fly. For research and AI use cases, the internal model quality matters enormously.

**"Can I run structured queries across the record?"**
If the answer requires extracting to a data warehouse first, the underlying storage probably isn't using a proper clinical knowledge model like OpenEHR.

---

## Where This Is Heading

**IPS (International Patient Summary)** — a FHIR-based specification for a minimal, cross-border patient summary — is gaining traction as part of the WHO Global Digital Health Strategy. It's built on FHIR R4 but references terminologies (SNOMED, LOINC) that provide the semantic layer FHIR alone lacks.

**The EU European Health Data Space (EHDS)** mandates FHIR-based APIs for patient access to data across member states. Implementation will force clarification of how FHIR and existing national EHR standards (many of which use OpenEHR) coexist.

For those of us in Digital Health research, the real opportunity is in the data: rich, semantically consistent longitudinal records that can feed next-generation AI systems. That future requires getting both the exchange (FHIR) and the modelling (OpenEHR) right.

---

*Further reading:*
- *HL7 FHIR R4 specification: hl7.org/fhir/R4*
- *OpenEHR specifications: openehr.org/programs/specification*
- *Clinical Knowledge Manager: ckm.openehr.org*
- *Kalra D, et al. (2020). OpenEHR — an open standard for electronic health records. Yearbook of Medical Informatics.*
