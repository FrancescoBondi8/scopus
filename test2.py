import openai

# Configura la tua API Key
openai.api_key="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"

def ask_chatgpt(prompt, model="gpt-3.5-turbo"):
    try:
        # Chiamata all'API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Sei un assistente utile e gentile."},
                {"role": "user", "content": prompt}
            ]
        )
        # Restituisce la risposta generata
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"Errore durante la richiesta: {e}"

# Esempio di utilizzo
if __name__ == "__main__":
    domanda = "Qual è il significato della vita?"
    risposta = ask_chatgpt(domanda)
    print("Risposta di ChatGPT:", risposta)

        document.getElementById("download-pdf").addEventListener("click", () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const margin = 15; // Margine sinistro e destro
    const pageWidth = doc.internal.pageSize.width - margin; // Larghezza utilizzabile
    const lineHeight = 8; // Altezza di ogni riga
    const startYOffset = 20; // Offset verticale iniziale per nuove pagine
    let yOffset = startYOffset; // Offset verticale corrente

    const resultsList = document.getElementById("results");
    const items = resultsList.getElementsByTagName("li");

    // Nome e cognome dell'autore interessato
    const firstname = globalFirstName.trim().toLowerCase();
    const lastname = globalLastName.trim().toLowerCase();

    // Regex per individuare sia "Nome Cognome" che "Cognome Nome"
    const fullNameRegex = new RegExp(
        `(${firstname}\\s*\\n?\\s*${lastname}|${lastname}\\s*\\n?\\s*${firstname}|${lastname}\\s*\\n?\\s*${firstname[0]}\\.)`,
        "gi"
    );

    // Aggiungi il titolo al PDF
    doc.setFontSize(16);
    doc.text("Pubblicazioni trovate", margin, yOffset);
    yOffset += 15;

    doc.setFont("times", "normal");
    doc.setFontSize(12);

    for (let i = 0; i < items.length; i++) {
        let articleText = items[i].textContent; // Testo completo dell'articolo

        articleText = articleText.replace(/ș/g, 's') // Sostituisci caratteri speciali
            .replace(/−/g, '-') // Sostituisci caratteri speciali
            .replace(/λ/g, 'l') // Sostituisci caratteri speciali
            .replace(/\s*\n\s*/g, ' ') // Sostituisci ritorni a capo con spazi singoli
            .trim(); // Rimuove spazi iniziali e finali

        const lines = doc.splitTextToSize(articleText, pageWidth - margin * 2); // Divide il testo in righe gestibili

        console.log("Righe suddivise:", lines);
        // Numero dell'articolo
        const itemNumber = `${i + 1}.`;
        const itemNumberWidth = doc.getTextWidth(itemNumber);
        let xOffset = margin + itemNumberWidth;

        // Verifica se c'è spazio per tutte le righe
        if (yOffset + lineHeight * lines.length > doc.internal.pageSize.height - margin) {
            doc.addPage();
            yOffset = startYOffset; // Reset dell'offset verticale
        }

        // Stampa il numero dell'articolo
        doc.text(itemNumber, xOffset, yOffset);
        xOffset += itemNumberWidth + 2;

        // Aggiungi ogni linea di testo
        lines.forEach((line, index) => {
            let currentXOffset = xOffset;

            // Divide la riga in parti usando la regex
            const parts = line.split(fullNameRegex); // Divide la riga in parti: testo normale e corrispondenze
            // Verifica se la riga precedente finisce con il cognome e questa riga inizia con il nome

            // Stampa la parte
            parts.forEach((part) => {
                console.log(part);
                if (fullNameRegex.test(part)) {
                    // Se è il nome completo, applica il grassetto
                    doc.setFont("times", "bold");
                } else {
                    // Altrimenti, font normale
                    doc.setFont("times", "normal");
                }

                // Stampa la parte
                doc.text(part, currentXOffset, yOffset);
                currentXOffset += doc.getTextWidth(part + " ");
            });

            yOffset += lineHeight; // Incrementa l'offset verticale

            // Controlla se l'offset è oltre la pagina e aggiungi una nuova pagina se necessario
            if (yOffset > doc.internal.pageSize.height - margin) {
                doc.addPage();
                yOffset = startYOffset; // Reset dell'offset verticale
            }
        });

        // Spazio extra tra articoli
        yOffset += 2;
    }

    // Salva il PDF
    doc.save("risultati.pdf");
});
