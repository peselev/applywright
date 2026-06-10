// Cover letter template — airy business-letter layout.
//
// Pipeline (same as document.typ):
//   1. strip-images-for-pdf.py
//   2. pandoc input.md -t typst
//   3. postprocess-typst.py
//   4. typst compile templates/cover-letter.typ output.pdf
//
// Inputs (via --input), all sourced from profile/config.yaml by the skill:
//   content_path : path to the processed Typst content (body of the letter)
//   footer_name  : full name shown in the footer
//   footer_email : email shown in the footer (also the mailto target)
//   footer_phone : phone shown in the footer (omitted if empty)
//   footer_site  : clean text shown for the site link (omitted if empty)
//   footer_href  : full URL the site link points to (may carry UTM params)
//
// The footer (email · name · phone · site) is a real page footer rendered
// here, NOT in the markdown body. The body markdown contains only greeting,
// paragraphs, and sign-off.
//
// SPACING NOTE: the greeting and sign-off get extra surrounding space. They
// are detected by content, not position, so the page footer never interferes:
//   - the greeting paragraph always contains "Hiring Team"
//   - the sign-off paragraph always begins "Sincerely,"
// Both phrases are fixed by the cover-letter skill. If those conventions
// change, update the matches below.

// Contact footer values come from profile/config.yaml, passed in by the
// cover-letter skill via --input. Defaults are neutral placeholders.
#let content_path = sys.inputs.at("content_path", default: "")
#let footer_name = sys.inputs.at("footer_name", default: "Your Name")
#let footer_email = sys.inputs.at("footer_email", default: "you@example.com")
#let footer_phone = sys.inputs.at("footer_phone", default: "")
#let footer_site = sys.inputs.at("footer_site", default: "")
#let footer_href = sys.inputs.at("footer_href", default: "")

// --- Page setup: generous top margin for white space at the top ---
#set page(
  paper: "us-letter",
  margin: (top: 1.6in, bottom: 1.1in, left: 1.1in, right: 1.1in),
  footer: [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(0.4em)
    #set text(size: 9pt, fill: rgb("#555555"))
    #align(center)[
      #link("mailto:" + footer_email)[#footer_email]
      #h(0.6em) · #h(0.6em) #footer_name
      #if footer_phone != "" [ #h(0.6em) · #h(0.6em) #footer_phone ]
      #if footer_site != "" [ #h(0.6em) · #h(0.6em) #link(footer_href)[#footer_site] ]
    ]
  ],
)

#set text(
  font: ("Calibri", "Carlito", "Helvetica", "Arial"),
  size: 11pt,
  hyphenate: false,
)

#set par(
  leading: 0.75em,
  spacing: 1.4em,
  justify: false,
)

#show emph: it => it.body
#show link: it => underline(text(fill: rgb("#0066cc"), it))

// Extra space around the greeting and sign-off (content-detected; see note above)
#show par: it => {
  let r = repr(it.body)
  if r.contains("Hiring Team") {
    it
    v(2.6em)        // extra space after the greeting
  } else if r.contains("Sincerely") {
    v(4.2em)        // ~4 extra lines before the sign-off
    it
  } else {
    it
  }
}

// --- Render the letter body ---
#if content_path != "" [
  #include content_path
]
