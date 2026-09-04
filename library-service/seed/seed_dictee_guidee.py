# -*- coding: utf-8 -*-
"""Seeds the 16 exercises (4 rubrics x [fr,en] x [niveau1,niveau2]) for the
"Dictee guidee" domain -- see server/seed/seed_dictee_guidee.py for the
curriculum side and _local-work/.../memory/project_dictee_guidee_spec.md
for the full design history.

grading_mode="open" throughout (not scored -- a listening/writing practice
space, not a test), trimester="T1" is the same required-but-inert
placeholder used by every other "expression"-category domain (see
seed_expression_recitation.py's docstring).

Content design:
  - alphabet (skill "alphabet", format "lecon_lettres"): niveau 1 gets the
    original 26-letter set (one mot-repere per letter, the simpler first
    pass). Niveau 2 gets that same 26 PLUS 60 additional mots-reperes
    (2-3 syllables each, generated 2026-09-04) for review depth -- 86
    entries grouped by letter. English keeps just the original 26 (no
    expansion was requested for English).
  - syllabe (skill "syllabe", format "lecon_syllabes"): French uses the
    classic syllabaire pattern (5 consonants x 5 voyelles = 25 CV
    syllables). English adapts to beginner "word family" chunks (the
    closest English equivalent), 5 families x 3 example words. Same set
    for niveau 1 and niveau 2 in both languages -- a small, fixed,
    foundational set doesn't need two depths.
  - mots_simples (skill "mots_simples", format "lecon_mots"): the
    school/family/house/garden/pets/farm/clothes word lists, exactly as
    given by the user (French) / drafted in the same spirit (English).
    Same list for niveau 1 and niveau 2.
  - ecoute_ecriture (skill "ecoute_ecriture", format "ecoute_ecriture"): no
    fixed target content -- a free-write prompt, the frontend reads back
    whatever the child typed, not a stored answer.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # library-service/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import Exercise, GenerationRun, Source  # noqa: E402

SOURCE_URL_PREFIX = "local://dictee_guidee_seed_v1"

# --- Alphabet mots-reperes -------------------------------------------------

ALPHABET_FR_ORIGINAL = [
    ("A", "ardoise"), ("B", "bébé"), ("C", "cahier"), ("D", "dictée"), ("E", "école"),
    ("F", "famille"), ("G", "grand-mère"), ("H", "horloge"), ("I", "institutrice"),
    ("J", "jeu"), ("K", "kiwi"), ("L", "livre"), ("M", "maman"), ("N", "note"),
    ("O", "ordinateur"), ("P", "papa"), ("Q", "question"), ("R", "récréation"),
    ("S", "sœur"), ("T", "tableau"), ("U", "uniforme"), ("V", "vélo"), ("W", "wagon"),
    ("X", "xylophone"), ("Y", "yoyo"), ("Z", "zèbre"),
]

# 60 additional mots-reperes (2026-09-04), 2-3 syllables each, grouped by letter.
ALPHABET_FR_EXTRA = [
    ("A", "avion"), ("A", "abeille"), ("A", "ananas"), ("A", "araignée"),
    ("B", "ballon"), ("B", "bateau"), ("B", "biberon"),
    ("C", "cravate"), ("C", "citron"), ("C", "camion"),
    ("D", "domino"), ("D", "dauphin"), ("D", "dragon"),
    ("E", "étoile"), ("E", "éléphant"), ("E", "escargot"),
    ("F", "fusée"), ("F", "fenêtre"), ("F", "framboise"),
    ("G", "gâteau"), ("G", "guitare"), ("G", "grenouille"),
    ("H", "hérisson"), ("H", "hibou"), ("H", "hôpital"),
    ("I", "image"), ("I", "igloo"), ("I", "iguane"),
    ("J", "jumeau"), ("J", "jardin"), ("J", "journal"),
    ("K", "kangourou"), ("K", "karaté"), ("K", "koala"),
    ("L", "lumière"), ("L", "lapin"),
    ("M", "montagne"), ("M", "musique"),
    ("N", "nuage"), ("N", "nombre"),
    ("O", "orange"), ("O", "oreille"),
    ("P", "pyjama"), ("P", "parapluie"),
    ("Q", "quartier"), ("Q", "quatre"),
    ("R", "radio"), ("R", "robot"),
    ("S", "soleil"), ("S", "sirène"),
    ("T", "tortue"), ("T", "tomate"),
    ("U", "usine"), ("U", "univers"),
    ("V", "violon"), ("V", "voiture"),
    ("W", "week-end"),
    ("Y", "yaourt"), ("Y", "yoga"),
    ("Z", "zigzag"),
]

ALPHABET_EN = [
    ("A", "apple"), ("B", "baby"), ("C", "class"), ("D", "dad"), ("E", "eraser"),
    ("F", "family"), ("G", "grandma"), ("H", "homework"), ("I", "ink"), ("J", "juice"),
    ("K", "keyboard"), ("L", "lesson"), ("M", "mom"), ("N", "notebook"), ("O", "orange"),
    ("P", "pencil"), ("Q", "question"), ("R", "ruler"), ("S", "school"), ("T", "teacher"),
    ("U", "uniform"), ("V", "van"), ("W", "watch"), ("X", "xylophone"), ("Y", "yard"),
    ("Z", "zebra"),
]

# --- Syllabes ---------------------------------------------------------------

SYLLABES_FR = [
    {"syllable": f"{c}{v}", "example": ex}
    for c, exs in [
        ("B", {"A": "banane", "E": "belette", "I": "bicyclette", "O": "bonbon", "U": "bulle"}),
        ("M", {"A": "maman", "E": "menu", "I": "midi", "O": "moto", "U": "mur"}),
        ("P", {"A": "papa", "E": "petit", "I": "pilote", "O": "pomme", "U": "puzzle"}),
        ("T", {"A": "tapis", "E": "tenue", "I": "tigre", "O": "tomate", "U": "tulipe"}),
        ("L", {"A": "lapin", "E": "lever", "I": "lion", "O": "loto", "U": "lune"}),
    ]
    for v, ex in exs.items()
]

SYLLABLES_EN = [
    {"family": "-AT", "words": ["cat", "hat", "bat"]},
    {"family": "-AN", "words": ["can", "man", "fan"]},
    {"family": "-IG", "words": ["big", "pig", "dig"]},
    {"family": "-OG", "words": ["dog", "log", "fog"]},
    {"family": "-UN", "words": ["sun", "run", "fun"]},
]

# --- Mots simples (themes) --------------------------------------------------

MOTS_FR = [
    {"theme": "École", "words": ["l'école", "la classe", "la maîtresse", "le livre", "le cahier", "le stylo", "le sac", "le banc", "ami/amie"]},
    {"theme": "Maison", "words": ["papa", "maman", "mon frère", "ma sœur", "la maison", "la porte", "la table", "le lit"]},
    {"theme": "Animaux", "words": ["le chat", "le chien", "le lapin", "l'oiseau", "le poisson"]},
    {"theme": "Jardin", "words": ["le jardin", "l'arbre", "la fleur", "l'herbe", "la terre"]},
    {"theme": "Ferme", "words": ["la vache", "le cheval", "la poule", "le poussin"]},
    {"theme": "Vêtements", "words": ["le pantalon", "la chemise", "la jupe", "le manteau", "la chaussure", "les lunettes"]},
]

MOTS_EN = [
    {"theme": "School", "words": ["school", "class", "teacher", "book", "notebook", "pen", "bag", "bench", "friend"]},
    {"theme": "Home", "words": ["dad", "mom", "my brother", "my sister", "house", "door", "table", "bed"]},
    {"theme": "Animals", "words": ["cat", "dog", "rabbit", "bird", "fish"]},
    {"theme": "Garden", "words": ["garden", "tree", "flower", "grass", "ground"]},
    {"theme": "Farm", "words": ["cow", "horse", "hen", "chick"]},
    {"theme": "Clothes", "words": ["trousers", "shirt", "skirt", "coat", "shoes", "glasses"]},
]


def _source(id_suffix, subject_code, level_code, content_snapshot):
    return {
        "url": f"{SOURCE_URL_PREFIX}#{id_suffix}",
        "title": "Contenu Dictée guidée (rédigé pour SmartProf)",
        "license_status": "explicit_open",
        "subject_code": subject_code,
        "level_code": level_code,
        "domain_hint": "dictee_guidee",
        "trimester_hint": None,
        "region_scope": "tunisia_web",
        "content_snapshot": content_snapshot,
        "status": "used_for_generation",
    }


def _exercise(level_code, subject_code, skill_code, exercise_format, language, content):
    return {
        "subject_code": subject_code, "level_code": level_code, "trimester": "T1",
        "domain_code": "dictee_guidee", "skill_code": skill_code,
        "exercise_format": exercise_format, "difficulty": "en_cours", "language": language,
        "grading_mode": "open",
        "content": content,
    }


def build_examples():
    examples = []

    for level_code, alpha_fr in [("1", ALPHABET_FR_ORIGINAL), ("2", ALPHABET_FR_ORIGINAL + ALPHABET_FR_EXTRA)]:
        examples.append({
            "source": _source(f"FR_ALPHA_{level_code}", "fr", level_code, "Prompt original — séquence alphabet avec mots-repères."),
            "exercise": _exercise(level_code, "fr", "alphabet", "lecon_lettres", "fr", {
                "question": "Écoute et regarde bien chaque lettre.",
                "letters": [{"letter": l, "word": w} for l, w in alpha_fr],
            }),
        })

    for level_code in ["1", "2"]:
        examples.append({
            "source": _source(f"EN_ALPHA_{level_code}", "en", level_code, "Prompt original — séquence alphabet avec mots-repères."),
            "exercise": _exercise(level_code, "en", "alphabet", "lecon_lettres", "en", {
                "question": "Listen and look at each letter carefully.",
                "letters": [{"letter": l, "word": w} for l, w in ALPHABET_EN],
            }),
        })

    for level_code in ["1", "2"]:
        examples.append({
            "source": _source(f"FR_SYLL_{level_code}", "fr", level_code, "Prompt original — syllabaire (5 consonnes x 5 voyelles)."),
            "exercise": _exercise(level_code, "fr", "syllabe", "lecon_syllabes", "fr", {
                "question": "Écoute chaque syllabe, puis retrouve-la.",
                "syllables": SYLLABES_FR,
            }),
        })
        examples.append({
            "source": _source(f"EN_SYLL_{level_code}", "en", level_code, "Prompt original — familles de mots (word families)."),
            "exercise": _exercise(level_code, "en", "syllabe", "lecon_syllabes", "en", {
                "question": "Listen to each sound family, then try the words.",
                "syllable_families": SYLLABLES_EN,
            }),
        })

    for level_code in ["1", "2"]:
        examples.append({
            "source": _source(f"FR_MOTS_{level_code}", "fr", level_code, "Prompt original — mots par thème (école, famille, maison, jardin, animaux, ferme, vêtements)."),
            "exercise": _exercise(level_code, "fr", "mots_simples", "lecon_mots", "fr", {
                "question": "Écoute comment on prononce ces mots, thème par thème.",
                "themes": MOTS_FR,
            }),
        })
        examples.append({
            "source": _source(f"EN_MOTS_{level_code}", "en", level_code, "Prompt original — mots par thème."),
            "exercise": _exercise(level_code, "en", "mots_simples", "lecon_mots", "en", {
                "question": "Listen to how these words are said, theme by theme.",
                "themes": MOTS_EN,
            }),
        })

    for level_code in ["1", "2"]:
        examples.append({
            "source": _source(f"FR_ECOUTE_{level_code}", "fr", level_code, "Prompt original — champ libre écris et écoute."),
            "exercise": _exercise(level_code, "fr", "ecoute_ecriture", "ecoute_ecriture", "fr", {
                "question": "Écris une lettre, un mot ou une phrase, puis écoute ce que tu as écrit.",
            }),
        })
        examples.append({
            "source": _source(f"EN_ECOUTE_{level_code}", "en", level_code, "Prompt original — free write and listen."),
            "exercise": _exercise(level_code, "en", "ecoute_ecriture", "ecoute_ecriture", "en", {
                "question": "Write a letter, a word or a sentence, then listen to what you wrote.",
            }),
        })

    return examples


def main():
    with app.app_context():
        db.create_all()

        if Exercise.query.filter(Exercise.source_id.isnot(None)).join(Source).filter(
            Source.url.like(f"{SOURCE_URL_PREFIX}%")
        ).first() is not None:
            print("Dictée guidée content already seeded, skipping.")
            return

        examples = build_examples()
        for example in examples:
            source = Source(**example["source"])
            db.session.add(source)
            db.session.flush()

            generation_run = GenerationRun(
                source_id=source.id,
                model_provider="anthropic",
                model_name="claude-opus-5",
                prompt_template_version="v1-dictee-guidee-seed",
                status="success",
                raw_model_output="(hand-authored seed content, not a real model call)",
            )
            db.session.add(generation_run)
            db.session.flush()

            exercise = Exercise(
                generation_run_id=generation_run.id,
                source_id=source.id,
                review_status="approved",
                reviewed_by="seed-script",
                status="published",
                curriculum_schema_version="v1",
                **example["exercise"],
            )
            db.session.add(exercise)

        db.session.commit()
        print(f"Seeded {len(examples)} dictée guidée exercises.")


if __name__ == "__main__":
    main()
