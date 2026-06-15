def calculate_score(data) -> array:
    score = 100
    issues = []

    if not data["title"]:
        score -= 20
        issues.append("Titolo mancante")
    elif not 30 <= data["title_length"] <= 60:
        score -= 10
        issues.append("Lunghezza del title non ottimale")

    if not data["meta_description"]:
        score -= 20
        issues.append("Meta description mancante")

    if data["h1_count"] != 1:
        score -= 15
        issues.append("La pagina dovrebbe avere un solo H1 principale")

    if data["images_count"] > 0:
        missing_ratio = data["images_missing_alt"] / data["images_count"]
        if missing_ratio > 0.3:
            score -= 15
            issues.append("Molte immagini non hanno attributo alt")

    return {
        "score": max(score, 0),
        "issues": issues,
    }