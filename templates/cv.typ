// CV template — resume layout.
//
// Font sizes are tuned to a clean one-page resume:
// - Name (H1):              18pt bold
// - Section headers (H2):   14pt bold, uppercase
// - Body/contact/tagline:   10pt
//
// All identity (name, contact line) lives in the CV markdown itself
// (profile/cv.md), not here. This file is pure styling.

#let content_path = sys.inputs.at("content_path", default: "")

// Font is a profile-wide setting (profile/config.yaml -> style.font), injected
// by `applywright export-pdf` as --input font=. Default Arial. The chosen font
// is tried first, with Arial as the fallback so a missing/misspelled name still
// renders. (When the choice already is Arial, the stack collapses to one entry.)
#let _font = sys.inputs.at("font", default: "Arial")
#let _font_stack = if _font == "Arial" { ("Arial",) } else { (_font, "Arial") }

// One-page auto-fit knobs (process-job tightens these on the retry path when the
// CV spills onto a second page). Values are Typst length literals, evaluated in
// code mode. Defaults match the original hand-tuned layout.
#let _margin_bottom = eval(sys.inputs.at("margin_bottom", default: "0.5in"), mode: "code")
#let _body_size = eval(sys.inputs.at("body_size", default: "10pt"), mode: "code")

// --- Page setup ---
#set page(
  paper: "us-letter",
  margin: (top: 0.45in, bottom: _margin_bottom, left: 0.55in, right: 0.55in),
)

#set text(
  font: _font_stack,
  size: _body_size,
  hyphenate: false,
)

#set par(
  leading: 0.8em,
  spacing: 0.8em,
  justify: false,
)

// Globally disable italic
#show emph: it => it.body

// --- Heading styles ---

// H1: Name — centered, bold, 18pt
#show heading.where(level: 1): it => {
  set text(size: 18pt, weight: "bold")
  set align(center)
  block(below: 0.5em, it.body)
}

// H2: Section headers — centered, bold, uppercase, rule BELOW
#show heading.where(level: 2): it => {
  v(1em)
  set align(center)
  block(
    below: 0.15em,
    text(size: 12pt, weight: "bold", upper(it.body))
  )
  set align(left)
  line(length: 100%, stroke: 0.5pt + rgb("#999999"))
  v(0.5em)
}

// H3 fallback (post-processor handles ||| company lines)
#show heading.where(level: 3): it => {
  set text(size: 10pt)
  block(above: 1em, below: 0.15em, it.body)
}

// --- Lists ---
#set list(
  marker: ([•]),
  indent: 0em,
  body-indent: 0.9em,
  spacing: 0.65em,
)

// --- Links: underlined blue ---
#show link: it => underline(text(fill: rgb("#0066cc"), it))

// --- Render content ---
#if content_path != "" [
  #include content_path
]

// Total physical page count, emitted as queryable metadata for the one-page
// auto-fit check. `applywright export-pdf` reads it with:
//   typst query ... templates/cv.typ "<aw-pages>"
// and parses the `value` field. Invisible (zero-size), so it never adds a page.
#context [
  #metadata(counter(page).final().at(0)) <aw-pages>
]
