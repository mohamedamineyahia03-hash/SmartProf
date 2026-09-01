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


# 50 more récits (batch 2, same structure: addition -> soustraction -> partage
# égal en 2), 50 new themes, per user request for 50 more of this model.
RECIT_EXAMPLES_BATCH2 = [
  {
    "theme": "chatons-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Yassine a 7 chatons blancs et 5 chatons noirs.",
      "sub_questions": [
        {
          "question": "Combien de chatons y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 7 + 5 = 12."
        },
        {
          "question": "Yassine donne 2 chatons à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les chatons donnés : 12 − 2 = 10."
        },
        {
          "question": "Yassine partage les chatons restants à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 chatons en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "poussins-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Meriem a 9 poussins jaunes et 7 poussins marron.",
      "sub_questions": [
        {
          "question": "Combien de poussins y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 9 + 7 = 16."
        },
        {
          "question": "Meriem donne 4 poussins à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les poussins donnés : 16 − 4 = 12."
        },
        {
          "question": "Meriem partage les poussins restants à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 6,
          "explanation": "On partage 12 poussins en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "canards-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Lina a 8 canetons blancs et 6 canetons jaunes.",
      "sub_questions": [
        {
          "question": "Combien de canetons y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 8 + 6 = 14."
        },
        {
          "question": "Lina donne 2 canetons à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les canetons donnés : 14 − 2 = 12."
        },
        {
          "question": "Lina partage les canetons restants à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 canetons en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "escargots-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Sami a 9 escargots grands et 5 escargots petits.",
      "sub_questions": [
        {
          "question": "Combien de escargots y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 9 + 5 = 14."
        },
        {
          "question": "Sami donne 4 escargots à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les escargots donnés : 14 − 4 = 10."
        },
        {
          "question": "Sami partage les escargots restants à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 escargots en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "coccinelles-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Amine a 7 coccinelles rouges et 7 coccinelles jaunes.",
      "sub_questions": [
        {
          "question": "Combien de coccinelles y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 7 + 7 = 14."
        },
        {
          "question": "Amine donne 6 coccinelles à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les coccinelles données : 14 − 6 = 8."
        },
        {
          "question": "Amine partage les coccinelles restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 4,
          "explanation": "On partage 8 coccinelles en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "abeilles-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Ahmed a 8 abeilles grandes et 4 abeilles petites.",
      "sub_questions": [
        {
          "question": "Combien de abeilles y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 8 + 4 = 12."
        },
        {
          "question": "Ahmed donne 4 abeilles à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les abeilles données : 12 − 4 = 8."
        },
        {
          "question": "Ahmed partage les abeilles restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 4,
          "explanation": "On partage 8 abeilles en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "tortues-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Ali a 9 tortues grandes et 9 tortues petites.",
      "sub_questions": [
        {
          "question": "Combien de tortues y a-t-il en tout ?",
          "answer": 18,
          "explanation": "On additionne les deux groupes : 9 + 9 = 18."
        },
        {
          "question": "Ali donne 4 tortues à un ami. Combien lui en reste-t-il ?",
          "answer": 14,
          "explanation": "On retire les tortues données : 18 − 4 = 14."
        },
        {
          "question": "Ali partage les tortues restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 7,
          "explanation": "On partage 14 tortues en 2 parts égales : 14 ÷ 2 = 7."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "grenouilles-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Aya a 6 grenouilles vertes et 8 grenouilles marron.",
      "sub_questions": [
        {
          "question": "Combien de grenouilles y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 6 + 8 = 14."
        },
        {
          "question": "Aya donne 2 grenouilles à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les grenouilles données : 14 − 2 = 12."
        },
        {
          "question": "Aya partage les grenouilles restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 grenouilles en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "herissons-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sara a 5 hérissons grands et 7 hérissons petits.",
      "sub_questions": [
        {
          "question": "Combien de hérissons y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 5 + 7 = 12."
        },
        {
          "question": "Sara donne 2 hérissons à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les hérissons donnés : 12 − 2 = 10."
        },
        {
          "question": "Sara partage les hérissons restants à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 hérissons en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "ecureuils-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Yassine a 9 écureuils rouges et 4 écureuils gris.",
      "sub_questions": [
        {
          "question": "Combien de écureuils y a-t-il en tout ?",
          "answer": 13,
          "explanation": "On additionne les deux groupes : 9 + 4 = 13."
        },
        {
          "question": "Yassine donne 3 écureuils à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les écureuils donnés : 13 − 3 = 10."
        },
        {
          "question": "Yassine partage les écureuils restants à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 5,
          "explanation": "On partage 10 écureuils en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "bananes-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Meriem a 6 bananes jaunes et 6 bananes vertes.",
      "sub_questions": [
        {
          "question": "Combien de bananes y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 6 + 6 = 12."
        },
        {
          "question": "Meriem donne 2 bananes à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les bananes données : 12 − 2 = 10."
        },
        {
          "question": "Meriem partage les bananes restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 bananes en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "poires-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Lina a 7 poires jaunes et 9 poires vertes.",
      "sub_questions": [
        {
          "question": "Combien de poires y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 7 + 9 = 16."
        },
        {
          "question": "Lina donne 6 poires à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les poires données : 16 − 6 = 10."
        },
        {
          "question": "Lina partage les poires restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 5,
          "explanation": "On partage 10 poires en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "cerises-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sami a 5 cerises rouges et 9 cerises jaunes.",
      "sub_questions": [
        {
          "question": "Combien de cerises y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 5 + 9 = 14."
        },
        {
          "question": "Sami donne 4 cerises à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les cerises données : 14 − 4 = 10."
        },
        {
          "question": "Sami partage les cerises restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 5,
          "explanation": "On partage 10 cerises en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "tomates-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Amine a 4 tomates grandes et 8 tomates petites.",
      "sub_questions": [
        {
          "question": "Combien de tomates y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 4 + 8 = 12."
        },
        {
          "question": "Amine donne 4 tomates à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les tomates données : 12 − 4 = 8."
        },
        {
          "question": "Amine partage les tomates restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 4,
          "explanation": "On partage 8 tomates en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "carottes-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Ahmed a 9 carottes grandes et 6 carottes petites.",
      "sub_questions": [
        {
          "question": "Combien de carottes y a-t-il en tout ?",
          "answer": 15,
          "explanation": "On additionne les deux groupes : 9 + 6 = 15."
        },
        {
          "question": "Ahmed donne 3 carottes à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les carottes données : 15 − 3 = 12."
        },
        {
          "question": "Ahmed partage les carottes restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 6,
          "explanation": "On partage 12 carottes en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "olives-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Ali a 7 olives noires et 5 olives vertes.",
      "sub_questions": [
        {
          "question": "Combien de olives y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 7 + 5 = 12."
        },
        {
          "question": "Ali donne 2 olives à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les olives données : 12 − 2 = 10."
        },
        {
          "question": "Ali partage les olives restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 olives en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "figues-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Aya a 9 figues vertes et 7 figues violettes.",
      "sub_questions": [
        {
          "question": "Combien de figues y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 9 + 7 = 16."
        },
        {
          "question": "Aya donne 4 figues à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les figues données : 16 − 4 = 12."
        },
        {
          "question": "Aya partage les figues restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 6,
          "explanation": "On partage 12 figues en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "gommes-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Sara a 8 gommes bleues et 6 gommes rouges.",
      "sub_questions": [
        {
          "question": "Combien de gommes y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 8 + 6 = 14."
        },
        {
          "question": "Sara donne 2 gommes à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les gommes données : 14 − 2 = 12."
        },
        {
          "question": "Sara partage les gommes restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 gommes en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "regles-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Yassine a 9 règles longues et 5 règles courtes.",
      "sub_questions": [
        {
          "question": "Combien de règles y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 9 + 5 = 14."
        },
        {
          "question": "Yassine donne 4 règles à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les règles données : 14 − 4 = 10."
        },
        {
          "question": "Yassine partage les règles restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 règles en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "feutres-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Meriem a 7 feutres bleus et 7 feutres rouges.",
      "sub_questions": [
        {
          "question": "Combien de feutres y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 7 + 7 = 14."
        },
        {
          "question": "Meriem donne 6 feutres à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les feutres donnés : 14 − 6 = 8."
        },
        {
          "question": "Meriem partage les feutres restants à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 4,
          "explanation": "On partage 8 feutres en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "taille_crayons-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Lina a 8 taille-crayons jaunes et 4 taille-crayons verts.",
      "sub_questions": [
        {
          "question": "Combien de taille-crayons y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 8 + 4 = 12."
        },
        {
          "question": "Lina donne 4 taille-crayons à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les taille-crayons donnés : 12 − 4 = 8."
        },
        {
          "question": "Lina partage les taille-crayons restants à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 4,
          "explanation": "On partage 8 taille-crayons en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "poupees-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Sami a 9 poupées grandes et 9 poupées petites.",
      "sub_questions": [
        {
          "question": "Combien de poupées y a-t-il en tout ?",
          "answer": 18,
          "explanation": "On additionne les deux groupes : 9 + 9 = 18."
        },
        {
          "question": "Sami donne 4 poupées à un ami. Combien lui en reste-t-il ?",
          "answer": 14,
          "explanation": "On retire les poupées données : 18 − 4 = 14."
        },
        {
          "question": "Sami partage les poupées restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 7,
          "explanation": "On partage 14 poupées en 2 parts égales : 14 ÷ 2 = 7."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "cerfs_volants-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Amine a 6 cerfs-volants rouges et 8 cerfs-volants bleus.",
      "sub_questions": [
        {
          "question": "Combien de cerfs-volants y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 6 + 8 = 14."
        },
        {
          "question": "Amine donne 2 cerfs-volants à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les cerfs-volants donnés : 14 − 2 = 12."
        },
        {
          "question": "Amine partage les cerfs-volants restants à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 cerfs-volants en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "toupies-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Ahmed a 5 toupies rouges et 7 toupies jaunes.",
      "sub_questions": [
        {
          "question": "Combien de toupies y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 5 + 7 = 12."
        },
        {
          "question": "Ahmed donne 2 toupies à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les toupies données : 12 − 2 = 10."
        },
        {
          "question": "Ahmed partage les toupies restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 toupies en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "pieces_puzzle-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Ali a 9 pièces de puzzle bleues et 4 pièces de puzzle jaunes.",
      "sub_questions": [
        {
          "question": "Combien de pièces de puzzle y a-t-il en tout ?",
          "answer": 13,
          "explanation": "On additionne les deux groupes : 9 + 4 = 13."
        },
        {
          "question": "Ali donne 3 pièces de puzzle à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les pièces de puzzle données : 13 − 3 = 10."
        },
        {
          "question": "Ali partage les pièces de puzzle restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 5,
          "explanation": "On partage 10 pièces de puzzle en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "figurines-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Aya a 6 figurines rouges et 6 figurines bleues.",
      "sub_questions": [
        {
          "question": "Combien de figurines y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 6 + 6 = 12."
        },
        {
          "question": "Aya donne 2 figurines à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les figurines données : 12 − 2 = 10."
        },
        {
          "question": "Aya partage les figurines restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 figurines en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "cailloux-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sara a 7 cailloux blancs et 9 cailloux gris.",
      "sub_questions": [
        {
          "question": "Combien de cailloux y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 7 + 9 = 16."
        },
        {
          "question": "Sara donne 6 cailloux à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les cailloux donnés : 16 − 6 = 10."
        },
        {
          "question": "Sara partage les cailloux restants à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 5,
          "explanation": "On partage 10 cailloux en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "glands-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Yassine a 5 glands grands et 9 glands petits.",
      "sub_questions": [
        {
          "question": "Combien de glands y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 5 + 9 = 14."
        },
        {
          "question": "Yassine donne 4 glands à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les glands donnés : 14 − 4 = 10."
        },
        {
          "question": "Yassine partage les glands restants à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 5,
          "explanation": "On partage 10 glands en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "pommes_pin-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Meriem a 4 pommes de pin grandes et 8 pommes de pin petites.",
      "sub_questions": [
        {
          "question": "Combien de pommes de pin y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 4 + 8 = 12."
        },
        {
          "question": "Meriem donne 4 pommes de pin à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les pommes de pin données : 12 − 4 = 8."
        },
        {
          "question": "Meriem partage les pommes de pin restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 4,
          "explanation": "On partage 8 pommes de pin en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "feuilles_automne-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Lina a 9 feuilles jaunes et 6 feuilles orange.",
      "sub_questions": [
        {
          "question": "Combien de feuilles y a-t-il en tout ?",
          "answer": 15,
          "explanation": "On additionne les deux groupes : 9 + 6 = 15."
        },
        {
          "question": "Lina donne 3 feuilles à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les feuilles données : 15 − 3 = 12."
        },
        {
          "question": "Lina partage les feuilles restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 6,
          "explanation": "On partage 12 feuilles en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "gateaux-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sami a 7 petits gâteaux au chocolat et 5 petits gâteaux à la vanille.",
      "sub_questions": [
        {
          "question": "Combien de petits gâteaux y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 7 + 5 = 12."
        },
        {
          "question": "Sami donne 2 petits gâteaux à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les petits gâteaux donnés : 12 − 2 = 10."
        },
        {
          "question": "Sami partage les petits gâteaux restants à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 petits gâteaux en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "madeleines-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Amine a 9 madeleines au miel et 7 madeleines au citron.",
      "sub_questions": [
        {
          "question": "Combien de madeleines y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 9 + 7 = 16."
        },
        {
          "question": "Amine donne 4 madeleines à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les madeleines données : 16 − 4 = 12."
        },
        {
          "question": "Amine partage les madeleines restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 6,
          "explanation": "On partage 12 madeleines en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "crepes-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Ahmed a 8 crêpes au miel et 6 crêpes à la confiture.",
      "sub_questions": [
        {
          "question": "Combien de crêpes y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 8 + 6 = 14."
        },
        {
          "question": "Ahmed donne 2 crêpes à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les crêpes données : 14 − 2 = 12."
        },
        {
          "question": "Ahmed partage les crêpes restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 crêpes en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "perles-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Ali a 9 perles bleues et 5 perles rouges.",
      "sub_questions": [
        {
          "question": "Combien de perles y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 9 + 5 = 14."
        },
        {
          "question": "Ali donne 4 perles à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les perles données : 14 − 4 = 10."
        },
        {
          "question": "Ali partage les perles restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 perles en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "rubans-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Aya a 7 rubans jaunes et 7 rubans roses.",
      "sub_questions": [
        {
          "question": "Combien de rubans y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 7 + 7 = 14."
        },
        {
          "question": "Aya donne 6 rubans à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les rubans donnés : 14 − 6 = 8."
        },
        {
          "question": "Aya partage les rubans restants à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 4,
          "explanation": "On partage 8 rubans en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "chaussettes-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Sara a 8 chaussettes bleues et 4 chaussettes blanches.",
      "sub_questions": [
        {
          "question": "Combien de chaussettes y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 8 + 4 = 12."
        },
        {
          "question": "Sara donne 4 chaussettes à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les chaussettes données : 12 − 4 = 8."
        },
        {
          "question": "Sara partage les chaussettes restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 4,
          "explanation": "On partage 8 chaussettes en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "gants-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Yassine a 9 gants rouges et 9 gants bleus.",
      "sub_questions": [
        {
          "question": "Combien de gants y a-t-il en tout ?",
          "answer": 18,
          "explanation": "On additionne les deux groupes : 9 + 9 = 18."
        },
        {
          "question": "Yassine donne 4 gants à un ami. Combien lui en reste-t-il ?",
          "answer": 14,
          "explanation": "On retire les gants donnés : 18 − 4 = 14."
        },
        {
          "question": "Yassine partage les gants restants à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 7,
          "explanation": "On partage 14 gants en 2 parts égales : 14 ÷ 2 = 7."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "seaux_plage-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Meriem a 6 seaux de plage jaunes et 8 seaux de plage rouges.",
      "sub_questions": [
        {
          "question": "Combien de seaux de plage y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 6 + 8 = 14."
        },
        {
          "question": "Meriem donne 2 seaux de plage à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les seaux de plage donnés : 14 − 2 = 12."
        },
        {
          "question": "Meriem partage les seaux de plage restants à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 seaux de plage en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "etoiles_mer-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Lina a 5 étoiles de mer orange et 7 étoiles de mer rouges.",
      "sub_questions": [
        {
          "question": "Combien de étoiles de mer y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 5 + 7 = 12."
        },
        {
          "question": "Lina donne 2 étoiles de mer à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les étoiles de mer données : 12 − 2 = 10."
        },
        {
          "question": "Lina partage les étoiles de mer restantes à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 étoiles de mer en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "crabes-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Sami a 9 crabes rouges et 4 crabes orange.",
      "sub_questions": [
        {
          "question": "Combien de crabes y a-t-il en tout ?",
          "answer": 13,
          "explanation": "On additionne les deux groupes : 9 + 4 = 13."
        },
        {
          "question": "Sami donne 3 crabes à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les crabes donnés : 13 − 3 = 10."
        },
        {
          "question": "Sami partage les crabes restants à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 5,
          "explanation": "On partage 10 crabes en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "libellules-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Amine a 6 libellules bleues et 6 libellules vertes.",
      "sub_questions": [
        {
          "question": "Combien de libellules y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 6 + 6 = 12."
        },
        {
          "question": "Amine donne 2 libellules à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les libellules données : 12 − 2 = 10."
        },
        {
          "question": "Amine partage les libellules restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 libellules en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "fourmis-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Ahmed a 7 fourmis noires et 9 fourmis rouges.",
      "sub_questions": [
        {
          "question": "Combien de fourmis y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 7 + 9 = 16."
        },
        {
          "question": "Ahmed donne 6 fourmis à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les fourmis données : 16 − 6 = 10."
        },
        {
          "question": "Ahmed partage les fourmis restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 5,
          "explanation": "On partage 10 fourmis en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "sauterelles-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Ali a 5 sauterelles vertes et 9 sauterelles marron.",
      "sub_questions": [
        {
          "question": "Combien de sauterelles y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 5 + 9 = 14."
        },
        {
          "question": "Ali donne 4 sauterelles à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les sauterelles données : 14 − 4 = 10."
        },
        {
          "question": "Ali partage les sauterelles restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 5,
          "explanation": "On partage 10 sauterelles en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "champignons-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Aya a 4 champignons blancs et 8 champignons marron.",
      "sub_questions": [
        {
          "question": "Combien de champignons y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 4 + 8 = 12."
        },
        {
          "question": "Aya donne 4 champignons à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les champignons donnés : 12 − 4 = 8."
        },
        {
          "question": "Aya partage les champignons restants à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 4,
          "explanation": "On partage 8 champignons en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "noix-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sara a 9 noix grandes et 6 noix petites.",
      "sub_questions": [
        {
          "question": "Combien de noix y a-t-il en tout ?",
          "answer": 15,
          "explanation": "On additionne les deux groupes : 9 + 6 = 15."
        },
        {
          "question": "Sara donne 3 noix à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les noix données : 15 − 3 = 12."
        },
        {
          "question": "Sara partage les noix restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 6,
          "explanation": "On partage 12 noix en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "amandes-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Yassine a 7 amandes grandes et 5 amandes petites.",
      "sub_questions": [
        {
          "question": "Combien de amandes y a-t-il en tout ?",
          "answer": 12,
          "explanation": "On additionne les deux groupes : 7 + 5 = 12."
        },
        {
          "question": "Yassine donne 2 amandes à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les amandes données : 12 − 2 = 10."
        },
        {
          "question": "Yassine partage les amandes restantes à parts égales entre 2 boîtes. Combien y en aura-t-il pour chaque boîte ?",
          "answer": 5,
          "explanation": "On partage 10 amandes en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "pistaches-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Meriem a 9 pistaches grandes et 7 pistaches petites.",
      "sub_questions": [
        {
          "question": "Combien de pistaches y a-t-il en tout ?",
          "answer": 16,
          "explanation": "On additionne les deux groupes : 9 + 7 = 16."
        },
        {
          "question": "Meriem donne 4 pistaches à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les pistaches données : 16 − 4 = 12."
        },
        {
          "question": "Meriem partage les pistaches restantes à parts égales entre 2 paniers. Combien y en aura-t-il pour chaque panier ?",
          "answer": 6,
          "explanation": "On partage 12 pistaches en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "craies-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Lina a 8 craies blanches et 6 craies de couleur.",
      "sub_questions": [
        {
          "question": "Combien de craies y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 8 + 6 = 14."
        },
        {
          "question": "Lina donne 2 craies à un ami. Combien lui en reste-t-il ?",
          "answer": 12,
          "explanation": "On retire les craies données : 14 − 2 = 12."
        },
        {
          "question": "Lina partage les craies restantes à parts égales entre 2 sacs. Combien y en aura-t-il pour chaque sac ?",
          "answer": 6,
          "explanation": "On partage 12 craies en 2 parts égales : 12 ÷ 2 = 6."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "badges-batch2",
    "trimester": "T2",
    "fr": {
      "question": "Sami a 9 badges bleus et 5 badges rouges.",
      "sub_questions": [
        {
          "question": "Combien de badges y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 9 + 5 = 14."
        },
        {
          "question": "Sami donne 4 badges à un ami. Combien lui en reste-t-il ?",
          "answer": 10,
          "explanation": "On retire les badges donnés : 14 − 4 = 10."
        },
        {
          "question": "Sami partage les badges restants à parts égales entre 2 amis. Combien y en aura-t-il pour chaque ami ?",
          "answer": 5,
          "explanation": "On partage 10 badges en 2 parts égales : 10 ÷ 2 = 5."
        }
      ]
    },
    "ar": {
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
  },
  {
    "theme": "barrettes-batch2",
    "trimester": "T3",
    "fr": {
      "question": "Amine a 7 barrettes roses et 7 barrettes jaunes.",
      "sub_questions": [
        {
          "question": "Combien de barrettes y a-t-il en tout ?",
          "answer": 14,
          "explanation": "On additionne les deux groupes : 7 + 7 = 14."
        },
        {
          "question": "Amine donne 6 barrettes à un ami. Combien lui en reste-t-il ?",
          "answer": 8,
          "explanation": "On retire les barrettes données : 14 − 6 = 8."
        },
        {
          "question": "Amine partage les barrettes restantes à parts égales entre 2 groupes. Combien y en aura-t-il pour chaque groupe ?",
          "answer": 4,
          "explanation": "On partage 8 barrettes en 2 parts égales : 8 ÷ 2 = 4."
        }
      ]
    },
    "ar": {
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
]

for _item in RECIT_EXAMPLES_BATCH2:
    EXAMPLES.append(
        {
            "source": {
                "url": f"local://recit-generique.docx#{_item['theme']}",
                "title": "Modèle de récit mathématique 1ère année (généré, même structure que le fichier fourni par l'utilisateur)",
                "license_status": "unlicensed",
                "subject_code": "math",
                "level_code": "1",
                "domain_hint": "problemes",
                "trimester_hint": _item["trimester"],
                "region_scope": "tunisia_web",
                "content_snapshot": "Généré à partir du modèle de récit validé (addition, soustraction, partage égal en 2), pas une copie.",
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

# 50 individual exercises across T1/T2/T3, distributed over the curriculum
# skills matching the official trimester breakdown (nombres 1-5 / 6-9+monnaie /
# 10-19+géométrie) — per user request for 50 more of this model.
INDIVIDUAL_BATCH2 = [
  {
    "domain": "numeration",
    "skill": "denombrement",
    "format": "comptage",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "Combien de étoiles vois-tu ?",
      "visual": "⭐⭐⭐",
      "answer": 3,
      "explanation": "On compte un par un : il y en a 3."
    },
    "ar": {
      "question": "كم عدد نجوم التي تراها؟",
      "visual": "⭐⭐⭐",
      "answer": 3,
      "explanation": "نعدّ واحدًا واحدًا: يوجد 3."
    }
  },
  {
    "domain": "numeration",
    "skill": "denombrement",
    "format": "comptage",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de ballons vois-tu ?",
      "visual": "🎈🎈🎈🎈🎈",
      "answer": 5,
      "explanation": "On compte un par un : il y en a 5."
    },
    "ar": {
      "question": "كم عدد بالونات التي تراها؟",
      "visual": "🎈🎈🎈🎈🎈",
      "answer": 5,
      "explanation": "نعدّ واحدًا واحدًا: يوجد 5."
    }
  },
  {
    "domain": "numeration",
    "skill": "denombrement",
    "format": "comptage",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de poissons vois-tu ?",
      "visual": "🐟🐟🐟🐟🐟🐟🐟",
      "answer": 7,
      "explanation": "On compte un par un : il y en a 7."
    },
    "ar": {
      "question": "كم عدد أسماك التي تراها؟",
      "visual": "🐟🐟🐟🐟🐟🐟🐟",
      "answer": 7,
      "explanation": "نعدّ واحدًا واحدًا: يوجد 7."
    }
  },
  {
    "domain": "numeration",
    "skill": "denombrement",
    "format": "comptage",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de fleurs vois-tu ?",
      "visual": "🌸🌸🌸🌸🌸🌸🌸🌸",
      "answer": 8,
      "explanation": "On compte un par un : il y en a 8."
    },
    "ar": {
      "question": "كم عدد أزهار التي تراها؟",
      "visual": "🌸🌸🌸🌸🌸🌸🌸🌸",
      "answer": 8,
      "explanation": "نعدّ واحدًا واحدًا: يوجد 8."
    }
  },
  {
    "domain": "numeration",
    "skill": "denombrement",
    "format": "comptage",
    "trimester": "T2",
    "difficulty": "maitrise",
    "fr": {
      "question": "Combien de bonbons vois-tu ?",
      "visual": "🍬🍬🍬🍬🍬🍬🍬🍬🍬",
      "answer": 9,
      "explanation": "On compte un par un : il y en a 9."
    },
    "ar": {
      "question": "كم عدد حلوى التي تراها؟",
      "visual": "🍬🍬🍬🍬🍬🍬🍬🍬🍬",
      "answer": 9,
      "explanation": "نعدّ واحدًا واحدًا: يوجد 9."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien font 2 + 3 ?",
      "choices": [
        "4",
        "5"
      ],
      "answer": "5",
      "explanation": "On additionne : 2 + 3 = 5."
    },
    "ar": {
      "question": "كم مجموع 2 + 3؟",
      "choices": [
        "4",
        "5"
      ],
      "answer": "5",
      "explanation": "نجمع: 2 + 3 = 5."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien font 4 + 5 ?",
      "choices": [
        "8",
        "9"
      ],
      "answer": "9",
      "explanation": "On additionne : 4 + 5 = 9."
    },
    "ar": {
      "question": "كم مجموع 4 + 5؟",
      "choices": [
        "8",
        "9"
      ],
      "answer": "9",
      "explanation": "نجمع: 4 + 5 = 9."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien font 3 + 3 ?",
      "choices": [
        "5",
        "6"
      ],
      "answer": "6",
      "explanation": "On additionne : 3 + 3 = 6."
    },
    "ar": {
      "question": "كم مجموع 3 + 3؟",
      "choices": [
        "5",
        "6"
      ],
      "answer": "6",
      "explanation": "نجمع: 3 + 3 = 6."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien font 1 + 6 ?",
      "choices": [
        "6",
        "7"
      ],
      "answer": "7",
      "explanation": "On additionne : 1 + 6 = 7."
    },
    "ar": {
      "question": "كم مجموع 1 + 6؟",
      "choices": [
        "6",
        "7"
      ],
      "answer": "7",
      "explanation": "نجمع: 1 + 6 = 7."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien font 4 + 4 ?",
      "choices": [
        "7",
        "8"
      ],
      "answer": "8",
      "explanation": "On additionne : 4 + 4 = 8."
    },
    "ar": {
      "question": "كم مجموع 4 + 4؟",
      "choices": [
        "7",
        "8"
      ],
      "answer": "8",
      "explanation": "نجمع: 4 + 4 = 8."
    }
  },
  {
    "domain": "numeration",
    "skill": "ordre_nombres",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "Quel est le plus grand nombre ?",
      "choices": [
        "2",
        "4",
        "1"
      ],
      "answer": "4",
      "explanation": "On compare les nombres : 4 est le plus grand des trois."
    },
    "ar": {
      "question": "ما هو أكبر عدد؟",
      "choices": [
        "2",
        "4",
        "1"
      ],
      "answer": "4",
      "explanation": "نقارن الأعداد: 4 هو الأكبر بين الثلاثة."
    }
  },
  {
    "domain": "numeration",
    "skill": "ordre_nombres",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quel est le plus grand nombre ?",
      "choices": [
        "5",
        "3",
        "2"
      ],
      "answer": "5",
      "explanation": "On compare les nombres : 5 est le plus grand des trois."
    },
    "ar": {
      "question": "ما هو أكبر عدد؟",
      "choices": [
        "5",
        "3",
        "2"
      ],
      "answer": "5",
      "explanation": "نقارن الأعداد: 5 هو الأكبر بين الثلاثة."
    }
  },
  {
    "domain": "numeration",
    "skill": "ordre_nombres",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quel est le plus grand nombre ?",
      "choices": [
        "13",
        "17",
        "11"
      ],
      "answer": "17",
      "explanation": "On compare les nombres : 17 est le plus grand des trois."
    },
    "ar": {
      "question": "ما هو أكبر عدد؟",
      "choices": [
        "13",
        "17",
        "11"
      ],
      "answer": "17",
      "explanation": "نقارن الأعداد: 17 هو الأكبر بين الثلاثة."
    }
  },
  {
    "domain": "numeration",
    "skill": "ordre_nombres",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel est le plus grand nombre ?",
      "choices": [
        "19",
        "12",
        "15"
      ],
      "answer": "19",
      "explanation": "On compare les nombres : 19 est le plus grand des trois."
    },
    "ar": {
      "question": "ما هو أكبر عدد؟",
      "choices": [
        "19",
        "12",
        "15"
      ],
      "answer": "19",
      "explanation": "نقارن الأعداد: 19 هو الأكبر بين الثلاثة."
    }
  },
  {
    "domain": "numeration",
    "skill": "ordre_nombres",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel est le plus grand nombre ?",
      "choices": [
        "14",
        "18",
        "10"
      ],
      "answer": "18",
      "explanation": "On compare les nombres : 18 est le plus grand des trois."
    },
    "ar": {
      "question": "ما هو أكبر عدد؟",
      "choices": [
        "14",
        "18",
        "10"
      ],
      "answer": "18",
      "explanation": "نقارن الأعداد: 18 هو الأكبر بين الثلاثة."
    }
  },
  {
    "domain": "mesure",
    "skill": "comparaison_longueurs",
    "format": "selection",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quelle ligne est la plus longue ?",
      "visual": "Ligne A : ▬▬▬▬▬▬▬<br>Ligne B : ▬▬▬▬",
      "choices": [
        "Ligne A",
        "Ligne B"
      ],
      "answer": "Ligne A",
      "explanation": "La ligne A a 7 segments contre 4 pour la ligne B : elle est plus longue."
    },
    "ar": {
      "question": "أي خط أطول؟",
      "visual": "الخط أ : ▬▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬",
      "choices": [
        "الخط أ",
        "الخط ب"
      ],
      "answer": "الخط أ",
      "explanation": "الخط أ يحتوي على 7 أجزاء مقابل 4 للخط ب: إذن هو الأطول."
    }
  },
  {
    "domain": "mesure",
    "skill": "comparaison_longueurs",
    "format": "selection",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quelle ligne est la plus longue ?",
      "visual": "Ligne A : ▬▬▬▬▬<br>Ligne B : ▬▬▬",
      "choices": [
        "Ligne A",
        "Ligne B"
      ],
      "answer": "Ligne A",
      "explanation": "La ligne A a 5 segments contre 3 pour la ligne B : elle est plus longue."
    },
    "ar": {
      "question": "أي خط أطول؟",
      "visual": "الخط أ : ▬▬▬▬▬<br>الخط ب : ▬▬▬",
      "choices": [
        "الخط أ",
        "الخط ب"
      ],
      "answer": "الخط أ",
      "explanation": "الخط أ يحتوي على 5 أجزاء مقابل 3 للخط ب: إذن هو الأطول."
    }
  },
  {
    "domain": "mesure",
    "skill": "comparaison_longueurs",
    "format": "selection",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quelle ligne est la plus longue ?",
      "visual": "Ligne A : ▬▬▬▬▬▬▬▬<br>Ligne B : ▬▬▬▬▬",
      "choices": [
        "Ligne A",
        "Ligne B"
      ],
      "answer": "Ligne A",
      "explanation": "La ligne A a 8 segments contre 5 pour la ligne B : elle est plus longue."
    },
    "ar": {
      "question": "أي خط أطول؟",
      "visual": "الخط أ : ▬▬▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬▬",
      "choices": [
        "الخط أ",
        "الخط ب"
      ],
      "answer": "الخط أ",
      "explanation": "الخط أ يحتوي على 8 أجزاء مقابل 5 للخط ب: إذن هو الأطول."
    }
  },
  {
    "domain": "mesure",
    "skill": "comparaison_longueurs",
    "format": "selection",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Quelle ligne est la plus longue ?",
      "visual": "Ligne A : ▬▬▬▬▬▬<br>Ligne B : ▬▬▬▬",
      "choices": [
        "Ligne A",
        "Ligne B"
      ],
      "answer": "Ligne A",
      "explanation": "La ligne A a 6 segments contre 4 pour la ligne B : elle est plus longue."
    },
    "ar": {
      "question": "أي خط أطول؟",
      "visual": "الخط أ : ▬▬▬▬▬▬<br>الخط ب : ▬▬▬▬",
      "choices": [
        "الخط أ",
        "الخط ب"
      ],
      "answer": "الخط أ",
      "explanation": "الخط أ يحتوي على 6 أجزاء مقابل 4 للخط ب: إذن هو الأطول."
    }
  },
  {
    "domain": "mesure",
    "skill": "reconnaissance_monnaie",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de millimes y a-t-il en tout ?",
      "visual": "🪙🪙🪙🪙 + 🪙🪙🪙",
      "choices": [
        "6",
        "7",
        "8"
      ],
      "answer": "7",
      "explanation": "On compte toutes les pièces : 4 + 3 = 7 millimes."
    },
    "ar": {
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
  },
  {
    "domain": "mesure",
    "skill": "reconnaissance_monnaie",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de millimes y a-t-il en tout ?",
      "visual": "🪙🪙🪙🪙🪙🪙 + 🪙🪙",
      "choices": [
        "7",
        "8",
        "9"
      ],
      "answer": "8",
      "explanation": "On compte toutes les pièces : 6 + 2 = 8 millimes."
    },
    "ar": {
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
  },
  {
    "domain": "mesure",
    "skill": "reconnaissance_monnaie",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de millimes y a-t-il en tout ?",
      "visual": "🪙🪙🪙🪙🪙 + 🪙🪙🪙🪙",
      "choices": [
        "8",
        "9",
        "10"
      ],
      "answer": "9",
      "explanation": "On compte toutes les pièces : 5 + 4 = 9 millimes."
    },
    "ar": {
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
  },
  {
    "domain": "mesure",
    "skill": "reconnaissance_monnaie",
    "format": "qcm",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de millimes y a-t-il en tout ?",
      "visual": "🪙🪙🪙 + 🪙🪙🪙",
      "choices": [
        "5",
        "6",
        "7"
      ],
      "answer": "6",
      "explanation": "On compte toutes les pièces : 3 + 3 = 6 millimes."
    },
    "ar": {
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
  },
  {
    "domain": "mesure",
    "skill": "addition_monnaie",
    "format": "saisie_nombre",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Karim a une pièce de 3 millimes et une pièce de 5 millimes.",
      "visual": "🪙×3 + 🪙×5",
      "answer": 8,
      "explanation": "On additionne les deux valeurs : 3 + 5 = 8 millimes."
    },
    "ar": {
      "question": "لدى كريم قطعة من 3 مليمات وقطعة من 5 مليمات.",
      "visual": "🪙×3 + 🪙×5",
      "answer": 8,
      "explanation": "نجمع القيمتين: 3 + 5 = 8 مليمات."
    }
  },
  {
    "domain": "mesure",
    "skill": "addition_monnaie",
    "format": "saisie_nombre",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Karim a une pièce de 2 millimes et une pièce de 6 millimes.",
      "visual": "🪙×2 + 🪙×6",
      "answer": 8,
      "explanation": "On additionne les deux valeurs : 2 + 6 = 8 millimes."
    },
    "ar": {
      "question": "لدى كريم قطعة من 2 مليمات وقطعة من 6 مليمات.",
      "visual": "🪙×2 + 🪙×6",
      "answer": 8,
      "explanation": "نجمع القيمتين: 2 + 6 = 8 مليمات."
    }
  },
  {
    "domain": "mesure",
    "skill": "addition_monnaie",
    "format": "saisie_nombre",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Karim a une pièce de 4 millimes et une pièce de 4 millimes.",
      "visual": "🪙×4 + 🪙×4",
      "answer": 8,
      "explanation": "On additionne les deux valeurs : 4 + 4 = 8 millimes."
    },
    "ar": {
      "question": "لدى كريم قطعة من 4 مليمات وقطعة من 4 مليمات.",
      "visual": "🪙×4 + 🪙×4",
      "answer": 8,
      "explanation": "نجمع القيمتين: 4 + 4 = 8 مليمات."
    }
  },
  {
    "domain": "mesure",
    "skill": "addition_monnaie",
    "format": "saisie_nombre",
    "trimester": "T2",
    "difficulty": "en_cours",
    "fr": {
      "question": "Karim a une pièce de 1 millimes et une pièce de 7 millimes.",
      "visual": "🪙×1 + 🪙×7",
      "answer": 8,
      "explanation": "On additionne les deux valeurs : 1 + 7 = 8 millimes."
    },
    "ar": {
      "question": "لدى كريم قطعة من 1 مليمات وقطعة من 7 مليمات.",
      "visual": "🪙×1 + 🪙×7",
      "answer": 8,
      "explanation": "نجمع القيمتين: 1 + 7 = 8 مليمات."
    }
  },
  {
    "domain": "numeration",
    "skill": "dizaine_unites",
    "format": "saisie_nombre",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel nombre forment 1 dizaine et 2 unités ?",
      "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 (2 unités)",
      "answer": 12,
      "explanation": "1 dizaine vaut 10. On ajoute les 2 unités : 10 + 2 = 12."
    },
    "ar": {
      "question": "ما هو العدد المكوَّن من عشرة واحدة و2 آحاد؟",
      "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 (2 آحاد)",
      "answer": 12,
      "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 2 = 12."
    }
  },
  {
    "domain": "numeration",
    "skill": "dizaine_unites",
    "format": "saisie_nombre",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel nombre forment 1 dizaine et 5 unités ?",
      "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 🔵 🔵 🔵 (5 unités)",
      "answer": 15,
      "explanation": "1 dizaine vaut 10. On ajoute les 5 unités : 10 + 5 = 15."
    },
    "ar": {
      "question": "ما هو العدد المكوَّن من عشرة واحدة و5 آحاد؟",
      "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 (5 آحاد)",
      "answer": 15,
      "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 5 = 15."
    }
  },
  {
    "domain": "numeration",
    "skill": "dizaine_unites",
    "format": "saisie_nombre",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel nombre forment 1 dizaine et 7 unités ?",
      "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 (7 unités)",
      "answer": 17,
      "explanation": "1 dizaine vaut 10. On ajoute les 7 unités : 10 + 7 = 17."
    },
    "ar": {
      "question": "ما هو العدد المكوَّن من عشرة واحدة و7 آحاد؟",
      "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 (7 آحاد)",
      "answer": 17,
      "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 7 = 17."
    }
  },
  {
    "domain": "numeration",
    "skill": "dizaine_unites",
    "format": "saisie_nombre",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel nombre forment 1 dizaine et 9 unités ?",
      "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 (9 unités)",
      "answer": 19,
      "explanation": "1 dizaine vaut 10. On ajoute les 9 unités : 10 + 9 = 19."
    },
    "ar": {
      "question": "ما هو العدد المكوَّن من عشرة واحدة و9 آحاد؟",
      "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 🔵 (9 آحاد)",
      "answer": 19,
      "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 9 = 19."
    }
  },
  {
    "domain": "numeration",
    "skill": "dizaine_unites",
    "format": "saisie_nombre",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quel nombre forment 1 dizaine et 3 unités ?",
      "visual": "📦 (1 dizaine = 10)<br>🔵 🔵 🔵 (3 unités)",
      "answer": 13,
      "explanation": "1 dizaine vaut 10. On ajoute les 3 unités : 10 + 3 = 13."
    },
    "ar": {
      "question": "ما هو العدد المكوَّن من عشرة واحدة و3 آحاد؟",
      "visual": "📦 (عشرة واحدة = 10)<br>🔵 🔵 🔵 (3 آحاد)",
      "answer": 13,
      "explanation": "العشرة الواحدة تساوي 10. نضيف الآحاد: 10 + 3 = 13."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition_verticale",
    "format": "calcul",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Pose et calcule : 11 + 6",
      "answer": 17,
      "explanation": "On aligne les unités et les dizaines : 1 + 6 = 7 unités, la dizaine ne change pas. Donc 11 + 6 = 17."
    },
    "ar": {
      "question": "ضع العملية عموديًا واحسب: 11 + 6",
      "answer": 17,
      "explanation": "نرتب الآحاد تحت الآحاد: 1 + 6 = 7 آحاد، والعشرة تبقى كما هي. إذن 11 + 6 = 17."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition_verticale",
    "format": "calcul",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Pose et calcule : 12 + 3",
      "answer": 15,
      "explanation": "On aligne les unités et les dizaines : 2 + 3 = 5 unités, la dizaine ne change pas. Donc 12 + 3 = 15."
    },
    "ar": {
      "question": "ضع العملية عموديًا واحسب: 12 + 3",
      "answer": 15,
      "explanation": "نرتب الآحاد تحت الآحاد: 2 + 3 = 5 آحاد، والعشرة تبقى كما هي. إذن 12 + 3 = 15."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition_verticale",
    "format": "calcul",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Pose et calcule : 14 + 5",
      "answer": 19,
      "explanation": "On aligne les unités et les dizaines : 4 + 5 = 9 unités, la dizaine ne change pas. Donc 14 + 5 = 19."
    },
    "ar": {
      "question": "ضع العملية عموديًا واحسب: 14 + 5",
      "answer": 19,
      "explanation": "نرتب الآحاد تحت الآحاد: 4 + 5 = 9 آحاد، والعشرة تبقى كما هي. إذن 14 + 5 = 19."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition_verticale",
    "format": "calcul",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Pose et calcule : 13 + 4",
      "answer": 17,
      "explanation": "On aligne les unités et les dizaines : 3 + 4 = 7 unités, la dizaine ne change pas. Donc 13 + 4 = 17."
    },
    "ar": {
      "question": "ضع العملية عموديًا واحسب: 13 + 4",
      "answer": 17,
      "explanation": "نرتب الآحاد تحت الآحاد: 3 + 4 = 7 آحاد، والعشرة تبقى كما هي. إذن 13 + 4 = 17."
    }
  },
  {
    "domain": "calcul",
    "skill": "addition_verticale",
    "format": "calcul",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Pose et calcule : 15 + 3",
      "answer": 18,
      "explanation": "On aligne les unités et les dizaines : 5 + 3 = 8 unités, la dizaine ne change pas. Donc 15 + 3 = 18."
    },
    "ar": {
      "question": "ضع العملية عموديًا واحسب: 15 + 3",
      "answer": 18,
      "explanation": "نرتب الآحاد تحت الآحاد: 5 + 3 = 8 آحاد، والعشرة تبقى كما هي. إذن 15 + 3 = 18."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "formes",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de côtés a un carré ?",
      "choices": [
        "3",
        "4",
        "5"
      ],
      "answer": "4",
      "explanation": "Un carré a 4 côtés égaux."
    },
    "ar": {
      "question": "كم ضلعًا للمربع؟",
      "choices": [
        "3",
        "4",
        "5"
      ],
      "answer": "4",
      "explanation": "المربع له 4 أضلاع متساوية."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "formes",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de côtés a un triangle ?",
      "choices": [
        "2",
        "3",
        "4"
      ],
      "answer": "3",
      "explanation": "Un triangle a 3 côtés."
    },
    "ar": {
      "question": "كم ضلعًا للمثلث؟",
      "choices": [
        "2",
        "3",
        "4"
      ],
      "answer": "3",
      "explanation": "المثلث له 3 أضلاع."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "formes",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "en_cours",
    "fr": {
      "question": "Combien de côtés a un rectangle ?",
      "choices": [
        "3",
        "4",
        "6"
      ],
      "answer": "4",
      "explanation": "Un rectangle a 4 côtés."
    },
    "ar": {
      "question": "كم ضلعًا للمستطيل؟",
      "choices": [
        "3",
        "4",
        "6"
      ],
      "answer": "4",
      "explanation": "المستطيل له 4 أضلاع."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "formes",
    "format": "selection",
    "trimester": "T3",
    "difficulty": "maitrise",
    "fr": {
      "question": "Quelle forme n'a pas de côtés droits ?",
      "choices": [
        "⬛ Carré",
        "🔺 Triangle",
        "⚪ Cercle"
      ],
      "answer": "⚪ Cercle",
      "explanation": "Le cercle est le seul de ces trois à ne pas avoir de côtés droits."
    },
    "ar": {
      "question": "أي شكل ليس له أضلاع مستقيمة؟",
      "choices": [
        "⬛ Carré",
        "🔺 Triangle",
        "⚪ Cercle"
      ],
      "answer": "⚪ Cercle",
      "explanation": "الدائرة هي الشكل الوحيد بدون أضلاع مستقيمة."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "dessus_dessous",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "Où est l'oiseau par rapport à l'arbre ?",
      "visual": "🐦<br>🌳",
      "choices": [
        "L'oiseau est dessus",
        "L'oiseau est dessous"
      ],
      "answer": "L'oiseau est dessus",
      "explanation": "L'oiseau est dessiné au-dessus de l'arbre."
    },
    "ar": {
      "question": "أين الطائر بالنسبة للشجرة؟",
      "visual": "🐦<br>🌳",
      "choices": [
        "الطائر فوق",
        "الطائر تحت"
      ],
      "answer": "الطائر فوق",
      "explanation": "الطائر مرسوم فوق الشجرة."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "gauche_droite",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "L'étoile est-elle à gauche ou à droite du rond rouge ?",
      "visual": "⭐ 🔴",
      "choices": [
        "À gauche",
        "À droite"
      ],
      "answer": "À gauche",
      "explanation": "L'étoile est dessinée avant le rond rouge, donc à gauche."
    },
    "ar": {
      "question": "هل النجمة على يسار أم يمين الدائرة الحمراء؟",
      "visual": "⭐ 🔴",
      "choices": [
        "على اليسار",
        "على اليمين"
      ],
      "answer": "على اليسار",
      "explanation": "النجمة مرسومة قبل الدائرة الحمراء، إذن على اليسار."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "haut_bas",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "Le nuage est-il en haut ou en bas de la maison ?",
      "visual": "☁️<br>🏠",
      "choices": [
        "En haut",
        "En bas"
      ],
      "answer": "En haut",
      "explanation": "Le nuage est dessiné au-dessus de la maison."
    },
    "ar": {
      "question": "هل الغيمة في أعلى أم أسفل المنزل؟",
      "visual": "☁️<br>🏠",
      "choices": [
        "في الأعلى",
        "في الأسفل"
      ],
      "answer": "في الأعلى",
      "explanation": "الغيمة مرسومة فوق المنزل."
    }
  },
  {
    "domain": "espace_geometrie",
    "skill": "dessus_dessous",
    "format": "selection",
    "trimester": "T1",
    "difficulty": "decouverte",
    "fr": {
      "question": "L'abeille est-elle dessus ou dessous la fleur ?",
      "visual": "🐝<br>🌼",
      "choices": [
        "Dessus",
        "Dessous"
      ],
      "answer": "Dessus",
      "explanation": "L'abeille est dessinée au-dessus de la fleur."
    },
    "ar": {
      "question": "هل النحلة فوق أم تحت الزهرة؟",
      "visual": "🐝<br>🌼",
      "choices": [
        "فوق",
        "تحت"
      ],
      "answer": "فوق",
      "explanation": "النحلة مرسومة فوق الزهرة."
    }
  },
  {
    "domain": "numeration",
    "skill": "composition",
    "format": "saisie_nombre",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "5 c'est 3 plus combien ?",
      "answer": 2,
      "explanation": "On cherche le nombre qui, ajouté à 3, donne 5 : 3 + 2 = 5."
    },
    "ar": {
      "question": "5 هو 3 زائد كم؟",
      "answer": 2,
      "explanation": "نبحث عن العدد الذي يُضاف إلى 3 ليعطي 5: 3 + 2 = 5."
    }
  },
  {
    "domain": "numeration",
    "skill": "composition",
    "format": "saisie_nombre",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "4 c'est 1 plus combien ?",
      "answer": 3,
      "explanation": "On cherche le nombre qui, ajouté à 1, donne 4 : 1 + 3 = 4."
    },
    "ar": {
      "question": "4 هو 1 زائد كم؟",
      "answer": 3,
      "explanation": "نبحث عن العدد الذي يُضاف إلى 1 ليعطي 4: 1 + 3 = 4."
    }
  },
  {
    "domain": "numeration",
    "skill": "composition",
    "format": "saisie_nombre",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "5 c'est 4 plus combien ?",
      "answer": 1,
      "explanation": "On cherche le nombre qui, ajouté à 4, donne 5 : 4 + 1 = 5."
    },
    "ar": {
      "question": "5 هو 4 زائد كم؟",
      "answer": 1,
      "explanation": "نبحث عن العدد الذي يُضاف إلى 4 ليعطي 5: 4 + 1 = 5."
    }
  },
  {
    "domain": "numeration",
    "skill": "decomposition",
    "format": "saisie_nombre",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "Décompose 4 : 4 = 1 + combien ?",
      "answer": 3,
      "explanation": "4 se décompose en 1 et 3, car 1 + 3 = 4."
    },
    "ar": {
      "question": "فكّك العدد 4: 4 = 1 + كم؟",
      "answer": 3,
      "explanation": "يتفكك 4 إلى 1 و3، لأن 1 + 3 = 4."
    }
  },
  {
    "domain": "numeration",
    "skill": "decomposition",
    "format": "saisie_nombre",
    "trimester": "T1",
    "difficulty": "en_cours",
    "fr": {
      "question": "Décompose 5 : 5 = 2 + combien ?",
      "answer": 3,
      "explanation": "5 se décompose en 2 et 3, car 2 + 3 = 5."
    },
    "ar": {
      "question": "فكّك العدد 5: 5 = 2 + كم؟",
      "answer": 3,
      "explanation": "يتفكك 5 إلى 2 و3، لأن 2 + 3 = 5."
    }
  }
]

for _ind in INDIVIDUAL_BATCH2:
    EXAMPLES.append(
        {
            "source": {
                "url": f"local://repartition-trimestrielle-batch2.docx#{_ind['domain']}-{_ind['skill']}-{len(EXAMPLES)}",
                "title": "Répartition trimestrielle du programme tunisien, 1ère année (fournie par l'utilisateur)",
                "license_status": "unlicensed",
                "subject_code": "math",
                "level_code": "1",
                "domain_hint": _ind["domain"],
                "trimester_hint": _ind["trimester"],
                "region_scope": "tunisia_web",
                "content_snapshot": "Répartition trimestrielle fournie par l'utilisateur : sert à confirmer quel sujet couvrir à quel trimestre, pas comme contenu recopié.",
                "status": "used_for_generation",
            },
            "exercise": {
                "subject_code": "math",
                "level_code": "1",
                "trimester": _ind["trimester"],
                "domain_code": _ind["domain"],
                "skill_code": _ind["skill"],
                "exercise_format": _ind["format"],
                "difficulty": _ind["difficulty"],
                "content_fr": _ind["fr"],
                "content_ar": _ind["ar"],
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
