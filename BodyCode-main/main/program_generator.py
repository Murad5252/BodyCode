from dataclasses import dataclass

MAJOR_MUSCLES = ["грудь", "спина", "квадрицепсы", "средняя дельта"]
INTERMEDIATE_ONLY = ["бицепс", "трицепс", "пресс", "верх груди", "бицепс бедра"]
ADVANCED_ONLY = ["передняя дельта", "задняя дельта", "предплечья"]

EXERCISE_POOL = {
    "грудь": ["Жим штанги лежа", "Сведение рук в кроссовере"],
    "спина": ["Тяга верхнего блока", "Тяга гантели в наклоне", "Горизонтальная тяга"],
    "квадрицепсы": ["Приседания со штангой", "Выпады с гантелями", "Разгибания ног"],
    "бицепс бедра": ["Румынская тяга", "Сгибания ног лежа"],
    "средняя дельта": ["Тяга к подбородку с EZ-грифом", "Махи гантелями в стороны"],
    "бицепс": ["Подъем гантелей на бицепс", "Подъем EZ-грифа на бицепс"],
    "трицепс": ["Разгибание рук на блоке", "Французский жим гантели сидя"],
    "пресс": ["Скручивания", "Подъем ног в висе"],
    "передняя дельта": ["Жим гантелей сидя", "Подъем гантелей перед собой"],
    "задняя дельта": ["Обратные разведения в тренажере", "Махи в наклоне"],
    "предплечья": ["Сгибание кистей", "Разгибание кистей"],
    "ягодицы": ["Ягодичный мост", "Разведение ног в тренажере"],
    "икры": ["Подъемы на носки стоя", "Подъемы на носки сидя"],
}

AXIAL_LOAD_KEYWORDS = ("присед", "станов", "жим штанги стоя", "тяга штанги")
spine_disc_keywords = ("приседания", "румынская тяга", "Ягодичный мост")
hernia_keywords = ("приседания", "выпады", "румынская тяга", "Ягодичный мост", "Скручивания", "Подъем ног в висе")
HEAVY_BASE_KEYWORDS = ("станов", "присед", "штанг")

# Противопоказания с осевой нагрузкой / вальсальвой (позвоночник и грыжи живота)
AXIAL_CONTRA_CODES = frozenset(
    {
        "spine_lumbar_disc",
        "spine_thoracic_disc",
        "hernia_inguinal",
        "hernia_umbilical",
        "hernia_femoral",
        "hernia_linea_alba",
        "hernia", 
        "protrusion",
    }
)

KNEE_EXCLUDE_KEYWORDS = ("присед", "жим ног", "выпад", "разгибание ног")
SHOULDER_EXCLUDE_KEYWORDS = (
    "отжиман",
    "махи гантелями",
    "тяга к подбородку",
    "жим гантелей",
    "подъем гантелей перед",
    "тяга верхнего блока",
)

ELBOW_EXCLUDE_KEYWORDS = (
    "французский",
    "разгибание рук",
    "подъем гантелей на бицепс",
    "подъем ez",
    "ez-грифа на бицепс",
)

PEC_BICEPS_TEAR_KEYWORDS = (
    "жим гантелей лежа",
    "отжиман",
    "сведение",
    "подъем гантелей на бицепс",
    "подъем ez",
)


@dataclass
class QuizProfile:
    gender: str
    age: int
    weight: float
    height: float
    chest: float
    waist: float
    hips: float
    forearm: float
    calves: float
    biceps: float
    training_now: str
    training_period: str
    goal: str
    contraindications: list[str]


def calculate_bmi(weight: float, height_cm: float) -> float:
    return round(weight / ((height_cm / 100) ** 2), 1)


def resolve_level(profile: QuizProfile) -> str:
    if profile.training_period == "gt1m":
        return "новичок"
    if profile.training_period == "w2_4":
        return "любитель"
    if profile.training_now == "yes" and profile.age < 45:
        return "опытный"
    return "новичок"


def resolve_program_type(profile: QuizProfile, level: str) -> str:
    if profile.gender == "female":
        if level == "новичок":
            return "Фулбади"
        return "Верх-низ"
    if level == "новичок":
        return "Фулбади"
    if level == "любитель":
        return "Тяни-толкай"
    return "Тяни-толкай-ноги"


