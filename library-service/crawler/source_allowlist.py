"""Curated source list. Discover reads ONLY from here — no open web search
yet. Two tiers, per the validated sourcing rule:

- region_scope="tunisia_official": ministry/institutional manuals — highest
  trust, used as the primary reference for curriculum alignment.
- region_scope="tunisia_web": everything else that still targets the
  Tunisian program — parascolaire homework/exercise banks, tutoring sites,
  independent teacher resources. Broader on purpose: more variety here
  means more inspiration material for generate_exercise.py to draw
  original exercises from. None of these are treated as more "official" —
  classify.py still defaults every one of them to license_status=
  "unlicensed" (inspiration-only, see generate_exercise.py) unless a page
  explicitly carries an open license.

Verified accessible as of 2026-09-01; add more entries as they're
identified and checked."""

SOURCES = [
    {
        "url": "http://www.ecolenumerique.cnte.tn/?p=6736",
        "title": "Manuels 1ère Année — Centre National des Technologies en Éducation (Tunisie)",
        "region_scope": "tunisia_official",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://examens.tn/fr/maths-1ere-annee-primaire-modele-dexamen-1-183/",
        "title": "Modèle d'examen Maths 1ère année primaire — examens.tn",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://examens.tn/fr/devoirs-mathematiques-4eme-primaire-exercices-tunisie-624/",
        "title": "Devoirs Mathématiques 4ème Primaire — examens.tn",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "4",
    },
    {
        "url": "https://www.devoir.tn/primaire.html",
        "title": "Devoir.TN — ressources primaire (maths, éveil scientifique, dictée...)",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://www.devoirat.net/",
        "title": "Devoirat.net — devoirs et séries multi-matières Tunisie",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://sites.google.com/site/topdevoirs/1ere-annee-primaire-exercice-tunisie",
        "title": "Top Devoirs — exercices 1ère année primaire Tunisie",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "1",
    },
]
