from models import CurriculumDomain, CurriculumLevel, CurriculumSubject


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
    results = results if isinstance(results, dict) else {}
    diagnosis = []

    domains = (
        CurriculumDomain.query.join(CurriculumLevel)
        .join(CurriculumSubject)
        .filter(CurriculumLevel.code == str(level), CurriculumSubject.code == subject)
        .order_by(CurriculumDomain.sort_order)
        .all()
    )

    for domain in domains:
        trimesters = [t.trimester for t in domain.trimesters] or ["T1"]
        for trimester in trimesters:
            for skill in domain.skills:
                result = results.get(skill.code, {})
                if not isinstance(result, dict):
                    result = {}

                correct = result.get("correct", 0)
                total = result.get("total", 0)
                score = calculate_mastery(correct, total)

                diagnosis.append(
                    {
                        "trimester": trimester,
                        "skill": skill.code,
                        "score": score,
                        "level": mastery_level(score),
                    }
                )

    return diagnosis