def circumference_focus(profile: QuizProfile) -> dict:
    upper = (profile.chest + profile.biceps + profile.forearm) / 3
    lower = (profile.hips + profile.calves) / 2
    core = profile.waist

    weakest = []
    dominant = []
    if upper < lower * 0.88:
        weakest.extend(["грудь", "спина", "бицепс", "трицепс"])
    else:
        dominant.extend(["верх тела"])
    if lower < upper * 0.88:
        weakest.extend(["квадрицепсы", "бицепс бедра", "ягодицы", "икры"])
    else:
        dominant.extend(["низ тела"])
    if core > (profile.hips * 0.92):
        weakest.append("пресс")
    return {"weakest": weakest, "dominant": dominant}


def build_muscle_groups(level: str) -> list[str]:
    groups = MAJOR_MUSCLES.copy()
    if level in ("любитель", "опытный"):
        groups += INTERMEDIATE_ONLY
    if level == "опытный":
        groups += ADVANCED_ONLY
    return groups


def apply_contra_filters(exercises: list[str], contraindications: list[str]) -> list[str]:
    if not contraindications:
        return exercises

    contra = set(contraindications)
    axial = bool(contra & AXIAL_CONTRA_CODES)

    filtered = []
    for exercise in exercises:
        lowered = exercise.lower()
        if axial:
            if any(keyword in lowered for keyword in AXIAL_LOAD_KEYWORDS):
                continue
            if any(keyword in lowered for keyword in HEAVY_BASE_KEYWORDS):
                continue
        if "injury_knee" in contra and any(k in lowered for k in KNEE_EXCLUDE_KEYWORDS):
            continue
        if "injury_shoulder" in contra and any(k in lowered for k in SHOULDER_EXCLUDE_KEYWORDS):
            continue
        if "injury_elbow" in contra and any(k in lowered for k in ELBOW_EXCLUDE_KEYWORDS):
            continue
        if "tear_biceps_pectoral" in contra and any(k in lowered for k in PEC_BICEPS_TEAR_KEYWORDS):
            continue
        filtered.append(exercise)
    return filtered


def resolve_load(profile: QuizProfile, level: str, bmi: float) -> dict:
    sets = 2
    reps = "10-15"
    cardio = "10-15 минут после силовой"

    if level == "новичок":
        sets = 2 if profile.training_period == "gt1m" else 3
    elif level == "любитель":
        sets = 2
    else:
        sets = 2
        reps = "8-12"

    if profile.training_period == "w2_4":
        sets = max(1, sets - 1)

    if bmi < 18.5:
        cardio = "5-10 минут легкого кардио"
    elif bmi >= 25:
        reps = "12-18"
        cardio = "20-30 минут кардио 3-4 раза в неделю"

    if profile.age >= 40:
        sets = max(1, sets - 1)
    return {"sets": sets, "reps": reps, "cardio": cardio}


def build_week_plan(program_type: str, gender: str) -> list[dict]:
    if program_type == "Фулбади":
        return [{"day": "День 1 (Пн)", "focus": "Фулбади"}, {"day": "День 2 (Чт)", "focus": "Фулбади"}]
    if program_type == "Тяни-толкай":
        return [
            {"day": "День 1 (Пн)", "focus": "Тяни"},
            {"day": "День 2 (Ср)", "focus": "Толкай"},
            {"day": "День 3 (Пт)", "focus": "Тяни/Толкай (чередование)"},
        ]
    if program_type == "Верх-низ":
        return [
            {"day": "День 1 (Пн)", "focus": "Низ + ягодицы"},
            {"day": "День 2 (Ср)", "focus": "Верх"},
            {"day": "День 3 (Пт)", "focus": "Низ + ягодицы" if gender == "female" else "Низ"},
        ]
    if program_type == "Тяни-толкай-ноги":
        return [
            {"day": "День 1 (Пн)", "focus": "Тяни"},
            {"day": "День 2 (Ср)", "focus": "Толкай"},
            {"day": "День 3 (Пт)", "focus": "Ноги"},
        ]
    return [
        {"day": "День 1 (Пн)", "focus": "Грудь"},
        {"day": "День 2 (Вт)", "focus": "Спина"},
        {"day": "День 3 (Ср)", "focus": "Ноги"},
        {"day": "День 4 (Пт)", "focus": "Плечи/Руки"},
    ]


