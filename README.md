# README – YOLO (Objekterkennung)

## Projektbeschreibung

Dieses Repository dokumentiert den Einsatz des Objekterkennungsmodells **YOLO** im Rahmen der Bachelorarbeit im Studiengang Wirtschaftsinformatik an der Hochschule für Technik und Wirtschaft Berlin (HTW Berlin).

Ziel des Projekts ist die Erstellung einer **Nutzungs- und Leistungsdokumentation für GPU-gestützte Leihlaptops**. YOLO dient dabei als praxisnahes Einstiegsszenario für Studierende sowie als Werkzeug zur **Leistungsbewertung der GPU-Hardware** unter realistischen Bedingungen.

---

## Art der Daten

1. **Eingabebilder (Testdaten)**

   * Bilder in *.jfif*-Form
   * Motive: Tiere und komplexe Bildkompositionen
   * Zweck: reproduzierbare Tests der Objekterkennungsleistung

2. **Ergebnisbilder (Analyseartefakte)**

   * Bilder mit Bounding Boxes, Klassenlabels und Confidence Scores
   * Ergebnis der Anwendung des YOLO-Modells auf die Eingabebilder

3. **Logdaten**

   * CSV-Dateien mit Laufzeiten, GPU-Auslastung und weiteren Performancekennzahlen

**Sprache:** Deutsch

**Methode:**
Experimentelle Leistungsanalyse durch Vergleich von Eingabe- und Ergebnisbildern sowie Auswertung der Systemlogs.

---

## Datenursprung

* **Autor:** Studierender der HTW Berlin, Wirtschaftsinformatik (Bachelorarbeit)

* **Eingabebilder (Testdaten):**
  Die verwendeten Eingabebilder wurden aus öffentlich zugänglichen Internetquellen bezogen und dienen ausschließlich als **technische Test- und Referenzdaten** für die Leistungsbewertung der GPU-gestützten Leihlaptops. Eine inhaltliche Analyse der Bilder erfolgte nicht.

* **Ergebnisbilder (Bounding Boxes):**
  Die Ergebnisbilder wurden durch die Anwendung des YOLO-Modells vom Autor selbst erzeugt und stellen **abgeleitete Daten** dar.

* **Log- und Messdaten:**
  Die Performance-Logs wurden vollständig selbst erhoben.

* **Lizenz:**

  * **Code & Logs:** GNU General Public License v3.0
  * **Bilder:** Nutzung als Test- und Referenzdaten im Rahmen der Abschlussarbeit

---

## Datenformate und -umfang

* Bilder: *.jfif* (mehrere KB pro Datei)
* Logs: *.csv* (1-2 KB)

---

## Qualitätssicherung

* Vergleich identischer Eingabebilder über mehrere Durchläufe
* Überprüfung der Bounding Boxes und Klassenzuordnung
* Konsistente Dateibenennung zur Zuordnung von Input und Output

---

## Ordnerstruktur

```
/
├─ images_input/
├─ images_output/
├─ logs/
└─ README.md
```

---

## Hinweis zur Nachnutzung

Dieses Projekt dient primär der Dokumentation und Leistungsbewertung von GPU-Leihlaptops. Eine Weiterverwendung erfolgt unter Beachtung der GPLv3-Lizenz.


## Hinweis zur Nachnutzung

Die Nutzung der Daten und Ergebnisse ist unter den Bedingungen der Apache License 2.0 zulässig.
