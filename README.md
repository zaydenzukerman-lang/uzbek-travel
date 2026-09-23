# Uzbek Travel — uzgbektravel.com
Static site for Mahmud's tour company (Tashkent). Built from the client's content blueprint.
- Edit content in `build.py`, then run `python3 build.py && python3 i18n.py build` (ALWAYS both, in that order).
- Translations: `i18n/ru.json`, `i18n/es.json` (keyed by English text hash). If you change English copy, run
  `python3 i18n.py extract` first — new/changed lines show as "untranslated" in the build output until added.
- Styles: `assets/css/style.css` · Scripts: `assets/js/main.js` · Photos: `assets/img/` (credits in CREDITS.md)
- Booking form posts to FormSubmit -> info.uzbektravelguide@gmail.com. The FIRST submission sends a one-time
  activation email to that inbox; someone must click it before enquiries start arriving.
- Preview locally: `python3 -m http.server 8000` then open http://localhost:8000
Live preview: https://zaydenzukerman-lang.github.io/uzbek-travel/ (GitHub Pages, repo zaydenzukerman-lang/uzbek-travel, deploys on push).
TODO: Instagram link (icon in footer, unlinked) · point uzgbektravel.com here when ready · activate FormSubmit.
