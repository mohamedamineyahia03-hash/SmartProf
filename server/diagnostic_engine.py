from data.skills_matrix import SKILLS_MATRIX

def calculate_mastery(correct, total):
    if total == 0:
        return 0
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

def diagnose(level, subject, results):
    skills = SKILLS_MATRIX.get(str(level), {}).get(subject, {})
    diagnosis = []

    for trimester, domains in skills.items():
        for domain in domains:
            result = results.get(domain, {"correct": 0, "total": 0})
            score = calculate_mastery(result["correct"], result["total"])

            diagnosis.append({
                "trimester": trimester,
                "skill": domain,
                "score": score,
                "level": mastery_level(score)
            })

    return diagnosis