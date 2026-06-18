// Document template — for JDs, fit assessments, and other readable documents.
// Plain layout, left-aligned, generous spacing. Different from CV — meant for
// reading prose, not scanning a resume.
//
// Pipeline:
//   1. pandoc input.md -t typst  →  raw Typst
//   2. python3 scripts/postprocess-typst.py  →  cleaned (handles ||| if present, strips anchors)
//   3. typst compile templates/document.typ output.pdf  →  PDF

#let content_path = sys.inputs.at("content_path", default: "")

// Profile-wide font (profile/config.yaml -> style.font), injected by
// `applywright export-pdf`. Default Arial, with Arial as the fallback.
#let _font = sys.inputs.at("font", default: "Arial")
#let _font_stack = if _font == "Arial" { ("Arial",) } else { (_font, "Arial") }

// --- Page setup ---
#set page(
  paper: "us-letter",
  margin: 1in,
)

#set text(
  font: _font_stack,
  size: 11pt,
  hyphenate: false,
)

#set par(
  leading: 0.7em,
  spacing: 0.9em,
  justify: false,
)

// Globally disable italic styling (consistent with CV template)
#show emph: it => it.body

// Horizontal rules: handled by scripts/postprocess-typst.py — it rewrites
// pandoc's `#horizontalrule` into a native Typst block before reaching here.

// --- Heading styles ---

// H1: document title — large, bold, left-aligned, with bottom rule
#show heading.where(level: 1): it => {
  set text(size: 18pt, weight: "bold")
  block(below: 0.4em, it.body)
  line(length: 100%, stroke: 0.5pt + rgb("#aaaaaa"))
  v(0.8em)
}

// H2: major sections — bold, medium-large, with extra space above
#show heading.where(level: 2): it => {
  set text(size: 14pt, weight: "bold")
  block(above: 1.4em, below: 0.5em, it.body)
}

// H3: subsections — bold, body-sized but distinct
#show heading.where(level: 3): it => {
  set text(size: 12pt, weight: "bold")
  block(above: 1em, below: 0.4em, it.body)
}

// H4 (rare) — bold inline
#show heading.where(level: 4): it => {
  set text(size: 11pt, weight: "bold")
  block(above: 0.7em, below: 0.3em, it.body)
}

// --- Lists ---
#set list(
  marker: ([•]),
  indent: 0em,
  body-indent: 0.6em,
  spacing: 0.5em,
)

// --- Links: subtle blue, underlined ---
#show link: it => underline(text(fill: rgb("#0066cc"), it))

// --- Render content ---
#if content_path != "" [
  #include content_path
]
