"""Erzeugt die Unterseiten (Leistungen + Bremen) aus einer gemeinsamen Vorlage.

Aufruf (im Repo-Root):  python scripts/build_pages.py
Die erzeugten HTML-Dateien landen in site/ und werden mit committet,
Vercel braucht also keinen Build-Schritt.
"""
import json
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
DOMAIN = "https://msh-photovoltaik.vercel.app"
VERSION = "10"  # Cache-Busting für styles.css / script.js, bei Änderungen hochzählen

ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ICON_ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/></svg>'

# Gemeinsame Daten -------------------------------------------------------------

SERVICES = [
    ("/leistungen/photovoltaik-wohngebaeude", "Wohngebäude"),
    ("/leistungen/photovoltaik-gewerbe", "Gewerbe & Industrie"),
    ("/leistungen/stromspeicher", "Stromspeicher"),
    ("/leistungen/wartung-service", "Wartung & Service"),
]

REFS = {
    "lilienthal": {
        "img": "ref1.webp", "w": 401, "h": 253,
        "alt": "Einfamilienhaus in Lilienthal in der Abenddämmerung",
        "meta": "12.4 kWp · Stromspeicher 10 kWh",
        "title": "Einfamilienhaus in Lilienthal",
        "text": "Saubere Montage, präzise Verkabelung und sichere Inbetriebnahme einer modernen Dachanlage.",
    },
    "bremen-nord": {
        "img": "ref2.webp", "w": 401, "h": 253,
        "alt": "Gewerbehalle in Bremen-Nord mit PV-Anlage aus der Luft",
        "meta": "84.5 kWp · Lastspitzenkappung",
        "title": "Gewerbehalle in Bremen-Nord",
        "text": "Präzise Montage, sichere Verkabelung und termingerechte Inbetriebnahme einer Gewerbeanlage.",
    },
    "weyhe": {
        "img": "ref3.webp", "w": 400, "h": 253,
        "alt": "Zweifamilienhaus in Weyhe mit Wallbox in der Einfahrt",
        "meta": "15.0 kWp · Wallbox-Integration",
        "title": "Zweifamilienhaus in Weyhe",
        "text": "Saubere Integration in die bestehende Anlage, fachgerecht verdrahtet und sicher umgesetzt.",
    },
}

PROVIDER = {"@type": "Organization", "name": "MSH Photovoltaik", "url": DOMAIN + "/"}
AREA = [
    {"@type": "City", "name": "Bremen"},
    {"@type": "AdministrativeArea", "name": "Umland von Bremen"},
    {"@type": "AdministrativeArea", "name": "Region Hannover"},
]

# Seiteninhalte ----------------------------------------------------------------

