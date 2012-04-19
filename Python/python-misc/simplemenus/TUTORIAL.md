==================================================
Tutorial für das Erstellen von einfachen Textmenüs
==================================================

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

Das sieht doch ganz einfach aus. In einer Endlosschleife geben wir mittels
`print` das Menü aus, holen uns die Eingabe des Benutzers via `input` und
testen dann in einem `if...elif...else`-Block die einzelnen gültigen
Optionen. Trifft eine Bedingung zu, so rufen wir die passende Funktion auf,
die die eigentliche *Arbeit* verrichtet. Der Code sieht ziemlich verständlich
und einfach aus.

Ist das also eine gute Lösung?

Ich überlege mir folgendes: Ich möchte mein Programm um eine Laden- und 
Speichern-Funktion erweitern. Was müsste ich also tun, um mein Menü
anzupassen?

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


Trenne Code und Daten!
----------------------

Unser Problem besteht darin, dass wir die Daten für das Menü mit dem Code
für die Auswertung und die Darstellung mischen. Somit müssen wir an zig
verschiedenen Stellen den Code anpassen, wenn sich etwas an der Menüstruktur
ändert.

Wir müssen also unsere Menüdefinition irgend wie an einer Stelle im Code
bündeln. Darüber hinaus müssen wir die Defintion von der Verarbeitung
(also der Ausgabe, dem User-Input und der Auswertung) trennen.

Doch wie macht man das?

Ganz einfach: Wir müssen die Daten in einer passenden Daten*struktur*
zusammenfassen!


Benutze Datenstrukturen
------------------------

Python bietet einem von Hause aus einige sehr praktische Datenstrukturen an.
Mit Hilfe solcher Strukturen, kann man Daten strukturieren.

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
und die aufzurufenden Funktionen?

Antwort: Weil das furchtbar kompliziert und wenig greifbar klingt... :-(

Schauen wir uns doch mal ein einfaches Beispiel an:
    
```python
menu = [
    "1  Eintrag hinzufügen",
    "2  Eintrag löschen",
    "3  Eintrag suchen",
    "4  Beenden"
]
```
Wir haben hier eine simple Liste angelegt, die unsere vier Menüeinträge
beinhaltet. Diese können wir nun ausgeben lassen:
    
```python
In [2]: for item in menu:
   ...:     print(item)
   ...:     
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Ich benutze die Shell [IPython](http://ipython.org/) für meine Snippets. Also
sei nicht durch die `[2\]` verwirrt, das ist lediglich Teil der Ausgabe
von IPython.

Ok, also wir können also Listen einfach ausgeben. Aber was haben wir jetzt
dadurch gewonnen? Im Moment noch nicht viel.

Denken wir noch einmal an unseren ersten Versuch zurück. Bei Änderungen musste
ich den Index immer manuell anpassen, sobald ich Elemente irgend wo eingefügt
habe, oder bestehende tauschen wollte. Das müssten wir hier auch :-(

Ich überlege mir, dass ich den Index nicht mehr hart codiert an meine Einträge
schreiben dürfte, sondern ihn irgend wie *berechnen* können müsste... und
das geht auch!

Ich könnte einfach in einer Schleife hochzählen und dann diesen Index zusammen
mit dem zugehörigen Item ausgeben lassen.

Frisch ans Werk:

```python
In [4]: menu = [
    "Eintrag hinzufügen",
    "Eintrag löschen",
    "Eintrag suchen",
    "Beenden"
]

In [5]: for index in range(len(menu)):
    print("{}  {}".format(index+1, menu[index]))
   ...:     
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Wunderbar :-) Ich konnte in `[4]` den Index aus den Optionen rauswerfen und
habe diesen durch das Zählen mittels `range` selber erzeugt. Die Anzahl,
wie weit wir zählen müssen, habe ich mir mittels `len()` geholt. Im 
Schleifenrumpf habe ich einen String mit zwei Platzhaltern erstellt, die ich 
durch die `format`-Methode des Strings auffülle. Ich muss beim Index `1`
addieren, damit ich nicht `0` als ersten Menüpunkt erhalte. 
Aber Vorsicht, beim Zugriff auf ein Listenelement mittels Index muss ich 
natürlich den ursprünglichen und bei `0` startenden Index benutzen.

