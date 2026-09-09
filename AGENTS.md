# Repository Guide

## Convention

* Naming
    * Prefer singular forms for section headings, file and directory names.

* Chat output
    * Surround display math blocks with blank lines for rendering compatibility.

* LaTeX
    * Prefer `pdfLaTeX` with `-synctex=1 -output-directory=.aux`.

* Python
    * Use `uv` for dependencies and `uv run <command>` for execution.

* Wolfram
    * Prefer file-based execution with `WolframKernel -script <file.wl>`.

* Lean
    * Manage toolchains with `elan`.
