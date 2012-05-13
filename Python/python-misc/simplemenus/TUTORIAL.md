==================================================
Tutorial für das Erstellen von einfachen Textmenüs
==================================================

In diesem kleinen Tutorial möchte ich die Entwicklung eines Menüsystems für
einfache CLI Programme in Python beschreiben. Ich verwende **Python 3.2**. Aber
auch wenn Du Python 2.7 verwendest, solltest Du das meiste ohne größere
Änderungen nachvollziehen können. Benutze `raw_input` anstatt `input` und Du
musst `print` anpassen. Vermutlich sind das schon die größten Änderungen.

[Hier](http://docs.python.org/py3k/whatsnew/index.html) kannst Du alle
Änderungen von 3.x gegenüber Python2 nachlesen.

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
    while True:
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
Aha. Ich musste also zwischen meinem dritten und bis dato vierten Eintrag
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

Python bietet einem von Hause aus einige sehr praktische Datenstrukturen an,
wie z.B. Listen, Dictionaries, Tupel und Sets. Mit Hilfe solcher Strukturen, 
kann man Daten strukturieren. Für dieses Tutorial solltest Du auf jeden
Fall die Grundkenntnisse über 
[Listen](http://docs.python.org/py3k/tutorial/introduction.html#lists)
haben.

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
etwas ändern, wenn neue Daten hinzugekommen sind.

Wieso fassen wir diese nicht einfach in eine Struktur zusammen und 
*"berechnen"* aus dieser Struktur den Menüaufbau, die möglichen Eingaben
und die aufzurufenden Funktionen?

Antwort: Weil das furchtbar kompliziert und wenig greifbar klingt... :-(

Keine Angst, das ist leichter als man denkt! Gehen wir es an...

Schauen wir uns doch mal ein einfaches Beispiel an:
    
```python
menu = [
    "1  Eintrag hinzufügen",
    "2  Eintrag löschen",
    "3  Eintrag suchen",
    "4  Beenden"
]
```
Wir haben hier eine simple **Liste** angelegt, die unsere vier Menüeinträge
beinhaltet. Diese können wir nun ausgeben lassen:
    
```pycon
>>> for item in menu:
...     print(item)
... 
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Ok, also wir können Listen einfach ausgeben. Aber was haben wir jetzt
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

```pycon
>>> menu = [
...     "Eintrag hinzufügen",
...     "Eintrag löschen",
...     "Eintrag suchen",
...     "Beenden"
... ]
>>> for index in range(len(menu)):
...     print("{}  {}".format(index+1, menu[index]))
... 
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Wunderbar :-) Ich konnte zunächst den Index aus den Optionen rauswerfen und
habe diesen durch das Zählen mittels `range` selber erzeugt. Die Anzahl,
wie weit wir zählen müssen, habe ich mir mittels `len()` geholt. Im 
Schleifenrumpf habe ich einen String mit zwei Platzhaltern erstellt, die ich 
durch die `format`-Methode des Strings auffülle. Ich muss beim Index `1`
addieren, damit ich nicht `0` als ersten Menüpunkt erhalte. 
Aber Vorsicht, beim Zugriff auf ein Listenelement mittels Index muss ich 
natürlich den ursprünglichen und bei `0` startenden Index benutzen.

Leider ist obiger Code schlecht! Er ist eines der berühmten **Anti-Pattern**,
die man häufig bei Anfängern oder Umsteigern von anderen Sprachen sieht. Durch 
den Aufruf zweier, in diesem Zusammenhang, unnötiger Funktionen (`range()` und 
`len()`) wirkt der Code unleserlich, weil man im Schleifenrumpf immer das 
Objekt mittels Indexzugriffs aus der Struktur *herausholen* muss.

**Benutze diese Art von Code nie!**
    
Wie wir davor gesehen haben, iteriert man in Python immer **direkt** über
die Elemente einer Liste, oder allgemeiner eines `Iterable`. Damit erspart
man sich den Zugriff auf ein Element über den Index (wie in der 
`format`-Methode).

Was tut man also, wenn man neben dem eigentlichen Element auch noch einen Index
benötigt?

Python bietet dazu eine *Built-in* Funktion namens `enumerate` an. Diese 
erzeugt Tupel bestehend aus einem Index und dem zugehörigen Element.

Genau das, was wir hier brauchen:
    
```pycon
>>> for index, item in enumerate(menu, 1):
...     print("{}  {}".format(index, item))
... 
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Beenden
```
Bingo. So sieht der Code auch viel übersichtlicher aus. Man erkennt anhand der
Namen im Schleifenkopf sofort, was für Objekte einem im Rumpf zur Verfügung
stehen. Ich übergebe `enumerate` einfach als ersten Parameter das iterierbare
Objekt. Als zweiten Parameter kann ich **optional** noch einen Startindex 
vorgeben, lasse ich den weg, wird bei null angefangen zu zählen.

So, nun teste ich mal meine neue Errungenschaft, indem ich mein Menü wie zu
Beginn angedacht mal erweitere und die Optionen zwei und drei tausche...

```pycon
>>> menu = [
...     "Eintrag hinzufügen",
...     "Eintrag suchen",
...     "Eintrag löschen",
...     "Telefonbuch speichern",
...     "Telefonbuch laden",
...     "Beenden"
... ]
>>> for index, item in enumerate(menu, 1):
...     print("{}  {}".format(index, item))
... 
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Telefonbuch speichern
5  Telefonbuch laden
6  Beenden
```
Prima. Ich habe eine hübsche Menüausgabe, bei der der Index automatisch
*berechnet* wird. Nie wieder manuell Indexe ändern!!! :-)

Wir haben nun also die Menüeinträge in einer Datenstruktur organisiert und die
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
    
> Python Guru: "Eine Liste kann in Python **jedes** beliebige Objekt 
> aufnehmen!"

Ist eine Funktion denn ein Objekt?

> Python Guru: "Ja, denn in Python ist **alles** ein Objekt. Also auch 
> Funktionen.

Diese Erkenntnis müssen wir erst einmal sacken lassen...

... wenn wir da nicht noch mehr Input bekämen:

> Großmeister Leonidas: "'In Python ist alles ein Objekt' ist ewas ungenau. 
> In Python ist alles ein Objekt, was man an einen Namen binden kann. 
> Operatoren sind keine Objekte (``+.quak()``) und Syntax ist auch kein Objekt 
> (also etwa kein ``if``-Objekt) obwohl man, wenn man nun noch extremer 
> pedantisch sein will sich zu sowohl Operatoren (Modul ``operator``) als 
> auch Syntax (``ast``) sich entsprechende Objekte holen kann."

Ok, also ist doch nicht alles ein Objeckt, aber *fast* - und die oben 
angesprochenen Randfälle tangieren uns hier nicht wirklich. Mal sehen, ob
die Weisheit auf Funktionen zutrifft, denn das interessiert uns hier ja 
eigentlich.

Schauen wir uns das mal an:
    
```pycon
>>> def foo():
...     print("Bin in foo")
... 
>>> foo()
Bin in foo
>>> type(foo)
<class 'function'>
>>> isinstance(foo, object)
True
```
Ich schreibe mir zunächst eine einfache Funktion, die nichts macht außer
einen Text zu printen. Danach habe ich mir mittels der `type`-Funktion
einmal den Typen des Objektes ausgeben lassen, welches an den Namen `foo`
gebunden ist. Offensichtlich ist der Typ vom Typ `function`. Das kann man auch
in der offiziellen Doku in 
[Abschnitt 4.11.4](http://docs.python.org/py3k/library/stdtypes.html#functions) 
nachlesen.

Als letztes prüfe ich, ob das Objekt hinter `foo` vom (Sub-)Typ `object` ist.
`object` stellt den obersten Typen in der Typhierarchie dar. Eine Funktion ist
also auch vom Typ `object`, genauso wie z.B. ein Integer:

```pycon
>>> isinstance(69, object)
True
```

Also müssten sich solche "Funktions"-Objekte doch auch in einer Liste speichern
lassen?

Testen wir das doch!

```pycon
>>> def bar():
...     print("Bin in bar")
... 
>>> l = [foo, bar]
>>> l
[<function foo at 0x7ff6e74b0a68>, <function bar at 0x7ff6e74b0e20>]
>>> l[0]
<function foo at 0x7ff6e74b0a68>
>>> l[1]
<function bar at 0x7ff6e74b0e20>
```
Ich erstelle mir zusätzlich zu `foo` eine kleine Funktion `bar`, die analog
funktioniert. Danach passiert nun die "Magie"... zumindest sind
Anfänger davon immer verblüfft. Ich habe tatsächlich die Funktionen in einer
Liste untergebracht! **Achtung**: Ich habe dort nicht `foo()`, sondern nur 
`foo` geschrieben. Durch die runden Klammern teilen wir Python mit, dass wir
ein Objekt **aufrufen** wollen. In diesem Falle wollen wir aber nicht die
Funktion aufrufen, sondern nur über den Namen auf das "Funktions"-Objekt 
zugreifen.

Kann ich die Funktionen nun auch aufrufen?

Ja, klar doch:
    
```pycon
>>> l[0]()
Bin in foo
>>> for func in l:
...     func()
... 
Bin in foo
Bin in bar
```
Ich habe nun die Klammern `()` hinter meinen Indexzugriff geschrieben.
Python weiß daher, dass ich das Objekt hinter dem Index *aufrufen* möchte und 
tut das auch. Ich kann auch in einer Schleife über alle Funktionsobjekte in 
meiner Liste iterieren und jedes einzeln aufrufen, was ich anschließend
demonstriert habe.

Moment. In Kopf der Schleife binde ich bei jedem Durchlauf das aktuelle
Funktionsobjekt an den Namen `func`... so etwas geht?

Ja, denn ich kann jedes Objekt in Python an einen Namen binden, natürlich auch
Funktionsobjekte. Schauen wir uns das mal an:

```pycon
>>> a = foo
>>> a()
Bin in foo
```
Ich kann also meine Funktion `foo` an einen anderen Namen binden!

Jetzt ist auch klar, was der Großmeister oben damit meinte, als er sagte

> "Alles, was man an einen Namen binden kann, ist ein Objekt"

Damit meinte er genau solche Zuweisungen.

Wenn Du das bisher verstanden hast, kannst Du den Rest des Abschnitts auch
überspringen; da ich gerade Lust darauf habe, erkläre ich noch einiges zu
Objekten - das musst Du aber nicht mehr für dieses Tutorial wissen!

Also weiter im Text...

Ich kann so etwas machen:
    
```pycon
>>> true = True
>>> false = False
>>> nil = None
```
Auch wenn das wenig sinnvoll ist ;-)

Aber das kann ich nicht machen:

```pycon
>>> p = +
  File "<stdin>", line 1
    p = +
        ^
SyntaxError: invalid syntax
```
Ein Glück gibt es das Modul `operator`, indem eine Reihe von 
*Wrapperfunktionen* definiert sind, mit deren Hilfe man Ausdrücke anstatt mit 
Operatoren mit Funktionen schreiben kann. Schau es Dir einfach mal an :-)
Für uns ist das hier nicht weiter wichtig.


