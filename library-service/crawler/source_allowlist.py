"""Curated source list. Discover reads ONLY from here — no open web search
yet. Three tiers, per the validated sourcing rule:

- region_scope="tunisia_official": ministry/institutional platforms and
  manuals — highest trust, used as the primary reference for curriculum
  alignment.
- region_scope="tunisia_web": everything else that still targets the
  Tunisian program — parascolaire homework/exercise banks, tutoring sites,
  independent teacher resources. Broader on purpose: more variety here
  means more inspiration material for generate_exercise.py to draw
  original exercises from.
- region_scope="international_aligned": non-Tunisian resources used ONLY
  where their specific topic genuinely matches a domain in the Tunisian
  program (e.g. a foreign 4th-grade "matter/technology" science lesson
  mapped to éveil scientifique) — not general-purpose foreign curricula.

None of these three tiers are treated as more "legally safe" than another —
classify.py defaults every one of them to license_status="unlicensed"
(inspiration-only, see generate_exercise.py: content is never copied, only
used to generate an original exercise) unless a page explicitly carries an
open license. "No copyright notice visible" is not the same as "free to
copy" in any of these tiers.

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
    {
        "url": "https://edusoutien.education.tn/",
        "title": "Edusoutien — plateforme officielle de soutien scolaire, Ministère de l'Éducation (Tunisie)",
        "region_scope": "tunisia_official",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://examens.tn/fr/evaluations-1ere-annee-primaire-trimestre-3-modele-7-778/",
        "title": "Évaluations 1ère année primaire, trimestre 3 — examens.tn",
        "region_scope": "tunisia_web",
        "subject_code": "math",
        "level_code": "1",
    },
    {
        "url": "https://examens.tn/fr/3eme-annee-primaire-evaluation-sciences-3eme-trimestre-avec-corrige-991/",
        "title": "3ème année primaire — Évaluation Sciences, 3ème trimestre — examens.tn",
        "region_scope": "tunisia_web",
        "subject_code": "science",
        "level_code": "3",
    },
    {
        "url": "https://examens.tn/fr/eveil-scientifique-5eme-annee-primaire-lecon-complete-et-conseils-544/",
        "title": "Éveil Scientifique 5ème année primaire — leçon complète — examens.tn",
        "region_scope": "tunisia_web",
        "subject_code": "science",
        "level_code": "5",
    },
    {
        "url": "https://www.pass-education.be/sciences-et-technologie-4eme-primaire/",
        "title": "Sciences et technologie, 4ème primaire — Pass Éducation (Belgique)",
        "region_scope": "international_aligned",
        "subject_code": "science",
        "level_code": "4",
    },
]
