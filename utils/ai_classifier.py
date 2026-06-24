"""
GreenTech AI Classifier
=======================
Lightweight rule-based AI engine for:
  1. Device classification (free-text → standard category)
  2. Recyclability detection (category + condition → recyclable/not)
  3. Recycling recommendations (category + condition → tips list)

No heavy ML dependencies — fully compatible with Flask.
"""

# ─── Device keyword map (English + Arabic keywords) ───────────────────────────
DEVICE_KEYWORDS = {
    "Mobile": [
        "mobile", "phone", "smartphone", "iphone", "samsung", "huawei", "xiaomi",
        "oppo", "vivo", "nokia", "android", "ios", "cell", "cellular",
        "هاتف", "جوال", "موبايل", "سامسونج", "آيفون", "هواوي", "اندرويد"
    ],
    "Laptop": [
        "laptop", "notebook", "macbook", "thinkpad", "dell", "hp", "lenovo",
        "asus", "acer", "surface", "chromebook", "ultrabook",
        "لابتوب", "حاسوب محمول", "كمبيوتر محمول", "ماك بوك"
    ],
    "Tablet": [
        "tablet", "ipad", "galaxy tab", "kindle", "e-reader", "drawing tablet",
        "تابلت", "جهاز لوحي", "آيباد", "لوحي"
    ],
    "Desktop": [
        "desktop", "pc", "computer", "tower", "workstation", "imac", "all-in-one",
        "كمبيوتر", "حاسوب مكتبي", "برج", "كمبيوتر مكتبي"
    ],
    "TV": [
        "tv", "television", "monitor", "screen", "display", "lcd", "led", "oled",
        "plasma", "smart tv", "projector",
        "تلفزيون", "شاشة", "بلازما", "تلفاز", "مونيتر"
    ],
    "Printer": [
        "printer", "scanner", "copier", "fax", "inkjet", "laser printer",
        "طابعة", "ماسح ضوئي", "ناسخة"
    ],
    "Camera": [
        "camera", "dslr", "mirrorless", "webcam", "camcorder", "gopro",
        "كاميرا", "كاميرات"
    ],
    "Audio": [
        "headphone", "earphone", "speaker", "headset", "airpods", "earbuds",
        "soundbar", "stereo", "amplifier",
        "سماعة", "سماعات", "مكبر صوت"
    ],
    "Gaming": [
        "playstation", "xbox", "nintendo", "ps4", "ps5", "game console",
        "controller", "gamepad", "joystick",
        "بلايستيشن", "إكس بوكس", "جهاز ألعاب"
    ],
    "Appliance": [
        "microwave", "refrigerator", "washing machine", "vacuum", "iron",
        "blender", "coffee maker", "kettle", "toaster", "fan", "heater",
        "مايكرويف", "ثلاجة", "غسالة", "مكنسة", "حديدة", "خلاط"
    ],
    "Other": []
}

# ─── Recyclability rules ───────────────────────────────────────────────────────
RECYCLABILITY = {
    "Mobile":     {"recyclable": True,  "rate": 95, "reason_en": "Smartphones contain valuable metals (gold, copper, lithium) — highly recyclable.", "reason_ar": "الهواتف تحتوي على معادن ثمينة (ذهب، نحاس، ليثيوم) — قابلة لإعادة التدوير بنسبة عالية."},
    "Laptop":     {"recyclable": True,  "rate": 90, "reason_en": "Laptops contain reusable aluminum, copper and rare earth elements.", "reason_ar": "تحتوي الحواسيب المحمولة على ألومنيوم ونحاس وعناصر أرضية نادرة قابلة لإعادة الاستخدام."},
    "Tablet":     {"recyclable": True,  "rate": 90, "reason_en": "Tablets share similar recyclable components with smartphones.", "reason_ar": "تشترك الأجهزة اللوحية في مكونات قابلة لإعادة التدوير مشابهة للهواتف الذكية."},
    "Desktop":    {"recyclable": True,  "rate": 85, "reason_en": "Desktop computers have highly recoverable steel, copper and circuit boards.", "reason_ar": "تحتوي الحواسيب المكتبية على فولاذ ونحاس وبطاقات دوائر قابلة للاستعادة."},
    "TV":         {"recyclable": True,  "rate": 80, "reason_en": "TVs can be recycled — screens require careful handling due to hazardous materials.", "reason_ar": "يمكن إعادة تدوير أجهزة التلفزيون — تتطلب الشاشات معالجة دقيقة بسبب المواد الخطرة."},
    "Printer":    {"recyclable": True,  "rate": 75, "reason_en": "Printers contain recyclable plastic and metal parts.", "reason_ar": "تحتوي الطابعات على أجزاء بلاستيكية ومعدنية قابلة لإعادة التدوير."},
    "Camera":     {"recyclable": True,  "rate": 85, "reason_en": "Cameras contain precision metals and optics that can be recovered.", "reason_ar": "تحتوي الكاميرات على معادن دقيقة ومواد بصرية يمكن استعادتها."},
    "Audio":      {"recyclable": True,  "rate": 70, "reason_en": "Audio devices contain recyclable metals and plastics.", "reason_ar": "تحتوي الأجهزة الصوتية على معادن وبلاستيك قابلين لإعادة التدوير."},
    "Gaming":     {"recyclable": True,  "rate": 80, "reason_en": "Game consoles contain recyclable circuit boards and plastics.", "reason_ar": "تحتوي أجهزة الألعاب على لوحات دوائر وبلاستيك قابلين لإعادة التدوير."},
    "Appliance":  {"recyclable": True,  "rate": 70, "reason_en": "Home appliances contain significant amounts of recyclable metals.", "reason_ar": "تحتوي الأجهزة المنزلية على كميات كبيرة من المعادن القابلة لإعادة التدوير."},
    "Other":      {"recyclable": True,  "rate": 60, "reason_en": "Most electronic devices contain recyclable materials. Our team will assess it.", "reason_ar": "تحتوي معظم الأجهزة الإلكترونية على مواد قابلة لإعادة التدوير. سيقيّمها فريقنا."},
}

