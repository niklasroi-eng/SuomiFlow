# SuomiFlow POC — Ryhti + Hilma

Tämä on **tekninen POC**, ei vielä valmis satojen hankkeiden tietokanta. Yhtään tekaistua hanketta tai yhteyshenkilöä ei ole mukana.

## Käyttöönotto

1. Asenna Python 3 sekä `pip install requests shapely pyproj`.
2. Suorita `python ryhti_import.py --max-pages 30 --output suomiflow_rakennushankkeet.json`.
3. Tarkista tulostettu määrä ja pistemäiset sijainnit. Älä julkaise ennen kuin kentät ja sijainnit on tarkistettu muutamasta alkuperäisestä tietueesta.
4. Nimeä `SuomiFlow_POC_Ryhti_Hilma_index.html` -> `index.html` ja lisää `suomiflow_rakennushankkeet.json` GitHub-repon juureen. Säilytä kaikki olemassa olevat KVL- ja väestöaineistot.

## Ryhti

- Virallinen avoin OGC API: https://paikkatiedot.ymparisto.fi/geoserver/ryhti_permit/ogc/features/v1
- `open_permit_building` sisältää lupavaiheen rakennustietoja. Ne eivät sellaisenaan ole rakennusurakoita tai myyntiliidejä.
- Tiedot eivät ole vielä kattavia kaikissa kunnissa. Pysyvässä sovelluksessa Syke edellyttää yksilöivää sovellustunnistetta.
- POC hakee enintään 30 sivua, joten aineisto voi olla osittainen.

## Hilma

Hilma AVP-Read on maksuton mutta vaatii API-avaimen; rajapinta ei tue selaimen CORS-pyyntöjä. **Älä laita avainta HTML:ään tai GitHub-repoon.** POC:ssa Hilma ei vielä tuota karttapisteitä. Seuraava integraatio on palvelinpuolen haku ja ilmoitusten yhdistely Ryhti-kohteisiin luotettavilla tunnisteilla / tarkistetuilla sijainneilla.

- Virallinen portaali: https://hns-hilma-prod-apim.developer.azure-api.net/
- Hakupalvelu: https://www.hankintailmoitukset.fi/

## Lähetys Kiinnikepajalle

Kerro rehellisesti, että kartta on prototyyppi: Ryhdin rakennustiedot on erotettu varsinaisista myyntiliideistä; Hilma on seuraava integrointilähde, ei jo yhdistetty tietokanta. Yhteyshenkilöt ja kiinniketarve selvitetään myöhemmin käsin.