PAGES = [
    {
        "path": "/leistungen/photovoltaik-wohngebaeude",
        "nav": "Leistungen",
        "crumb": "Wohngebäude",
        "title": "Photovoltaik für Wohngebäude in Bremen | MSH Photovoltaik",
        "desc": "PV-Montage für Einfamilien- und Zweifamilienhäuser in Bremen und Umland: Unterkonstruktion, Module, Verkabelung und Inbetriebnahme durch eigene Monteure, in der Regel in 2 bis 3 Werktagen.",
        "service_type": "Montage von Photovoltaikanlagen auf Wohngebäuden",
        "h1": "Photovoltaik für Ihr Wohnhaus",
        "lead": "Wir montieren Photovoltaikanlagen auf Einfamilien-, Doppel- und Zweifamilienhäusern in Bremen und Umgebung. Unsere eigenen Monteure bauen Unterkonstruktion, Module und Verkabelung auf und nehmen die Anlage mit Ihnen in Betrieb.",
        "img": ("wohn.webp", 622, 254, "Einfamilienhaus mit Photovoltaikanlage auf dem Dach"),
        "included_title": "Das gehört zur Montage",
        "included": [
            ("Besichtigung vor Ort", "Wir sehen uns Dach, Dachaufbau, Zählerschrank und den Platz für Wechselrichter und Speicher an."),
            ("Gerüst und Absicherung", "Für die Arbeiten auf dem Dach wird ein Gerüst gestellt und der Arbeitsbereich gesichert."),
            ("Unterkonstruktion und Module", "Dachhaken oder Klemmen passend zu Ihrer Eindeckung, darauf die Schienen und Module."),
            ("DC- und AC-Verkabelung", "Leitungen vom Dach zum Wechselrichter und von dort zum Zählerschrank, sauber verlegt."),
            ("Inbetriebnahme und Übergabe", "Wir prüfen die Anlage, nehmen sie in Betrieb und zeigen Ihnen, wie Sie Ihren Ertrag ablesen."),
        ],
        "body_title": "Worauf es bei einem Wohnhaus ankommt",
        "body": [
            "Die meisten Häuser in Bremen und im Umland haben ein Sattel- oder Walmdach mit Ziegeln oder Betondachsteinen. Dort werden Dachhaken unter die Pfannen gesetzt, auf denen später die Schienen liegen. Bei Blech- und Flachdächern sieht die Befestigung anders aus. Was zu Ihrem Dach passt, klären wir bei der Besichtigung.",
            "Einfamilienhäuser haben meist eine Anlage zwischen 6 und 15 kWp. Wie groß Ihre Anlage wird, hängt von der freien Dachfläche, der Ausrichtung und Ihrem Stromverbrauch ab, etwa durch ein E-Auto oder eine Wärmepumpe.",
            "Ältere Zählerschränke müssen für eine PV-Anlage manchmal angepasst werden. Ob das bei Ihnen der Fall ist, sehen wir beim Termin vor Ort, bevor Sie ein Angebot unterschreiben.",
        ],
        "facts_title": "Auf einen Blick",
        "facts": [
            ("Montagedauer", "in der Regel 2 bis 3 Werktage"),
            ("Typische Größe", "6 bis 15 kWp beim Einfamilienhaus"),
            ("Mehrwertsteuer", "0 % auf Anlagen bis 30 kWp auf Wohngebäuden, inklusive Speicher und Montage"),
            ("Einsatzgebiet", "Bremen, Umland und Region Hannover"),
        ],
        "refs": ["lilienthal", "weyhe"],
        "faq": [
            ("Wie lange dauert die Montage auf einem Einfamilienhaus?", "In der Regel 2 bis 3 Werktage. Die genaue Dauer hängt von der Größe der Anlage, der Dachform und davon ab, ob ein Speicher oder eine Wallbox dazukommt."),
            ("Muss ich während der Montage zu Hause sein?", "Für die Arbeiten auf dem Dach nicht durchgehend. Für den Anschluss im Haus und die Übergabe am Ende sollte jemand da sein, das stimmen wir vorher ab."),
            ("Wer meldet die Anlage beim Netzbetreiber an?", "Die Anmeldung, die Planung und die Wirtschaftlichkeitsberechnung übernimmt ein Fachplaner, mit dem wir zusammenarbeiten. Wir sorgen für die Montage und eine saubere Inbetriebnahme."),
            ("Kann ich später einen Speicher oder eine Wallbox ergänzen?", "Ja. Beides lässt sich nachrüsten. Wenn Sie es schon planen, sagen Sie es uns bei der Besichtigung, dann legen wir Leitungen und Platz gleich passend aus."),
        ],
    },
    {
        "path": "/leistungen/photovoltaik-gewerbe",
        "nav": "Leistungen",
        "crumb": "Gewerbe & Industrie",
        "title": "PV-Anlagen für Gewerbe & Industrie in Bremen | MSH Photovoltaik",
        "desc": "PV-Montage auf Hallen- und Flachdächern in Bremen und Umland: Aufständerung, Verkabelung und Inbetriebnahme von Gewerbeanlagen, abgestimmt auf Ihren Betrieb.",
        "service_type": "Montage von Photovoltaikanlagen auf Gewerbe- und Industriegebäuden",
        "h1": "PV-Anlagen für Gewerbe und Industrie",
        "lead": "Hallen, Werkstätten und Lagergebäude haben oft große, ungenutzte Dachflächen. Wir montieren dort Photovoltaikanlagen und stimmen die Arbeiten so ab, dass Ihr Betrieb weiterlaufen kann.",
        "img": ("gewerbe.webp", 622, 254, "Große Gewerbehalle mit PV-Anlage auf dem Flachdach"),
        "included_title": "Das gehört zur Montage",
        "included": [
            ("Begehung von Dach und Technikräumen", "Dachaufbau, Zugänge, Platz für Wechselrichter und der Weg der Leitungen."),
            ("Abstimmung mit Ihrem Betrieb", "Wann wir aufs Dach können, wo Material lagert und welche Bereiche frei bleiben müssen."),
            ("Unterkonstruktion", "Aufständerung auf dem Flachdach oder Befestigung auf Trapezblech, je nach Dach und Statik."),
            ("Verkabelung und Wechselrichter", "Strangverkabelung, Wechselrichter und Anschluss an Ihre Verteilung."),
            ("Inbetriebnahme", "Prüfung der Anlage, Inbetriebnahme und Übergabe der Unterlagen."),
        ],
        "body_title": "Was bei Gewerbedächern anders ist",
        "body": [
            "Auf Flachdächern werden die Module meist aufgeständert und mit Ballast gesichert, damit die Dachhaut möglichst wenig durchdrungen wird. Wie viel Zusatzlast das Dach tragen kann, muss vorher geklärt sein. Bei älteren Hallen ist dafür oft ein Blick in die Statik nötig.",
            "Viele Betriebe verbrauchen tagsüber viel Strom, also genau dann, wenn die Anlage am meisten erzeugt. Ein großer Teil des Solarstroms wird so direkt im eigenen Betrieb genutzt.",
            "Mit einem Speicher lassen sich außerdem Lastspitzen abfangen: Der Speicher springt ein, wenn Maschinen kurzzeitig viel Leistung ziehen. Das kann den Leistungspreis senken, den Ihr Versorger für die höchste Spitze im Jahr berechnet. So haben wir es bei einer Gewerbehalle in Bremen-Nord umgesetzt.",
        ],
        "facts_title": "Auf einen Blick",
        "facts": [
            ("Dachformen", "Flachdach, Trapezblech, Sheddach"),
            ("Referenz", "84,5 kWp mit Lastspitzenkappung in Bremen-Nord"),
            ("Ablauf", "Begehung, Planung mit unserem Fachplaner, Montage, Inbetriebnahme"),
            ("Einsatzgebiet", "Bremen, Umland und Region Hannover"),
        ],
        "refs": ["bremen-nord"],
        "faq": [
            ("Kann der Betrieb während der Montage weiterlaufen?", "In den meisten Fällen ja. Gearbeitet wird vor allem auf dem Dach. Wann Leitungen im Gebäude verlegt werden und wann kurz abgeschaltet werden muss, stimmen wir mit Ihnen ab."),
            ("Trägt unser Hallendach eine PV-Anlage?", "Das hängt von der Konstruktion ab. Bei der Begehung schauen wir uns den Dachaufbau an. Wenn die Reserven unklar sind, sollte ein Statiker die Lastannahmen prüfen, bevor geplant wird."),
            ("Was bedeutet Lastspitzenkappung?", "Ein Speicher gibt Strom ab, sobald Ihr Betrieb kurzzeitig sehr viel Leistung zieht. Dadurch sinkt die höchste gemessene Spitze, nach der sich bei vielen Gewerbekunden ein Teil der Stromkosten richtet."),
        ],
    },
    {
        "path": "/leistungen/stromspeicher",
        "nav": "Leistungen",
        "crumb": "Stromspeicher",
        "title": "Stromspeicher nachrüsten in Bremen | MSH Photovoltaik",
        "desc": "Stromspeicher für neue und bestehende PV-Anlagen in Bremen und Umland: Einbau, Verdrahtung und Inbetriebnahme durch eigene Monteure.",
        "service_type": "Installation von Batteriespeichern für Photovoltaikanlagen",
        "h1": "Stromspeicher für Ihre PV-Anlage",
        "lead": "Ein Speicher hebt den Solarstrom vom Tag für den Abend auf. Wir bauen Speicher zusammen mit einer neuen Anlage ein oder rüsten sie in eine bestehende Anlage nach.",
        "img": ("speicher.webp", 622, 254, "Stromspeicher und Wallbox an einer Garagenwand"),
        "included_title": "Das gehört zum Einbau",
        "included": [
            ("Standort prüfen", "Keller, Hauswirtschaftsraum oder Garage: Wir prüfen Platz, Temperatur und den Weg zum Zählerschrank."),
            ("Passende Anbindung", "Ob der Speicher am Wechselrichter oder separat im Hausnetz hängt, richtet sich nach Ihrer Anlage."),
            ("Montage und Verdrahtung", "Speicher montieren, Leitungen verlegen, Messung im Zählerschrank einbauen."),
            ("Einrichtung", "Speicher in Betrieb nehmen und mit dem Monitoring Ihrer Anlage verbinden."),
        ],
        "body_title": "Neu planen oder nachrüsten",
        "body": [
            "Ohne Speicher wird der Strom, den Sie tagsüber nicht selbst brauchen, ins Netz eingespeist. Mit Speicher nutzen Sie ihn am Abend und in der Nacht. Wie viel das bringt, hängt davon ab, wann Sie Strom verbrauchen.",
            "Bei einer neuen Anlage wird der Speicher meist über einen Hybrid-Wechselrichter direkt angebunden. In bestehende Anlagen wird oft ein Speicher mit eigenem Wechselrichter eingebaut, der am Hausnetz hängt. So muss an der vorhandenen Anlage wenig geändert werden.",
            "Als grobe Richtschnur gilt etwa 1 kWh Speicher je 1.000 kWh Jahresverbrauch. Ein E-Auto oder eine Wärmepumpe verschieben die Rechnung. Ob ein Speicher für Ihren Haushalt sinnvoll ist, besprechen wir beim Termin vor Ort.",
        ],
        "facts_title": "Auf einen Blick",
        "facts": [
            ("Typische Größe", "5 bis 15 kWh im Einfamilienhaus"),
            ("Nachrüsten", "in bestehende Anlagen möglich"),
            ("Referenz", "10 kWh Speicher zu 12,4 kWp in Lilienthal"),
            ("Einsatzgebiet", "Bremen, Umland und Region Hannover"),
        ],
        "refs": ["lilienthal"],
        "faq": [
            ("Kann ich einen Speicher in meine bestehende Anlage einbauen lassen?", "Ja, in den meisten Fällen. Welche Lösung passt, hängt vom vorhandenen Wechselrichter und vom Platz ab. Das sehen wir uns vor Ort an."),
            ("Liefert ein Speicher Strom bei einem Stromausfall?", "Nicht automatisch. Dafür braucht es eine Notstrom- oder Ersatzstromfunktion, die Speicher und Wechselrichter unterstützen müssen und die beim Einbau mit eingerichtet wird. Sagen Sie uns vorher, ob Ihnen das wichtig ist."),
            ("Wo wird der Speicher aufgestellt?", "Meist im Keller, im Hauswirtschaftsraum oder in der Garage. Der Raum sollte trocken und frostfrei sein und nicht zu warm werden."),
        ],
    },
    {
        "path": "/leistungen/wartung-service",
        "nav": "Leistungen",
        "crumb": "Wartung & Service",
        "title": "Wartung & Service für PV-Anlagen in Bremen | MSH Photovoltaik",
        "desc": "Inbetriebnahme, Übergabe und Unterstützung bei Fehlermeldungen für PV-Anlagen in Bremen und Umland, dazu Erweiterungen wie Speicher und Wallbox.",
        "service_type": "Inbetriebnahme, Service und Erweiterung von Photovoltaikanlagen",
        "h1": "Wartung und Service für Ihre PV-Anlage",
        "lead": "Eine Anlage läuft 20 Jahre und länger. Wir nehmen sie sauber in Betrieb, erklären Ihnen, wie Sie sie im Blick behalten, und kommen vorbei, wenn etwas nicht stimmt oder die Anlage erweitert werden soll.",
        "img": ("wartung.webp", 622, 254, "Techniker prüft einen Wechselrichter mit einem Tablet"),
        "included_title": "Wobei wir helfen",
        "included": [
            ("Inbetriebnahme und Übergabe", "Funktionsprüfung, Inbetriebnahme und eine Übergabe mit allen Unterlagen zu Ihrer Anlage."),
            ("Monitoring einrichten", "Wir verbinden Wechselrichter und Speicher mit der App des Herstellers und zeigen Ihnen, was die Werte bedeuten."),
            ("Fehlermeldungen", "Meldet der Wechselrichter einen Fehler oder bricht der Ertrag ein, suchen wir vor Ort nach der Ursache."),
            ("Sichtprüfung", "Befestigung, Module, Kabel und Steckverbindungen werden auf Schäden geprüft."),
            ("Erweiterungen", "Speicher oder Wallbox nachrüsten und in die bestehende Anlage einbinden."),
        ],
        "body_title": "Woran Sie merken, dass etwas nicht stimmt",
        "body": [
            "Der einfachste Weg ist der Blick in die App Ihres Wechselrichters. Liegt der Ertrag an sonnigen Tagen deutlich unter dem, was die Anlage sonst bringt, oder zeigt der Wechselrichter eine Fehlermeldung, sollte jemand nachsehen.",
            "Häufige Ursachen sind ein Wechselrichter, der sich abgeschaltet hat, eine gelöste Steckverbindung oder Verschattung durch gewachsene Bäume. Vieles davon lässt sich vor Ort schnell eingrenzen.",
            "Wenn Ihr Haushalt wächst, etwa durch ein E-Auto, lässt sich die Anlage um einen Speicher oder eine Wallbox ergänzen. In Weyhe haben wir eine Wallbox in eine bestehende 15-kWp-Anlage eingebunden.",
        ],
        "facts_title": "Auf einen Blick",
        "facts": [
            ("Leistungen", "Inbetriebnahme, Übergabe, Fehlersuche, Sichtprüfung, Erweiterungen"),
            ("Erweiterungen", "Stromspeicher, Wallbox"),
            ("Kontakt", "telefonisch oder über das Anfrageformular"),
            ("Einsatzgebiet", "Bremen, Umland und Region Hannover"),
        ],
        "refs": ["weyhe"],
        "faq": [
            ("Muss eine PV-Anlage regelmäßig gewartet werden?", "Eine PV-Anlage braucht wenig Pflege. Wichtig ist, dass Sie den Ertrag im Blick behalten und bei Auffälligkeiten nachsehen lassen. Herstellergarantien können eigene Vorgaben machen, die stehen in den Unterlagen Ihrer Komponenten."),
            ("Was tun, wenn der Wechselrichter einen Fehler meldet?", "Notieren Sie die Fehlermeldung oder machen Sie ein Foto vom Display und melden Sie sich bei uns. Am Wechselrichter oder Zählerschrank sollten Sie selbst nichts öffnen."),
            ("Lässt sich eine Wallbox an die bestehende Anlage anbinden?", "Ja. Die Wallbox wird an Ihre Hausinstallation angeschlossen und kann so eingestellt werden, dass sie bevorzugt Solarstrom lädt, wenn die Komponenten das unterstützen."),
        ],
    },
    {
        "path": "/pv-montage-bremen",
        "nav": "",
        "crumb": "PV-Montage in Bremen",
        "title": "PV-Montage in Bremen & Umland | MSH Photovoltaik",
        "desc": "MSH Photovoltaik montiert PV-Anlagen und Stromspeicher in Bremen, Bremen-Nord und im Umland wie Lilienthal und Weyhe. Eigene Monteure aus Bremen, Besichtigung vor Ort.",
        "service_type": "Montage von Photovoltaikanlagen in Bremen",
        "area_override": [{"@type": "City", "name": "Bremen"}, {"@type": "City", "name": "Lilienthal"}, {"@type": "City", "name": "Weyhe"}],
        "h1": "PV-Montage in Bremen und Umland",
        "lead": "MSH Photovoltaik ist ein Familienbetrieb aus Bremen. Unsere eigenen Monteure bauen Photovoltaikanlagen und Stromspeicher in den Bremer Stadtteilen, in Bremen-Nord und in den Gemeinden rund um Bremen.",
        "img": ("map.webp", 491, 391, "Stilisierte Karte von Bremen"),
        "included_title": "Wo wir montieren",
        "included": [
            ("Stadt Bremen", "Alle Stadtteile, von Mitte und Schwachhausen über Findorff und Hemelingen bis Huchting und Obervieland."),
            ("Bremen-Nord", "Vegesack, Burglesum und Blumenthal. Hier haben wir eine 84,5-kWp-Gewerbeanlage gebaut."),
            ("Umland", "Gemeinden rund um Bremen wie Lilienthal und Weyhe, wo unsere Referenzanlagen stehen. Für weitere Orte fragen Sie einfach an."),
            ("Region Hannover", "Neben Bremen sind wir auch in der Region Hannover im Einsatz."),
        ],
        "body_title": "Photovoltaik in Bremen: was Sie vorab wissen sollten",
        "body": [
            "In Bremen gilt das Bremische Solargesetz. Es verlangt bei Neubauten, deren Bauantrag ab dem 1. Juli 2025 eingeht, eine Solaranlage auf dem Dach, und auch eine grundlegende Dachsanierung kann die Pflicht auslösen. Ob und in welchem Umfang das Ihr Haus betrifft, erklärt die <a href=\"https://umwelt.bremen.de/\" target=\"_blank\" rel=\"noopener\">Senatorin für Umwelt</a> in ihren Fragen und Antworten zum BremSolarG.",
            "Netzbetreiber in der Stadt Bremen ist in der Regel wesernetz. Bei ihm wird die Anlage angemeldet, bevor sie Strom ins Netz einspeist. Die Anmeldung und die Planung übernimmt unser Partner-Fachplaner, wir kümmern uns um Montage und Inbetriebnahme.",
            "Viele Bremer Altbauten, vor allem die typischen Bremer Häuser in Reihe, haben steile Satteldächer mit begrenzter Fläche. Hier kommt es auf eine genaue Belegung an. In Gebieten mit Denkmalschutz braucht es vorab eine Genehmigung der Denkmalbehörde.",
        ],
        "facts_title": "Auf einen Blick",
        "facts": [
            ("Firmensitz", "Bremen"),
            ("Netzbetreiber", "in der Stadt Bremen meist wesernetz"),
            ("Solarpflicht", "Bremisches Solargesetz (BremSolarG)"),
            ("Montagedauer", "in der Regel 2 bis 3 Werktage beim Einfamilienhaus"),
        ],
        "refs": ["lilienthal", "bremen-nord", "weyhe"],
        "services_block": True,
        "faq": [
            ("Gilt in Bremen eine Solarpflicht?", "Ja, über das Bremische Solargesetz. Sie betrifft Neubauten mit Bauantrag ab dem 1. Juli 2025 und kann auch bei einer grundlegenden Dachsanierung greifen. Die genauen Voraussetzungen und Ausnahmen beschreibt die Umweltbehörde in ihren FAQ zum BremSolarG."),
            ("Wer ist in Bremen der Netzbetreiber?", "In der Stadt Bremen in der Regel wesernetz. In den Gemeinden im Umland kann ein anderer Netzbetreiber zuständig sein. Die Anmeldung übernimmt unser Partner-Fachplaner."),
            ("Kommen Sie auch ins Bremer Umland?", "Ja. Referenzanlagen von uns stehen zum Beispiel in Lilienthal und Weyhe. Schreiben Sie uns Ihre PLZ, dann sagen wir Ihnen, ob wir zu Ihnen kommen."),
            ("Kann ich mir eine Ihrer Anlagen in Bremen ansehen?", "Fragen Sie uns. Wenn Kunden in Ihrer Nähe einverstanden sind, vermitteln wir gern einen Kontakt."),
        ],
    },
]

