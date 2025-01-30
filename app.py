import io
from flask import Flask, logging, render_template, request, jsonify
import requests
import pdfkit
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Funzione per cercare su Scopus

def search_scopus(firstname, lastname, university):
    url = "https://api.elsevier.com/content/search/scopus"
    query = f"(AUTHLASTNAME({lastname}) AND AUTHFIRST({firstname})) OR (AUTHLASTNAME({lastname}) AND AUTHFIRST({firstname[0].upper()})) AND AFFIL({university}) AND PUBYEAR > 2000"
    params = {
        "query": query,
        "apikey": "8785fd1058bf05eb5984f24b22caedb6",
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        results = data.get("search-results", {}).get("entry", [])
        publications = []
        for result in results:

            # Ottieni ID dell'articolo
            dc_identifier = result.get("dc:identifier", "").replace("SCOPUS_ID:", "")
            authors = "Autori non disponibili"
            authors_list = []
            if dc_identifier:
                details_url = f"https://api.elsevier.com/content/abstract/scopus_id/{dc_identifier}"
                details_response = requests.get(details_url, headers={"X-ELS-APIKey": "8785fd1058bf05eb5984f24b22caedb6"})

                if details_response.status_code == 200: 
                    xml_data = details_response.text
                    print("XML ricevuto:", xml_data)
                    try:
                        root = ET.fromstring(xml_data)
                        root = remove_namespace(root)

                        # Cerca tutti i nodi <author> nel documento XML
                        for author in root.findall(".//author"):
                            indexed_name = author.find("indexed-name")
                            if indexed_name is not None:
                                authors_list.append(indexed_name.text)

                    except ET.ParseError as e:
                        logging.error(f"Errore nel parsing XML: {e}")


            authors = ", ".join(authors_list) if authors_list else "Autori non disponibili"
            title = result.get("dc:title", "Titolo non disponibile")
            journal = result.get("prism:publicationName", "Rivista non disponibile")
            volume = result.get("prism:volume", "N/D")
            issue = result.get("prism:issueIdentifier", "N/D")
            pages = result.get("prism:pageRange", "N/D")
            doi = result.get("prism:doi", "N/D")
            year = result.get("prism:coverDate", "").split("-")[0]

            # Formatta i dettagli della pubblicazione
            publication = {
                "title": title,
                "authors": authors,
                "journal": journal,
                "volume": volume,
                "issue": issue,
                "pages": pages,
                "doi": doi,
                "year": year,
            }
            publications.append(publication)

        return publications
    else:
        print(f"Errore API: {response.status_code} - {response.text}")
        return []


def remove_namespace(doc):
    for elem in doc.iter():  # Usa iter() invece di getiterator()
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]  # Rimuove il namespace
        for key in list(elem.attrib.keys()):  # Rimuove namespace dagli attributi
            if '}' in key:
                new_key = key.split('}', 1)[1]
                elem.attrib[new_key] = elem.attrib.pop(key)
    return doc

# Rotta principale per visualizzare il modulo
@app.route("/")
def index():
    return render_template("index.html")



# Rotta per elaborare la richiesta
@app.route("/search", methods=["POST"])
def search():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    university = request.form.get("university")

    results = search_scopus(firstname, lastname, university)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)