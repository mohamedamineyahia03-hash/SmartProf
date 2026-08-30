from data.skills_matrix import SKILLS_MATRIX


def calculate_mastery(correct, total):
    try:
        correct = max(0, int(correct))
        total = max(0, int(total))
    except (TypeError, ValueError):
        return 0

    if total == 0:
        return 0

    correct = min(correct, total)
    return round((correct / total) * 100)


def mastery_level(score):
    if score < 30:
        return "Découverte"
    if score < 50:
        return "Fragile"
    if score < 70:
        return "En cours"
    if score < 90:
        return "Maîtrisée"
    return "Excellente"


def diagnose(level, subject, results=None):
    skills = SKILLS_MATRIX.get(str(level), {}).get(subject, {})
    results = results if isinstance(results, dict) else {}
    diagnosis = []

    for trimester, domains in skills.items():
        for domain in domains:
            result = results.get(domain, {})
            if not isinstance(result, dict):
                result = {}

            correct = result.get("correct", 0)
            total = result.get("total", 0)
            score = calculate_mastery(correct, total)

            diagnosis.append({
                "trimester": trimester,
                "skill": domain,
                "score": score,
                "level": mastery_level(score),
            })

    return diagnosis
