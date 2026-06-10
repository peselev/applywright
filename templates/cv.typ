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

// --- Page setup ---
#set page(
  paper: "us-letter",
  margin: (top: 0.45in, bottom: 0.5in, left: 0.55in, right: 0.55in),
)

#set text(
  font: ("Calibri", "Carlito", "Helvetica", "Arial"),
  size: 10pt,
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
