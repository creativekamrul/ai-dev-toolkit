---
name: web-foundations
description: "Build plain HTML, CSS and progressive JavaScript interfaces with semantic structure, responsive layouts and no unrequested framework."
---

# Web foundations

Use semantic HTML and CSS for the requested plain web project. Do not introduce React, Next.js,
a bundler or a CSS framework just to implement layout. Inspect existing asset and deployment
conventions. Keep styling tokens and component boundaries understandable.

Start with real content structure, native form elements and accessible navigation. Use grid or
flex layout, fluid sizing and deliberate breakpoints based on content. Keep pages usable when
JavaScript fails where practical. Add JavaScript for behavior that requires it, with explicit
loading and error states. Avoid DOM injection of untrusted HTML.

Verify keyboard traversal, focus visibility, mobile overflow, form errors and link destinations.
Check real browser output and console errors. Optimize assets according to actual loading needs;
keep image dimensions and responsive sources explicit. Use the selected design contract rather
than a generic template. Report validation and any browser coverage not performed.