def pick_exercises_for_day(focus: str, groups: list[str], contraindications: list[str], level: str) -> list[str]:
    selected_groups = []
    focus_l = focus.lower()
    if "тяни" in focus_l:
        selected_groups = ["спина", "бицепс", "средняя дельта", "задняя дельта"]
    elif "толкай" in focus_l:
        selected_groups = ["грудь", "трицепс", "передняя дельта", "пресс"]
    elif "ног" in focus_l or "низ" in focus_l:
        selected_groups = ["квадрицепсы", "бицепс бедра", "ягодицы", "икры", "пресс"]
    elif "груд" in focus_l:
        selected_groups = ["грудь", "трицепс"]
    elif "спина" in focus_l:
        selected_groups = ["спина", "бицепс", "задняя дельта"]
    elif "плеч" in focus_l:
        selected_groups = ["средняя дельта", "передняя дельта", "задняя дельта", "предплечья"]
    else:
        selected_groups = [g for g in groups if g in MAJOR_MUSCLES]

    selected_groups = [g for g in selected_groups if g in groups]

    output = []
    for group in selected_groups:
        output.extend(EXERCISE_POOL.get(group, [])[: 1 if level == "новичок" else 2])
    return apply_contra_filters(output, contraindications)


def varicocele_note(contraindications: list[str]) -> str:
    if "varicocele" not in contraindications:
        return ""
    return "При варикоцеле используйте умеренные веса, избегайте пикового натуживания и работайте в средне-высоком диапазоне повторений."


def generate_program(cleaned_data: dict) -> dict:
    profile = QuizProfile(**cleaned_data)
    bmi = calculate_bmi(profile.weight, profile.height)
    level = resolve_level(profile)
    program_type = resolve_program_type(profile, level)
    load = resolve_load(profile, level, bmi)
    focus = circumference_focus(profile)
    groups = build_muscle_groups(level)
    week_plan = build_week_plan(program_type, profile.gender)

    exercises_by_day = []
    for day in week_plan:
        day_exercises = pick_exercises_for_day(day["focus"], groups, profile.contraindications, level)
        if profile.age >= 40:
            day_exercises = day_exercises[: max(3, len(day_exercises) - 1)]
        exercises_by_day.append(
            {
                "day": day["day"],
                "focus": day["focus"],
                "exercises": day_exercises,
            }
        )

    recommendations = []
    if bmi < 18.5:
        recommendations.append("Фокус на набор силовых показателей и умеренный профицит калорий.")
    elif bmi >= 25:
        recommendations.append("Добавьте кардио и контролируйте дефицит калорий для снижения веса.")
    else:
        recommendations.append("Сохраняйте стабильный режим питания и восстановления.")

    if focus["weakest"]:
        recommendations.append(f"Отстающие зоны для акцента: {', '.join(sorted(set(focus['weakest'])))}.")
    if focus["dominant"]:
        recommendations.append(f"Доминирующие зоны, держите меньший объем: {', '.join(focus['dominant'])}.")
    if profile.training_period == "w2_4":
        recommendations.append("Первые 1-2 недели после перерыва держите нагрузку ниже обычной.")
    if profile.training_period == "gt1m":
        recommendations.append("После длительного перерыва начинайте как новичок и увеличивайте объем постепенно.")

    varicocele_recommendation = varicocele_note(profile.contraindications)
    if varicocele_recommendation:
        recommendations.append(varicocele_recommendation)

    return {
        "bmi": bmi,
        "level": level,
        "program_type": program_type,
        "sets": load["sets"],
        "reps": load["reps"],
        "cardio": load["cardio"],
        "week_plan": week_plan,
        "exercises_by_day": exercises_by_day,
        "recommendations": recommendations,
        "focus": focus,
        "contraindications": profile.contraindications,
    }
