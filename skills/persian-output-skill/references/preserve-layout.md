# Translate the text where it already belongs

The desired result is a Persian counterpart of the supplied article/page/document: translated text in its original semantic regions, with images, captions, media, links, and layout relationships preserved. This route supplements existing RTL guidance; it does not rebuild the original from a generic template.

## Intake and layout contract

Inspect the actual source and its rendered appearance. Identify text regions, image/media positions and dimensions, captions, columns, tables, links, and protected content. Preserve an original and write a translated copy by default. A URL authorizes reading and making that copy, not modifying or publishing the live site.

Distinguish preserving **structure** from preserving **exact coordinates**. Retain the image region, order, aspect ratio, crop, caption association, and surrounding sections. Compare coordinates when the user requests images in exactly the same place. Persian can occupy more lines: never promise pixel-identical layout without rendering and checking it. First fit text with natural equivalent wording and supported font metrics, without omitting meaning. If text cannot fit, present the concrete conflict and seek a choice between text reflow and exact geometry. Do not silently shrink to unreadable text, clip it, overlay an image, remove details, or move figures.

## HTML and websites

- Prefer editing supplied HTML/source components or the existing DOM structure. Translate coherent text blocks and map inline emphasis/links back into them; do not translate each fragment independently.
- Preserve element identity, content order, image `src`/`srcset`, alt-image association, dimensions, object-fit/crop, links, IDs, classes, data attributes, interactive behavior, and stylesheet/media references. Translate user-facing labels/alt text where appropriate; do not translate machine attributes, scripts, styles, code, math, or URLs.
- Scope `lang="fa" dir="rtl"` to translated text blocks. For this layout-preservation route, do not blindly set RTL on a grid/flex/table/layout ancestor: inherited direction can move columns or images. Keep layout containers in their original direction, and set Persian cells/labels independently. A newly designed Persian page uses the normal web route instead.
- Keep technical fragments LTR with existing inline markup or narrowly scoped isolation. Escape translated strings through safe text binding; never evaluate markup obtained from prose.
- Retain responsive rules. Compare before/after at equal viewport sizes, including mobile: media rectangles, section order, text overflow, caption pairing, and links. A screenshot checks appearance; DOM/source comparisons check protected text and assets.
- A text-only fetch loses original layout/assets. If full HTML or rendering is unavailable, offer a text translation or request the source; do not claim a faithful site copy. For an interactive site, hydration or later navigation may overwrite text; test actual states and report snapshot-only behavior when applicable.
- For an inline fragment or explicitly source-only transformation, preserve the supplied asset references and return the transformed source. Do not search for missing relative assets or launch a rendering pipeline outside that request; report geometry as unverified if a verification claim is needed. Static source translation does not require a complete deployed website.

Use the optional read-only helper for conservative static HTML pairs:

```text
python -X utf8 scripts/audit_html.py original.html translated.html --json
```

Paths are relative to the installed skill folder. The helper compares structural tags, stable attributes and protected code/scripts/styles. It permits text and language/direction attribute changes. A failure means inspect the difference: legitimate inline markup changes can also trigger it. It does not fetch URLs, translate, execute a page, or prove layout/translation quality. For changed asset URLs in an offline copy, verify file hashes explicitly; this helper intentionally flags the URL change.

## Word articles

Edit text in the existing document rather than create a new document with extracted paragraphs. Preserve styles, sections, headers/footers, relationships, hyperlinks, numbering, tables, inline pictures, floating anchors, wrap settings, extents, crop and caption references. Replacing a paragraph's entire `.text` can destroy runs and embedded objects: edit the relevant text runs while preserving their XML neighbors. For translation spanning runs, map sentence-level translation back to styled runs and validate the object anchors.

Apply RTL to Persian paragraphs and runs while protecting technical runs. Do not reverse an existing table globally if that would move graphics or change the user's layout; apply RTL within its text cells and keep its original column arrangement. Render all pages before/after and compare figure positions and page breaks. Without a capable renderer, state that geometry is unverified. Do not automatically convert Word to PDF unless requested.

## PDF articles

First classify the PDF as text-based, scanned, multi-column, or mixed. Inspect text bounding boxes, embedded fonts, figure/caption relationships and page geometry. When editable source exists, translate that and re-export; it is usually more reliable than replacing PDF drawing instructions.

For a source-less PDF, use a PDF editor/layout reconstruction pipeline only if available and permitted. Replace the source text in identified text regions, respecting columns and reading order; preserve page count/size, image positions, crop, resolution and links when exact layout is required. Do not white-out or redact a region without checking whether it overlaps a figure, chart label, or other page content. Preserve math and citations. Scanned PDFs need OCR and OCR review; rasterizing all content is not a substitute for translated selectable text.

Text embedded in a bitmap remains unchanged unless image-label translation is explicitly requested. State that limitation rather than repaint the image by default. Check shaped Persian visually and also search/copy extraction. If no pipeline can preserve geometry and provide usable Persian, explain this concrete limitation and request editable source or permission for a reflowed version; do not deliver an unrelated redesigned PDF as the same article.

## Completion evidence

Report which source regions were translated, what assets were preserved, what rendering was reviewed, and any geometry/extraction limit. Do not claim all sites or PDFs are supported because a static demo passed. The renderer-dependent limits in the existing document reference continue to apply.
