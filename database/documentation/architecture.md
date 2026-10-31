# CLAIMSIGHT AI - Database Architecture Documentation

## Multimodal Graph & Relational Entity Structure
CLAIMSIGHT AI blends MongoDB document flexibility with graph traversal characteristics:
1. **Claims**: Central entity referencing policies and vehicles.
2. **Evidence**: Stores cryptographic fingerprints (SHA-256) and file paths.
3. **Extracted Facts**: Structured atomic assertions extracted from documents and photos.
4. **Evidence Relationships**: Graph edges (`Supports`, `Contradicts`, `Corroborates`) forming the Evidence Relationship Graph.
5. **Accident Hypotheses**: Competing reconstructions (`H1`, `H2`, `H3`) with evidence attribution.
6. **Next-Best-Evidence**: Ranked forensic requests driven by the EIG heuristic formula.

