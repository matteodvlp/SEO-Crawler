def analyze_seo(soup) -> array:
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    h1_tags = soup.find_all("h1")
    images = soup.find_all("img")

    missing_alt = [
        img.get("src") for img in images
        if not img.get("alt")
    ]

    return {
        "title": title,
        "title_length": len(title),
        "meta_description": meta_desc.get("content", "") if meta_desc else "",
        "h1_count": len(h1_tags),
        "images_count": len(images),
        "images_missing_alt": len(missing_alt),
    }