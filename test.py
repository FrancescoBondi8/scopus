import io
import logging
import os
from flask import Flask, render_template, request, jsonify, send_file
import pybliometrics
from pybliometrics.scopus import AuthorSearch, ScopusSearch, AbstractRetrieval,AuthorRetrieval
from fpdf import FPDF
app = Flask(__name__)

pybliometrics.scopus.init()



def find_author_articles(first_name, last_name, affiliation = None):
    try:
        # Step 1: Cerca l'autore
        query_parts = [f"AUTHFIRST({first_name})", f"AUTHLASTNAME({last_name})"]
        if affiliation:
            query_parts.append(f"AFFIL({affiliation})")
        query = " AND ".join(query_parts)
        author_search = AuthorSearch(query)

        if not author_search.authors:
            return {"error": f"No author found for {first_name} {last_name} at {affiliation}."}

        # Identifica l'ID dell'autore
        author = author_search.authors[0]  # Prendiamo il primo autore trovato
        author_id = author.eid.split('-')[-1]

        # Step 2: Recupera gli articoli dell'autore
        document_query = f"AU-ID({author_id})"
        document_search = ScopusSearch(document_query)

        if not document_search.results:
            return {"error": f"No articles found for author {first_name} {last_name}."}

        # Estrai i dettagli degli articoli
        articles = []
        for result in document_search.results:
            articles.append({
                "title": result.title,
                "authors": result.author_names or "Autori non disponibili",
                "journal": result.publicationName,
                "volume": result.volume,
                "issue": result.issueIdentifier,
                "pages": result.pageRange,
                "doi": result.doi,
                "year": result.coverDate.split("-")[0],
                "cited_by": result.citedby_count
            })
        return {"articles": articles}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": f"An internal error occurred: {e}"}

def find_author_articles_by_id(author_id):
    try:
        author = AuthorRetrieval(author_id)
        first_name = author.given_name
        last_name = author.surname
        document_query = f"AU-ID({author_id})"
        document_search = ScopusSearch(document_query)
        if not document_search.results:
            return {
                "error": f"No articles found for author ID {author_id}.",
                "first_name": first_name,
                "last_name": last_name,
            }

        # Estrai i dettagli degli articoli
        articles = []
        for result in document_search.results:
            articles.append({
                "title": result.title,
                "authors": result.author_names or "Autori non disponibili",
                "journal": result.publicationName,
                "volume": result.volume,
                "issue": result.issueIdentifier,
                "pages": result.pageRange,
                "doi": result.doi,
                "year": result.coverDate.split("-")[0],
                "cited_by": result.citedby_count
            })
        # Restituisci nome, cognome e articoli
        return {
            "first_name": first_name,
            "last_name": last_name,
            "articles": articles
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": f"An internal error occurred: {e}"}


# Funzione PDF per la creazione del documento
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(200, 10, 'Risultati della Ricerca', ln=True, align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

# Rotta principale per visualizzare il modulo
@app.route("/")
def index():
    return render_template("index.html")

# Rotta per elaborare la richiesta
@app.route("/search", methods=["POST"])
def search():
    form_type = request.form.get("form_type")

    if form_type == "name_search":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        university = request.form.get("university")
        results = find_author_articles(firstname, lastname, university)
        #prompt = (f"Scrivi un CV dettagliato del Prof. {firstname} {lastname}, affiliato all'università {university}. ")
    
        # Ottieni la risposta da GPT
        #print(prompt)
        #risposta = chat_with_gpt(prompt)
        #print(risposta)
        # Aggiungi la risposta al risultato JSON
        #results["chatgpt_response"] = risposta
        return jsonify(results)
    
    elif form_type == "id_search":
        author_id = request.form.get("id")
        results = find_author_articles_by_id(author_id)
        return jsonify(results)
    
    else:
        return jsonify({"error": "Invalid form type"}), 400
    

from fpdf import FPDF
import io
from flask import send_file

from fpdf import FPDF
import io
from flask import send_file, jsonify, request
import os
import tempfile

from fpdf import FPDF
import io
from flask import send_file, jsonify, request
import os
import tempfile

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        results = data.get('results')

        if not firstname or not lastname or not results:
            return jsonify({'error': 'Dati incompleti'}), 400

        # Creazione del PDF
        pdf = FPDF()
        pdf.add_page()

        # Aggiungi un font Unicode per gestire i caratteri speciali
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf', uni=True)  # Font grassetto

        # Aggiungi il titolo
        pdf.cell(200, 10, txt=f"Articoli per {firstname} {lastname}", ln=True, align="C")

        # Itera sugli articoli
        for article in results.get('articles', []):
            authors = article.get('authors', '')
            title = article.get('title', '')
            journal = article.get('journal', '')
            volume = article.get('volume', '')
            issue = article.get('issue', '')
            pages = article.get('pages', '')
            year = article.get('year', '')
            cited_by = article.get('cited_by', '')
            
            # Aggiungi il contenuto per gli autori, evidenziando l'autore ricercato
            highlighted_authors = ''
            for author in authors.split(';'):
                author = author.strip()
                author_firstname, author_lastname = author.split(",")[1].strip(), author.split(",")[0].strip()

                if f"{firstname} {lastname}".lower() == f"{author_firstname} {author_lastname}".lower():
                    # Cambia il font a grassetto per l'autore interessato
                    pdf.set_font('DejaVu', 'B', 12)
                    highlighted_authors += f"{author_lastname} {author_firstname}, "
                    pdf.set_font('DejaVu', '', 12)
                else:
                    highlighted_authors += f"{author_lastname} {author_firstname}, "

            # Rimuovi l'ultima virgola
            highlighted_authors = highlighted_authors.rstrip(', ')

            # Aggiungi il contenuto dell'articolo al PDF
            pdf.multi_cell(0, 10, txt=f"{highlighted_authors}. {title}, {journal}, Vol. {volume}, Issue {issue}, p. {pages}, Year {year}, Cited by: {cited_by}")

        # Salva il PDF in un file temporaneo
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf_path = temp_pdf.name
            pdf.output(temp_pdf_path)

        # Leggi il contenuto del file temporaneo in memoria
        with open(temp_pdf_path, 'rb') as f:
            pdf_output = io.BytesIO(f.read())

        # Elimina il file temporaneo
        os.remove(temp_pdf_path)

        # Restituisci il PDF come file
        return send_file(pdf_output, as_attachment=True, download_name="risultati_articoli.pdf", mimetype="application/pdf")

    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({'error': 'Errore durante la generazione del PDF'}), 500





if __name__ == "__main__":
    app.run(debug=True)
