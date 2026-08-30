/*
 * SmartProf — Traducteur pédagogique Français ↔ Arabe
 * Version 0.2.0
 */

const SmartProfTranslator = {

    version: "0.2.0",

    supportedLanguages: ["fr", "ar"],

    persons: {
        Yassine: { ar: "ياسين", gender: "m" },
        Meriem: { ar: "مريم", gender: "f" },
        Lina: { ar: "لينا", gender: "f" },
        Sami: { ar: "سامي", gender: "m" },
        Amine: { ar: "أمين", gender: "m" },
        Ahmed: { ar: "أحمد", gender: "m" },
        Ali: { ar: "علي", gender: "m" },
        Aya: { ar: "آية", gender: "f" },
        Sara: { ar: "سارة", gender: "f" }
    },

    objects: {
        pomme: {
            frSingular: "pomme",
            frPlural: "pommes",
            arSingular: "تفاحة",
            arPlural: "تفاحات"
        },
        orange: {
            frSingular: "orange",
            frPlural: "oranges",
            arSingular: "برتقالة",
            arPlural: "برتقالات"
        },
        ballon: {
            frSingular: "ballon",
            frPlural: "ballons",
            arSingular: "كرة",
            arPlural: "كرات"
        },
        stylo: {
            frSingular: "stylo",
            frPlural: "stylos",
            arSingular: "قلم",
            arPlural: "أقلام"
        },
        carnet: {
            frSingular: "carnet",
            frPlural: "carnets",
            arSingular: "دفتر",
            arPlural: "دفاتر"
        },
        livre: {
            frSingular: "livre",
            frPlural: "livres",
            arSingular: "كتاب",
            arPlural: "كتب"
        },
        crayon: {
            frSingular: "crayon",
            frPlural: "crayons",
            arSingular: "قلم رصاص",
            arPlural: "أقلام رصاص"
        },
        jouet: {
            frSingular: "jouet",
            frPlural: "jouets",
            arSingular: "لعبة",
            arPlural: "ألعاب"
        }
    },

    grammar: {
        m: {
            has: "لديه",
            friend: "صديقه",
            gave: "أعطاه",
            became: "أصبح لديه"
        },
        f: {
            has: "لديها",
            friend: "صديقتها",
            gave: "أعطاها",
            became: "أصبح لديها"
        }
    },

    getPerson(name) {
        return this.persons[name] || {
            ar: name,
            gender: "m"
        };
    },

    getObject(object) {
        return this.objects[object] || null;
    },

    getArabicObject(object, quantity) {
        const item = this.getObject(object);

        if (!item) {
            return object;
        }

        return quantity === 1
            ? item.arSingular
            : item.arPlural;
    },


    translateSkill(skill, format, data={}) {
        const fr = {
            tri: "Trie les éléments selon la consigne.",
            classement: "Classe les éléments selon la consigne.",
            correspondance: "Associe chaque élément à celui qui lui correspond.",
            rangement: "Range les éléments dans l’ordre demandé.",
            rythmes: "Complète la suite en respectant le rythme."
        };

        const ar = {
            tri: "رتّب العناصر حسب المطلوب.",
            classement: "صنّف العناصر حسب المطلوب.",
            correspondance: "اربط كل عنصر بالعنصر الذي يناسبه.",
            rangement: "رتّب العناصر حسب الترتيب المطلوب.",
            rythmes: "أكمل النمط مع احترام الترتيب."
        };

        const formats = {
            selection: "اختر الإجابة الصحيحة.",
            drag_drop: "اسحب العناصر وضعها في المكان الصحيح.",
            association: "اربط كل عنصر بما يناسبه.",
            classement: "صنّف العناصر في المكان المناسب.",
            suite_visuelle: "أكمل النمط البصري."
        };

        if (!fr[skill] || !formats[format])
            return null;

        return {
            skill,
            format,
            instruction_fr: fr[skill],
            instruction_ar: ar[skill],
            format_ar: formats[format]
        };
    },


    translateNumeration(skill, format, data={}) {
        const ar = {
            denombrement: "عدّ العناصر.",
            reconnaissance_quantite: "تعرّف على الكمية.",
            lecture_nombre: "اقرأ العدد.",
            ecriture_nombre: "اكتب العدد.",
            suite_numerique: "أكمل السلسلة العددية.",
            precedent_suivant: "حدّد العدد السابق والعدد اللاحق.",
            ordre_nombres: "رتّب الأعداد حسب المطلوب.",
            composition: "كوّن العدد.",
            decomposition: "فكّك العدد.",
            nombre_manquant: "أوجد العدد الناقص."
        };

        const formats = {
            comptage: "عدّ العناصر.",
            selection: "اختر الإجابة الصحيحة.",
            association: "اربط العدد بالكمية المناسبة.",
            qcm: "اختر الإجابة الصحيحة من بين الاقتراحات.",
            saisie_nombre: "اكتب العدد الصحيح.",
            classement: "رتّب الأعداد.",
            drag_drop: "اسحب العناصر وضعها في المكان الصحيح."
        };

        if (!ar[skill] || !formats[format]) return null;

        return {
            skill,
            format,
            instruction_ar: ar[skill],
            format_ar: formats[format]
        };
    },

    translateCalcul(skill, format, data={}) {
        const ar = {
            addition: "احسب عملية الجمع.",
            calcul_mental: "احسب ذهنيًا.",
            egalite: "تحقّق من المساواة.",
            situations_additives: "حلّ المسألة."
        };

        const formats = {
            calcul: "احسب.",
            qcm: "اختر الإجابة الصحيحة.",
            saisie_nombre: "اكتب العدد الصحيح.",
            selection: "اختر الإجابة الصحيحة.",
            probleme: "حلّ المسألة.",
            recit: "اقرأ القصة وأجب عن السؤال."
        };

        if (!ar[skill] || !formats[format]) return null;

        return {
            skill,
            format,
            instruction_ar: ar[skill],
            format_ar: formats[format]
        };
    },

    translateGeometry(skill, format, data={}) {
        const ar = {
            positions: "حدّد موقع العنصر.",
            gauche_droite: "حدّد اليسار واليمين.",
            haut_bas: "حدّد الأعلى والأسفل.",
            dessus_dessous: "حدّد فوق وتحت.",
            dedans_dehors: "حدّد داخل وخارج.",
            devant_derriere: "حدّد أمام وخلف.",
            pres_loin: "حدّد القريب والبعيد.",
            entre: "حدّد العنصر الموجود بين عنصرين.",
            lignes: "تعرّف على الخطوط.",
            formes: "تعرّف على الأشكال الهندسية.",
            frises: "أكمل الإفريز.",
            pavages: "أكمل التبليط.",
            traces: "تتبّع وارسم حسب المطلوب."
        };

        const formats = {
            selection: "اختر الإجابة الصحيحة.",
            visuel: "انظر إلى الشكل ثم اختر الإجابة الصحيحة.",
            association: "اربط كل شكل بما يناسبه.",
            suite_visuelle: "أكمل النمط البصري.",
            "tracé": "تتبّع وارسم حسب المطلوب."
        };

        if (!ar[skill] || !formats[format]) return null;

        return {
            skill,
            format,
            instruction_ar: ar[skill],
            format_ar: formats[format]
        };
    },

    translateMeasures(skill,format){const a={comparaison_longueurs:"قارن بين الأطوال.",rangement_longueurs:"رتّب الأطوال حسب المطلوب.",comparaison_masses:"قارن بين الكتل."};const f={selection:"اختر الإجابة الصحيحة.",classement:"رتّب العناصر حسب المطلوب.",drag_drop:"اسحب العناصر وضعها في الترتيب الصحيح."};return a[skill]&&f[format]?{skill,format,instruction_ar:a[skill],format_ar:f[format]}:null;},

    translateProblems(skill, format, data={}) {
        const ar = {
            identifier_information: "حدّد المعلومات المهمة في المسألة.",
            choisir_operation: "اختر العملية المناسبة لحل المسألة.",
            resoudre: "حلّ المسألة.",
            expliquer_demarche: "اشرح طريقة الحل.",
            recit_multi_questions: "اقرأ القصة وأجب عن الأسئلة."
        };

        const formats = {
            probleme: "حلّ المسألة.",
            selection: "اختر الإجابة الصحيحة.",
            saisie_nombre: "اكتب العدد الصحيح.",
            "réponse_libre": "اكتب إجابتك واشرح طريقة الحل.",
            recit: "اقرأ القصة ثم أجب.",
            multi_questions: "أجب عن جميع الأسئلة."
        };

        if (!ar[skill] || !formats[format]) return null;

        return {
            skill,
            format,
            instruction_ar: ar[skill],
            format_ar: formats[format]
        };
    },

    translateStoryToArabic({
        person,
        object,
        startNumber,
        addedNumber
    }) {
        const p = this.getPerson(person);
        const item = this.getObject(object);

        if (!item) {
            throw new Error("Objet non reconnu : " + object);
        }

        const objectStart = this.getArabicObject(object, startNumber);
        const objectAdded = this.getArabicObject(object, addedNumber);
        const total = startNumber + addedNumber;
        const objectTotal = this.getArabicObject(object, total);
        const g = this.grammar[p.gender];

        return {
            story:
                "لدى " + p.ar + " " +
                startNumber + " " + objectStart +
                "، و" + g.gave + " " + g.friend + " " + addedNumber + " " + objectAdded + " أخرى.",

            questions: [
                {
                    q:
                        "كم عدد " + objectTotal +
                        " التي أصبحت عند " + p.ar + "؟",
                    answer: total,
                    explanation:
                        "لنحل المسألة خطوة بخطوة. في البداية كان " +
                        (p.gender === "f" ? "لدى " : "لدى ") +
                        p.ar + " " + startNumber + " " +
                        objectStart + ". ثم " +
                        g.gave + " " + addedNumber + " " +
                        objectAdded + " أخرى. " +
                        "أصبح العدد أكبر، لذلك نستخدم عملية الجمع. " +
                        "نحسب: " + startNumber + " + " +
                        addedNumber + " = " + total + ". " +
                        "إذن أصبح لدى " + p.ar + " " +
                        total + " " + objectTotal + "."
                },
                {
                    q:
                        "كم كان لدى " + p.ar + " في البداية؟",
                    answer: startNumber,
                    explanation:
                        "نعود إلى بداية القصة. كان لدى " +
                        p.ar + " " + startNumber + " " +
                        objectStart + ". " +
                        "إذن العدد الموجود في البداية هو " +
                        startNumber + "."
                },
                {
                    q:
                        "كم " + objectAdded + " أعطى صديق " + p.ar + "؟",
                    answer: addedNumber,
                    explanation:
                        "نعود إلى الجملة الثانية من القصة. " +
                        g.friend + " أعطى " + p.ar + " " + addedNumber + " " +
                        objectAdded + ". " +
                        "إذن العدد الذي أُضيف هو " +
                        addedNumber + "."
                }
            ]
        };
    },

    translate(text, from, to, context = {}) {
        if (!text || from === to) {
            return text;
        }

        if (!this.supportedLanguages.includes(from) ||
            !this.supportedLanguages.includes(to)) {
            throw new Error("Langue non supportée.");
        }

        if (
            from === "fr" &&
            to === "ar" &&
            context.type === "story" &&
            context.person &&
            context.object
        ) {
            return this.translateStoryToArabic(context);
        }

        return text;
    }
};

if (typeof window !== "undefined") {
    window.SmartProfTranslator = SmartProfTranslator;
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = SmartProfTranslator;
}
