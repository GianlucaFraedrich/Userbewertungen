# __Dokumentation des Projektes für das Userbewertungsprojekt__

- [__Dokumentation des Projektes für das Userbewertungsprojekt__](#dokumentation-des-projektes-für-das-userbewertungsprojekt)
  - [__Projektbeschreibung__](#projektbeschreibung)
  - [__Datenbankentwurf__](#datenbankentwurf)
  - [__Übersicht Tabellen__](#übersicht-tabellen)
  - [__Überprüfung Normalform__](#überprüfung-normalform)
  - [__Überlegungen zur Datenintegrität__](#überlegungen-zur-datenintegrität)
  - [__SQL Befehle__](#sql-befehle)
  - [__Extra Features__](#extra-features)
  

---

## __Projektbeschreibung__

---

Ansprechpartner: Jan, Gianluca, Marius

Zeitraum: 24.11.2021 - 19.01.2022

Das von uns gestartete Projekt zielt darauf ab, eine Website zu verfügung zu stellen auf welcher es dem Nutzer möglich ist sowohl alte als auch neue Filmen zu bewerten. 
Die Nutzerdaten und Filminformationen werden in einer Datenbank.
Dies richtet sich nicht nur an junge Leute sondern auch an ältere, welche sich wieder jung fühlen können, wenn sie die Filme aus ihrer Jugend wiederfinden und sich diesen dann gegebenenfalls ausleihen und nochmal anschauen.
Die Gui soll simpel und leicht zu bedienen sein, so das es möglich ist ohne viel Kopfschmerzen sich auf der Seite zurechtzufinden.

---

## __Datenbankentwurf__

---

Im nachfolgendem Bild ist das Entiy-Relationship-Diagramm zusehen, welches uns als Entwurf der Datenbank diente. 

![Entity-Relationship-Diagramm](ERM.png)

---

## __Übersicht Tabellen__

----

_Relationsschreibweise_:

1. User(__Bewertung__, Name, PW-Hash)

2. Bewertung(__ID__, ↑User-ID, ↑Content-Id, Rating)

3. Content(__ID__, Name)

4. Genres(↑Genre-ID, ↑Content-ID)

5. Genre(__ID__, Name)


--- 

## __Überprüfung Normalform__

--- 

![Tabelle: User](Url.png)

- Die Tabelle ist in der dritten Normalform
  - zweite Normalform erfüllt
  - beinhaltet keine abhänigkeit zwischen   Nichtschlüsselattributen

    --- 

![Tabelle: Bewertung](Url.png)

- Die Tabelle ist in der dritten Normalform
  - zweite Normalform erfüllt
  - beinhaltet keine abhänigkeit zwischen Nichtschlüsselattributen
  
    --- 

![Tabelle: Content](Url.png)

- Die Tabelle ist in der dritten Normalform
  - zweite Normalform erfüllt
  - beinhaltet keine abhänigkeit zwischen Nichtschlüsselattributen
    
    --- 

![Tabelle: Genres](Url.png)

- Die Tabelle ist in der dritten Normalform
- zweite Normalform erfüllt
  - beinhaltet keine abhänigkeit zwischen Nichtschlüsselattributen

 --- 

![Tabelle: Genre](Url.png)

- Die Tabelle ist in der dritten Normalform
- zweite Normalform erfüllt
  - beinhaltet keine abhänigkeit zwischen Nichtschlüsselattributen

 --- 

## __Überlegungen zur Datenintegrität__

---

- ja

---

## __SQL Befehle__

---

Es folgen nun die SQL-Befehle, welche wir für die Manipulation und zum Anzeigen einzelner Datensätze benutzt habe.

```
Manipulation:

    SELECT ort.name AS Stadt, ort.Breite, land.Name AS Land
    FROM ort,land
    WHERE ort.LNR = land.LNR AND ort.Breite > 65 
    ORDER BY ort.Breite DESC

    SELECT ort.name AS Stadt, ort.Breite, land.Name AS Land
    FROM ort,land
    WHERE ort.LNR = land.LNR AND ort.Breite > 65 
    ORDER BY ort.Breite DESC

Anzeige:

    SELECT ort.name AS Stadt, ort.Breite, land.Name AS Land
    FROM ort,land
    WHERE ort.LNR = land.LNR AND ort.Breite > 65 
    ORDER BY ort.Breite DESC

    SELECT ort.name AS Stadt, ort.Breite, land.Name AS Land
    FROM ort,land
    WHERE ort.LNR = land.LNR AND ort.Breite > 65 
    ORDER BY ort.Breite DESC

```

Des Weiteren die SQL Befehle zum erstellen der Tabellen

```

  CREATE TABLE IF NOT EXISTS ratings (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  rating INT,
  userID INT,
  contentID INT
  );

  CREATE TABLE IF NOT EXISTS genre (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  genre VARCHAR(255)
  );

```

---

## __Extra Features__

--- 

Login:

    