Leider ist obiger Code schlecht! Er ist eines der berühmten **Anti-Pattern**,
die man häufig bei Anfängern oder Umsteigern von anderen Sprachen sieht.

**Benutze diese Art von Code nie!**
    
Wie wir in `[2]` gesehen haben, iteriert man in Python immer **direkt** über
die Elemente einer Liste, oder allgemeiner eines `Iterable`. Damit erspart
man sich den Zugriff auf ein Element über den Index (wie in der 
`format`-Methode).

Was tut man also, wenn man neben dem eigentlichen Element auch noch einen Index
benötigt?

Python bietet dazu eine *Built-In* Funktion namens `enumerate` an. Diese 
erzeugt Tupel bestehend aus einem Index und dem zugehörigen Element.

Genau das, was wir hier brauchen:
    
```python
In [6]: for index, item in enumerate(menu, 1):
    print("{}  {}".format(index, item))
   ...:     
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Bingo. So sieht der Code auch viel übersichtlicher aus. Man erkennt anhand der
Namen im Schleifenkopf sofort, was für Objekte einem im Rumpf zur Verfügung
stehen. Ich übergebe `enumerate` einfach als ersten Parameter das iterierbare
Objekt. Als zweiten Parameter kann ich optional noch einen Startindex vorgeben.

So, nun teste ich mal meine neue Errungenschaft, indem ich mein Menü wie zu
Beginn angedacht mal erweitere und die Optionen zwei und drei tausche...

```python
In [8]: menu = [
...:    "Eintrag hinzufügen",
...:    "Eintrag suchen",
...:    "Eintrag löschen",
...:    "Telefonbuch speichern",
...:    "Telefonbuch laden",
...:    "Beenden"
...: ]

In [9]: for index, item in enumerate(menu, 1):
    print("{}  {}".format(index, item))
   ...:     
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Telefonbuch speichern
5  Telefonbuch laden
6  Beenden
```
Prima. Ich habe eine hübsche Menüausgabe, bei der der Index automatisch
*berechnet* wird. Nie wieder manuell Indexe ändern!!! :-)

Wir haben nun also Die Menüeinträge in einer Datenstruktur organisiert und die
Indexe komplett aus den Daten eleminiert, da wir diese direkt aus den 
Einträgen berechnen können.

Aber wie können wir nun die eigentlichen Funktionen (`add_entry`, 
`search_entry`, usw.) diesen Einträgen zuordnen? Und das müssen wir, wenn wir
diese ellen langen `if...elif`-Kaskaden loswerden und sämtliche Daten 
tatsächlich bündeln wollen.

Man müsste die Funktionen auch in dieser Liste eintragen können...

... und das kann man auch!


Funktionen sind auch Objekte!
-----------------------------

Wir haben bisher nur Strings in unserer Menü-Liste gespeichert, möglich sind 
aber auch Integer-, Float- oder auch boolsche Werte. Man kann es noch viel
drastischer und präziser formulieren:
    
Eine Liste kann in Python **jedes** beliebige Objekt aufnehmen!

Ist eine Funktion denn ein Objekt?

Ja, denn in Python ist **alles** ein Objekt. Also auch Funktionen.

Schauen wir uns das mal an:
    
```python    
In [11]: def foo():
   ....:     print("Bin in foo")
   ....:     

In [12]: foo()
Bin in foo

In [14]: type(foo)
Out[14]: builtins.function