# ─── Recycling recommendations ────────────────────────────────────────────────
RECOMMENDATIONS = {
    "Mobile": {
        "en": [
            "🔒 Perform a factory reset and remove your SIM card before submission.",
            "🔋 Lithium batteries in phones require special certified handling — do not throw in regular trash.",
            "💎 Your phone contains gold, silver and rare earth metals that will be professionally recovered.",
            "📊 Recycling one million phones recovers ~35 lbs of copper, ~772 lbs of silver, ~75 lbs of gold.",
            "✅ Condition 'Not Working' is perfectly fine — components can still be salvaged.",
        ],
        "ar": [
            "🔒 قم بإعادة ضبط المصنع وإزالة شريحة SIM قبل التسليم.",
            "🔋 تتطلب بطاريات الليثيوم في الهواتف معالجة متخصصة معتمدة — لا تتخلص منها في القمامة العادية.",
            "💎 هاتفك يحتوي على ذهب وفضة ومعادن أرضية نادرة سيتم استعادتها باحترافية.",
            "📊 إعادة تدوير مليون هاتف تسترجع حوالي 35 رطلاً من النحاس و772 رطلاً من الفضة.",
            "✅ حالة 'لا يعمل' مقبولة تماماً — لا تزال المكونات قابلة للاستخدام.",
        ]
    },
    "Laptop": {
        "en": [
            "💾 Backup and securely wipe your data before submission (use tools like DBAN).",
            "🔋 Laptop batteries must be handled separately — they contain hazardous lithium compounds.",
            "🪙 Laptops contain aluminum chassis and copper wiring with high recovery value.",
            "⚡ Even a broken laptop with a cracked screen has ~80% recyclable components.",
            "♻️ One recycled laptop saves enough energy to power a home for 2 days.",
        ],
        "ar": [
            "💾 احتفظ بنسخة احتياطية وامسح بياناتك بشكل آمن قبل التسليم.",
            "🔋 يجب معالجة بطاريات اللابتوب بشكل منفصل — تحتوي على مركبات ليثيوم خطرة.",
            "🪙 تحتوي اللابتوبات على هيكل ألومنيوم وأسلاك نحاسية ذات قيمة استعادة عالية.",
            "⚡ حتى اللابتوب المعطوب يحتوي على ~80% من المكونات القابلة لإعادة التدوير.",
            "♻️ إعادة تدوير لابتوب واحد توفر طاقة كافية لتشغيل منزل لمدة يومين.",
        ]
    },
    "TV": {
        "en": [
            "⚠️ Old CRT TVs contain lead — they MUST be recycled through certified centers like ours.",
            "🔩 Modern LED/LCD TVs contain aluminum frames, copper wiring and recyclable glass.",
            "🚫 Never dispose of TVs in regular landfill — it's illegal in Saudi Arabia.",
            "📏 Large screens may require special pickup — contact the collection point in advance.",
        ],
        "ar": [
            "⚠️ أجهزة التلفزيون القديمة (CRT) تحتوي على رصاص — يجب إعادة تدويرها عبر مراكز معتمدة مثل مركزنا.",
            "🔩 أجهزة التلفزيون الحديثة (LED/LCD) تحتوي على إطارات ألومنيوم وأسلاك نحاسية وزجاج قابل لإعادة التدوير.",
            "🚫 لا تتخلص أبداً من أجهزة التلفزيون في مكبات النفايات العادية — فهذا مخالف للقانون في المملكة.",
            "📏 قد تتطلب الشاشات الكبيرة استلامًا خاصًا — تواصل مع نقطة التجميع مسبقًا.",
        ]
    },
    "Desktop": {
        "en": [
            "🖥️ Desktops are ~85% recyclable by weight — one of the most eco-friendly e-waste items.",
            "💾 Remove and destroy your hard drive (or use secure wipe software) before submission.",
            "🔩 RAM, CPUs and GPU cards have high metal recovery value.",
            "📦 Multiple components can be separated: case, motherboard, PSU — all recyclable.",
        ],
        "ar": [
            "🖥️ الحواسيب المكتبية قابلة لإعادة التدوير بنسبة ~85% من وزنها — من أكثر مخلفات الإلكترونيات صديقة للبيئة.",
            "💾 أزل القرص الصلب وأتلفه (أو استخدم برنامج مسح آمن) قبل التسليم.",
            "🔩 ذاكرة RAM والمعالجات وبطاقات GPU لها قيمة عالية من استعادة المعادن.",
            "📦 يمكن فصل المكونات المتعددة: الهيكل، اللوحة الأم، وحدة الطاقة — جميعها قابلة لإعادة التدوير.",
        ]
    },
    "Tablet": {
        "en": [
            "🔒 Erase all personal data and remove SD cards before submission.",
            "🔋 Like phones, tablet batteries need certified recycling handling.",
            "✨ Tablets contain high-purity aluminum and valuable display components.",
        ],
        "ar": [
            "🔒 امسح جميع البيانات الشخصية وأزل بطاقات SD قبل التسليم.",
            "🔋 مثل الهواتف، تحتاج بطاريات الأجهزة اللوحية إلى معالجة إعادة تدوير معتمدة.",
            "✨ تحتوي الأجهزة اللوحية على ألومنيوم عالي النقاء ومكونات شاشة ذات قيمة.",
        ]
    },
    "Printer": {
        "en": [
            "🖨️ Remove and properly dispose of ink/toner cartridges before submission.",
            "♻️ Printer casings are mostly recyclable ABS plastic.",
            "⚠️ Laser printer toner is considered hazardous — our team handles it safely.",
        ],
        "ar": [
            "🖨️ أزل خراطيش الحبر/مسحوق الحبر وتخلص منها بشكل صحيح قبل التسليم.",
            "♻️ هياكل الطابعات مصنوعة أساساً من بلاستيك ABS القابل لإعادة التدوير.",
            "⚠️ حبر الطابعات الليزرية يُعدّ خطرًا — يتولى فريقنا التعامل معه بأمان.",
        ]
    },
    "Camera": {
        "en": [
            "📸 Transfer and delete all photos/videos before submission.",
            "🔋 Remove batteries before submitting the camera.",
            "💡 Camera lenses contain rare optical glass and metals with recovery value.",
        ],
        "ar": [
            "📸 انقل واحذف جميع الصور/مقاطع الفيديو قبل التسليم.",
            "🔋 أزل البطاريات قبل تسليم الكاميرا.",
            "💡 تحتوي عدسات الكاميرا على زجاج بصري نادر ومعادن ذات قيمة استعادة.",
        ]
    },
    "Audio": {
        "en": [
            "🎧 Audio devices contain copper wiring and recyclable plastics.",
            "♻️ Even earbuds with dead batteries can be recycled for their metal components.",
        ],
        "ar": [
            "🎧 الأجهزة الصوتية تحتوي على أسلاك نحاسية وبلاستيك قابل لإعادة التدوير.",
            "♻️ حتى سماعات الأذن ذات البطاريات المستنفدة يمكن إعادة تدويرها لمكوناتها المعدنية.",
        ]
    },
    "Gaming": {
        "en": [
            "🎮 Perform a factory reset and delink your accounts before submission.",
            "🔩 Game consoles contain high-value circuit boards and GPU components.",
            "♻️ Controllers and accessories should also be submitted for recycling.",
        ],
        "ar": [
            "🎮 أجرِ إعادة ضبط المصنع وفصل حساباتك قبل التسليم.",
            "🔩 تحتوي أجهزة الألعاب على لوحات دوائر ومكونات GPU ذات قيمة عالية.",
            "♻️ يجب أيضًا تسليم وحدات التحكم والإكسسوارات لإعادة التدوير.",
        ]
    },
    "Appliance": {
        "en": [
            "🏠 Large appliances may require special pickup arrangements.",
            "⚠️ Refrigerants in fridges/ACs are environmentally hazardous — certified handling required.",
            "🔩 Appliances are mostly steel and copper — very high recyclability.",
        ],
        "ar": [
            "🏠 قد تتطلب الأجهزة الكبيرة ترتيبات استلام خاصة.",
            "⚠️ مبردات الثلاجات/المكيفات ضارة بالبيئة — يلزم التعامل المعتمد معها.",
            "🔩 الأجهزة المنزلية مصنوعة أساساً من الفولاذ والنحاس — قابلية إعادة التدوير عالية جداً.",
        ]
    },
    "Other": {
        "en": [
            "✅ Most electronic devices contain recyclable materials.",
            "📋 Our certified team will assess your device and determine the best recycling method.",
            "♻️ When in doubt — submit it! Recycling is always better than landfill.",
        ],
        "ar": [
            "✅ تحتوي معظم الأجهزة الإلكترونية على مواد قابلة لإعادة التدوير.",
            "📋 سيقيّم فريقنا المعتمد جهازك ويحدد أفضل طريقة لإعادة تدويره.",
            "♻️ عند الشك — سلّمه! إعادة التدوير دائماً أفضل من مكبات النفايات.",
        ]
    },
}

