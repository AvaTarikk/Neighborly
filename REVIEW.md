# REVIEW.md

### **Reviewer 1: Sean Park**

### 1. **Verbeterpunt: meer en duidelijkere comments**  
**Tegengekomen probleem:**  
Er werd opgemerkt dat niet alle functies van mij even goed zijn gedocumenteerd. Sommige functies hebben wel (onduidelijke) comments, maar de meeste missen uitleg over wat ze precies doen en waarom ze bestaan. Dit maakt de code moeilijk te begrijpen voor anderen (of mezelf later). Ook staan er een hoop comments bij die alleen voor de user zelf begrijpelijk zijn, maar niet voor derden en vaak wordt er ook gemixt met het nederlands en engels wat het onnodig lastiger maakt om te volgen

**Hoe zou je dit beter kunnen maken?**  
Ik kan bij elke functie een korte beschrijving toevoegen, wat parameters uitleggen, en aangeven wat de functie retourneert. Dit helpt om de code sneller te begrijpen zonder dat je alles stap voor stap hoeft door te lezen. Verder kan ik bestaande comments duidelijker maken en checken of het ook voor andere partijen makkelijk te volgen is.

**Afweging:**
Door betere en consistente comments toe te voegen wordt de code veel overzichtelijker, waardoor het niet alleen voor mij makkelijk volgbaar is maar ook voor andere mensen die mijn code gaan lezen en wellicht aanpassingen willen maken eraan. Echter kost het wel extra tijd en moeite om dit aan te passen.

**Voorbeeld:**  
```python
# Slecht:
def handle_send_message(message):
    # Doet iets met berichten
    pass  

# Verbeterd:
def handle_send_message(message):
    """
    Verwerkt een binnenkomend bericht en retourneert een aangepast antwoord.
    Parameters:
        message (str): Het binnenkomende bericht van de gebruiker.
    Returns:
        str: Het verwerkte antwoord dat naar de chat wordt gestuurd.
    """
    pass  
```  

### 2. **Verbeterpunt: styles.css kan veel korter en overzichterlijker**
**Tegengekomen probleem:**
De reviewers gaven aan dat mijn styles.css bestand bijna 900 regels lang is. Elke HTML-pagina heeft aparte CSS-classes gekregen, waardoor er veel herhaling is en het bestand niet meer overzichtelijk is. Dit maakt het lastig om te begrijpen en te onderhouden.

**Hoe zou je dit beter kunnen maken?**
Ik kan herbruikbare stijlen maken door gebruik te maken van algemene utility-classes. Daarnaast kan ik overwegen om het bestand op te splitsen per component of per sectie (bijvoorbeeld header.css, footer.css, etc.). Dit maakt het makkelijker om alleen die delen te wijzigen die nodig zijn.

**Afweging:**
Het samenvoegen van stijlen met utility-classes maakt het bestand korter en overzichtelijker, maar het kan leiden tot minder unieke pagina-stijlen en ook minder onoverzichtelijkheid welke class bij welke pagina behoort. Ik kan ook kijken naar CSS-frameworks zoals Bootstrap, die al veel standaard classes hebben zodat mijn CSS-bestand minder lang wordt, alleen wordt het dan wel eentonig en meer beperkt.

**Voorbeeld:**

```css
/* Slecht: unieke stijlen per pagina */
.home-title {
    font-size: 24px;
    color: blue;
}
.about-title {
    font-size: 24px;
    color: blue;
}

/* Verbeterd: herbruikbare utility-classes */
.title {
    font-size: 24px;
    color: blue;
}
```

### 3. **Verbeterpunt: Error-checks toevoegen**  
**Tegengekomen probleem:**  
Opgemerkt is dat als een fout optreedt, zoals een API die niet reageert of een databasequery die mislukt, de code gewoon blijft doorgaan alsof er niets is gebeurd, omdat er niet wordt gecheckt of die data is opgehaald. Dit kan leiden tot onvoorspelbare fouten en slechte gebruikerservaringen. Bijvoorbeeld bij het ophalen van een ip adress is het belangrijk dat het goed werkt zodat we later op basis van afstand tot andere taken het kunnen filteren en weergeven aan de user.

