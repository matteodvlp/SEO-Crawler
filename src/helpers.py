import re
from datetime import datetime
from urllib.parse import urlparse


def build_pdf_filename(url):
    domain = urlparse(url).netloc.replace("www.", "")

    safe_domain = re.sub(
        r"[^a-zA-Z0-9.-]",
        "_",
        domain
    )

    date = datetime.now().strftime("%Y-%m-%d")

    return f"reports/{safe_domain}_seo_report_{date}.pdf"