Scraper výsledků voleb 2017

Tento projekt obsahuje skript main.py, který stáhne výsledky voleb do Poslanecké sněmovny 2017 pro všechny obce vybraného územního celku a uloží je do CSV souboru.

Požadavky:
Python 3.10+ a knihovny requests a beautifulsoup4. Tyto knihovny jsou uvedeny v souboru requirements.txt.

Instalace:
Vytvořte virtuální prostředí:
python3 -m venv venv
Aktivujte ho:
Windows: venv\Scripts\activate
Linux/macOS: source venv/bin/activate
Nainstalujte knihovny:
pip install -r requirements.txt

Použití:
Skript spouštíte s dvěma argumenty:
python main.py <URL_územního_celku> <výstupní_soubor.csv>
Například:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
První argument je odkaz na kraj nebo okres, druhý je jméno CSV souboru, kam se uloží výsledky.

Výstupní CSV:
Každý řádek obsahuje jednu obec a sloupce: kód obce, název obce, voliči v seznamu, vydané obálky, platné hlasy a hlasy pro jednotlivé kandidující strany. Pořadí stran odpovídá pořadí z webu.

Poznámky:
Program kontroluje správnost URL a jména souboru, pokud není vše správně, ukončí se s chybou.