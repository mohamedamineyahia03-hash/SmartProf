"""Seed: 28 exercises from a user-supplied 1800-item exercise bank
(banque_exercices_1ere_complete.json), after inspection found the file was
really ~30 unique templates each duplicated 50-67x with identical text, plus
4 templates with unusable/wrong answers (2 image-dependent with no image on
hand, 2 with a stated answer that contradicted the text's own numbers 4
times out of 5). Kept: the 26 genuinely distinct + correct exercises, plus 2
whose answer could be recomputed straight from the text (no image needed).
Rejected: the 2 truly unrecoverable ones. See the migration notes in
project memory for the full inspection. No 'explanation' field existed in
the source at all -- every explanation below was authored here, competence
by competence, consistent with the pedagogy-first rule.
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
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T1_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "espace_geometrie",
            "skill_code": "positions",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أَيْنَ تَقَعُ الكُرَةُ بالنسبةِ لِلطَّاوِلَةِ ؟",
                "answer": "فَوْقَ الطَّاوِلَةِ",
                "explanation": "نلاحظ موقع الشيء في الصورة بدقة: الإجابة الصحيحة هي فَوْقَ الطَّاوِلَةِ.",
                "choices": [
                    "فَوْقَ الطَّاوِلَةِ",
                    "تَحْتَ الطَّاوِلَةِ",
                    "بِجَانِبِ الطَّاوِلَةِ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T1_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "pre_numeric",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "pre_numeric",
            "skill_code": "classement",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "اخْتَرْ الأَشْكَالَ التِّي لَهَا نَفْسُ اللَّوْنِ.",
                "answer": "المَجْمُوعَةُ حَمْرَاءُ",
                "explanation": "نلاحظ الخاصية المشتركة بين العناصر (اللون أو الشكل) لنختار المَجْمُوعَةُ حَمْرَاءُ.",
                "choices": [
                    "المَجْمُوعَةُ حَمْرَاءُ",
                    "المَجْمُوعَةُ خَضْرَاءُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T1_004",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "قَارِنْ بِاسْتِعْمَالِ الرَّمْزِ: 4 ... 2",
                "answer": ">",
                "explanation": "نقارن العددين 4 و2: العلامة الصحيحة هي >.",
                "choices": [
                    ">",
                    "<",
                    "="
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T2_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "احْسِبْ المَجْمُوعَ التَّالِي: 5 + 4 = ...",
                "answer": "9",
                "explanation": "نجمع العددين: 5 + 4 = 9.",
                "choices": [
                    "8",
                    "9",
                    "7"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T2_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "reconnaissance_monnaie",
            "exercise_format": "saisie_nombre",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "كَمْ مِلِيمًا لَدَى أَحْمَدَ ؟ (5 مِلِيمَات + 1 مِلِيم)",
                "answer": "6",
                "explanation": "نجمع قيمة القطع: 5 + 1 = 6 مليمًا."
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T2_004",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "mesure",
            "skill_code": "comparaison_longueurs",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أَيُّ الشَّرِيطَيْنِ هُوَ الأَقْصَرُ ؟",
                "answer": "الشَّرِيطُ الأَصْفَرُ",
                "explanation": "نقارن طولي العنصرين في الصورة مباشرة: الإجابة هي الشَّرِيطُ الأَصْفَرُ.",
                "choices": [
                    "الشَّرِيطُ الأَصْفَرُ",
                    "الشَّرِيطُ الأَزْرَقُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T3_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "numeration",
            "skill_code": "lecture_nombre",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "مَا هُوَ العَدَدُ الذِّي يُمَثِّلُ 1 عَشَرَة وَ 5 آحَادٍ ؟",
                "answer": "15",
                "explanation": "نحسب عدد العشرات وعدد الآحاد لنحصل على العدد 15.",
                "choices": [
                    "15",
                    "51",
                    "10"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T3_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
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
                "question": "أَنْجِزْ العَمَلِيَّةَ: 14 + 2 = ...",
                "answer": "16",
                "explanation": "نرتب الآحاد تحت الآحاد والعشرات تحت العشرات، ثم نجمع: 14 + 2 = 16."
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T3_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "مَا هُوَ اسْمُ هَذَا الشَّكْلِ الدَّائِرِيِّ ؟",
                "answer": "دَائِرَةٌ",
                "explanation": "نلاحظ شكل الرسم وعدد أضلاعه لنتعرف عليه: هو دَائِرَةٌ.",
                "choices": [
                    "مُرَبَّعٌ",
                    "دَائِرَةٌ",
                    "مُثَلَّثٌ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_MATH_1_T3_004",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "mesure",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "mesure",
            "skill_code": "utilisation_dinar",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "ثَمَنُ اللُّعْبَةِ 5 دَنَانِير. هَلْ تَكْفِي قِطْعَةٌ مِنْ فِئَةِ 2 دِينَارٍ ؟",
                "answer": "لَا",
                "explanation": "نقارن ثمن الشيء بقيمة القطعة أو الورقة النقدية المذكورة، فتكون الإجابة: لَا.",
                "choices": [
                    "نَعَمْ",
                    "لَا"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T1_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "huruf",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "huruf",
            "skill_code": "tamyiz_huruf",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "مَا هُوَ الحَرْفُ الأَوَّلُ فِي كَلِمَةِ (مَدْرَسَةٌ) ؟",
                "answer": "مَ",
                "explanation": "نستمع إلى صوت أول حرف في الكلمة وننطقه بمفرده: هو مَ.",
                "choices": [
                    "مَ",
                    "بَ",
                    "دَ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T1_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "qiraa",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "qiraa",
            "skill_code": "qiraat_kalimat",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "اخْتَرْ الكَلِمَةَ المُنَاسِبَةَ لِصُورَةِ الكَلْبِ:",
                "answer": "كَلْبٌ",
                "explanation": "نلاحظ الصورة جيدًا ونختار الكلمة التي تصفها: كَلْبٌ.",
                "choices": [
                    "قِطٌّ",
                    "كَلْبٌ",
                    "عُصْفُورٌ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T1_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "kitaba",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "kitaba",
            "skill_code": "imla_kalima",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "أَكْمِلْ الكَلِمَةَ بِالحَرْفِ المُنَاسِبِ: ...ـقَـرَةٌ",
                "answer": "بـ",
                "explanation": "ننطق الكلمة كاملة لنسمع الحرف الناقص: هو بـ.",
                "choices": [
                    "بـ",
                    "تـ",
                    "مـ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T2_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "huruf",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "huruf",
            "skill_code": "tanwin",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أَيُّ الكَلِمَاتِ التَّالِيَةِ تَنْتَهِي بِتَنْوِينِ ضَمٍّ ؟",
                "answer": "كِتَابٌ",
                "explanation": "ننظر إلى الحركة الأخيرة المكررة في آخر الكلمة (تنوين): الكلمة الصحيحة هي كِتَابٌ.",
                "choices": [
                    "كِتَابًا",
                    "كِتَابٌ",
                    "كِتَابٍ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T2_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "taabir",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "taabir",
            "skill_code": "tartib_kalimat",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "رَتِّبْ لِتُكَوِّنَ جُمْلَةً: التِّلْمِيذُ - إِلَى - ذَهَبَ - المَدْرَسَةِ",
                "answer": "ذَهَبَ التِّلْمِيذُ إِلَى المَدْرَسَةِ",
                "explanation": "نبحث عن الترتيب الذي يعطي معنى مفيدًا وصحيحًا: ذَهَبَ التِّلْمِيذُ إِلَى المَدْرَسَةِ.",
                "choices": [
                    "ذَهَبَ التِّلْمِيذُ إِلَى المَدْرَسَةِ",
                    "إِلَى المَدْرَسَةِ التِّلْمِيذُ ذَهَبَ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T2_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "qiraa",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "qiraa",
            "skill_code": "qiraat_maqate",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "كَمْ عَدَدُ المَقَاطِعِ الصَّوْتِيَّةِ فِي كَلِمَةِ (وَلَدٌ) ؟",
                "answer": "3",
                "explanation": "نقطّع الكلمة مقطعًا مقطعًا بالتصفيق مثلًا، فنجد 3 مقاطع.",
                "choices": [
                    "2",
                    "3",
                    "4"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T3_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "kitaba",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "kitaba",
            "skill_code": "damir_munasib",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "أَكْمِلْ الفَرَاغَ بِالضَّمِيرِ المُنَاسِبِ: ...... أَكْتُبُ دَرْسِي.",
                "answer": "أَنَا",
                "explanation": "ننظر إلى الفعل والفاعل لنختار الضمير المناسب: هو أَنَا.",
                "choices": [
                    "أَنَا",
                    "أَنْتَ",
                    "هُوَ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T3_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "fahm",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "fahm",
            "skill_code": "fahm_jumla",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "طَارَ العُصْفُورُ فِي السَّمَاءِ. أَيْنَ طَارَ العُصْفُورُ ؟",
                "answer": "فِي السَّمَاءِ",
                "explanation": "نعود إلى الجملة ونبحث فيها عن الإجابة مباشرة: فِي السَّمَاءِ.",
                "choices": [
                    "فِي السَّمَاءِ",
                    "عَلَى الأَرْضِ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_ARABE_1_T3_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "ar",
            "level_code": "1",
            "domain_hint": "huruf",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "ar",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "huruf",
            "skill_code": "lam_shamsiya_qamariya",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "كَلِمَةُ (الشَّمْسُ) تَحْتَوِي عَلَى :",
                "answer": "لَامٍ شَمْسِيَّةٍ",
                "explanation": "ننطق الكلمة: إذا اختفى صوت اللام ونُطق الحرف الذي يليه مشددًا، فهي لَامٍ شَمْسِيَّةٍ.",
                "choices": [
                    "لَامٍ شَمْسِيَّةٍ",
                    "لَامٍ قَمَرِيَّةٍ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T1_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "corps_humain",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "corps_humain",
            "skill_code": "les_sens",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "بِأَيِّ عُضْوٍ أَسْتَمِعُ إِلَى أَنَاشِيدَ جَمِيلَةٍ ؟",
                "answer": "الأُذُنُ",
                "explanation": "نفكر في العضو الذي يقوم بهذا العمل في جسمنا: هو الأُذُنُ.",
                "choices": [
                    "الأُذُنُ",
                    "العَيْنُ",
                    "اللِّسَانُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T1_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "etres_vivants",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "etres_vivants",
            "skill_code": "animaux_domestiques",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "أَيُّ الحَيَوَانَاتِ التَّالِيَةِ هُوَ حَيَوَانٌ أَلِيفٌ ؟",
                "answer": "الخَرُوفُ",
                "explanation": "الحيوان الأليف هو الذي يعيش قرب الإنسان ويرعاه: هو الخَرُوفُ.",
                "choices": [
                    "الأَسَدُ",
                    "الخَرُوفُ",
                    "الذِّئْبُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T1_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "saisons",
            "trimester_hint": "T1",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "saisons",
            "skill_code": "moments_journee",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "تَظْهَرُ النُّجُومُ وَالقَمَرُ فِي السَّمَاءِ فِي :",
                "answer": "اللَّيْلِ",
                "explanation": "نلاحظ العلامات الموجودة (الشمس، القمر، النجوم) لنحدد الفترة: هي اللَّيْلِ.",
                "choices": [
                    "الصَّبَاحِ",
                    "اللَّيْلِ",
                    "الظُّهْرِ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T2_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "etres_vivants",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "etres_vivants",
            "skill_code": "parties_plante",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "مَا هُوَ الجُزْءُ الذِّي يَمْتَصُّ المَاءَ مِنَ التُّرْبَةِ ؟",
                "answer": "الجُذُورُ",
                "explanation": "كل جزء من النبتة له دور خاص؛ الجزء المسؤول هنا هو الجُذُورُ.",
                "choices": [
                    "الجُذُورُ",
                    "الأَوْرَاقُ",
                    "الأَزْهَارُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T2_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "corps_humain",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "corps_humain",
            "skill_code": "alimentation_saine",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "التُّفَّاحُ وَالمَوْزُ هِيَ أَغْذِيَةٌ مِنْ مَصْدَرٍ :",
                "answer": "نَبَاتِيٍّ",
                "explanation": "نفكر من أين يأتي هذا الغذاء: مصدره نَبَاتِيٍّ.",
                "choices": [
                    "نَبَاتِيٍّ",
                    "حَيَوَانِيٌّ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T2_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "etres_vivants",
            "trimester_hint": "T2",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "etres_vivants",
            "skill_code": "couverture_corporelle",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "مَاذَا يُغَطِّي جِسْمَ الحَمَامَةِ ؟",
                "answer": "الرِّيشُ",
                "explanation": "نلاحظ جسم الحيوان: يغطيه الرِّيشُ.",
                "choices": [
                    "الرِّيشُ",
                    "الصُّوفُ",
                    "الشَّعْرُ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T3_001",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "eau",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "eau",
            "skill_code": "etats_eau",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "language": "ar",
            "content": {
                "question": "الـمَاءُ وَالحَلِيبُ هِيَ أَجْسَامٌ فِي حَالَةٍ :",
                "answer": "سَائِلَةٍ",
                "explanation": "نلاحظ شكل الجسم: هل يحافظ على شكله (صلب) أم يأخذ شكل إنائه (سائل)؟ هنا هو سَائِلَةٍ.",
                "choices": [
                    "صَلْبَةٍ",
                    "سَائِلَةٍ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T3_002",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "saisons",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "saisons",
            "skill_code": "reconnaissance_saisons",
            "exercise_format": "qcm",
            "difficulty": "maitrise",
            "language": "ar",
            "content": {
                "question": "نَرْتَدِي المَلَابِسَ الصُّوفِيَّةَ الثَّقِيلَةَ فِي فَصْلِ :",
                "answer": "الشِّتَاءِ",
                "explanation": "نربط الوصف بما يميز كل فصل من الفصول الأربعة: الإجابة هي الشِّتَاءِ.",
                "choices": [
                    "الشِّتَاءِ",
                    "الصَّيْفِ",
                    "الرَّبِيعِ"
                ]
            }
        }
    },
    {
        "source": {
            "url": "local://banque_exercices_1ere_complete.json#TN_EVEIL_1_T3_003",
            "title": "Banque d'exercices 1ère année (fournie par l'utilisateur)",
            "license_status": "unlicensed",
            "subject_code": "science",
            "level_code": "1",
            "domain_hint": "etres_vivants",
            "trimester_hint": "T3",
            "region_scope": "tunisia_web",
            "content_snapshot": "Banque fournie par l'utilisateur : structure et sujet utilisés comme inspiration, explication ajoutée ici (absente de la source), contenu vérifié avant import.",
            "status": "used_for_generation"
        },
        "exercise": {
            "subject_code": "science",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "etres_vivants",
            "skill_code": "reproduction_croissance",
            "exercise_format": "qcm",
            "difficulty": "decouverte",
            "language": "ar",
            "content": {
                "question": "أَيُّ الحَيَوَانَاتِ التَّالِيَةِ يَلِدُ وَلَا بِيضُ ؟",
                "answer": "البَقَرَةُ",
                "explanation": "نفكر في طريقة تكاثر كل حيوان: يلد صغاره مباشرة أم يضع بيضًا؟ الإجابة هي البَقَرَةُ.",
                "choices": [
                    "الدَّجَاجَةُ",
                    "البَقَرَةُ",
                    "العُصْفُورُ"
                ]
            }
        }
    }
]


def main():
    with app.app_context():
        db.create_all()

        if Exercise.query.filter(Exercise.source_id.isnot(None)).join(Source).filter(Source.url.like("local://banque_exercices_1ere_complete.json%")).first() is not None:
            print("Bank examples already seeded, skipping.")
            return

        for example in EXAMPLES:
            source = Source(**example["source"])
            db.session.add(source)
            db.session.flush()

            generation_run = GenerationRun(
                source_id=source.id,
                model_provider="anthropic",
                model_name="claude-opus-5",
                prompt_template_version="v1-bank-import",
                status="success",
                raw_model_output="(bank import, not a real model call)",
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
        print(f"Seeded {len(EXAMPLES)} exercises from the user-supplied bank.")


if __name__ == "__main__":
    main()
