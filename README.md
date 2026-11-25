# MSH Photovoltaik – Website

Onepager für MSH Photovoltaik, PV-Montagepartner aus Bremen.
Statisches HTML/CSS/JS, keine Build-Tools nötig.

## Lokal starten

```bash
python -m http.server 5510 --directory site
```

Dann http://localhost:5510 öffnen.

## Struktur

- `site/index.html` – Seite
- `site/styles.css` – Styles (Fonts self-hosted, keine Google-Server)
- `site/script.js` – Navigation, Scroll-Animationen, Zähler, FAQ, Formular
- `site/assets/` – Bilder (WebP), Hero-Video (Desktop + Mobil), Fonts, Favicon
- `site/leistungen/*/`, `site/pv-montage-bremen/` – Unterseiten, **erzeugt** von `scripts/build_pages.py`
  (Texte dort ändern, dann `python scripts/build_pages.py` ausführen; schreibt auch `sitemap.xml` und `robots.txt`)

## Offen

- Originalbilder statt Mockup-Ausschnitte
- Formular-Backend (aktuell nur clientseitige Validierung)
- Impressum & Datenschutz
- Echte Kontaktdaten und Kennzahlen bestätigen

Webdesign by [Luminary Studio](https://www.luminary-studio.at/)