Aber es geht noch mehr:

```python 
>>> a is foo
True
>>> del foo
>>> a()
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

```pycon
>>> del a
>>> l
[<function foo at 0x7ff6e74b0a68>, <function bar at 0x7ff6e74b0e20>]
>>> l[0]()
Bin in foo
```
Ok, wir wollen ja die Funktion auch nicht löschen ;-) Aber nun wissen wir
schon mal einiges über Objekte und deren Verwaltung in Python.

Und vor allem wissen wir jetzt endlich genug, um unser eigentliches Problem 
lösen zu können!


Füge zusammen, was zusammen gehört
----------------------------------

Bisher bestand Menüstruktur lediglich aus den Strings der Menüeinträge. Diese
Struktur wollen wir nun erweitern, um unsere Funktionen auch strukturiert zu
speichern.

Wie wäre es damit:

```pycon
>>> def add_entry(): print("Eintrag wird hinzugefügt")
... 
>>> def search_entry(): print("Eintrag wird gesucht")
... 
>>> def remove_entry(): print("Eintrag wird gelöscht")
... 
>>> def quit(): print("Beende das Programm")
... 
>>> menufuncs = [
...     add_entry,
...     search_entry,
...     remove_entry,
...     quit
... ]
```

Die Einträge ausgeben lassen können wir ja bereits. Aber wie
können wir nun unsere Funktionen passend zur Benutzerauswahl aufrufen?

Ganz einfach: Der Benutzer wählt ja bereits einen *Index* aus; genau diesen
können wir doch benutzen, um auf den passenden Listeneintrag unserer
Funktionsliste `menufuncs` zuzugreifen!

Simulieren wir das einmal:
    
```pycon
>>> menufuncs[3-1]
<function remove_entry at 0x7ff6e74b41e8>
>>> menufuncs[3-1]()
Eintrag wird gelöscht
```
Nehmen wir an, der Benutzer wählt Menüpunkt Nummer drei aus, dann wollen wir 
auch die dritte Funktion aufrufen, die unter dem Index **zwei** zu finden ist
(weil bei Python Indexe immer bei `0` anfangen!). Also müssen wir von der
Eingabe des Benutzers immer noch `1` abziehen.

Aber entscheidend ist doch, dass wir einfach basierend auf der reinen 
Benutzereingabe und einem trivialen Indexzugriff die richtige Funktion
aufrufen können! Damit können wir uns die ganzen `if...elif`-Kaskaden sparen.

Überlegen wir uns mal, wie wir das umsetzen können...

```pycon
>>> choice = int(input("Ihre Wahl: "))
Ihre Wahl: 3
>>> menufuncs[choice-1]()
Eintrag wird gelöscht
```
Eigentlich exakt so, wie angedacht. Wir müssen nur die passende Funktion
heraussuchen und mittels `()` aufrufen. Fertig. Heißa! Nie wieder stupide
`if...elif`-Konstrukte :-)

Fügen wir doch mal alles in einer Funktion zusammen:

```python 
menutexts = [
    "Eintrag hinzufügen",
    "Eintrag suchen",
    "Eintrag löschen",
    "Beenden"
]

