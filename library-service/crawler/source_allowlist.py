"""Curated source list per region_scope, per the validated sourcing rule:
Tunisian official manuals first for levels 3-5 and for Arabe/Sciences/Math at
levels 1-2, French-Ministry/British-approved manuals only for Français/
Anglais at levels 1-2. Discover reads ONLY from here — no open web search
yet. Verified accessible sources as of 2026-09-01; add more entries as they
are identified and checked."""

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
]
