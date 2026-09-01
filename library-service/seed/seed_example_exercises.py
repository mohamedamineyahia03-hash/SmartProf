"""Phase 1 seed: example exercises with real provenance (source ->
generation_run -> exercise), so the sync API and the Main App's pull job can be
exercised end-to-end. Content is single-language (Arabic for math, per the
Arabic-only content policy) -- see library-service/generation/generate_exercise.py
for LANGUAGE_BY_SUBJECT, which the real crawler pipeline follows too.

These specific rows are manually authored placeholders, not real AI-generated
content -- they exist to prove the FK chain and the export contract work, and
to give the app real content to serve before the crawler has produced volume.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # library-service/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import Exercise, GenerationRun, Source  # noqa: E402

EXAMPLES = [
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/numeration",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de dénombrement d'objets illustrés (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "عدّ التفاحات واكتب العدد.",
                "visual": "🍎 🍎 🍎 🍎",
                "answer": 4,
                "explanation": "أشر إلى كل تفاحة وعدّها مرة واحدة فقط: 1، 2، 3، 4. المجموع هو 4 تفاحات."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/calcul",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple d'addition simple avec supports visuels (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 3 + 2؟",
                "choices": [
                    "4",
                    "5",
                    "6"
                ],
                "answer": "5",
                "explanation": "ابدأ من 3 وتقدّم خطوتين: 4، 5. إذن 3 + 2 = 5."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/geometrie",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de reconnaissance de formes géométriques (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "أي شكل له 3 أضلاع؟",
                "choices": [
                    "⬛ مربع",
                    "🔺 مثلث",
                    "⚪ دائرة"
                ],
                "answer": "🔺 مثلث",
                "explanation": "المثلث له بالضبط 3 أضلاع و3 رؤوس. أما المربع فله 4 أضلاع، والدائرة ليس لها أضلاع مستقيمة."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/numeration-comparaison",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de comparaison de petits nombres (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "3",
                    "7",
                    "5"
                ],
                "answer": "7",
                "explanation": "قارن الأعداد اثنين اثنين: 7 أكبر من 3 وأكبر من 5. إذن هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/problemes-additifs",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de petit problème additif avec récit (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "resoudre",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ليلى 6 كرات. ربحت 3 كرات إضافية. كم كرة أصبح لديها الآن؟",
                "answer": 9,
                "explanation": "ليلى ربحت كرات، إذن نجمع: 6 + 3 = 9. أصبح لديها الآن 9 كرات."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/reperage-spatial",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de repérage spatial dessus/dessous avec support visuel (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "dessus_dessous",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "أين يوجد القط بالنسبة للصندوق؟",
                "visual": "📦<br>🐱",
                "choices": [
                    "القط فوق",
                    "القط تحت",
                    "القط بجانب"
                ],
                "answer": "القط تحت",
                "explanation": "انظر جيدًا إلى الصورة: الصندوق مرسوم في الأعلى والقط في الأسفل. إذن القط تحت الصندوق."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/comparaison-longueurs",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de comparaison de longueurs avec support visuel (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬▬<br>الخط ب : ▬▬▬",
                "choices": [
                    "الخط أ",
                    "الخط ب"
                ],
                "answer": "الخط أ",
                "explanation": "لاحظ الخطين: الخط أ يحتوي على أجزاء أكثر من الخط ب، إذن هو الأطول."
            }
        }
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/recit-multi-questions",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de récit avec plusieurs questions liées (source d'inspiration uniquement).",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى أمين سلة فواكه: 5 تفاحات و3 موزات وحبتا كمثرى.",
                "sub_questions": [
                    {
                        "question": "كم عدد التفاحات التي يملكها أمين؟",
                        "answer": 5,
                        "explanation": "تذكر القصة مباشرة أن أمين لديه 5 تفاحات."
                    },
                    {
                        "question": "كم عدد الفواكه لديه في المجموع؟",
                        "answer": 10,
                        "explanation": "نجمع كل الفواكه في السلة: 5 + 3 + 2 = 10."
                    },
                    {
                        "question": "هل لديه تفاح أكثر أم موز أكثر؟",
                        "choices": [
                            "تفاح أكثر",
                            "موز أكثر",
                            "نفس العدد"
                        ],
                        "answer": "تفاح أكثر",
                        "explanation": "5 تفاحات أكثر من 3 موزات. إذن لدى أمين تفاح أكثر."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#poissons-aquarium",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "في مقصورة السمك بالقسم، يوجد 7 أسماك حمراء و5 أسماك زرقاء.",
                "sub_questions": [
                    {
                        "question": "كم عدد الأسماك الجملي في المقصورة؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 7 + 5 = 12."
                    },
                    {
                        "question": "أعطت المعلمة 2 سمكتين لقسم آخر. كم سمكة بقيت في المقصورة؟",
                        "answer": 10,
                        "explanation": "نطرح الأسماك التي أُعطيت: 12 − 2 = 10."
                    },
                    {
                        "question": "قسّم التلاميذ الأسماك الباقية بالتساوي بين مقصورتين. كم سمكة ستكون في كل مقصورة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 أسماك على مقصورتين بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#ballons-fete",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لحفل المدرسة، نفخت ياسمين 9 بالونات حمراء و7 بالونات صفراء.",
                "sub_questions": [
                    {
                        "question": "كم بالونًا نفخت ياسمين في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع البالونات الحمراء والصفراء: 9 + 7 = 16."
                    },
                    {
                        "question": "انفجرت 4 بالونات قبل بداية الحفل. كم بالونًا بقي؟",
                        "answer": 12,
                        "explanation": "نطرح البالونات التي انفجرت: 16 − 4 = 12."
                    },
                    {
                        "question": "علّقت ياسمين البالونات الباقية بالتساوي على جانبي الباب. كم بالونًا سيكون في كل جانب؟",
                        "answer": 6,
                        "explanation": "نقسم 12 بالونًا على جانبين بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#biscuits-maman",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "تحضّر الأم صينية فيها 8 قطع حلوى بالشوكولاطة و6 قطع بالفانيليا.",
                "sub_questions": [
                    {
                        "question": "كم قطعة حلوى في الصينية إجمالًا؟",
                        "answer": 14,
                        "explanation": "نجمع النوعين: 8 + 6 = 14."
                    },
                    {
                        "question": "أكل الأب قطعتين بعد رجوعه من العمل. كم قطعة بقيت؟",
                        "answer": 12,
                        "explanation": "نطرح القطع التي أُكلت: 14 − 2 = 12."
                    },
                    {
                        "question": "تقاسمت الأختان القطع الباقية بالتساوي. كم قطعة ستأخذ كل واحدة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 قطعة على الأختين بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#autocollants-nour",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى نور 9 ملصقات على شكل نجمة و5 ملصقات على شكل قلب.",
                "sub_questions": [
                    {
                        "question": "كم ملصقًا لدى نور في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع النجوم والقلوب: 9 + 5 = 14."
                    },
                    {
                        "question": "أعطت نور 4 ملصقات لصديقتها المفضلة. كم ملصقًا بقي لديها؟",
                        "answer": 10,
                        "explanation": "نطرح الملصقات التي أُعطيت: 14 − 4 = 10."
                    },
                    {
                        "question": "لصقت نور الملصقات الباقية بالتساوي على كراسين. كم ملصقًا سيكون على كل كراس؟",
                        "answer": 5,
                        "explanation": "نقسم 10 ملصقات على كراسين بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#coquillages-plage",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "على الشاطئ، جمع آدم 8 أصداف كبيرة و6 أصداف صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم صدفة جمع آدم في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع الأصداف الكبيرة والصغيرة: 8 + 6 = 14."
                    },
                    {
                        "question": "فقد آدم صدفتين أثناء الجري على الرمل. كم صدفة بقيت لديه؟",
                        "answer": 12,
                        "explanation": "نطرح الأصداف المفقودة: 14 − 2 = 12."
                    },
                    {
                        "question": "رتّب آدم الأصداف الباقية بالتساوي في علبتين صغيرتين. كم صدفة ستكون في كل علبة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 صدفة على علبتين بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#dattes-recolte",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "أثناء جني التمور، قطف الجد 9 تمرات ناضجة وقطف علي 7 تمرات أخرى.",
                "sub_questions": [
                    {
                        "question": "كم تمرة قطفا في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع الكميتين: 9 + 7 = 16."
                    },
                    {
                        "question": "أهديا 4 تمرات لجيرانهما. كم تمرة بقيت لديهما؟",
                        "answer": 12,
                        "explanation": "نطرح التمرات المُهداة: 16 − 4 = 12."
                    },
                    {
                        "question": "قسّما التمرات الباقية بالتساوي في سلّتين. كم تمرة ستكون في كل سلة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 تمرة على سلتين بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#cubes-construction",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "في صندوق الألعاب، توجد 7 مكعبات حمراء و7 مكعبات زرقاء.",
                "sub_questions": [
                    {
                        "question": "كم مكعبًا في الصندوق إجمالًا؟",
                        "answer": 14,
                        "explanation": "نجمع المكعبات الحمراء والزرقاء: 7 + 7 = 14."
                    },
                    {
                        "question": "رتّب الأخ الصغير 6 مكعبات في مكان آخر بالخطأ. كم مكعبًا بقي في الصندوق؟",
                        "answer": 8,
                        "explanation": "نطرح المكعبات التي رُتبت في مكان آخر: 14 − 6 = 8."
                    },
                    {
                        "question": "قسّم الأطفال المكعبات الباقية بالتساوي لبناء برجين. كم مكعبًا سيكون في كل برج؟",
                        "answer": 4,
                        "explanation": "نقسم 8 مكعبات على برجين بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#papillons-jardin",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "في الحديقة، توجد 9 فراشات بيضاء و5 فراشات برتقالية.",
                "sub_questions": [
                    {
                        "question": "كم فراشة في الحديقة إجمالًا؟",
                        "answer": 14,
                        "explanation": "نجمع الفراشات البيضاء والبرتقالية: 9 + 5 = 14."
                    },
                    {
                        "question": "طارت فراشتان فوق الجدار. كم فراشة بقيت في الحديقة؟",
                        "answer": 12,
                        "explanation": "نطرح الفراشات التي طارت: 14 − 2 = 12."
                    },
                    {
                        "question": "استقرت الفراشات الباقية بالتساوي على شجيرتي ورد. كم فراشة ستكون على كل شجيرة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 فراشة على شجيرتين بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#fraises-jardin",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "في الحديقة، قطفت سارة 8 حبات فراولة وقطفت أمها 4 حبات أخرى.",
                "sub_questions": [
                    {
                        "question": "كم حبة فراولة قطفتا في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع الكميتين: 8 + 4 = 12."
                    },
                    {
                        "question": "أكلتا 4 حبات على الفور. كم حبة بقيت لديهما؟",
                        "answer": 8,
                        "explanation": "نطرح الحبات التي أُكلت: 12 − 4 = 8."
                    },
                    {
                        "question": "قسّمتا الحبات الباقية بالتساوي في سلتين صغيرتين. كم حبة ستكون في كل سلة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 حبات على سلتين بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://exercices_math_1ere_annee_tunisie.docx#bougies-gateau",
            "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لعيد الميلاد، اشترت الأم 9 شموع حمراء و9 شموع ذهبية.",
                "sub_questions": [
                    {
                        "question": "كم شمعة اشترت الأم في المجموع؟",
                        "answer": 18,
                        "explanation": "نجمع الشموع الحمراء والذهبية: 9 + 9 = 18."
                    },
                    {
                        "question": "سقطت 4 شموع وانكسرت قبل الحفل. كم شمعة صالحة بقيت؟",
                        "answer": 14,
                        "explanation": "نطرح الشموع المكسورة: 18 − 4 = 14."
                    },
                    {
                        "question": "وضعت الأم الشموع الباقية بالتساوي على كعكتين. كم شمعة ستكون على كل كعكة؟",
                        "answer": 7,
                        "explanation": "نقسم 14 شمعة على كعكتين بالتساوي: 14 ÷ 2 = 7."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#monnaie-reconnaissance",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur (programme Tunisie 2025/2026) : sert uniquement à confirmer quels sujets couvrir, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مليمًا يوجد في يد ياسين إجمالًا؟",
                "visual": "🪙🪙🪙🪙🪙 + 🪙🪙",
                "choices": [
                    "6",
                    "7",
                    "8"
                ],
                "answer": "7",
                "explanation": "نعدّ كل القطع: 5 قطع + قطعتان = 7 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#monnaie-addition",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur (programme Tunisie 2025/2026) : sert uniquement à confirmer quels sujets couvrir, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "addition_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى أمل قطعة من 5 مليمات وقطعة من 3 مليمات في جيبها.",
                "visual": "🪙×5 + 🪙×3",
                "answer": 8,
                "explanation": "نجمع القيمتين: 5 + 3 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#dizaine-unites",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur (programme Tunisie 2025/2026) : sert uniquement à confirmer quels sujets couvrir, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و4 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 (4 آحاد)",
                "answer": 14,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد الأربعة: 10 + 4 = 14."
            }
        }
    },
    {
        "source": {
            "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#addition-verticale",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur (programme Tunisie 2025/2026) : sert uniquement à confirmer quels sujets couvrir, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 13 + 6",
                "answer": 19,
                "explanation": "نرتب الآحاد تحت الآحاد والعشرات تحت العشرات: 3 + 6 = 9 آحاد، والعشرة الواحدة تبقى كما هي. إذن 13 + 6 = 19."
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#chatons-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 7 قِطَط بيضاء و5 قِطَط سوداء.",
                "sub_questions": [
                    {
                        "question": "كم عدد قِطَط في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 7 + 5 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من قِطَط لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#poussins-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 9 كتاكيت صفراء و7 كتاكيت بنية.",
                "sub_questions": [
                    {
                        "question": "كم عدد كتاكيت في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 9 + 7 = 16."
                    },
                    {
                        "question": "بعد إهداء 4 من كتاكيت لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 16 − 4 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#canards-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 8 بطّات بيضاء و6 بطّات صفراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد بطّات في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 8 + 6 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من بطّات لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#escargots-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 9 حلزونات كبيرة و5 حلزونات صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد حلزونات في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 9 + 5 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من حلزونات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#coccinelles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 7 دعاسيق حمراء و7 دعاسيق صفراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد دعاسيق في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 7 + 7 = 14."
                    },
                    {
                        "question": "بعد إهداء 6 من دعاسيق لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 14 − 6 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#abeilles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أحمد 8 نحلات كبيرة و4 نحلات صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد نحلات في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 8 + 4 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من نحلات لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#tortues-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى علي 9 سلاحف كبيرة و9 سلاحف صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد سلاحف في المجموع؟",
                        "answer": 18,
                        "explanation": "نجمع المجموعتين: 9 + 9 = 18."
                    },
                    {
                        "question": "بعد إهداء 4 من سلاحف لصديق، كم بقي؟",
                        "answer": 14,
                        "explanation": "نطرح ما أُهدي: 18 − 4 = 14."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 7,
                        "explanation": "نقسم 14 على 2 بالتساوي: 14 ÷ 2 = 7."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#grenouilles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى آية 6 ضفادع خضراء و8 ضفادع بنية.",
                "sub_questions": [
                    {
                        "question": "كم عدد ضفادع في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 6 + 8 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من ضفادع لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#herissons-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سارة 5 قنافذ كبيرة و7 قنافذ صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد قنافذ في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 5 + 7 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من قنافذ لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#ecureuils-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 9 سناجب حمراء و4 سناجب رمادية.",
                "sub_questions": [
                    {
                        "question": "كم عدد سناجب في المجموع؟",
                        "answer": 13,
                        "explanation": "نجمع المجموعتين: 9 + 4 = 13."
                    },
                    {
                        "question": "بعد إهداء 3 من سناجب لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 13 − 3 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#bananes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 6 موز أصفر و6 موز أخضر.",
                "sub_questions": [
                    {
                        "question": "كم عدد موز في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 6 + 6 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من موز لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#poires-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 7 كمثرى صفراء و9 كمثرى خضراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد كمثرى في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 7 + 9 = 16."
                    },
                    {
                        "question": "بعد إهداء 6 من كمثرى لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 16 − 6 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#cerises-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 5 كرز أحمر و9 كرز أصفر.",
                "sub_questions": [
                    {
                        "question": "كم عدد كرز في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 5 + 9 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من كرز لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#tomates-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 4 طماطم كبيرة و8 طماطم صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد طماطم في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 4 + 8 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من طماطم لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#carottes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أحمد 9 جزر كبير و6 جزر صغير.",
                "sub_questions": [
                    {
                        "question": "كم عدد جزر في المجموع؟",
                        "answer": 15,
                        "explanation": "نجمع المجموعتين: 9 + 6 = 15."
                    },
                    {
                        "question": "بعد إهداء 3 من جزر لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 15 − 3 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#olives-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى علي 7 زيتون أسود و5 زيتون أخضر.",
                "sub_questions": [
                    {
                        "question": "كم عدد زيتون في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 7 + 5 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من زيتون لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#figues-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى آية 9 تين أخضر و7 تين أرجواني.",
                "sub_questions": [
                    {
                        "question": "كم عدد تين في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 9 + 7 = 16."
                    },
                    {
                        "question": "بعد إهداء 4 من تين لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 16 − 4 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#gommes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سارة 8 ممحيات زرقاء و6 ممحيات حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد ممحيات في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 8 + 6 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من ممحيات لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#regles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 9 مساطر طويلة و5 مساطر قصيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد مساطر في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 9 + 5 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من مساطر لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#feutres-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 7 أقلام تلوين زرقاء و7 أقلام تلوين حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد أقلام تلوين في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 7 + 7 = 14."
                    },
                    {
                        "question": "بعد إهداء 6 من أقلام تلوين لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 14 − 6 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#taille_crayons-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 8 مبريات صفراء و4 مبريات خضراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد مبريات في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 8 + 4 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من مبريات لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#poupees-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 9 دمى كبيرة و9 دمى صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد دمى في المجموع؟",
                        "answer": 18,
                        "explanation": "نجمع المجموعتين: 9 + 9 = 18."
                    },
                    {
                        "question": "بعد إهداء 4 من دمى لصديق، كم بقي؟",
                        "answer": 14,
                        "explanation": "نطرح ما أُهدي: 18 − 4 = 14."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 7,
                        "explanation": "نقسم 14 على 2 بالتساوي: 14 ÷ 2 = 7."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#cerfs_volants-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 6 طائرات ورقية حمراء و8 طائرات ورقية زرقاء.",
                "sub_questions": [
                    {
                        "question": "كم عدد طائرات ورقية في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 6 + 8 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من طائرات ورقية لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#toupies-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أحمد 5 دوامات حمراء و7 دوامات صفراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد دوامات في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 5 + 7 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من دوامات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#pieces_puzzle-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى علي 9 قطع أحجية زرقاء و4 قطع أحجية صفراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد قطع أحجية في المجموع؟",
                        "answer": 13,
                        "explanation": "نجمع المجموعتين: 9 + 4 = 13."
                    },
                    {
                        "question": "بعد إهداء 3 من قطع أحجية لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 13 − 3 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#figurines-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى آية 6 دمى صغيرة حمراء و6 دمى صغيرة زرقاء.",
                "sub_questions": [
                    {
                        "question": "كم عدد دمى صغيرة في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 6 + 6 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من دمى صغيرة لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#cailloux-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سارة 7 حصيات بيضاء و9 حصيات رمادية.",
                "sub_questions": [
                    {
                        "question": "كم عدد حصيات في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 7 + 9 = 16."
                    },
                    {
                        "question": "بعد إهداء 6 من حصيات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 16 − 6 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#glands-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 5 حبات بلوط كبيرة و9 حبات بلوط صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد حبات بلوط في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 5 + 9 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من حبات بلوط لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#pommes_pin-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 4 أكواز صنوبر كبيرة و8 أكواز صنوبر صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد أكواز صنوبر في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 4 + 8 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من أكواز صنوبر لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#feuilles_automne-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 9 أوراق خريف صفراء و6 أوراق خريف برتقالية.",
                "sub_questions": [
                    {
                        "question": "كم عدد أوراق خريف في المجموع؟",
                        "answer": 15,
                        "explanation": "نجمع المجموعتين: 9 + 6 = 15."
                    },
                    {
                        "question": "بعد إهداء 3 من أوراق خريف لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 15 − 3 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#gateaux-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 7 كعكات صغيرة بالشوكولاطة و5 كعكات صغيرة بالفانيليا.",
                "sub_questions": [
                    {
                        "question": "كم عدد كعكات صغيرة في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 7 + 5 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من كعكات صغيرة لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#madeleines-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 9 قطع مادلين بالعسل و7 قطع مادلين بالليمون.",
                "sub_questions": [
                    {
                        "question": "كم عدد قطع مادلين في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 9 + 7 = 16."
                    },
                    {
                        "question": "بعد إهداء 4 من قطع مادلين لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 16 − 4 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#crepes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أحمد 8 قطع كريب بالعسل و6 قطع كريب بالمربى.",
                "sub_questions": [
                    {
                        "question": "كم عدد قطع كريب في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 8 + 6 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من قطع كريب لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#perles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى علي 9 خرز زرقاء و5 خرز حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد خرز في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 9 + 5 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من خرز لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#rubans-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى آية 7 أشرطة صفراء و7 أشرطة وردية.",
                "sub_questions": [
                    {
                        "question": "كم عدد أشرطة في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 7 + 7 = 14."
                    },
                    {
                        "question": "بعد إهداء 6 من أشرطة لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 14 − 6 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#chaussettes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سارة 8 جوارب زرقاء و4 جوارب بيضاء.",
                "sub_questions": [
                    {
                        "question": "كم عدد جوارب في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 8 + 4 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من جوارب لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#gants-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 9 قفازات حمراء و9 قفازات زرقاء.",
                "sub_questions": [
                    {
                        "question": "كم عدد قفازات في المجموع؟",
                        "answer": 18,
                        "explanation": "نجمع المجموعتين: 9 + 9 = 18."
                    },
                    {
                        "question": "بعد إهداء 4 من قفازات لصديق، كم بقي؟",
                        "answer": 14,
                        "explanation": "نطرح ما أُهدي: 18 − 4 = 14."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 7,
                        "explanation": "نقسم 14 على 2 بالتساوي: 14 ÷ 2 = 7."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#seaux_plage-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 6 دِلاء شاطئ صفراء و8 دِلاء شاطئ حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد دِلاء شاطئ في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 6 + 8 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من دِلاء شاطئ لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#etoiles_mer-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 5 نجوم بحر برتقالية و7 نجوم بحر حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد نجوم بحر في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 5 + 7 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من نجوم بحر لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#crabes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 9 سلطعونات حمراء و4 سلطعونات برتقالية.",
                "sub_questions": [
                    {
                        "question": "كم عدد سلطعونات في المجموع؟",
                        "answer": 13,
                        "explanation": "نجمع المجموعتين: 9 + 4 = 13."
                    },
                    {
                        "question": "بعد إهداء 3 من سلطعونات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 13 − 3 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#libellules-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 6 يعاسيب زرقاء و6 يعاسيب خضراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد يعاسيب في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 6 + 6 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من يعاسيب لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#fourmis-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أحمد 7 نملات سوداء و9 نملات حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد نملات في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 7 + 9 = 16."
                    },
                    {
                        "question": "بعد إهداء 6 من نملات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 16 − 6 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#sauterelles-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى علي 5 جرادات خضراء و9 جرادات بنية.",
                "sub_questions": [
                    {
                        "question": "كم عدد جرادات في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 5 + 9 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من جرادات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#champignons-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى آية 4 فطريات بيضاء و8 فطريات بنية.",
                "sub_questions": [
                    {
                        "question": "كم عدد فطريات في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 4 + 8 = 12."
                    },
                    {
                        "question": "بعد إهداء 4 من فطريات لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 12 − 4 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#noix-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سارة 9 حبات جوز كبيرة و6 حبات جوز صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد حبات جوز في المجموع؟",
                        "answer": 15,
                        "explanation": "نجمع المجموعتين: 9 + 6 = 15."
                    },
                    {
                        "question": "بعد إهداء 3 من حبات جوز لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 15 − 3 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#amandes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى ياسين 7 حبات لوز كبيرة و5 حبات لوز صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد حبات لوز في المجموع؟",
                        "answer": 12,
                        "explanation": "نجمع المجموعتين: 7 + 5 = 12."
                    },
                    {
                        "question": "بعد إهداء 2 من حبات لوز لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 12 − 2 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين علبتين، كم سيكون في كل علبة؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#pistaches-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى مريم 9 حبات فستق كبيرة و7 حبات فستق صغيرة.",
                "sub_questions": [
                    {
                        "question": "كم عدد حبات فستق في المجموع؟",
                        "answer": 16,
                        "explanation": "نجمع المجموعتين: 9 + 7 = 16."
                    },
                    {
                        "question": "بعد إهداء 4 من حبات فستق لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 16 − 4 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين سلتين، كم سيكون في كل سلة؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#craies-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى لينا 8 طباشير بيضاء و6 طباشير ملونة.",
                "sub_questions": [
                    {
                        "question": "كم عدد طباشير في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 8 + 6 = 14."
                    },
                    {
                        "question": "بعد إهداء 2 من طباشير لصديق، كم بقي؟",
                        "answer": 12,
                        "explanation": "نطرح ما أُهدي: 14 − 2 = 12."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين كيسين، كم سيكون في كل كيس؟",
                        "answer": 6,
                        "explanation": "نقسم 12 على 2 بالتساوي: 12 ÷ 2 = 6."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#badges-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى سامي 9 شارات زرقاء و5 شارات حمراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد شارات في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 9 + 5 = 14."
                    },
                    {
                        "question": "بعد إهداء 4 من شارات لصديق، كم بقي؟",
                        "answer": 10,
                        "explanation": "نطرح ما أُهدي: 14 − 4 = 10."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين صديقين، كم سيكون في كل صديق؟",
                        "answer": 5,
                        "explanation": "نقسم 10 على 2 بالتساوي: 10 ÷ 2 = 5."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://recit-generique.docx#barrettes-batch2",
            "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "لدى أمين 7 مشابك شعر وردية و7 مشابك شعر صفراء.",
                "sub_questions": [
                    {
                        "question": "كم عدد مشابك شعر في المجموع؟",
                        "answer": 14,
                        "explanation": "نجمع المجموعتين: 7 + 7 = 14."
                    },
                    {
                        "question": "بعد إهداء 6 من مشابك شعر لصديق، كم بقي؟",
                        "answer": 8,
                        "explanation": "نطرح ما أُهدي: 14 − 6 = 8."
                    },
                    {
                        "question": "بعد تقسيم الباقي بالتساوي بين مجموعتين، كم سيكون في كل مجموعة؟",
                        "answer": 4,
                        "explanation": "نقسم 8 على 2 بالتساوي: 8 ÷ 2 = 4."
                    }
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-denombrement-72",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "كم عدد نجوم التي تراها؟",
                "visual": "⭐⭐⭐",
                "answer": 3,
                "explanation": "نعدّ واحدًا واحدًا: يوجد 3."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-denombrement-73",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم عدد بالونات التي تراها؟",
                "visual": "🎈🎈🎈🎈🎈",
                "answer": 5,
                "explanation": "نعدّ واحدًا واحدًا: يوجد 5."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-denombrement-74",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم عدد أسماك التي تراها؟",
                "visual": "🐟🐟🐟🐟🐟🐟🐟",
                "answer": 7,
                "explanation": "نعدّ واحدًا واحدًا: يوجد 7."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-denombrement-75",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم عدد أزهار التي تراها؟",
                "visual": "🌸🌸🌸🌸🌸🌸🌸🌸",
                "answer": 8,
                "explanation": "نعدّ واحدًا واحدًا: يوجد 8."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-denombrement-76",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "كم عدد حلوى التي تراها؟",
                "visual": "🍬🍬🍬🍬🍬🍬🍬🍬🍬",
                "answer": 9,
                "explanation": "نعدّ واحدًا واحدًا: يوجد 9."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition-77",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 2 + 3؟",
                "choices": [
                    "4",
                    "5"
                ],
                "answer": "5",
                "explanation": "نجمع: 2 + 3 = 5."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition-78",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 4 + 5؟",
                "choices": [
                    "8",
                    "9"
                ],
                "answer": "9",
                "explanation": "نجمع: 4 + 5 = 9."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition-79",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 3 + 3؟",
                "choices": [
                    "5",
                    "6"
                ],
                "answer": "6",
                "explanation": "نجمع: 3 + 3 = 6."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition-80",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 1 + 6؟",
                "choices": [
                    "6",
                    "7"
                ],
                "answer": "7",
                "explanation": "نجمع: 1 + 6 = 7."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition-81",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مجموع 4 + 4؟",
                "choices": [
                    "7",
                    "8"
                ],
                "answer": "8",
                "explanation": "نجمع: 4 + 4 = 8."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-ordre_nombres-82",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "2",
                    "4",
                    "1"
                ],
                "answer": "4",
                "explanation": "نقارن الأعداد: 4 هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-ordre_nombres-83",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "5",
                    "3",
                    "2"
                ],
                "answer": "5",
                "explanation": "نقارن الأعداد: 5 هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-ordre_nombres-84",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "13",
                    "17",
                    "11"
                ],
                "answer": "17",
                "explanation": "نقارن الأعداد: 17 هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-ordre_nombres-85",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "19",
                    "12",
                    "15"
                ],
                "answer": "19",
                "explanation": "نقارن الأعداد: 19 هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-ordre_nombres-86",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو أكبر عدد؟",
                "choices": [
                    "14",
                    "18",
                    "10"
                ],
                "answer": "18",
                "explanation": "نقارن الأعداد: 18 هو الأكبر بين الثلاثة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-comparaison_longueurs-87",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬",
                "choices": [
                    "الخط أ",
                    "الخط ب"
                ],
                "answer": "الخط أ",
                "explanation": "الخط أ يحتوي على 7 أجزاء مقابل 4 للخط ب: إذن هو الأطول."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-comparaison_longueurs-88",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬<br>الخط ب : ▬▬▬",
                "choices": [
                    "الخط أ",
                    "الخط ب"
                ],
                "answer": "الخط أ",
                "explanation": "الخط أ يحتوي على 5 أجزاء مقابل 3 للخط ب: إذن هو الأطول."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-comparaison_longueurs-89",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬▬",
                "choices": [
                    "الخط أ",
                    "الخط ب"
                ],
                "answer": "الخط أ",
                "explanation": "الخط أ يحتوي على 8 أجزاء مقابل 5 للخط ب: إذن هو الأطول."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-comparaison_longueurs-90",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬",
                "choices": [
                    "الخط أ",
                    "الخط ب"
                ],
                "answer": "الخط أ",
                "explanation": "الخط أ يحتوي على 6 أجزاء مقابل 4 للخط ب: إذن هو الأطول."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-reconnaissance_monnaie-91",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مليمًا يوجد في المجموع؟",
                "visual": "🪙🪙🪙🪙 + 🪙🪙🪙",
                "choices": [
                    "6",
                    "7",
                    "8"
                ],
                "answer": "7",
                "explanation": "نعدّ كل القطع: 4 + 3 = 7 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-reconnaissance_monnaie-92",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مليمًا يوجد في المجموع؟",
                "visual": "🪙🪙🪙🪙🪙🪙 + 🪙🪙",
                "choices": [
                    "7",
                    "8",
                    "9"
                ],
                "answer": "8",
                "explanation": "نعدّ كل القطع: 6 + 2 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-reconnaissance_monnaie-93",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مليمًا يوجد في المجموع؟",
                "visual": "🪙🪙🪙🪙🪙 + 🪙🪙🪙🪙",
                "choices": [
                    "8",
                    "9",
                    "10"
                ],
                "answer": "9",
                "explanation": "نعدّ كل القطع: 5 + 4 = 9 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-reconnaissance_monnaie-94",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم مليمًا يوجد في المجموع؟",
                "visual": "🪙🪙🪙 + 🪙🪙🪙",
                "choices": [
                    "5",
                    "6",
                    "7"
                ],
                "answer": "6",
                "explanation": "نعدّ كل القطع: 3 + 3 = 6 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-addition_monnaie-95",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "addition_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى كريم قطعة من 3 مليمات وقطعة من 5 مليمات.",
                "visual": "🪙×3 + 🪙×5",
                "answer": 8,
                "explanation": "نجمع القيمتين: 3 + 5 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-addition_monnaie-96",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "addition_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى كريم قطعة من 2 مليمات وقطعة من 6 مليمات.",
                "visual": "🪙×2 + 🪙×6",
                "answer": 8,
                "explanation": "نجمع القيمتين: 2 + 6 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-addition_monnaie-97",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "addition_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى كريم قطعة من 4 مليمات وقطعة من 4 مليمات.",
                "visual": "🪙×4 + 🪙×4",
                "answer": 8,
                "explanation": "نجمع القيمتين: 4 + 4 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#mesure-addition_monnaie-98",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "addition_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "لدى كريم قطعة من 1 مليمات وقطعة من 7 مليمات.",
                "visual": "🪙×1 + 🪙×7",
                "answer": 8,
                "explanation": "نجمع القيمتين: 1 + 7 = 8 مليمات."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-dizaine_unites-99",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و2 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 (2 آحاد)",
                "answer": 12,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 2 = 12."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-dizaine_unites-100",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و5 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 (5 آحاد)",
                "answer": 15,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 5 = 15."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-dizaine_unites-101",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و7 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 (7 آحاد)",
                "answer": 17,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 7 = 17."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-dizaine_unites-102",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و9 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 (9 آحاد)",
                "answer": 19,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 9 = 19."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-dizaine_unites-103",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "dizaine_unites",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ما هو العدد المكوَّن من عشرة واحدة و3 آحاد؟",
                "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 (3 آحاد)",
                "answer": 13,
                "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 3 = 13."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition_verticale-104",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "calcul",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 11 + 6",
                "answer": 17,
                "explanation": "نرتب الآحاد تحت الآحاد: 1 + 6 = 7 آحاد، والعشرة تبقى كما هي. إذن 11 + 6 = 17."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition_verticale-105",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "calcul",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 12 + 3",
                "answer": 15,
                "explanation": "نرتب الآحاد تحت الآحاد: 2 + 3 = 5 آحاد، والعشرة تبقى كما هي. إذن 12 + 3 = 15."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition_verticale-106",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "calcul",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 14 + 5",
                "answer": 19,
                "explanation": "نرتب الآحاد تحت الآحاد: 4 + 5 = 9 آحاد، والعشرة تبقى كما هي. إذن 14 + 5 = 19."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition_verticale-107",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "calcul",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 13 + 4",
                "answer": 17,
                "explanation": "نرتب الآحاد تحت الآحاد: 3 + 4 = 7 آحاد، والعشرة تبقى كما هي. إذن 13 + 4 = 17."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#calcul-addition_verticale-108",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "calcul",
            "skill_code": "addition_verticale",
            "exercise_format": "calcul",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "ضع العملية عموديًا واحسب: 15 + 3",
                "answer": 18,
                "explanation": "نرتب الآحاد تحت الآحاد: 5 + 3 = 8 آحاد، والعشرة تبقى كما هي. إذن 15 + 3 = 18."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-formes-109",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم ضلعًا للمربع؟",
                "choices": [
                    "3",
                    "4",
                    "5"
                ],
                "answer": "4",
                "explanation": "المربع له 4 أضلاع متساوية."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-formes-110",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم ضلعًا للمثلث؟",
                "choices": [
                    "2",
                    "3",
                    "4"
                ],
                "answer": "3",
                "explanation": "المثلث له 3 أضلاع."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-formes-111",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "كم ضلعًا للمستطيل؟",
                "choices": [
                    "3",
                    "4",
                    "6"
                ],
                "answer": "4",
                "explanation": "المستطيل له 4 أضلاع."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-formes-112",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "أي شكل ليس له أضلاع مستقيمة؟",
                "choices": [
                    "⬛ Carré",
                    "🔺 Triangle",
                    "⚪ Cercle"
                ],
                "answer": "⚪ Cercle",
                "explanation": "الدائرة هي الشكل الوحيد بدون أضلاع مستقيمة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-dessus_dessous-113",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "espace_geometrie",
            "skill_code": "dessus_dessous",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "أين الطائر بالنسبة للشجرة؟",
                "visual": "🐦<br>🌳",
                "choices": [
                    "الطائر فوق",
                    "الطائر تحت"
                ],
                "answer": "الطائر فوق",
                "explanation": "الطائر مرسوم فوق الشجرة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-gauche_droite-114",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "espace_geometrie",
            "skill_code": "gauche_droite",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "هل النجمة على يسار أم يمين الدائرة الحمراء؟",
                "visual": "⭐ 🔴",
                "choices": [
                    "على اليسار",
                    "على اليمين"
                ],
                "answer": "على اليسار",
                "explanation": "النجمة مرسومة قبل الدائرة الحمراء، إذن على اليسار."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-haut_bas-115",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "espace_geometrie",
            "skill_code": "haut_bas",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "هل الغيمة في أعلى أم أسفل المنزل؟",
                "visual": "☁️<br>🏠",
                "choices": [
                    "في الأعلى",
                    "في الأسفل"
                ],
                "answer": "في الأعلى",
                "explanation": "الغيمة مرسومة فوق المنزل."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#espace_geometrie-dessus_dessous-116",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "espace_geometrie",
            "skill_code": "dessus_dessous",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "هل النحلة فوق أم تحت الزهرة؟",
                "visual": "🐝<br>🌼",
                "choices": [
                    "فوق",
                    "تحت"
                ],
                "answer": "فوق",
                "explanation": "النحلة مرسومة فوق الزهرة."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-composition-117",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "composition",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "5 هو 3 زائد كم؟",
                "answer": 2,
                "explanation": "نبحث عن العدد الذي يُضاف إلى 3 ليعطي 5: 3 + 2 = 5."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-composition-118",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "composition",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "4 هو 1 زائد كم؟",
                "answer": 3,
                "explanation": "نبحث عن العدد الذي يُضاف إلى 1 ليعطي 4: 1 + 3 = 4."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-composition-119",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "composition",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "5 هو 4 زائد كم؟",
                "answer": 1,
                "explanation": "نبحث عن العدد الذي يُضاف إلى 4 ليعطي 5: 4 + 1 = 5."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-decomposition-120",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "decomposition",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "فكّك العدد 4: 4 = 1 + كم؟",
                "answer": 3,
                "explanation": "يتفكك 4 إلى 1 و3، لأن 1 + 3 = 4."
            }
        }
    },
    {
        "source": {
            "url": "local://repartition-trimestrielle-batch2.docx#numeration-decomposition-121",
            "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "decomposition",
            "exercise_format": "saisie_nombre",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "فكّك العدد 5: 5 = 2 + كم؟",
                "answer": 3,
                "explanation": "يتفكك 5 إلى 2 و3، لأن 2 + 3 = 5."
            }
        }
    }
]


def main():
    with app.app_context():
        db.create_all()

        if Exercise.query.first() is not None:
            print("Examples already seeded, skipping.")
            return

        for example in EXAMPLES:
            source = Source(**example["source"])
            db.session.add(source)
            db.session.flush()

            generation_run = GenerationRun(
                source_id=source.id,
                model_provider="anthropic",
                model_name="claude-opus-5",
                prompt_template_version="v1-seed-example",
                status="success",
                raw_model_output="(seed example, not a real model call)",
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
        print(f"Seeded {len(EXAMPLES)} example exercises.")


if __name__ == "__main__":
    main()
