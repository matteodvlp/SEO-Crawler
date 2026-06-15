import argparse

from crawler import crawl_site
from analyzer import analyze_seo
from scoring import calculate_score
from llm_report import generate_llm_site_report
from pdf_report import generate_site_pdf_report
from helpers import build_pdf_filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--llm", action="store_true")
    parser.add_argument("--pdf", action="store_true")

    args = parser.parse_args()

    pages = crawl_site(args.url, max_pages=args.max_pages)

    site_results = []

    for page in pages:
        seo_data = analyze_seo(page["soup"])
        score_data = calculate_score(seo_data)

        site_results.append({
            "url": page["url"],
            "seo_data": seo_data,
            "score_data": score_data,
        })

    average_score = sum(
        result["score_data"]["score"]
        for result in site_results
    ) / len(site_results)

    average_score = round(average_score, 1)

    print(f"Pagine analizzate: {len(site_results)}")
    print(f"Score medio sito: {average_score}/100")

    for result in site_results:
        print()
        print(result["url"])
        print(result["score_data"])

    if args.llm or args.pdf:
        llm_report = generate_llm_site_report(
            args.url,
            site_results,
            average_score
        )

        print()
        print("COMMENTO LLM:")
        print(llm_report["summary"])

        if args.pdf:
            generate_site_pdf_report(
                args.url,
                site_results,
                average_score,
                llm_report,
                build_pdf_filename(args.url)
            )

            print()
            print("PDF generato: " + build_pdf_filename(args.url))


if __name__ == "__main__":
    main()