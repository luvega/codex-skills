# Research Interpretation Card

Use a card when a result may become a manuscript claim, review statement, slide takeaway, or teaching example.

Required fields:

```json
{
  "schema_version": "0.1",
  "card_id": "short-id",
  "domain": "bioinformatics | tumor-immunology | medicinal-chemistry | ai-methods | mixed",
  "finding": "what was observed",
  "method_context": {},
  "evidence_sources": [
    {
      "type": "figure | table | text | dataset | code | literature | passport | user_data",
      "locator": "Fig. 2b or passport:...",
      "summary": "what this source supports"
    }
  ],
  "interpretation": "what the result means, conservatively",
  "alternative_explanations": ["..."],
  "validation_needed": ["..."],
  "allowed_claim": "claim wording that can be used",
  "claim_status": "supported | partial | needs evidence | unsupported"
}
```

Claim rules:

- `supported`: direct evidence with a locator supports the full claim.
- `partial`: direction is supported, but mechanism, generality, or scope is limited.
- `needs evidence`: plausible but missing a figure, table, result, citation, or source note.
- `unsupported`: should be removed or reframed as a hypothesis.

Run:

```powershell
python scripts\check_research_interpretation_card.py path\to\card.json
```
