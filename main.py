import sys
import csv

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

"""
Kontrola vstupů
"""

def check_arguments():
    """
    Zkontroluuje argumenty příkazového řádku.
    Vrací URL a název výstupního CSV souboru.
    """
    if len(sys.argv) != 3:
        print("Chyba: Zadejte URL a název výstupního CSV souboru.")
        sys.exit(1)
    url = sys.argv[1]
    output_file = sys.argv[2]

    if not url.startswith(BASE_URL):
        print("Chyba: Neplatná URL.")
        sys.exit(1)
    if not output_file.endswith(".csv"):
        print("Chyba: Výstupní soubor musí být .csv")
        sys.exit(1)
    return url, output_file

"""
Načtení seznamu obcí
"""

def get_municipalities(url):
    """
    Načte seznam obcí a odkazy na jejich výsledky.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    municipalities = []

    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        code = cells[0].text.strip()
        name = cells[1].text.strip()
        link_tag = cells[0].find("a")
        if link_tag:
            link = BASE_URL + link_tag.get("href")
            municipalities.append({"kód obce": code, "název obce": name, "link": link})
    return municipalities

"""
Načtení výsledků pro obce
"""

def get_results_for_municipality(url):
    """
    Vytáhne počet voličů, vydané obálky, platné hlasy
    a hlasy jednotlivých stran pro jednu obec.
    Vrací: voliči, obálky, platné hlasy, slovník {strana: hlasy},
    pořadí stran
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    """ Základní info """
    for td in soup.find_all("td", class_="cislo"):
        headers = td.get("headers", "")
        value = td.get_text(strip=True).replace("\xa0", "").replace(" ", "")
        if not value.isdigit():
            continue
        value = int(value)
        if "sa2" in headers:
            voliči = value
        elif "sa3" in headers:
            obálky = value
        elif "sa6" in headers:
            platné = value

    """ Hlasy stran """
    results = {}
    party_order = []

    """ Tabulky obsahující strany """
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")[2:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            party = cells[1].get_text(strip=True)
            votes = cells[2].get_text(strip=True).replace("\xa0", "").replace(" ", "")
            if not votes.isdigit():
                continue
            votes = int(votes)
            results[party] = results.get(party, 0) + votes
            if party not in party_order:
                party_order.append(party)

    return voliči, obálky, platné, results, party_order

"""
Uložení do CSV
"""

def save_to_csv(filename, data, party_order):
    """
    Uloží výsledky do CSV souboru s hlavičkou:
    kód obce, název obce, voliči, obálky, platné hlasy, hlasy pro strany
    """
    headers = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + party_order
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

"""
Hlavní funkce
"""
def main():
    url, output_file = check_arguments()
    municipalities = get_municipalities(url)

    all_results = []
    final_party_order = []

    for municipality in municipalities:
        voliči, obálky, platné, results, party_order = get_results_for_municipality(municipality["link"])

        """ zachovat pořadí stran """
        for party in party_order:
            if party not in final_party_order:
                final_party_order.append(party)

        row = {
            "kód obce": municipality["kód obce"],
            "název obce": municipality["název obce"],
            "voliči v seznamu": voliči,
            "vydané obálky": obálky,
            "platné hlasy": platné
        }
        row.update(results)
        all_results.append(row)

    save_to_csv(output_file, all_results, final_party_order)
    print(f"Hotovo. Výsledky byly uloženy do {output_file}")

if __name__ == "__main__":
    main()