In [15]: isinstance(foo, object)
Out[15]: True
```
Ich schreibe mir in `[11]` eine einfache Funktion, die nichts macht außer
einen Text zu printen. In `[14]` habe ich mir mittels der `type`-Funktion
einmal den Typen des Objektes ausgeben lassen, welches an den Namen `foo`
gebunden ist. Offensichtlich ist der Typ vom Typ `function`. Das kann man auch
in der offiziellen Doku in Abschnitt 4.11.4 nachlesen.

In `[15]` prüfe ich, ob das Objekt hinter `foo` vom (Sub-)Typ `object` ist.
`object` stellt den obersten Typen in der Typhirarchie dar. Eine Funktion ist
also auch vom Typ `object`, genauso wie z.B. ein Integer:

```python    
In [17]: isinstance(69, object)
Out[17]: True
```

Also müssten sich solche "Funktions"-Objekte doch auch in einer Liste speichern
lassen?

Testen wir das doch!

```python 
In [18]: def bar():
   ....:     print("Bin in bar")
   ....:     

In [19]: l = [foo, bar]

In [20]: l
Out[20]: [<function __main__.foo>, <function __main__.bar>]

In [21]: l[0]
Out[21]: <function __main__.foo>

In [22]: l[1]
Out[22]: <function __main__.bar>
```
In `[18]` erstelle ich mir zunächst noch eine kleine Funktion `bar`, die analog
zu `foo` funktioniert. In `[19]` passiert nun die "Magie"... zumindest sind
Anfänger davon immer verblüfft. Ich habe tatsächlich die Funktionen in einer
Liste untergebracht! **Achtung**: Ich habe dort nicht `foo()`, sondern nur 
`foo` geschrieben. Durch die runden Klammern teilen wir Python mit, dass wir
ein Objekt **aufrufen** wollen. In diesem Falle wollen wir aber nicht die
Funktion aufrufen, sondern nur über den Namen auf das "Funktions"-Objekt 
zugreifen.

Kann ich die Funktionen nun auch aufrufen?

Ja, klar doch:
    
```python 
In [26]: l[0]()
Bin in foo

In [27]: for func in l:
   ....:     func()
   ....:     
Bin in foo
Bin in bar
```
In `[26]` habe ich nun die Klammern `()` hinter meinen Indexzugriff geschrieben.
Python weiß nun, dass ich das Objekt hinter dem Index *aufrufen* möchte und tut
das auch.

Ich kann auch in einer Schleife über alle Funktionsobjekte in meiner Liste
iterieren und jedes einzeln aufrufen, wie in `[27]` zu sehen ist.

Moment. In Kopf der Schleife binde ich bei jedem Durchlauf das aktuelle
Funktionsobjekt an den Namen `func`... so etwas geht?

Ja, denn ich kann jedes Objekt in Python an einen Namen binden, natürlich auch
Funktionsobjekte. Schauen wir uns das mal an:

```python 
n [28]: a = foo

In [29]: a()
Bin in foo
```
Ich kann also meine Funktion `foo` an einen anderen Namen binden!

Aber es geht noch mehr:

```python 
In [30]: a is foo
Out[30]: True

In [31]: del foo

In [32]: a()
Bin in foo
```
Ich kann mittels `is` Operator prüfen, ob zwei Objekte **identisch** sind. Da
ich `a` an dasselbe Objekt binde, welches ursprünglich an `foo` gebunden wurde,
verweisen beide Namen also auf dasselbe Objekt. Wenn ich den Namen `foo`
lösche, so lösche ich nicht **direkt** das Objekt dahinter, sondern wirklich 
nur den Namen und damit meine Zugriffsmöglichkeit auf das Objekt. Ich kann
hier jedoch `a` immer noch aufrufen; das Objekt existiert weiter! Erst wenn ich
die letzte Referenz auf das Objekt lösche, also `a`, dann wird Pythons
*Garbage Collector* irgend wann das nicht mehr benutzbare Objekt löschen.

Aber halt. Das stimmt in diesem Falle noch nicht, da das Objekt ja inzwischen
auch in meiner Liste `l` gebunden ist.

```python 
In [37]: del a

In [38]: l
Out[38]: [<function __main__.foo>, <function __main__.bar>]

In [39]: l[0]()
Bin in foo
```
Ok, wir wollen ja die Funktion auch nicht löschen ;-) Aber nun wissen wir
schon mal einiges über Objkte und deren Verwaltung in Pyton.

Und vor allem wissen wir jetzt endlich genug, um unsere eigentliches Problem 
lösen zu können!

