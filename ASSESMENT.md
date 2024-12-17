# **ASSESSMENT.md**  

## **Belangrijke Punten**

### 1. **View_Tasks Functie en Filters**  
**view_tasks functie in `app.py` (regels 228 t/m 273) en templates/view_tasks.html**
Heb dit zo ontworpen om een overzicht van openstaande taken weer te geven, met de mogelijkheid om te filteren op verschillende criteria zoals categorie, urgentie, locatie en afstand. Aanvankelijk wilde ik gebruikers gewoon een lijst van alle taken tonen, maar ik realiseerde me al snel dat een filterfunctie de gebruikerservaring aanzienlijk zou verbeteren. Door de filters toe te voegen, kunnen gebruikers snel de taken vinden die het beste bij hun situatie passen. De combinatie van deze filters met een visueel aantrekkelijke layout in de bijbehorende `view_task.html` maakt het niet alleen functioneel, maar ook gebruiksvriendelijk en aesthathic wijs mooi ;)

### 2. **Afstandsberekening tussen Users* 
**De code in `app.py` van regel 205 t/m 225**
Een best belangrijke beslissing in het project was het gebruik van de Haversine formule voor de berekening van de distance tussen twee users op basis van hun IP-adressen. In eerste instantie dacht ik er eigenlijk aan om simpelweg gewoon mensen in dezelfde stad met elkaar te matchen maar dat zou te breed zijn en de gebruikerservaring verminderen. Door de Haversine-formule te implementeren, kon ik een veel nauwkeurigere berekening van de afstand tussen twee punten op de kaart maken. Dit maakte het mogelijk om gebruikers te matchen op basis van hun exacte locatie, door hun IP-adress te gebruiken. Deze oplossing verbetert de functionaliteit van de app aanzienlijk door een meer flexibele en geavanceerde manier van locatie bepalen te hanteren.


### 3. **Real-Time Chat (met socket.io)**
**code in templates/chat.html**
Ik heb gekozen voor real time communicatie mogelijk te maken tussen gebruikers, zo hoeven ze niet steeds van applicatie te switchen om met een andere partij te communiceren. In de eerste fase van het project onderzocht ik alternatieven zoals traditionele HTTP-requests, maar deze waren te traag voor directe communicatie tussen twee partijen. Socket.IO biedt een efficiënte manier om berichten direct tussen gebruikers te verzenden, wat essentieel is voor de chatfunctie. Door socket.io te implementeren kan de applicatie snel reageren op user zijn invoer en is de interactie veel vloeiender en gewoon efficienter.

### 4. **Homepage**
**code in templates/index.html en styles.css r. 677-821**
Heb hier best wat moeite in de front-end gestopt om de homepage van de site aesthatic pleasing te maken en dat alles heel duidelijk is voor de user. Dus waar je naar toe moet, hoe de site in elkaar zit en hoe alles werkt.