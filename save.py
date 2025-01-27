from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet

# Dati ricevuti dal backend
articoli = [
    {"nome": "Mario", "cognome": "Rossi", "anno": 2021, "cited_by": 15, "titolo": "Studio sulla biologia"},
    {"nome": "Giulia", "cognome": "Verdi", "anno": 2020, "cited_by": 10, "titolo": "Analisi dei dati"},
    {"nome": "Luca", "cognome": "Bianchi", "anno": 2019, "cited_by": 8, "titolo": "Ricerca sulla fisica"},
]

# Autore da evidenziare
autore_interessato = {"nome": "Giulia", "cognome": "Verdi"}

# Creazione del PDF
file_pdf = "articoli.pdf"
doc = SimpleDocTemplate(file_pdf, pagesize=letter)
styles = getSampleStyleSheet()

# Funzione per formattare gli articoli
def formatta_articolo(articolo, autore_interessato):
    nome = articolo["nome"]
    cognome = articolo["cognome"]
    titolo = articolo["titolo"]
    anno = articolo["anno"]
    cited_by = articolo["cited_by"]

    # Controlla se l'autore è quello da evidenziare
    if nome == autore_interessato["nome"] and cognome == autore_interessato["cognome"]:
        autore = f"<b>{nome} {cognome}</b>"
    else:
        autore = f"{nome} {cognome}"

    return f"{autore}, \"{titolo}\", {anno}, Cited by: {cited_by}"

# Creazione dell'elenco numerato
elenco = []
for i, articolo in enumerate(articoli, start=1):
    testo = formatta_articolo(articolo, autore_interessato)
    item = ListItem(Paragraph(f"{i}. {testo}", styles["Normal"]))
    elenco.append(item)

lista_numerata = ListFlowable(elenco, bulletType="1")

# Scrittura del contenuto nel PDF
elements = [lista_numerata]
doc.build(elements)

print(f"PDF generato: {file_pdf}")