# Bausteine --------------------------------------------------------------------


def nav(active):
    items = [("/#ueber-uns", "Über uns"), ("/#leistungen", "Leistungen"), ("/#referenzen", "Referenzen"), ("/#faq", "FAQ"), ("#kontakt", "Kontakt")]
    links = ['<a href="/" class="nav__link">Startseite</a>']
    for href, label in items:
        cls = "nav__link is-active" if label == active else "nav__link"
        cur = ' aria-current="page"' if label == active else ""
        links.append(f'<a href="{href}" class="{cls}"{cur}>{label}</a>')
    links.append('<a href="#kontakt" class="btn btn--navy nav__cta-mobile">Montageanfrage</a>')
    return "\n        ".join(links)


def breadcrumb(p):
    parts = ['<a href="/">Startseite</a>']
    if p["path"].startswith("/leistungen/"):
        parts.append('<a href="/#leistungen">Leistungen</a>')
    parts.append(f'<span aria-current="page">{escape(p["crumb"])}</span>')
    sep = '<span class="crumbs__sep" aria-hidden="true">/</span>'
    return f'<nav class="crumbs" aria-label="Brotkrumen">{sep.join(parts)}</nav>'


def schema(p):
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Startseite", "item": DOMAIN + "/"}]
    if p["path"].startswith("/leistungen/"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Leistungen", "item": DOMAIN + "/#leistungen"})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": p["crumb"], "item": DOMAIN + p["path"]})
    data = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs},
        {
            "@context": "https://schema.org", "@type": "Service",
            "name": p["h1"], "serviceType": p["service_type"], "description": p["desc"],
            "url": DOMAIN + p["path"], "provider": PROVIDER,
            "areaServed": p.get("area_override", AREA),
        },
    ]
    return "\n".join(f'  <script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in data)


def ref_card(key):
    r = REFS[key]
    return f'''          <article class="card reveal">
            <div class="card__media card__media--ref"><img src="/assets/img/{r["img"]}" alt="{escape(r["alt"])}" loading="lazy" width="{r["w"]}" height="{r["h"]}" decoding="async" /></div>
            <div class="card__body">
              <p class="card__meta">{escape(r["meta"])}</p>
              <h3>{escape(r["title"])}</h3>
              <p>{escape(r["text"])}</p>
            </div>
          </article>'''


def page(p):
    img, iw, ih, ialt = p["img"]
    included = "\n".join(
        f'''            <li class="reveal">
              <span class="checklist__icon" aria-hidden="true">{ICON_CHECK}</span>
              <div>
                <h3>{escape(t)}</h3>
                <p>{escape(d)}</p>
              </div>
            </li>''' for t, d in p["included"])
    body = "\n".join(f"          <p>{para}</p>" for para in p["body"])  # body may contain trusted links
    facts = "\n".join(f"            <div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>" for k, v in p["facts"])
    refs = "\n".join(ref_card(k) for k in p["refs"])
    refs_cls = "refs" if len(p["refs"]) == 3 else "refs refs--few"
    faq = "\n".join(
        f'''          <details class="faq__item reveal"{" open" if i == 0 else ""}>
            <summary>{escape(q)}</summary>
            <div class="faq__answer"><p>{escape(a)}</p></div>
          </details>''' for i, (q, a) in enumerate(p["faq"]))
    others = [(h, l) for h, l in SERVICES if h != p["path"]]
    related_title = "Unsere Leistungen in Bremen" if p.get("services_block") else "Weitere Leistungen"
    related = "\n".join(f'          <a class="related__link" href="{h}">{escape(l)} {ICON_ARROW}</a>' for h, l in others)
    if p["path"] != "/pv-montage-bremen":
        related += f'\n          <a class="related__link" href="/pv-montage-bremen">PV-Montage in Bremen {ICON_ARROW}</a>'

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(p["title"])}</title>
  <meta name="description" content="{escape(p["desc"])}" />
  <link rel="canonical" href="{DOMAIN}{p["path"]}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{escape(p["title"])}" />
  <meta property="og:description" content="{escape(p["desc"])}" />
  <meta property="og:url" content="{DOMAIN}{p["path"]}" />
  <meta property="og:image" content="{DOMAIN}/assets/img/{img}" />
  <meta property="og:locale" content="de_DE" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="preload" href="/assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/styles.css?v={VERSION}" />
{schema(p)}
</head>
<body class="subpage">

  <!-- Erzeugt von scripts/build_pages.py – Änderungen bitte dort vornehmen. -->

  <header class="header" id="header">
    <div class="container header__inner">
      <a href="/" class="logo">
        <span class="logo__msh">MSH</span><span class="logo__bar" aria-hidden="true">|</span><span class="logo__pv">PHOTOVOLTAIK</span>
      </a>

      <nav class="nav" id="nav" aria-label="Hauptnavigation">
        {nav(p["nav"])}
      </nav>

      <a href="#kontakt" class="btn btn--navy header__cta">Montageanfrage</a>

      <button class="burger" id="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="nav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <main id="top">

    <section class="page-hero">
      <div class="container page-hero__grid">
        <div class="page-hero__body">
          {breadcrumb(p)}
          <h1 class="page-hero__title">{escape(p["h1"])}</h1>
          <p class="page-hero__lead">{escape(p["lead"])}</p>
          <div class="page-hero__actions">
            <a href="#kontakt" class="btn btn--orange btn--lg">Montageanfrage {ICON_ARROW}</a>
            <a href="tel:+4942198765432" class="page-hero__phone">{ICON_PHONE} 0421 987 654 32</a>
          </div>
        </div>
        <div class="page-hero__media">
          <img src="/assets/img/{img}" alt="{escape(ialt)}" width="{iw}" height="{ih}" fetchpriority="high" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container detail">
        <div class="detail__main">
          <h2 class="h2 reveal">{escape(p["included_title"])}</h2>
          <ul class="checklist checklist--spaced">
{included}
          </ul>
        </div>
        <aside class="facts reveal" aria-label="{escape(p["facts_title"])}">
          <h2 class="facts__title">{escape(p["facts_title"])}</h2>
          <dl>
{facts}
          </dl>
        </aside>
      </div>
    </section>

    <section class="section section--light">
      <div class="container prose reveal">
        <h2 class="h2">{escape(p["body_title"])}</h2>
{body}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head">
          <h2 class="h2 reveal">{"Referenzen aus der Region" if len(p["refs"]) > 1 else "Referenz aus der Region"}</h2>
        </header>
        <div class="{refs_cls}">
{refs}
        </div>
      </div>
    </section>

    <section class="section section--light">
      <div class="container container--narrow">
        <header class="section-head section-head--center">
          <h2 class="h2 reveal">Häufige Fragen</h2>
        </header>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

    <section class="section related-section">
      <div class="container">
        <h2 class="h2 reveal">{related_title}</h2>
        <div class="related reveal">
{related}
        </div>
      </div>
    </section>

    <section class="section section--gray" id="kontakt">
      <div class="container">
        <div class="cta reveal">
          <div class="cta__body">
            <h2 class="h2">Montage anfragen</h2>
            <p class="lead">Schreiben Sie uns Name, Telefonnummer und PLZ. Wir melden uns und vereinbaren einen Termin vor Ort.</p>
            <ul class="contact-list">
              <li>
                {ICON_PHONE}
                <a href="tel:+4942198765432">0421 987 654 32</a>
              </li>
              <li>
                {ICON_MAIL}
                <a href="mailto:beratung@msh-photovoltaik.de">beratung@msh-photovoltaik.de</a>
              </li>
            </ul>
          </div>

          <form class="quick-form" id="quickForm" novalidate>
            <h3>Schnellanfrage</h3>
            <label class="sr-only" for="f-name">Vollständiger Name</label>
            <input id="f-name" name="name" type="text" placeholder="Vollständiger Name" autocomplete="name" required />
            <label class="sr-only" for="f-tel">Telefonnummer</label>
            <input id="f-tel" name="tel" type="tel" placeholder="Telefonnummer" autocomplete="tel" required />
            <label class="sr-only" for="f-plz">PLZ / Ort</label>
            <input id="f-plz" name="plz" type="text" placeholder="PLZ / Ort (z.B. 28195 Bremen)" autocomplete="postal-code" required />
            <button type="submit" class="btn btn--orange btn--block">Montageanfrage senden</button>
            <p class="quick-form__msg" id="formMsg" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>
  </main>

