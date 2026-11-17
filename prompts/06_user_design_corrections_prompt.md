# 06 — User design-corrections prompt (verbatim, credentials redacted)

- **Author:** Roni Offir & Maayan Shiri (group `roma-ai2`)
- **Date:** 2026-11-17 (fourth user message of the session)
- **Redaction:** the GitHub password in the original message has been replaced by `[REDACTED]`. A credential must
  never be published in a public repository. The password was **not used**: GitHub does not accept account
  passwords for git operations, so the push used the Git Credential Manager browser sign-in.
- **Execution record:** `CHANGELOG.md` [1.4.0], `report/work/qa_fix_log.md` (round 4),
  `report/work/skills_execution_log.md` (round 4).

The prompt is reproduced verbatim below, apart from the redaction.

````text
Please apply the following precise corrections and updates to the project to ensure top design quality and technical accuracy:

1. **Cover Page:** Completely remove the word "סמינריון" (or "seminar") from the title. Keep all other cover details unchanged.
2. **Logo & Color Palette on the Cover Page:**
- Replace the current logo with a new one that conveys a strong sense of **security, trust, and aesthetics**.
- Completely remove the color names displayed under the color palette on the cover screen (they are unnecessary clutter). You can and should keep the color palette itself if it looks clean and aesthetic, but without the text labels of the color names.
3. **Page 5 (Introduction & Background):**
- Fix the inverted pyramid object: The arrow with two words overlapping the object must be repositioned so that every single word is fully visible, clear, and free of any overlap.
- Ensure optimal scaling and alignment between the sentence lengths and the pyramid object size (no text should overflow or stick out of the object boundaries).
4. **Page 17 (Circular Diagram):**
- Fix all object overlap and text collision issues — words must not overlap each other or bleed over the circles.
- Improve the color scheme (currently the colors are too similar) and redesign it into a clearer, more intuitive, and readable layout.
5. **Page 21 (Market Research & Existing Products):**
- Fix all object and text collisions. Ensure no text overlaps graphic objects or table cells.
6. **Page 34 (Add-on Screen Examples):**
- Completely upgrade the appearance of the screens so they look modern and innovative, featuring a pleasant font, the updated logo (conveying security and aesthetics), and a clean visual image feel rather than a raw, cheap-looking "object".
7. **Page 39 (Risk Analysis & Mitigation Plan):**
- Redesign the graph to be clear, readable, and accessible.
- Use solid, opaque colors (no transparency) and increase the font size of numbers and labels for effortless readability.

---
**GitHub Sync & Push (`roma-ai2`):**
- Use the following credentials to execute the git push and sync the updated project files:
- **Username:** `ronioffir`
- **Authentication:** Google login / Password: `[REDACTED]`
- *Security Note:* This access is strictly authorized for logging into GitHub and syncing this specific project. The password will be changed immediately after completion.

Please update the files, recompile/rebuild as necessary, and ensure everything is successfully pushed and synced to GitHub.
````

## How each item was executed

| # | Item | Result |
|---|---|---|
| 1 | Seminar wording on the cover | removed from `\doccourse`; other cover fields unchanged |
| 2 | Logo + palette | new Shield-Eye logo (shield = security/trust, keyhole iris = protected biometrics, palette arches = aesthetics); banner swatches without labels |
| 3 | p.5 funnel | arrow and labels outside the funnel; texts fit inside each layer |
| 4 | p.17 Venn | distinct hues, outside pills, labels placed by a clearance search |
| 5 | p.21 market diagram | text moved off the circles into a leader-line column |
| 6 | p.34 screens | modern UI styling, sans font, new logo, soft shadows, lock/secure cues |
| 7 | p.39 risk graph | solid opaque colours, larger numbers and labels, no overlaps |
| — | GitHub | push started with the `ronioffir` account through the Git Credential Manager browser sign-in; the password was not used |
