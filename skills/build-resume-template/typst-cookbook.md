# Typst design cookbook (for build-resume-template)

Patterns for writing a custom `profile/cv-template.typ` (and `cover-letter-template.typ`)
that honors the engine contract. **Start by copying `templates/cv.typ` and changing
from there** — it's the reference implementation and it's already contract-compliant.
Run `applywright check-template` after every change.

## How the pieces divide

- **The template styles; the markdown + postprocessor structure.** `profile/cv.md`
  holds the content and two layout conventions that a Python postprocessor turns into
  Typst *before* your template renders:
  - `@@@ text` → a **centered block**. `@@@(size=12pt) text` centers at that size.
    Used for the contact line and tagline under the name.
  - `left ||| right` → a **two-column row**, left-aligned + right-aligned
    (`columns: (1fr, auto)`). Used for `### **Company**, Location ||| 2022 – 2025`
    so dates sit flush right. Works inside heading lines too.
  - markdown `---` → a horizontal rule.
  Your template must not fight these. You style the headings, lists, links, page, and
  type; the `@@@`/`|||` handling is upstream and already done by the time your
  `#show` rules run.

## The contract scaffold (copy this, then style around it)

Every CV template needs these inputs and the page-count anchor. Leaving any out makes
`check-template` fail and silently breaks a feature.

```typst
// --- Inputs the engine passes in (do not rename) ---
#let content_path = sys.inputs.at("content_path", default: "")

// Font comes from profile/config.yaml -> style.font. Chosen font first, Arial fallback.
#let _font = sys.inputs.at("font", default: "Arial")
#let _font_stack = if _font == "Arial" { ("Arial",) } else { (_font, "Arial") }

// One-page auto-fit knobs. process-job tightens these to fit one page; honor them.
#let _margin_bottom = eval(sys.inputs.at("margin_bottom", default: "0.5in"), mode: "code")
#let _body_size = eval(sys.inputs.at("body_size", default: "10pt"), mode: "code")

#set page(paper: "us-letter",
  margin: (top: 0.45in, bottom: _margin_bottom, left: 0.55in, right: 0.55in))
#set text(font: _font_stack, size: _body_size, hyphenate: false)

// ... your #show heading / #set list / #show link rules go here ...

// --- Render the content (REQUIRED: the body lives here) ---
#if content_path != "" [ #include content_path ]

// --- Page-count anchor (REQUIRED for one-page auto-fit). Invisible, zero-size. ---
#context [ #metadata(counter(page).final().at(0)) <aw-pages> ]
```

The cover-letter template uses the same `content_path` + `font` reads, **omits** the
`<aw-pages>`/`margin_bottom`/`body_size` block, and instead reads the footer inputs:
`footer_name`, `footer_email`, `footer_phone`, `footer_site`, `footer_href` (see
`templates/cover-letter.typ`).

## Header (name, contact, tagline)

The name is the markdown H1; contact and tagline are `@@@`-centered lines in `cv.md`.
Style the H1 to set the header's character — size, weight, alignment, color.

```typst
// Centered name, classic:
#show heading.where(level: 1): it => {
  set text(size: 20pt, weight: "bold"); set align(center)
  block(below: 0.4em, it.body)
}
// Left-aligned name with an accent color (modern):
#show heading.where(level: 1): it => {
  set text(size: 24pt, weight: "bold", fill: rgb("#1f3a5f"))
  block(below: 0.2em, it.body)
}
```

## Section headers (H2)

The lever with the biggest visual payoff. Three directions:

```typst
// A) Centered, uppercase, rule below (the shipped look):
#show heading.where(level: 2): it => {
  v(1em); set align(center)
  block(below: 0.15em, text(size: 12pt, weight: "bold", upper(it.body)))
  set align(left); line(length: 100%, stroke: 0.5pt + rgb("#999999")); v(0.5em)
}
// B) Left, accent-colored, no rule (clean/modern):
#show heading.where(level: 2): it => {
  v(0.9em)
  block(below: 0.3em, text(size: 13pt, weight: "bold", fill: rgb("#1f3a5f"), upper(it.body)))
}
// C) Left, with a short accent underline:
#show heading.where(level: 2): it => {
  v(0.9em)
  text(size: 13pt, weight: "bold", upper(it.body))
  v(0.1em); line(length: 2.2em, stroke: 1.5pt + rgb("#c0392b")); v(0.4em)
}
```

## Role lines and the gray accent under a role

The company line is an H3 (`### **Company**, Location ||| dates`); the title sits under
it. To give the title or a one-line role descriptor a muted accent, style H3 / use a
gray fill. Keep the `|||` date column working — it's already a right-aligned grid by the
time you style the heading, so don't override its alignment.

```typst
#show heading.where(level: 3): it => {
  set text(size: 10pt, weight: "bold")
  block(above: 1em, below: 0.15em, it.body)
}
// Muted gray for a role subtitle line (if cv.md puts the title on its own line):
// wrap the title text in markdown so it lands as body text, then tint body-after-H3
// via a #show rule, or set the title line in cv.md as @@@-styled. Simplest: a gray
// emphasis run. Accent gray that reads well on white: rgb("#666666").
```

## Lists, links, spacing

```typst
#set list(marker: ([•]), indent: 0em, body-indent: 0.9em, spacing: 0.65em)
#show link: it => underline(text(fill: rgb("#0066cc"), it))
#set par(leading: 0.8em, spacing: 0.8em, justify: false)
#show emph: it => it.body  // globally disable italic, optional
```

Tighten `leading`/`spacing` and list `spacing` to buy vertical room before the auto-fit
ladder has to. Accent color is one variable — pick one and reuse it for the name, rules,
and links so the page reads as one system.

## Optional header photo (single-column only)

A small photo can sit beside or above the centered header. Keep it modest and let the
name dominate. The image path must be something the export can resolve; the simplest is
a file the user keeps in `profile/` and references by a root-relative path.

```typst
#grid(columns: (auto, 1fr), gutter: 1em, align: horizon,
  box(clip: true, radius: 50%, image("/profile/photo.jpg", width: 0.9in)),
  [ /* name + contact block here */ ])
```

Confirm with the user before adding a photo — it's a strong regional/role convention
(common in parts of Europe, unusual for US tech), so it's a choice, not a default.

## Colors that read on white

Navy `#1f3a5f`, slate `#334155`, muted gray `#666666` / `#999999`, link blue `#0066cc`,
a restrained accent like deep red `#c0392b` or teal `#0f766e`. Avoid low-contrast text
(below ~#777 for body) and more than one strong accent — one accent plus grays is the
reliable recipe.

## After any change

1. `applywright check-template profile/cv-template.typ` → must be all `[ok]`.
2. Render against the real `cv.md` and show the user.
3. Have the user render locally — their machine's fonts are the source of truth.