menufuncs = [
    add_entry,
    search_entry,
    remove_entry,
    quit
]

def handle_menu(texts, funcs):
    while True:
        for index, text in enumerate(texts, 1):
            print("{}  {}".format(index, text))
        choice = int(input("Ihre Wahl? ")) - 1
        funcs[choice]()
```
Sieht doch recht handlich aus. Wir ziehen die `1` hier einfach direkt von der
Nutzereingabe ab, das sieht dann beim Indexzugriff übersichtlicher aus und
wir brauchen die "verfälschte" Eingabe ja auch nicht weiter.
Testen wir das einmal:

```pycon
>>> handle_menu(menutexts, menufuncs)
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Beenden
Ihre Wahl? 1
Eintrag wird hinzugefügt
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Beenden
Ihre Wahl? 3
Eintrag wird gelöscht
```
Prima :-) Es klappt genauso, wie wir uns das mühsam zusammengereimt haben.

Aber halt... was passiert denn nun, wenn wir wieder Funktionen hinzufügen
wollen? Hält unserer Konzept dieser Anforderung stand?

```python 
def load(): print("Datensatz wird geladen")

def save(): print("Datensatz wird gespeichert")

menutexts = [
    "Eintrag hinzufügen",
    "Eintrag löschen",
    "Eintrag suchen",
    "Telefonbuch speichern",
    "Telefonbuch laden",
    "Beenden"
]

