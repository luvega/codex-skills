# PPT Storyboard

Use storyboard first for group meetings, literature reports, course reports, defenses, and project updates.

Required elements:

```json
{
  "schema_version": "0.1",
  "brief_id": "short-id",
  "brief_type": "ppt_storyboard",
  "audience": "who will see it",
  "purpose": "why the deck exists",
  "slide_plan": [
    {
      "slide": 1,
      "action_title": "claim-style title",
      "core_point": "one message",
      "evidence_refs": ["Fig. 2b"]
    }
  ],
  "visual_assets": ["path or planned figure"],
  "evidence_map": [
    {
      "claim": "...",
      "evidence": "...",
      "status": "supported | partial | needs evidence | unsupported"
    }
  ]
}
```

Rules:

- Put the conclusion in the title.
- Use figures and tables instead of dense paragraphs.
- Put caveats in speaker notes when they are important but not the slide's main message.
- Add a methods slide before results if the audience cannot evaluate the evidence without it.