**Hoe zou je dit beter kunnen maken?**  
Ik moet meer foutafhandeling toevoegen, vooral in functies die werken met externe bronnen zoals de database of een API. Een goede foutmelding zorgt ervoor dat het systeem blijft draaien en dat de gebruiker feedback krijgt.

**Afweging:**
Meer error-checks maken de applicatie stabieler, maar voegen extra checks toe die de code iets langer maken.

**Voorbeeld:**  
```python
# Slecht:
def get_user_data(user_id):
    result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return result  

# Verbeterd:
def get_user_data(user_id):
    try:
        result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result
    except Exception as e:
        print(f"Databasefout: {e}")
        return None  
```  


### **Reviewer 2: Otharo Mitsuhashi**

### 4. **Verbeterpunt: Lange functies die meerdere verantwoordelijkheden hebben opsplitsen**  
**Tegengekomen probleem:**  
Sommige functies (zoals `handle_send_message` en `view_tasks`) doen te veel dingen tegelijk. Ze valideren gegevens, updaten de database, en versturen berichten. Dit maakt het lastig om specifieke onderdelen te begrijpen of fouten op te sporen. Deze functies bevatten hoge complexiity levels in vergelijking met andere functies, het opslitsen van de functie zal ervoor zorgen dat dit niveau omlaag gaat wat de efficiente van de functie verhoogt.

**Hoe zou je dit beter kunnen maken?**  
Ik kan de logica van zulke functies opsplitsen in kleinere hulpfuncties. Dat maakt de code niet alleen leesbaarder, maar ook herbruikbaarder. Verder zorgt dit er ook voor dat de complexity van de functie daalt en het efficienter werkt.

**Afweging:**
Door functies op te splitsen in kleinere delen wordt de code overzichtelijker en makkelijk aanpasbaar voor niet alleen mij maar ook voor andere mensen die iets aan mijn code willen weghalen of toevoegen, maar het vereist wel extra tijd, planning en ook het risico op de kans dat de code het niet meer gaat functioneren als eerst.

**Voorbeeld:**  
```python
# Slecht:
def handle_send_message(data):
    # Validate user
    # Update database
    # Send message
    pass  

# Verbeterd:
def handle_send_message(data):
    if not validate_user(data['user_id']):
        return False
    save_message_to_db(data)
    send_message_to_socket(data)
    return True  
```  

### 5. **Verbeterpunt: De structuur van models.py kan duidelijker**  
### 5. **Probleem: Elke tabel heeft te veel kolommen, wat het onoverzichtelijk maakt**  
**Tegengekomen probleem:**  
De `User`, `Task`, en `Message` tabellen in `models.py` bevatten veel kolommen, waardoor ze lang en moeilijk leesbaar zijn. Dit kan ervoor zorgen dat de structuur van de databse onoverzichtelijk wordt en lastig te onderhouden is naarmate het project verder gaat. Elke tabel bevat heel veel keys die eenvoudig kunnen worden opgespiltst naar andere tabelle waardoor het een stuk overzichtelijker wordt. Je voorkomt hierdoor dat individuele tabellen onnodig groot worden. Bij uitbreidingen of aanpassingen kan ik efficiënter werken met kleinere tabellen. En relaties worden gewoon veel duidelijker.

**Hoe zou je dit beter kunnen maken?**  
Het zou beter zijn om sommige kolommen op te splitsen in aparte tabellen. Dit zorgt ervoor dat de tabellen compacter en overzichtelijker worden. Het maakt het makkelijker om wijzigingen aan te brengen en voorkomt dat tabellen onnodig groot worden.

**Afweging:**
Het opsplitsen van tabellen maakt de database gewoon veel overzichtelijker en een stuk logischer, maar het kan queries complexer maken door extra joins en tegelijkertijd ook onoverzichterlijker door het aantal tabbelen en verschillende relaties.

Bijvoorbeeld:  
1. **User-tabel**: Kolommen zoals `latitude` en `longitude` kunnen worden verplaatst naar een aparte `Location`-tabel.  
2. **Task-tabel**: Sommige velden zoals `photo` en `short_description` kunnen worden gescheiden in een tabel `TaskDetails`.  