menufuncs = [
    add_entry,
    search_entry,
    remove_entry,
    save,
    load,
    quit
]
```
Nicht wirklich etwas neues... also testen wir es mal:

```pycon
>>> handle_menu(menutexts, menufuncs)
1  Eintrag hinzufügen
2  Eintrag löschen
3  Eintrag suchen
4  Telefonbuch speichern
5  Telefonbuch laden
6  Beenden
Ihre Wahl? 3
Eintrag wird gelöscht
```
Oha. Verdammt! Wir haben bei den Texten die Optionen zwei und drei getauscht,
aber vergessen dieses auch bei den Funktionen umzusetzen. Ein Glück kann bei
unseren Demo-Funktionen nicht viel passieren!

So ganz optimal ist unsere Struktur nicht. Vielleicht bist Du ja schon zu 
Beginn darauf gekommen, wie man es besser machen kann?

Wir wollten ja unsere Daten **zusammenfassen**. Wir haben bisher zwar die
Menüdaten *strukturiert*, aber eben noch nicht stark *gekoppelt*. Beide
"Datentypen" sind noch in zwei separaten Strukturen abgelegt. Die Verbindung
entsteht eigentlich nur implizit über denselben Index. Das zweite Item der
Menüeinträge passt also zum zweiten Eintrag in der Funkionsliste. Bei längeren
Listen kann man sich da schnell mal "verzählen" und es kommt zu obigen Fehlern.

Wieso koppeln wir nicht "Text" und "Funktion" direkt zusammen? Wir könnten
doch einfach eine Liste von Paaren bilden...

```python 
menu = [
    ["Eintrag hinzufügen", add_entry],
    ["Eintrag suchen", search_entry],
    ["Eintrag löschen", remove_entry],
    ["Beenden", quit]
]
```
Für den Zugriff können wir nach wie vor über den Index gehen, erhalten 
darunter aber wiederum eine Liste, die aus zwei Elementen besteht. Index `0`
beheimatet den Menütext, Index `1` die aufzurufende Funktion:

```pycon
>>> menu[1]
['Eintrag suchen', <function search_entry at 0x7ff6e74b40d8>]
>>> menu[1][0]
'Eintrag suchen'
>>> menu[1][1]()
Eintrag wird gesucht
```
Wunderbar einfach :-)

Schauen wir uns mal die nötigen Änderungen in `handle_menu` an:

```python 
def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(input("Ihre Wahl? ")) - 1
        menu[choice][1]()
