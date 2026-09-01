"""Phase 1 seed: a handful of example exercises with real provenance (source ->
generation_run -> exercise), so the sync API and the Main App's pull job can be
exercised end-to-end before the real crawler/generation pipeline exists (Phase 2).

These specific rows are manually authored placeholders, not real AI-generated
content — they exist only to prove the FK chain and the export contract work.
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "content_fr": {
                "question": "Compte les pommes et écris le nombre.",
                "visual": "🍎 🍎 🍎 🍎",
                "answer": 4,
                "explanation": "Pointe chaque pomme du doigt en comptant une seule fois : 1, 2, 3, 4. Il y a bien 4 pommes en tout.",
            },
            "content_ar": {
                "question": "عدّ التفاحات واكتب العدد.",
                "visual": "🍎 🍎 🍎 🍎",
                "answer": 4,
                "explanation": "أشر إلى كل تفاحة وعدّها مرة واحدة فقط: 1، 2، 3، 4. المجموع هو 4 تفاحات.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "content_fr": {
                "question": "Combien font 3 + 2 ?",
                "choices": ["4", "5", "6"],
                "answer": "5",
                "explanation": "Pars de 3 et avance de 2 : 4, 5. Donc 3 + 2 = 5.",
            },
            "content_ar": {
                "question": "كم مجموع 3 + 2؟",
                "choices": ["4", "5", "6"],
                "answer": "5",
                "explanation": "ابدأ من 3 وتقدّم خطوتين: 4، 5. إذن 3 + 2 = 5.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "content_fr": {
                "question": "Quelle forme a 3 côtés ?",
                "choices": ["⬛ Carré", "🔺 Triangle", "⚪ Cercle"],
                "answer": "🔺 Triangle",
                "explanation": "Un triangle a exactement 3 côtés et 3 sommets. Le carré en a 4, et le cercle n'a pas de côtés droits.",
            },
            "content_ar": {
                "question": "أي شكل له 3 أضلاع؟",
                "choices": ["⬛ مربع", "🔺 مثلث", "⚪ دائرة"],
                "answer": "🔺 مثلث",
                "explanation": "المثلث له بالضبط 3 أضلاع و3 رؤوس. أما المربع فله 4 أضلاع، والدائرة ليس لها أضلاع مستقيمة.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "content_fr": {
                "question": "Quel est le plus grand nombre ?",
                "choices": ["3", "7", "5"],
                "answer": "7",
                "explanation": "Compare les nombres deux à deux : 7 est plus grand que 3 et plus grand que 5. C'est donc le plus grand des trois.",
            },
            "content_ar": {
                "question": "ما هو أكبر عدد؟",
                "choices": ["3", "7", "5"],
                "answer": "7",
                "explanation": "قارن الأعداد اثنين اثنين: 7 أكبر من 3 وأكبر من 5. إذن هو الأكبر بين الثلاثة.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "resoudre",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "content_fr": {
                "question": "Léa a 6 billes. Elle en gagne 3 de plus. Combien de billes a-t-elle maintenant ?",
                "answer": 9,
                "explanation": "Léa gagne des billes, donc on additionne : 6 + 3 = 9. Elle a maintenant 9 billes.",
            },
            "content_ar": {
                "question": "لدى ليلى 6 كرات. ربحت 3 كرات إضافية. كم كرة أصبح لديها الآن؟",
                "answer": 9,
                "explanation": "ليلى ربحت كرات، إذن نجمع: 6 + 3 = 9. أصبح لديها الآن 9 كرات.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "dessus_dessous",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "content_fr": {
                "question": "Où est le chat par rapport à la boîte ?",
                "visual": "📦<br>🐱",
                "choices": ["Le chat est dessus", "Le chat est dessous", "Le chat est à côté"],
                "answer": "Le chat est dessous",
                "explanation": "Regarde bien l'image : la boîte est dessinée en haut et le chat en dessous. Le chat est donc dessous la boîte.",
            },
            "content_ar": {
                "question": "أين يوجد القط بالنسبة للصندوق؟",
                "visual": "📦<br>🐱",
                "choices": ["القط فوق", "القط تحت", "القط بجانب"],
                "answer": "القط تحت",
                "explanation": "انظر جيدًا إلى الصورة: الصندوق مرسوم في الأعلى والقط في الأسفل. إذن القط تحت الصندوق.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "selection",
            "difficulty": "en_cours",
            "content_fr": {
                "question": "Quelle ligne est la plus longue ?",
                "visual": "Ligne A : ▬▬▬▬▬▬<br>Ligne B : ▬▬▬",
                "choices": ["Ligne A", "Ligne B"],
                "answer": "Ligne A",
                "explanation": "Observe les deux lignes : la ligne A a plus de segments que la ligne B, elle est donc plus longue.",
            },
            "content_ar": {
                "question": "أي خط أطول؟",
                "visual": "الخط أ : ▬▬▬▬▬▬<br>الخط ب : ▬▬▬",
                "choices": ["الخط أ", "الخط ب"],
                "answer": "الخط أ",
                "explanation": "لاحظ الخطين: الخط أ يحتوي على أجزاء أكثر من الخط ب، إذن هو الأطول.",
            },
        },
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
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "recit_multi_questions",
            "exercise_format": "multi_questions",
            "difficulty": "en_cours",
            "content_fr": {
                "question": "Amine a un panier de fruits : 5 pommes, 3 bananes et 2 poires.",
                "sub_questions": [
                    {
                        "question": "Combien de pommes Amine a-t-il ?",
                        "answer": 5,
                        "explanation": "Le récit dit directement qu'Amine a 5 pommes.",
                    },
                    {
                        "question": "Combien de fruits a-t-il en tout ?",
                        "answer": 10,
                        "explanation": "On additionne tous les fruits du panier : 5 + 3 + 2 = 10.",
                    },
                    {
                        "question": "A-t-il plus de pommes ou plus de bananes ?",
                        "choices": ["Plus de pommes", "Plus de bananes", "Autant des deux"],
                        "answer": "Plus de pommes",
                        "explanation": "5 pommes, c'est plus que 3 bananes. Amine a donc plus de pommes.",
                    },
                ],
            },
            "content_ar": {
                "question": "لدى أمين سلة فواكه: 5 تفاحات و3 موزات وحبتا كمثرى.",
                "sub_questions": [
                    {
                        "question": "كم عدد التفاحات التي يملكها أمين؟",
                        "answer": 5,
                        "explanation": "تذكر القصة مباشرة أن أمين لديه 5 تفاحات.",
                    },
                    {
                        "question": "كم عدد الفواكه لديه في المجموع؟",
                        "answer": 10,
                        "explanation": "نجمع كل الفواكه في السلة: 5 + 3 + 2 = 10.",
                    },
                    {
                        "question": "هل لديه تفاح أكثر أم موز أكثر؟",
                        "choices": ["تفاح أكثر", "موز أكثر", "نفس العدد"],
                        "answer": "تفاح أكثر",
                        "explanation": "5 تفاحات أكثر من 3 موزات. إذن لدى أمين تفاح أكثر.",
                    },
                ],
            },
        },
    },
]

# 10 additional récits (addition -> soustraction -> partage égal en 2), même
# structure pédagogique qu'un modèle fourni par l'utilisateur (série de
# problèmes 1ère année, programme Tunisie 2025/2026, nombres 0-19) — thèmes et
# nombres originaux, pas une copie des énoncés fournis.
RECIT_EXAMPLES = [
    {
        "theme": "poissons-aquarium",
        "trimester": "T2",
        "fr": {
            "question": "Dans l'aquarium de la classe, il y a 7 poissons rouges et 5 poissons bleus.",
            "sub_questions": [
                {
                    "question": "Combien de poissons y a-t-il en tout dans l'aquarium ?",
                    "answer": 12,
                    "explanation": "On additionne les deux groupes de poissons : 7 + 5 = 12.",
                },
                {
                    "question": "La maîtresse donne 2 poissons à une autre classe. Combien de poissons reste-t-il dans l'aquarium ?",
                    "answer": 10,
                    "explanation": "On retire les poissons donnés : 12 − 2 = 10.",
                },
                {
                    "question": "Les élèves partagent les poissons restants entre 2 aquariums, à parts égales. Combien de poissons y aura-t-il dans chaque aquarium ?",
                    "answer": 5,
                    "explanation": "On partage 10 poissons en 2 parts égales : 10 ÷ 2 = 5.",
                },
            ],
        },
        "ar": {
            "question": "في مقصورة السمك بالقسم، يوجد 7 أسماك حمراء و5 أسماك زرقاء.",
            "sub_questions": [
                {
                    "question": "كم عدد الأسماك الجملي في المقصورة؟",
                    "answer": 12,
                    "explanation": "نجمع المجموعتين: 7 + 5 = 12.",
                },
                {
                    "question": "أعطت المعلمة 2 سمكتين لقسم آخر. كم سمكة بقيت في المقصورة؟",
                    "answer": 10,
                    "explanation": "نطرح الأسماك التي أُعطيت: 12 − 2 = 10.",
                },
                {
                    "question": "قسّم التلاميذ الأسماك الباقية بالتساوي بين مقصورتين. كم سمكة ستكون في كل مقصورة؟",
                    "answer": 5,
                    "explanation": "نقسم 10 أسماك على مقصورتين بالتساوي: 10 ÷ 2 = 5.",
                },
            ],
        },
    },
    {
        "theme": "ballons-fete",
        "trimester": "T2",
        "fr": {
            "question": "Pour la fête de l'école, Yasmine gonfle 9 ballons rouges et 7 ballons jaunes.",
            "sub_questions": [
                {
                    "question": "Combien de ballons Yasmine a-t-elle gonflés en tout ?",
                    "answer": 16,
                    "explanation": "On additionne les ballons rouges et jaunes : 9 + 7 = 16.",
                },
                {
                    "question": "4 ballons éclatent avant le début de la fête. Combien de ballons reste-t-il ?",
                    "answer": 12,
                    "explanation": "On retire les ballons éclatés : 16 − 4 = 12.",
                },
                {
                    "question": "Yasmine accroche les ballons restants également des deux côtés de la porte. Combien de ballons y aura-t-il de chaque côté ?",
                    "answer": 6,
                    "explanation": "On partage 12 ballons en 2 parts égales : 12 ÷ 2 = 6.",
                },
            ],
        },
        "ar": {
            "question": "لحفل المدرسة، نفخت ياسمين 9 بالونات حمراء و7 بالونات صفراء.",
            "sub_questions": [
                {
                    "question": "كم بالونًا نفخت ياسمين في المجموع؟",
                    "answer": 16,
                    "explanation": "نجمع البالونات الحمراء والصفراء: 9 + 7 = 16.",
                },
                {
                    "question": "انفجرت 4 بالونات قبل بداية الحفل. كم بالونًا بقي؟",
                    "answer": 12,
                    "explanation": "نطرح البالونات التي انفجرت: 16 − 4 = 12.",
                },
                {
                    "question": "علّقت ياسمين البالونات الباقية بالتساوي على جانبي الباب. كم بالونًا سيكون في كل جانب؟",
                    "answer": 6,
                    "explanation": "نقسم 12 بالونًا على جانبين بالتساوي: 12 ÷ 2 = 6.",
                },
            ],
        },
    },
    {
        "theme": "biscuits-maman",
        "trimester": "T2",
        "fr": {
            "question": "Maman prépare un plateau avec 8 biscuits au chocolat et 6 biscuits à la vanille.",
            "sub_questions": [
                {
                    "question": "Combien de biscuits y a-t-il en tout sur le plateau ?",
                    "answer": 14,
                    "explanation": "On additionne les deux sortes de biscuits : 8 + 6 = 14.",
                },
                {
                    "question": "Papa mange 2 biscuits en rentrant du travail. Combien de biscuits reste-t-il ?",
                    "answer": 12,
                    "explanation": "On retire les biscuits mangés : 14 − 2 = 12.",
                },
                {
                    "question": "Les deux sœurs se partagent les biscuits restants à parts égales. Combien de biscuits chacune aura-t-elle ?",
                    "answer": 6,
                    "explanation": "On partage 12 biscuits en 2 parts égales : 12 ÷ 2 = 6.",
                },
            ],
        },
        "ar": {
            "question": "تحضّر الأم صينية فيها 8 قطع حلوى بالشوكولاطة و6 قطع بالفانيليا.",
            "sub_questions": [
                {
                    "question": "كم قطعة حلوى في الصينية إجمالًا؟",
                    "answer": 14,
                    "explanation": "نجمع النوعين: 8 + 6 = 14.",
                },
                {
                    "question": "أكل الأب قطعتين بعد رجوعه من العمل. كم قطعة بقيت؟",
                    "answer": 12,
                    "explanation": "نطرح القطع التي أُكلت: 14 − 2 = 12.",
                },
                {
                    "question": "تقاسمت الأختان القطع الباقية بالتساوي. كم قطعة ستأخذ كل واحدة؟",
                    "answer": 6,
                    "explanation": "نقسم 12 قطعة على الأختين بالتساوي: 12 ÷ 2 = 6.",
                },
            ],
        },
    },
    {
        "theme": "autocollants-nour",
        "trimester": "T2",
        "fr": {
            "question": "Nour a 9 autocollants en forme d'étoile et 5 autocollants en forme de cœur.",
            "sub_questions": [
                {
                    "question": "Combien d'autocollants Nour a-t-elle en tout ?",
                    "answer": 14,
                    "explanation": "On additionne les étoiles et les cœurs : 9 + 5 = 14.",
                },
                {
                    "question": "Nour donne 4 autocollants à sa meilleure amie. Combien lui en reste-t-il ?",
                    "answer": 10,
                    "explanation": "On retire les autocollants donnés : 14 − 4 = 10.",
                },
                {
                    "question": "Nour colle les autocollants restants à parts égales sur 2 cahiers. Combien y en aura-t-il sur chaque cahier ?",
                    "answer": 5,
                    "explanation": "On partage 10 autocollants en 2 parts égales : 10 ÷ 2 = 5.",
                },
            ],
        },
        "ar": {
            "question": "لدى نور 9 ملصقات على شكل نجمة و5 ملصقات على شكل قلب.",
            "sub_questions": [
                {
                    "question": "كم ملصقًا لدى نور في المجموع؟",
                    "answer": 14,
                    "explanation": "نجمع النجوم والقلوب: 9 + 5 = 14.",
                },
                {
                    "question": "أعطت نور 4 ملصقات لصديقتها المفضلة. كم ملصقًا بقي لديها؟",
                    "answer": 10,
                    "explanation": "نطرح الملصقات التي أُعطيت: 14 − 4 = 10.",
                },
                {
                    "question": "لصقت نور الملصقات الباقية بالتساوي على كراسين. كم ملصقًا سيكون على كل كراس؟",
                    "answer": 5,
                    "explanation": "نقسم 10 ملصقات على كراسين بالتساوي: 10 ÷ 2 = 5.",
                },
            ],
        },
    },
    {
        "theme": "coquillages-plage",
        "trimester": "T3",
        "fr": {
            "question": "À la plage, Adam ramasse 8 grands coquillages et 6 petits coquillages.",
            "sub_questions": [
                {
                    "question": "Combien de coquillages Adam a-t-il ramassés en tout ?",
                    "answer": 14,
                    "explanation": "On additionne les grands et les petits coquillages : 8 + 6 = 14.",
                },
                {
                    "question": "Adam perd 2 coquillages en courant sur le sable. Combien lui en reste-t-il ?",
                    "answer": 12,
                    "explanation": "On retire les coquillages perdus : 14 − 2 = 12.",
                },
                {
                    "question": "Adam range les coquillages restants à parts égales dans 2 petites boîtes. Combien y en aura-t-il dans chaque boîte ?",
                    "answer": 6,
                    "explanation": "On partage 12 coquillages en 2 parts égales : 12 ÷ 2 = 6.",
                },
            ],
        },
        "ar": {
            "question": "على الشاطئ، جمع آدم 8 أصداف كبيرة و6 أصداف صغيرة.",
            "sub_questions": [
                {
                    "question": "كم صدفة جمع آدم في المجموع؟",
                    "answer": 14,
                    "explanation": "نجمع الأصداف الكبيرة والصغيرة: 8 + 6 = 14.",
                },
                {
                    "question": "فقد آدم صدفتين أثناء الجري على الرمل. كم صدفة بقيت لديه؟",
                    "answer": 12,
                    "explanation": "نطرح الأصداف المفقودة: 14 − 2 = 12.",
                },
                {
                    "question": "رتّب آدم الأصداف الباقية بالتساوي في علبتين صغيرتين. كم صدفة ستكون في كل علبة؟",
                    "answer": 6,
                    "explanation": "نقسم 12 صدفة على علبتين بالتساوي: 12 ÷ 2 = 6.",
                },
            ],
        },
    },
    {
        "theme": "dattes-recolte",
        "trimester": "T3",
        "fr": {
            "question": "Pendant la récolte, Grand-père cueille 9 dattes bien mûres et Ali en cueille 7 autres.",
            "sub_questions": [
                {
                    "question": "Combien de dattes ont-ils cueillies en tout ?",
                    "answer": 16,
                    "explanation": "On additionne les deux quantités de dattes : 9 + 7 = 16.",
                },
                {
                    "question": "Ils offrent 4 dattes à leurs voisins. Combien de dattes leur reste-t-il ?",
                    "answer": 12,
                    "explanation": "On retire les dattes offertes : 16 − 4 = 12.",
                },
                {
                    "question": "Ils partagent les dattes restantes à parts égales dans 2 paniers. Combien de dattes y aura-t-il dans chaque panier ?",
                    "answer": 6,
                    "explanation": "On partage 12 dattes en 2 parts égales : 12 ÷ 2 = 6.",
                },
            ],
        },
        "ar": {
            "question": "أثناء جني التمور، قطف الجد 9 تمرات ناضجة وقطف علي 7 تمرات أخرى.",
            "sub_questions": [
                {
                    "question": "كم تمرة قطفا في المجموع؟",
                    "answer": 16,
                    "explanation": "نجمع الكميتين: 9 + 7 = 16.",
                },
                {
                    "question": "أهديا 4 تمرات لجيرانهما. كم تمرة بقيت لديهما؟",
                    "answer": 12,
                    "explanation": "نطرح التمرات المُهداة: 16 − 4 = 12.",
                },
                {
                    "question": "قسّما التمرات الباقية بالتساوي في سلّتين. كم تمرة ستكون في كل سلة؟",
                    "answer": 6,
                    "explanation": "نقسم 12 تمرة على سلتين بالتساوي: 12 ÷ 2 = 6.",
                },
            ],
        },
    },
    {
        "theme": "cubes-construction",
        "trimester": "T3",
        "fr": {
            "question": "Dans la boîte de jeux, il y a 7 cubes rouges et 7 cubes bleus.",
            "sub_questions": [
                {
                    "question": "Combien de cubes y a-t-il en tout dans la boîte ?",
                    "answer": 14,
                    "explanation": "On additionne les cubes rouges et bleus : 7 + 7 = 14.",
                },
                {
                    "question": "Le petit frère range 6 cubes ailleurs par erreur. Combien de cubes reste-t-il dans la boîte ?",
                    "answer": 8,
                    "explanation": "On retire les cubes rangés ailleurs : 14 − 6 = 8.",
                },
                {
                    "question": "Les enfants partagent les cubes restants à parts égales pour construire 2 tours. Combien de cubes chaque tour aura-t-elle ?",
                    "answer": 4,
                    "explanation": "On partage 8 cubes en 2 parts égales : 8 ÷ 2 = 4.",
                },
            ],
        },
        "ar": {
            "question": "في صندوق الألعاب، توجد 7 مكعبات حمراء و7 مكعبات زرقاء.",
            "sub_questions": [
                {
                    "question": "كم مكعبًا في الصندوق إجمالًا؟",
                    "answer": 14,
                    "explanation": "نجمع المكعبات الحمراء والزرقاء: 7 + 7 = 14.",
                },
                {
                    "question": "رتّب الأخ الصغير 6 مكعبات في مكان آخر بالخطأ. كم مكعبًا بقي في الصندوق؟",
                    "answer": 8,
                    "explanation": "نطرح المكعبات التي رُتبت في مكان آخر: 14 − 6 = 8.",
                },
                {
                    "question": "قسّم الأطفال المكعبات الباقية بالتساوي لبناء برجين. كم مكعبًا سيكون في كل برج؟",
                    "answer": 4,
                    "explanation": "نقسم 8 مكعبات على برجين بالتساوي: 8 ÷ 2 = 4.",
                },
            ],
        },
    },
    {
        "theme": "papillons-jardin",
        "trimester": "T3",
        "fr": {
            "question": "Dans le jardin, il y a 9 papillons blancs et 5 papillons orange.",
            "sub_questions": [
                {
                    "question": "Combien de papillons y a-t-il en tout dans le jardin ?",
                    "answer": 14,
                    "explanation": "On additionne les papillons blancs et orange : 9 + 5 = 14.",
                },
                {
                    "question": "2 papillons s'envolent par-dessus le mur. Combien de papillons reste-t-il dans le jardin ?",
                    "answer": 12,
                    "explanation": "On retire les papillons envolés : 14 − 2 = 12.",
                },
                {
                    "question": "Les papillons restants se posent à parts égales sur 2 rosiers. Combien de papillons y aura-t-il sur chaque rosier ?",
                    "answer": 6,
                    "explanation": "On partage 12 papillons en 2 parts égales : 12 ÷ 2 = 6.",
                },
            ],
        },
        "ar": {
            "question": "في الحديقة، توجد 9 فراشات بيضاء و5 فراشات برتقالية.",
            "sub_questions": [
                {
                    "question": "كم فراشة في الحديقة إجمالًا؟",
                    "answer": 14,
                    "explanation": "نجمع الفراشات البيضاء والبرتقالية: 9 + 5 = 14.",
                },
                {
                    "question": "طارت فراشتان فوق الجدار. كم فراشة بقيت في الحديقة؟",
                    "answer": 12,
                    "explanation": "نطرح الفراشات التي طارت: 14 − 2 = 12.",
                },
                {
                    "question": "استقرت الفراشات الباقية بالتساوي على شجيرتي ورد. كم فراشة ستكون على كل شجيرة؟",
                    "answer": 6,
                    "explanation": "نقسم 12 فراشة على شجيرتين بالتساوي: 12 ÷ 2 = 6.",
                },
            ],
        },
    },
    {
        "theme": "fraises-jardin",
        "trimester": "T2",
        "fr": {
            "question": "Dans le jardin, Sara cueille 8 fraises et sa maman en cueille 4 autres.",
            "sub_questions": [
                {
                    "question": "Combien de fraises ont-elles cueillies en tout ?",
                    "answer": 12,
                    "explanation": "On additionne les deux quantités de fraises : 8 + 4 = 12.",
                },
                {
                    "question": "Elles mangent 4 fraises tout de suite. Combien de fraises leur reste-t-il ?",
                    "answer": 8,
                    "explanation": "On retire les fraises mangées : 12 − 4 = 8.",
                },
                {
                    "question": "Elles partagent les fraises restantes à parts égales dans 2 petits paniers. Combien de fraises y aura-t-il dans chaque panier ?",
                    "answer": 4,
                    "explanation": "On partage 8 fraises en 2 parts égales : 8 ÷ 2 = 4.",
                },
            ],
        },
        "ar": {
            "question": "في الحديقة، قطفت سارة 8 حبات فراولة وقطفت أمها 4 حبات أخرى.",
            "sub_questions": [
                {
                    "question": "كم حبة فراولة قطفتا في المجموع؟",
                    "answer": 12,
                    "explanation": "نجمع الكميتين: 8 + 4 = 12.",
                },
                {
                    "question": "أكلتا 4 حبات على الفور. كم حبة بقيت لديهما؟",
                    "answer": 8,
                    "explanation": "نطرح الحبات التي أُكلت: 12 − 4 = 8.",
                },
                {
                    "question": "قسّمتا الحبات الباقية بالتساوي في سلتين صغيرتين. كم حبة ستكون في كل سلة؟",
                    "answer": 4,
                    "explanation": "نقسم 8 حبات على سلتين بالتساوي: 8 ÷ 2 = 4.",
                },
            ],
        },
    },
    {
        "theme": "bougies-gateau",
        "trimester": "T3",
        "fr": {
            "question": "Pour l'anniversaire, Maman achète 9 bougies rouges et 9 bougies dorées.",
            "sub_questions": [
                {
                    "question": "Combien de bougies Maman a-t-elle achetées en tout ?",
                    "answer": 18,
                    "explanation": "On additionne les bougies rouges et dorées : 9 + 9 = 18.",
                },
                {
                    "question": "4 bougies tombent et se cassent avant la fête. Combien de bougies utilisables reste-t-il ?",
                    "answer": 14,
                    "explanation": "On retire les bougies cassées : 18 − 4 = 14.",
                },
                {
                    "question": "Maman met les bougies restantes à parts égales sur 2 gâteaux. Combien de bougies y aura-t-il sur chaque gâteau ?",
                    "answer": 7,
                    "explanation": "On partage 14 bougies en 2 parts égales : 14 ÷ 2 = 7.",
                },
            ],
        },
        "ar": {
            "question": "لعيد الميلاد، اشترت الأم 9 شموع حمراء و9 شموع ذهبية.",
            "sub_questions": [
                {
                    "question": "كم شمعة اشترت الأم في المجموع؟",
                    "answer": 18,
                    "explanation": "نجمع الشموع الحمراء والذهبية: 9 + 9 = 18.",
                },
                {
                    "question": "سقطت 4 شموع وانكسرت قبل الحفل. كم شمعة صالحة بقيت؟",
                    "answer": 14,
                    "explanation": "نطرح الشموع المكسورة: 18 − 4 = 14.",
                },
                {
                    "question": "وضعت الأم الشموع الباقية بالتساوي على كعكتين. كم شمعة ستكون على كل كعكة؟",
                    "answer": 7,
                    "explanation": "نقسم 14 شمعة على كعكتين بالتساوي: 14 ÷ 2 = 7.",
                },
            ],
        },
    },
]

for _item in RECIT_EXAMPLES:
    EXAMPLES.append(
        {
            "source": {
                "url": f"local://exercices_math_1ere_annee_tunisie.docx#{_item['theme']}",
                "title": "Série de récits mathématiques 1ère année (fournie par l'utilisateur, programme Tunisie 2025/2026)",
                "license_status": "unlicensed",
                "subject_code": "math",
                "level_code": "1",
                "domain_hint": "problemes",
                "trimester_hint": _item["trimester"],
                "region_scope": "tunisia_web",
                "content_snapshot": (
                    "Modèle fourni par l'utilisateur : récit + addition + soustraction + partage égal en 2, "
                    "nombres 0-19, servant uniquement d'inspiration de structure pour ce nouvel exercice."
                ),
                "status": "used_for_generation",
            },
            "exercise": {
                "subject_code": "math",
                "level_code": "1",
                "trimester": _item["trimester"],
                "domain_code": "problemes",
                "skill_code": "recit_multi_questions",
                "exercise_format": "multi_questions",
                "difficulty": "maitrise",
                "content_fr": _item["fr"],
                "content_ar": _item["ar"],
            },
        }
    )

# 4 examples covering the curriculum gap found via the user-supplied trimester
# breakdown docx: Tunisian money (monnaie, T2) and the tens/units concept +
# vertical addition (dizaine, T3) — neither existed in math1_curriculum.json
# before this pass.
CURRICULUM_GAP_EXAMPLES = [
    {
        "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#monnaie-reconnaissance",
        "domain_hint": "mesure",
        "trimester": "T2",
        "domain_code": "mesure",
        "skill_code": "reconnaissance_monnaie",
        "exercise_format": "selection",
        "difficulty": "en_cours",
        "content_fr": {
            "question": "Combien de millimes y a-t-il en tout dans la main de Yassine ?",
            "visual": "🪙🪙🪙🪙🪙 + 🪙🪙",
            "choices": ["6", "7", "8"],
            "answer": "7",
            "explanation": "On compte toutes les pièces : 5 pièces + 2 pièces = 7 millimes.",
        },
        "content_ar": {
            "question": "كم مليمًا يوجد في يد ياسين إجمالًا؟",
            "visual": "🪙🪙🪙🪙🪙 + 🪙🪙",
            "choices": ["6", "7", "8"],
            "answer": "7",
            "explanation": "نعدّ كل القطع: 5 قطع + قطعتان = 7 مليمات.",
        },
    },
    {
        "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#monnaie-addition",
        "domain_hint": "mesure",
        "trimester": "T2",
        "domain_code": "mesure",
        "skill_code": "addition_monnaie",
        "exercise_format": "saisie_nombre",
        "difficulty": "en_cours",
        "content_fr": {
            "question": "Amal a une pièce de 5 millimes et une pièce de 3 millimes dans sa poche.",
            "visual": "🪙×5 + 🪙×3",
            "answer": 8,
            "explanation": "On additionne les deux valeurs : 5 + 3 = 8 millimes.",
        },
        "content_ar": {
            "question": "لدى أمل قطعة من 5 مليمات وقطعة من 3 مليمات في جيبها.",
            "visual": "🪙×5 + 🪙×3",
            "answer": 8,
            "explanation": "نجمع القيمتين: 5 + 3 = 8 مليمات.",
        },
    },
    {
        "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#dizaine-unites",
        "domain_hint": "numeration",
        "trimester": "T3",
        "domain_code": "numeration",
        "skill_code": "dizaine_unites",
        "exercise_format": "saisie_nombre",
        "difficulty": "maitrise",
        "content_fr": {
            "question": "Quel nombre forment 1 dizaine et 4 unités ?",
            "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 🔵 🔵 (4 unités)",
            "answer": 14,
            "explanation": "1 dizaine vaut 10. On ajoute les 4 unités : 10 + 4 = 14.",
        },
        "content_ar": {
            "question": "ما هو العدد المكوَّن من عشرة واحدة و4 آحاد؟",
            "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 (4 آحاد)",
            "answer": 14,
            "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد الأربعة: 10 + 4 = 14.",
        },
    },
    {
        "url": "local://je-vais-te-communiquer-la-repartition-du-programme-tunisien.docx#addition-verticale",
        "domain_hint": "calcul",
        "trimester": "T3",
        "domain_code": "calcul",
        "skill_code": "addition_verticale",
        "exercise_format": "saisie_nombre",
        "difficulty": "maitrise",
        "content_fr": {
            "question": "Pose et calcule : 13 + 6",
            "answer": 19,
            "explanation": "On aligne unités sous unités et dizaines sous dizaines : 3 + 6 = 9 unités, 1 dizaine ne change pas. Donc 13 + 6 = 19.",
        },
        "content_ar": {
            "question": "ضع العملية عموديًا واحسب: 13 + 6",
            "answer": 19,
            "explanation": "نرتب الآحاد تحت الآحاد والعشرات تحت العشرات: 3 + 6 = 9 آحاد، والعشرة الواحدة تبقى كما هي. إذن 13 + 6 = 19.",
        },
    },
]

for _gap in CURRICULUM_GAP_EXAMPLES:
    EXAMPLES.append(
        {
            "source": {
                "url": _gap["url"],
                "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
                "license_status": "unlicensed",
                "subject_code": "math",
                "level_code": "1",
                "domain_hint": _gap["domain_hint"],
                "trimester_hint": _gap["trimester"],
                "region_scope": "tunisia_web",
                "content_snapshot": (
                    "Répartition trimestrielle fournie par l'utilisateur (programme Tunisie 2025/2026) : "
                    "sert uniquement à confirmer quels sujets couvrir, pas comme contenu recopié."
                ),
                "status": "used_for_generation",
            },
            "exercise": {
                "subject_code": "math",
                "level_code": "1",
                "trimester": _gap["trimester"],
                "domain_code": _gap["domain_code"],
                "skill_code": _gap["skill_code"],
                "exercise_format": _gap["exercise_format"],
                "difficulty": _gap["difficulty"],
                "content_fr": _gap["content_fr"],
                "content_ar": _gap["content_ar"],
            },
        }
    )


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
