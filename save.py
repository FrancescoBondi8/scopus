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



                            <em>Cited by: ${article.cited_by}</em>,
                            <em>Journal Quartile Scopus: ${article.quartile_scopus}</em>.

Journal Quartile Scopus: ${articolo.quartile_scopus}














        // Assegna l'evento al pulsante
        document.getElementById("download-pdf").addEventListener("click", async () => {
            await generaPDF();
        });
        
        //funzioni utili alla generazione del pdf

        function normalizeText(text) {
            if (typeof text !== 'string') return text; // Verifica se 'text' è una stringa

            return text
            .replace(/ș/g, "s")  // Sostituisci "ș" con "s"
            .replace(/ț/g, "t")  // Sostituisci "ț" con "t"
            .replace(/−/g, "-")  // Sostituisci "−" con "-"
            .replace(/λ/g, "l")  // Sostituisci "λ" con "l"
            .replace(/ł/g, "l")  // Sostituisci "ł" con "l"
            .replace(/ź/g, "z")  // Sostituisci "ź" con "z"
            .replace(/ę/g, "e")  // Sostituisci "ę" con "e"
            .replace(/ć/g, "c")  // Sostituisci "ć" con "c"
            .replace(/ó/g, "o")  // Sostituisci "ó" con "o"
            .replace(/ń/g, "n")  // Sostituisci "ń" con "n"
            .replace(/ä/g, "a")  // Sostituisci "ä" con "a"
            .replace(/ö/g, "o")  // Sostituisci "ö" con "o"
            .replace(/ü/g, "u")  // Sostituisci "ü" con "u"
            .replace(/ß/g, "ss") // Sostituisci "ß" con "ss"
            .replace(/á/g, "a")  // Sostituisci "á" con "a"
            .replace(/é/g, "e")  // Sostituisci "é" con "e"
            .replace(/í/g, "i")  // Sostituisci "í" con "i"
            .replace(/ó/g, "o")  // Sostituisci "ó" con "o"
            .replace(/ú/g, "u")  // Sostituisci "ú" con "u"
            .replace(/ñ/g, "n")  // Sostituisci "ñ" con "n"
            .replace(/č/g, "c")  // Sostituisci "č" con "c"
            .replace(/š/g, "s")  // Sostituisci "š" con "s"
            .replace(/ž/g, "z")  // Sostituisci "ž" con "z"
            .replace(/ř/g, "r")  // Sostituisci "ř" con "r"
            .replace(/å/g, "a")  // Sostituisci "å" con "a"
            .replace(/ø/g, "o")  // Sostituisci "ø" con "o"
            .replace(/æ/g, "ae") // Sostituisci "æ" con "ae"
            .replace(/œ/g, "oe") // Sostituisci "œ" con "oe"
            .replace(/ð/g, "d")  // Sostituisci "ð" con "d"
            .replace(/þ/g, "th") // Sostituisci "þ" con "th"
            .replace(/ý/g, "y")  // Sostituisci "ý" con "y")
            .replace(/ü/g, "u")  // Sostituisci "ü" con "u"
            .replace(/ã/g, "a") // Sostituisci "ã" con "a"
        }

        // Funzione per parsare gli autori
        function parseAuthors(authors) {
            return authors.split(";").map((author) => {
                const [cognome, nome] = author.trim().split(",").map((a) => normalizeText(a.trim())); // Normalizza ogni parte
                return { nome, cognome };
            });
        }

        // Funzione per generare il PDF
        async function generaPDF() {
            
            // Autore da evidenziare
            const { PDFDocument, rgb, StandardFonts } = PDFLib;

            // Crea un nuovo documento PDF
            const pdfDoc = await PDFDocument.create();

            let page = pdfDoc.addPage();
            const { width, height } = page.getSize();

            const fontNormal = await pdfDoc.embedFont(StandardFonts.Helvetica);
            const fontBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

            let y = height - 50; // Posizione iniziale verticale
            const margin = 50;  // Margine sinistro
            const lineHeight = 12; // Spazio tra le linee

            function drawTextWrapped(text, x, y, font, size, maxWidth) {
                let currentLine = '';
                const words = text.split(' '); // Dividi il testo in parole

                for (let word of words) {
                    const testLine = currentLine ? `${currentLine} ${word}` : word;
                    const testWidth = font.widthOfTextAtSize(testLine, size);

                    if (testWidth > maxWidth) {
                        // Disegna la riga corrente e vai a capo
                        page.drawText(currentLine, { x, y, font, size, color: rgb(0, 0, 0) });
                        y -= lineHeight;
                        currentLine = word;
                    } else {
                        currentLine = testLine;
                    }
                }

                // Disegna l'ultima riga
                if (currentLine) {
                    page.drawText(currentLine, { x, y, font, size, color: rgb(0, 0, 0) });
                    y -= lineHeight;
                }

                return y; // Restituisce la nuova posizione 'y'
            
                // Disegna l'ultima riga
                if (currentLine) {
                    page.drawText(currentLine, {
                        x,
                        y,
                        font,
                        size,
                        color: rgb(0, 0, 0),
                    });
                    y -= lineHeight;
                }

                return y; // Restituisce la nuova posizione 'y' dopo aver disegnato il testo
            }

            // Funzione per aggiungere una nuova pagina
            function addNewPageIfNeeded() {
                if (y < 100) { // Se rimangono meno di 100px di spazio
                    page = pdfDoc.addPage();
                    y = height - 50; // Ripristina la posizione verticale
                }
            }

            // Scrive gli articoli nell'elenco
            const autoreInteressato = { nome: globalFirstName, cognome: globalLastName };
            // Funzione per scrivere gli autori con font differenziato
            function drawAuthorsWithNumber(index, authors, x, y, fontNormal, fontBold, size, maxWidth) {
                let currentX = x;

                // Disegna il numero della lista
                const listNumber = `${index + 1}. `;
                const numberWidth = fontNormal.widthOfTextAtSize(listNumber, size);

                if (currentX + numberWidth > maxWidth) {
                    currentX = x;
                    y -= lineHeight;
                }

                // Controlla se serve una nuova pagina
                if (y < 100) {
                    page = pdfDoc.addPage();
                    y = height - 50;
                }

                // Disegna il numero
                page.drawText(listNumber, {
                    x: currentX,
                    y,
                    font: fontNormal,
                    size,
                    color: rgb(0, 0, 0),
                });

                currentX += numberWidth; // Avanza la posizione corrente dopo il numero

                // Disegna gli autori uno alla volta
                authors.forEach(({ nome, cognome, isHighlighted }, index) => {
                    const font = isHighlighted ? fontBold : fontNormal;
                    const separator = index === authors.length - 1 ? '.' : ', ';
                    const authorText = `${nome} ${cognome}${separator}`;
                    const textWidth = font.widthOfTextAtSize(authorText, size);

                    if (currentX + textWidth > maxWidth) {
                        currentX = x;
                        y -= lineHeight;
                    }

                    if (y < 100) {
                        page = pdfDoc.addPage();
                        y = height - 50;
                    }

                    page.drawText(authorText, {
                        x: currentX,
                        y,
                        font,
                        size,
                        color: rgb(0, 0, 0),
                    });

                    currentX += textWidth;
                });

                y -= lineHeight; // Spazio extra dopo gli autori
                return y;
            }

            globalResults.articles.forEach((articolo, index) => {
                const parsedAuthors = parseAuthors(articolo.authors);

                // Aggiungi una nuova pagina se necessario
                addNewPageIfNeeded();

                // **1️⃣ Costruisci la stringa con autori e informazioni**
                let authorsText = `${index + 1}. `; // Numero dell'articolo

                parsedAuthors.forEach(({ nome, cognome }, i) => {
                    const isHighlighted = nome === autoreInteressato.nome && cognome === autoreInteressato.cognome;
                    const separator = (i === parsedAuthors.length - 1) ? ". " : ", ";

                    if (isHighlighted) {
                        // Usa il font grassetto per evidenziare l'autore interessato
                        authorsText += `**${cognome} ${nome}**${separator}`;
                    } else {
                        authorsText += `${cognome} ${nome}${separator}`;
                    }
                });

                // **2️⃣ Aggiungi le informazioni dell'articolo nella stessa riga**
                const articleInfo = `${normalizeText(articolo.title)}, ${normalizeText(articolo.journal)}, Vol. ${articolo.volume}, p. ${articolo.pages}, Year ${articolo.year}, Cited by: ${articolo.cited_by}, Journal Quartile Scopus: ${articolo.quartile_scopus}`;

                // **3️⃣ Unisci autori e informazioni in una stringa unica**
                const fullText = authorsText + articleInfo;

                // **4️⃣ Disegna il testo senza uscire dai margini**
                y = drawTextWrapped(fullText, margin, y, fontNormal, 10, width - 2 * margin);

                // Aggiungi uno spazio extra tra gli articoli
                y -= 10;
            });

        

            // Esporta il PDF
            const pdfBytes = await pdfDoc.save();

            // Avvia il download del PDF
            const blob = new Blob([pdfBytes], { type: "application/pdf" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "articoli.pdf";
            link.click();