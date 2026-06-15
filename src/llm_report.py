import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_llm_site_report(start_url, site_results, average_score):
    prompt = f"""
            Sei un consulente SEO senior.

            Analizza questo audit SEO multi-pagina.

            URL iniziale:
            {start_url}

            Score medio sito:
            {average_score}/100

            Risultati tecnici per pagina:
            {json.dumps(site_results, indent=2, ensure_ascii=False)}

            Rispondi esclusivamente in JSON valido con questo schema:

            {{
              "summary": "Commento generale sul sito",
              "strengths": [
                "Punto di forza 1",
                "Punto di forza 2"
              ],
              "priorities": [
                "Priorità 1",
                "Priorità 2",
                "Priorità 3"
              ]
            }}

            Regole:
            - Non aggiungere testo fuori dal JSON.
            - Non fare domande.
            - Non scrivere frasi tipo "Se vuoi".
            - Le priorities devono essere esattamente 3.
            """

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )

    return json.loads(response.output_text)