{FOOTER}

  <script src="/script.js?v={VERSION}"></script>
</body>
</html>
'''


FOOTER = '''  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="/" class="logo logo--light"><span class="logo__msh">MSH</span><span class="logo__bar" aria-hidden="true">|</span><span class="logo__pv">PHOTOVOLTAIK</span></a>
          <p>Ihr zuverlässiger PV-Montagepartner aus Bremen. Wir setzen Ihre Photovoltaikanlage fachgerecht um – präzise, sauber und termingerecht.</p>
        </div>
        <div class="footer__col">
          <h4>Über uns</h4>
          <a href="/#ueber-uns">Unternehmen</a>
          <a href="/#ueber-uns">Unser Team</a>
          <a href="/pv-montage-bremen">PV-Montage in Bremen</a>
          <a href="/#kontakt">Karriere</a>
        </div>
        <div class="footer__col">
          <h4>Leistungen</h4>
          <a href="/leistungen/photovoltaik-wohngebaeude">Wohngebäude</a>
          <a href="/leistungen/photovoltaik-gewerbe">Gewerbe &amp; Industrie</a>
          <a href="/leistungen/stromspeicher">Stromspeicher</a>
          <a href="/leistungen/wartung-service">Wartung &amp; Service</a>
        </div>
        <div class="footer__col">
          <h4>Rechtliches</h4>
          <a href="#">Impressum</a>
          <a href="#">Datenschutz</a>
          <a href="#">AGB</a>
          <a href="#">Netzanschlussrichtlinien</a>
        </div>
      </div>
      <div class="footer__bottom">
        <p>© 2026 MSH Photovoltaik. Alle Rechte vorbehalten.</p>
        <p>Webdesign by <a class="footer__credit" href="https://www.luminary-studio.at/" target="_blank" rel="noopener">Luminary Studio</a></p>
      </div>
    </div>
  </footer>'''


def sitemap():
    urls = ["/"] + [p["path"] for p in PAGES]
    rows = "\n".join(f"  <url><loc>{DOMAIN}{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def main():
    for p in PAGES:
        out = SITE / p["path"].lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p), encoding="utf-8")
        print("wrote", out.relative_to(SITE.parent))
    (SITE / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print("wrote site/sitemap.xml, site/robots.txt")


if __name__ == "__main__":
    main()
