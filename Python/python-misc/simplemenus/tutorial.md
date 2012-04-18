==========================
Tutorial für "simplemenus"
==========================

In diesem kleinen Tutorial möchte ich die Entwicklung eines Menüsystems für
einfache CLI Programme in Python beschreiben.

Viele Anfänger stehen vor dem Problem, zur Steuerung ihrer typischen kleinen
einsteigerfreundlichen Tools - wie Adressverwaltungen, Telefonbücher, TODO-
Listen, usw. - ein Menüsystem zu implementieren. Dieses soll einfach wie folgt
aussehen

```
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```

Der Benutzer soll dann durch Eingabe des zugehörigen Indizes die Aktion
auslösen.

So weit so gut und einfach.

Doch wie setzt man so etwas um?


Naiver Versuch
--------------

Man sieht recht häufig Code wie diesen:

```python
def menu():
    while True
        print(
            "1  Eintrag hinzufügen",
            "2  Eintrag löschen",
            "3  Eintrag suchen",
            "4  Beenden",
            sep="\n"
        )
        choice = int(input("Ihre Wahl? "))
        if choice == 1:
            add_entry()
        elif choice == 2:
            remove_entry()
        elif choice == 3:
            search_entry()
        elif choice == 4:
            sys.exit(0)
        else:
            print("Bitte nur Zahlen zwischen 1 und 4 eingeben!")
```

Das sieht doch ganz einfach aus. Ist das also eine gute Lösung?

Ich überlege mir folgendes: Ich möchte mein Programm um eine Laden- und 
Speichern-Funktion erweitern. Was müsste ich also tun, um mein Menü zu 
erweitern?

Schauen wir uns die Stellen im einzelnen an:

```python
        print(
            "1  Eintrag hinzufügen",
            "2  Eintrag löschen",
            "3  Eintrag suchen",
            "4  Telefonbuch speichern",
            "5  Telefonbuch laden",
            "6  Beenden",
            sep="\n"
        )
```
Aha. Ich musste also zwischen meinen dritten und bis dato vierten Eintrag
etwas dazuschreiben. Ich muss dann noch daran denken, dass ich den Eintrag
"Beenden" nun mit der "6" nummeriere.

Weiter im Code...

In meinem `if...elif`-Block muss ich die Wahlmöglichkeiten des Benutzers 
erweitern und die neuen Funktionen verfügbar machen:

```python
        if choice == 1:
            add_entry()
        elif choice == 2:
            remove_entry()
        elif choice == 3:
            search_entry()
        elif choice == 4:
            save()
        elif choice == 5:
            load()
        elif choice == 6:
            sys.exit(0)
        else:
            print("Bitte nur Zahlen zwischen 1 und 6 eingeben!")
```
Auch hier muss ich daran denken, den Indexvergleich für das Beenden auf "6" zu
setzen. Außerdem muss ich die Schranken in der Fehlerausgabe anpassen...

Insgesamt sieht die Funktion nun so aus:

```python
def menu():
    while True
        print(
            "1  Eintrag hinzufügen",
            "2  Eintrag löschen",
            "3  Eintrag suchen",
            "4  Telefonbuch speichern",
            "5  Telefonbuch laden",
            "6  Beenden",
            sep="\n"
        )
        choice = int(input("Ihre Wahl? "))
        if choice == 1:
            add_entry()
        elif choice == 2:
            remove_entry()
        elif choice == 3:
            search_entry()
        elif choice == 4:
            save()
        elif choice == 5:
            load()
        elif choice == 6:
            sys.exit(0)
        else:
            print("Bitte nur Zahlen zwischen 1 und 6 eingeben!")
```

Puh! Ganz schön viel Arbeit! Dazu kommt noch, dass der Code immer aufgeblähter
wirkt, je mehr Optionen hinzukommen.

Das muss doch auch einfacher gehen...

... und das tut es!


Datenstrukturen
---------------

Python bietet einem von Hause aus einige sehr praktische Datenstrukturen an.
Mit Hilfe solcher *Strukturen*, kann man *Daten* *strukturieren*.

Welche Daten können wir denn in unserem Menü bisher identifizieren?

Wir haben einen zusammengesetzten String (in der `print`-Funktion), einzelne
Indizes und letztlich die Funktionen, die wir verfügbar machen wollen.

Aber halt? Sind Funktionen denn *Daten*? Das hängt ganz vom Betrachtungswinkel
ab. Funktionen sind erst einmal direkte Bestandteile eines Programms. Aber
für mein Menü kann ich die Funktionen ja auch als Bestandteil meiner
Menü-Definition ansehen... dann könnte man sie durchaus als Daten
interpretieren.

Auf jeden Fall können wir festhalten, dass alle diese Daten im Moment nicht
zusammengehörig sind; sie existieren lose gekoppelt in der `menu`-Funktion.
Wir erinneren uns an meine Änderungen - ich musste an mehreren Stellen im Code
etwas ändern, da Daten hinzugekommen sind.

Wieso fassen wir diese nicht einfach in eine Struktur zusammen und 
*"berechnen"* aus dieser Struktur den Menüaufbau, die möglichen Eingaben
und die aufzurufende Funktion?

Antwort: Weil das furchtbar kompliziert und wenig greifbar klingt... :-(
