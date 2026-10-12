# HTML and CSS

Set language and direction on the Persian document root:

```html
<html lang="fa" dir="rtl">
```

For a Persian section inside another-language page, scope `lang="fa" dir="rtl"` to that section. Use semantic markup, not text reversal or a page-wide Unicode prefix.

Known technical fragments should be isolated without changing text:

```html
<p>مسیر فایل: <bdi dir="ltr">C:\Projects\demo\config.json</bdi></p>
<p>نسخهٔ <bdi dir="ltr">v2.1.0</bdi> آماده است.</p>
<p>نام کاربر: <bdi dir="auto">user-provided name</bdi></p>
<pre dir="ltr"><code>python -m http.server 8080</code></pre>
```

Escape dynamic text with the framework's normal text-binding mechanism; never interpolate untrusted strings into raw HTML. Keep URL targets separate from their editable labels. Mark code blocks LTR and left-aligned, with horizontal overflow where needed.

Use CSS logical properties: `margin-inline`, `padding-inline`, `border-inline-start`, `text-align: start`. RTL can affect flex/grid placement and table column presentation: inspect reading order rather than blindly reversing DOM arrays. Preserve meaningful ordering of steps and data. Mirror directional navigation icons only when their meaning calls for it; logos and ordinary media need no automatic mirroring.

Use a font with Persian glyphs and shaping support; check actual fallback in the target browser. Do not download or redistribute a font without verifying its license. Maintain readable line-height, keyboard focus, and labels. Test at a narrow mobile width and desktop width, including long technical fragments.

For print/PDF export, check page breaks, margins, fonts, and links in the exported file; an on-screen page is not proof of print layout.

Source: [W3C inline bidi markup](https://www.w3.org/International/articles/inline-bidi-markup/).