```
Anstelle von zwei Listen übergeben wir unsere Menüdefinition nun als einen
einzelnen Parameter. Zur Ausgabe benennen wir `text` in `item` um, da das
Listenelement tatsächlich ja das Paar aus Text und Funktion beinhaltet. Ergo
greifen wir in der `format`-Methode auf den `0` Index zu, in dem der Text 
steht. Beim Aufruf der Funktion in der letzten Zeile ergänzen wir den zweiten 
Indexzugriff auf den `1` Index.

That's it :-)

Zeit zu testen:

```pycon
>>> handle_menu(menu)
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Beenden
Ihre Wahl? 2
Eintrag wird gesucht
1  Eintrag hinzufügen
2  Eintrag suchen
3  Eintrag löschen
4  Beenden
Ihre Wahl? 1
Eintrag wird hinzugefügt
```
Cool :-)

Und wenn wir nun wiederum Einträge hinzufügen oder tauschen wollen, so müssen
wir das nur an einer Stelle, nämlich unserer Menüdefinition. Beim Tauschen
können wir ganze Tupel ausschneiden und kopieren; somit ist es fast 
auszuschließen, dass wir Text und Funktion nicht zusammenpassend definieren.

Und auch das Suchen von Fehlern wird einfacher. Wir brauchen nicht an zwei 
separaten Stellen gucken, ob nun der Menütext falsch definiert war oder aber 
der Fehler an einem falschen Funktionseintrag lag. Vergleiche das auch einmal
mit der ursprünglichen, naiven Fassung!

```python 
menu = [
    ["Eintrag hinzufügen", add_entry],
    # Einträge getauscht
    ["Eintrag löschen", remove_entry],
    ["Eintrag suchen", search_entry],
    # neue Einträge
    ["Telefonbuch laden", load],
    ["Telefonbuch speichern", save],
    # den gab es schon ;-)
    ["Beenden", quit]
]
```
Wie man sieht, ist das ziemlich **übersichtlich** und **flexibel**! Genau das 
wollten wir ja erreichen. Der Code für die eigentliche Menüführung hat nun
genau sechs Zeilen (`handle_menu`). Die Daten sind nun davon getrennt.
Zudem sind sie schön kompakt zusammengefasst, so dass man leicht neue Einträge
hinzufügen kann, ohne an mehreren Stellen im Code Änderungen vornehmen zu
müssen.


Auf der Zielgeraden
-------------------

Bisher haben wir ausschließlich Listen für die Verwaltung unserer 
Menüdefinition verwendet. An dieser Stelle kann man noch optimieren. Da wir die
Paare aus Text und Funktion immer zusammmen erstellen und eigentlich nicht
mehr ändern wollen, können wir dafür auch den Datentyp `tuple` verwenden.
Dieser verhällt sich exakt so wie eine Liste, außer, dass man Tupel-Objekte
nach dem Anlegen nicht mehr ändern kann.

Den Indexzugriff mittels `obj[x]` bieten aber beide Strukturen (Verwechsle das 
nicht mit der `index`-Methode! Diese sucht den Index zu einem gegebenen Objekt
heraus, also z.B. an welcher Stelle ein bestimmter String oder ein Integerwert
in der Struktur steht)

Wir können unseren Code bei der Definition einer Menüstruktur einfach auf Tupel 
umstellen, ohne dass wir an unserer `handle_menu`-Funktion etwas ändern müssen.

Hier mal ein kleines Beispiel:

```pycon
>>> t = 1, 2, 3
>>> t.append(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
>>> t = ("Hallo", "Welt")
>>> for item in t:
...     print(item)
... 
Hallo
Welt
```
Man erkennt Tupel an den runden Klammern, die man aber auch bei einer flachen
Definition weglassen kann. Danach teste ich mal an, ob ich nicht
doch ein Element hinzufügen kann. Wie man sieht, geht das natürlich nicht; die
entsprechende Methode fehlt - wie wir ja auch schon oben gehört haben.
Damit ist sichergestellt, dass nachträglich nichts an den Definitionen 
geändert werden kann - egal, ob das nun unabsichtlich oder absichtlich 
passieren soll. Wenn Du Dir ein Szenario vorstellen kannst, bei dem Änderungen
erwünscht sind, dann kannst Du natürlich wieder auf Listen umsteigen.
Wie man sieht funktioniert das Iterieren und der Indexzugriff exakt so wie bei
Listen.

In meinen mitgelieferten Modulen wirst Du sehen, dass ich dort Tupel verwende.

So, zum Abschluss wollen wir noch etwas anders, sehr wichtiges besprechen.

Wenn wir ganz pedantisch sein wollen, dann fehlt noch jegliche 
Plausibilitätsprüfung der Benutzereingaben. In der ersten naiven Fassung
hatten wir noch diese hübsche Ausgabe, wenn der Benutzer einen Index außerhalb
des gültigen Bereichs wählt. Das können wir aber leicht einbauen, indem wir
prüfen, ob die Eingabe des Benutzers in den Schranken zwischen `0` 
einschließlich und der Anzahl an Menüitems liegt.

Du kennst das sicherlich aus der Mathematik. Dort schreibt man auch häufig
Sachen wie `x ≥ 0 ∧ x < 10` wenn `x` Werte aus der Menge `{0, 1, 2, ..., 9}`
annehmen darf. Das kommt z.B. bei der Formulierung eines Definitionsbereichs
oder eines Wertebereichs bei Kurvendiskussionen vor. Ich kann das ganze auch
noch in einen Ausdruck zusammenziehen, der dann so aussähe: `0 ≤ x < 10`.

In Python sieht das exakt genauso aus :-)

```pycon
>>> x = 4
>>> 0 <= x < 10
True
>>> x = 10
>>> 0 <= x < 10
False
```
Genau das ist unsere Bedingung, nur dass wir keine feste obere Schranke wie die
`10` haben, sondern hier die Anzahl der Menüeinträge benutzen müssen. Die 
bekommmen wir über die `len`-Funktion einfach heraus. Beachte, dass die `0`
ja immer fixiert ist durch unser Nummerierungsschema. Auch hier müssen wir 
darauf achten, dass wir `1` vom eingegebenen Menüindex abgezogen haben, um das 
bei `0` beginnende Indexschema von Pythons Datenstrukturen zu erfüllen. Also
muss unsere untere Schranke bei `0` beginnen und die obere ist die Anzahl der
Menüeinträge - `1`. Da wir die obere Schranke *exklusiv* definiert haben (also
nur `<`, nicht `<=`) passt das auch ohne eine zusätzliche Subtraktion.

Damit ergibt sich unsere neue `handle_menu`-Funktion wie folgt:
    
```python 
def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(input("Ihre Wahl? ")) - 1
        if 0 <= choice < len(menu):
            menu[choice][1]()
        else:
            print("Bitte nur Zahlen im Bereich 1 - {} eingeben".format(
                                                                    len(menu)))
```
Es fehlt auch noch die Überprüfung, ob der Benutzer einen Buchstaben oder sonst
ein Zeichen eingibt.

Diese Details sind im Modul 
[simplemenu.py](https://github.com/Lysander/snippets/blob/master/Python/python-misc/simplemenus/simplemenu.py) 
zu finden. Dort habe ich die Funktionen der Ausgabe und der Benutzereingabe 
auch noch in separate Funktionen ausgelagert. Insgesamt findet man dort genau 
das hier besprochene in einem Modul.

Zum Abschluss packe ich noch einmal alles zusammen, so dass wir einen hübschen 
Überblick über die Gesamtsituation haben. Vergleiche das einmal mit dem ersten 
Ansatz!

```python 
def add_entry(): 
    print("Eintrag wird hinzugefügt")

def search_entry(): 
    print("Eintrag wird gesucht")

def remove_entry(): 
    print("Eintrag wird gelöscht")

def quit(): 
    print("Beende das Programm")

def load(): 
    print("Datensatz wird geladen")

def save(): 
    print("Datensatz wird gespeichert")

def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(input("Ihre Wahl? ")) - 1
        if 0 <= choice < len(menu):
            menu[choice][1]()
        else:
            print("Bitte nur Zahlen im Bereich 1 - {} eingeben".format(
                                                                    len(menu)))

menu = [
    ["Eintrag hinzufügen", add_entry],
    ["Eintrag löschen", remove_entry],
    ["Eintrag suchen", search_entry],
    ["Telefonbuch laden", load],
    ["Telefonbuch speichern", save],
    ["Beenden", quit]
]

handle_menu(menu)
```
Stolz können wir uns zurücklehnen und unser Werk betrachten... oder die anderen
Module studieren. Schließlich fehlen ja noch Dinge wie Submenüs, 
Beschreibungen, uvm. Dies wird in den folgenden Modulen Schritt für Schritt
umgesetzt:

- `submenu.py`
- `metamenu.py`
- `classymenu.py`

In den ersten beiden handelt es sich nur um geringfügige Abweichungen
von dem hier vorgestellten Schema.

In `classymenu.py` führe ich eine Klasse ein, die sich um die Darstellung und 
Auswertung eines Menüs kümmert.

Ich hoffe dieses Tutorial ist hilfreich für Dich gewesen. Wenn es Dir gefallen 
hat, sag es weiter, wenn nicht, sag es **mir**!
