# SEO Site Auditor

Un tool sviluppato in Python che esegue un audit SEO automatico di un sito web, analizzando le pagine interne, calcolando uno score SEO e generando un report PDF arricchito da un commento generato tramite OpenAI.

## Features

* Crawling automatico delle pagine interne di un dominio
* Analisi SEO base:

    * Title tag
    * Meta Description
    * H1
    * Immagini senza attributo ALT
* Calcolo di uno score SEO per ogni pagina
* Calcolo dello score medio del sito
* Generazione di un commento SEO tramite LLM
* Esportazione di un report PDF professionale

---

## Installazione

Configurare la chiave OpenAI:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Utilizzo

Analisi tecnica del sito:

```bash
python src/main.py https://example.com
```

Analisi con commento LLM:

```bash
python src/main.py https://example.com --llm
```

Analisi con generazione PDF:

```bash
python src/main.py https://example.com --pdf
```

Limitare il numero di pagine analizzate:

```bash
python src/main.py https://example.com --max-pages 20 --pdf
```