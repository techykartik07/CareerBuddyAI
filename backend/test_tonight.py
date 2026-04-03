import pdfplumber, re, spacy

# Part 1: pdfplumber — extract text from any PDF
with pdfplumber.open("any_pdf.pdf") as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)
print("PDF text extracted:", len(text), "characters")

# Part 2: regex — extract contact info
email = re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', text)
phone = re.findall(r'[\+\(]?[0-9][0-9\s\-\(\)]{7,}[0-9]', text)
print("Email found:", email[:1])
print("Phone found:", phone[:1])

# Part 3: spaCy — extract named entities
nlp = spacy.load("en_core_web_sm")
doc = nlp(text[:1000])
orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
print("Organisations found:", orgs[:5])