# ─── Category icons ────────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    "Mobile": "📱", "Laptop": "💻", "Tablet": "📲", "Desktop": "🖥️",
    "TV": "📺", "Printer": "🖨️", "Camera": "📸", "Audio": "🎧",
    "Gaming": "🎮", "Appliance": "🏠", "Other": "📦"
}


# ─── Core functions ────────────────────────────────────────────────────────────

def classify_device(device_name: str) -> dict:
    """
    Classify a free-text device name into a standard category.
    Returns: { category, icon, confidence, recyclable, rate }
    """
    if not device_name:
        return _build_result("Other", 50)

    text = device_name.lower().strip()
    scores = {cat: 0 for cat in DEVICE_KEYWORDS}

    for category, keywords in DEVICE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                # Exact word match scores higher
                if kw == text or f" {kw} " in f" {text} ":
                    scores[category] += 3
                else:
                    scores[category] += 1

    best_category = max(scores, key=lambda c: scores[c])
    best_score = scores[best_category]

    if best_score == 0:
        return _build_result("Other", 55)

    # Confidence: cap at 99%
    confidence = min(99, 60 + best_score * 10)
    return _build_result(best_category, confidence)


def _build_result(category: str, confidence: int) -> dict:
    rec = RECYCLABILITY.get(category, RECYCLABILITY["Other"])
    return {
        "category": category,
        "icon": CATEGORY_ICONS.get(category, "📦"),
        "confidence": confidence,
        "recyclable": rec["recyclable"],
        "recycle_rate": rec["rate"],
        "reason_en": rec["reason_en"],
        "reason_ar": rec["reason_ar"],
    }


def get_recommendations(device_type: str, condition: str, lang: str = "en") -> list:
    """
    Return a list of recycling recommendation strings.
    device_type: standard category string
    condition: 'Working' or 'Not Working'
    lang: 'en' or 'ar'
    """
    recs = RECOMMENDATIONS.get(device_type, RECOMMENDATIONS["Other"])
    tips = recs.get(lang, recs["en"])[:]  # copy the list

    # Add condition-specific tip
    if condition and "not" in condition.lower():
        if lang == "ar":
            tips.insert(0, "⚠️ الأجهزة غير العاملة مقبولة تماماً — يمكن الاستفادة من مكوناتها.")
        else:
            tips.insert(0, "⚠️ Non-working devices are fully accepted — their components can still be salvaged.")
    else:
        if lang == "ar":
            tips.insert(0, "✅ جهاز يعمل بشكل جيد — لديه أعلى قيمة لإعادة التدوير وأعلى إمكانية لإعادة الاستخدام.")
        else:
            tips.insert(0, "✅ Working device — highest recycling value and reuse potential.")

    return tips


def get_all_categories() -> list:
    """Return list of all standard categories with icons."""
    return [{"name": k, "icon": v} for k, v in CATEGORY_ICONS.items()]
