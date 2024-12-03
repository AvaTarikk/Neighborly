# Projectvoorstel: Neighborly
Van: Tarik Ulgen


## Probleemomschrijving
In veel buurten en wijken is er een gebrek aan eenvoudige en toegankelijke manieren om hulp te vragen of aan te bieden. Mensen die kleine klusjes willen laten doen (zoals het verschuiven van een kast) of hulp nodig hebben (zoals boodschappen halen) weten vaak niet waar ze terechtkunnen. Dit probleem wordt versterkt doordat buren elkaar soms niet kennen, waardoor spontane hulp zeldzaam wordt. Tegelijkertijd willen er een hele boel mensen graag een bijdrage leveren, maar weten ze niet hoe ze iemand in hun omgeving kunnen vinden die hulp nodig heeft.


## Doelgroep
De primaire gebruikers zijn:
- **Oudere mensen** die niet in staat zijn om zelf bepaalde taken uit te voeren, zoals boodschappen doen of huishoudelijke klusjes.
- **(Jong) volwassenen** die tijd over hebben en graag iets willen bijdragen aan hun gemeenschap.
- **Gezinnen of individuen** die van tijd tot tijd hulp nodig hebben met iets.


## In welke setting?
De app zal voornamelijk worden gebruikt op smartphones zodat users snel hulp kunnen vragen of bieden.


## Unieke oplossing  
Deze app onderscheidt zich van de rest door volledig te focussen op hulp vragen en bieden, in tegenstelling tot sociale media apps zoals Facebook en Instagram, waar er ook hier en dan om hulp wordt gevraagd, maar niet de primaire focus is.  
- Het platform is lokaal georiënteerd en maakt directe matches op basis van locatie.  
- Het biedt een eenvoudige interface, zodat ook ouderen het makkelijk kunnen gebruiken.  
- Vrijwillige hulpverlening staat centraal, met een optionele bedank-tipfunctie.  



## Korte samenvatting oplossing
Deze applicatie zal:
1. Een platform bieden waar gebruikers om hulp kunnen vragen of aanbieden.
2. users op basis van hun locatie matchen met mensen in de buurt.
3. De mogelijkheid bieden om taken te categoriseren, zoals huishoudelijk werk, boodschappen, of eenvoudige reparaties.
4. Een chatfunctie bevatten, zodat gebruikers details over een taak kunnen bespreken.
5. Een optionele tip functie hebben waarmee gebruikers een fooi of bedankje kunnen sturen.

## Schets
1. **Startscherm**: Login/aanmelden
![Login scherm](schets/login.jpg)
![Homepagina](schets/homepage.jpg)

2. **Hulpopdracht aanmaken**: Formulier om een taak te beschrijven, locatie in te vullen en urgentie aan te geven.
![Taak overzicht](schets/taak.jpg)

3. **Takenoverzicht**: Een lijst van beschikbare taken in de buurt, gefilterd op afstand en categorie.
![Taak beschrijving](schets/taakdescr.jpg)

4. **Profielpagina**: Gebruikers kunnen een kort profiel zien van anderen (naam, foto, gemiddelde beoordelingen).
![Profiel scherm](schets/profiel.jpg)

5. **Chatfunctie**: Een eenvoudige interface om berichten uit te wisselen over de opdracht.
![Chat scherm](schets/chat.jpg)


## Benodigde Features
1. **Locatiegebaseerd matchen**: Helpt gebruikers om taken in de buurt te vinden.
2. **Taakcreatie en -overzicht**: Een formulier om taken te posten en een lijst om taken te bekijken.
3. **Chatfunctie**: Voor communicatie tussen de hulpvrager en -bieder.
4. **Authenticatie**: Login en registratie met profielinformatie en wellicht legitimeren.
5. **Notificaties**: Real-time meldingen bij nieuwe taken of berichten.

## Leuke Features
1. **fooi optie**: Gebruikers kunnen een vrijwillige bijdrage geven.
2. **Beoordelingen**: Gebruikers kunnen elkaar beoordelen na een afgeronde taak.
3. **Gamification**: Badges en statistieken voor helpers om betrokkenheid te vergroten.
4. **Meertaligheid**: Ondersteuning voor meerdere talen.


## Requirements
## Gegevensbronnen
1. **Geolocatie API**: Voor locatiegebaseerde matching (ik dacht aan Google Maps API, maar dat kost geld dus daan maar IPstack). 
    - link: https://developers.google.com/maps/documentation/geolocation/overview
    - link IpStack: https://ipstack.com/?utm_source=google&utm_medium=cpc&utm_campaign=ipstack_Search_EU&gad_source=1&gclid=CjwKCAiA0rW6BhAcEiwAQH28ItTxIXEDiEY-ISmMYsIbPCp3ehkyLq287FV6Fzdmm2uai6ZNp01mHxoCmOkQAvD_BwE
    - Toegang: Account aanmaken, tot 100 maandelijke requests gratis
2. **Database**: Opslag van gebruikersprofielen, taken en berichten (door PostgreSQL).

### Externe componenten
1. **Flask** natuurlijk
2. **SQLAlchemy** voor orm database om gegevens te beheren
3. **Bootstrap**: Voor responsieve en goed toegankelijke front-end.
4. **Socket.IO**: Voor eenvoudige real time chat
    -link: https://socket.io/docs/v4/tutorial/introduction


## Mogelijke moeilijkheden
1. **Locatiegebaseerde matching**: het goed berekenen van locaties en daarbij andere users matchen kan ingewikkeld zijn, denk ik.
   - **Uitweg**: Users hun eigen locatie laten invullen bij het registreren, en daarop gebruikers met elkaar matchen.
2. **Veiligheid en privacy**: Het beschermen van gebruikersinformatie en voorkomen van misbruik door zogenaamde "helpers".
   - **Uitweg**: Goede verificatie doormiddel van ID en beveiligingsmaatregelen nemen.
