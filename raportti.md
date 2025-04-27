# Asuntojen hintakehityksen visualisointi Plotlylla

## Esittely

Tämän seminaarityön tavoitteena oli visualisoida asuntojen hintakehitystä Helsingin eri postinumeroalueilla vuosina 2000–2016.
Toteutin projektin Pythonin avulla hyödyntäen Plotly- ja Flask-kirjastoja sekä avointa dataa asuntojen hinnoista ja postinumeroalueiden rajoista.

## Työn tausta ja tavoitteet

Asuntojen hintakehitys on tärkeä ja ajankohtainen aihe kaupunkisuunnittelun, talouden ja yksityishenkilöiden päätöksenteon kannalta.
Visualisoimalla hintatiedot kartalle käyttäjän on helppo havaita alueellisia eroja ja kehityssuuntia.
Tavoitteenani oli tehdä dynaaminen ja vuorovaikutteinen web-sovellus, jossa käyttäjä voi liukusäätimellä tarkastella hintakehitystä eri vuosina.

## Aineistot

1. Sisense.com, [Plotly Choropleth With Slider (Map Charts Over Time)](https://community.sisense.com/t5/cdt/plotly-choropleth-with-slider-map-charts-over-time/ta-p/9387)
2. Mikael Ahonen, [Finland postal code data including boundary coordinates](https://mikaelahonen.com/en/data/finland-postal-codes-data/) ja [Visualize postal code areas of Finland in Python](https://mikaelahonen.com/en/data/postal-codes-map-python/)
3. Avoindata.fi, [Helsingin vanhojen asunto-osakehuoneistojen neliöhinnat postinumeroalueittain](https://www.avoindata.fi/data/fi/dataset/helsingin-vanhojen-asunto-osakehuoneistojen-neliohinnat-postinumeroalueittain-vuodesta-2000)

## Teknologiat

- Python
- Flask - helppo tapa luoda web-sovellus Pythonilla
- Plotly - mahdollistaa interaktiivisen karttavisualisoinnin
- Pandas - excel-tiedoston lukemiseen ja datan muokkaamiseen

## Työvaiheet

Ensin tein Asuntojen_hinnat_postinumeroalueittain-excelistä kopion ja poistin siitä tiedot, joita en tarvitse (ks. kuvat):

<img width="640" alt="image" src="https://github.com/user-attachments/assets/715271d4-42e6-4708-bf57-e32cb57abc5e" />

<img width="640" alt="image" src="https://github.com/user-attachments/assets/048bca4b-7046-4288-afe1-d83ba18b1345" />

Sen jälkeen hain excelin tiedot. Postinumeroita ei aluksi meinannut löytyä geojson-tiedostosta, kunnes tajusin syyn olevan se, että excelissä ne ovat kokonaislukuja ja geojsonissa merkkijonoja. Siispä muutin excelin postinumero-sarakkeen merkkijonoksi:

```df_long = pd.read_excel('Asuntojen_hinnat_postinumeroalueittain kopio.xlsx', dtype={'Postinumero': str})```

Tuonnin yhteydessä postinumeroiden alussa olevat nollat tippuivat myös pois, joten jouduin käyttämään zfill-metodia, jotta sain ne takaisin:

```df_long['Postinumero'] = df_long['Postinumero'].str.zfill(5)```

Avasin geojson-tiedoston:

```with open("finland-postal-codes.geojson", encoding='utf-8') as f: geojson = json.load(f)```

Sovellukseni oli alkuun todella hidas ja ymmärsin myöhemmin sen johtuvan siitä, että käsittelin siinä kaikki geojson-tiedostossa olevat postinumerot eli kaikki Suomen postinumerot. Siispä etsin excelistä uniikit Helsingin postinumerot ja suodatin niitä vastaavat arvot geojson-tiedostosta:

```excel_postinumerot = df_long['Postinumero'].unique()```
```geojson_filtered = {"type": "FeatureCollection", "features": [f for f in geojson['features'] if str(f['properties']['postinumeroalue']).zfill(5) in excel_postinumerot]}```
```df_long_filtered = df_long[df_long['Postinumero'].isin(excel_postinumerot)]```

Excelin rakenteesta johtuen vuosi- ja hinta-sarakkeita ei ollut. Jouduin luomaan ne Pandasin melt-funktiolla:

```df_long_melted = pd.melt(df_long_filtered, id_vars=["Postinumero", "Toimipaikka"], var_name="Vuosi", value_name="Hinta")```
```df_long_melted['Vuosi'] = df_long_melted['Vuosi'].astype(int)```
```df_long_melted['Hinta'] = pd.to_numeric(df_long_melted['Hinta'], errors='coerce')```

Sitten loin choroplethilla kartan ja lisäsin sen index.html-tiedostoon:

<img width="640" alt="image" src="https://github.com/user-attachments/assets/203edc25-33bb-4910-83fe-7dbd01a01e3a" />

<img width="640" alt="image" src="https://github.com/user-attachments/assets/5793b25f-6d5a-4edd-89da-66c0a26a19ea" />

Kuva valmiista sovelluksesta:

<img width="640" alt="image" src="https://github.com/user-attachments/assets/69b01c2c-242b-4616-a025-79e6538a9979" />

## [Linkki projektikansioon](https://github.com/joonas-hh-dev/Seminaari/tree/main/seminaari)

## [Demovideo](https://haagahelia-my.sharepoint.com/personal/bgz332_myy_haaga-helia_fi/_layouts/15/stream.aspx?id=%2Fpersonal%2Fbgz332%5Fmyy%5Fhaaga%2Dhelia%5Ffi%2FDocuments%2FRecording%2D20250426%5F171134%2Ewebm&nav=%7B%22defaultNavPanel%22%3A%7B%22pluginName%22%3A%22MediaSettingsLayer%22%7D%7D&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E9488cfbe%2De26f%2D4343%2D9b39%2D1d55cf3481d7)
