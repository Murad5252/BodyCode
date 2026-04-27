from dataclasses import dataclass, field

level_status = ["beginner", "fanat", "pro", "legend"]

beginner_muscles = ["грудь", "спина", "квадрицепсы", "средняя дельта"]
fanat_only = ["бицепс", "трицепс", "пресс", "верх груди", "бицепс бедра"]
pro_only = ["передняя дельта", "задняя дельта", "икры", "приводящая ноги"]
legend_only = ["предплечья", "низ груди"]
woman_only = ["ягодицы"]

exercise_list = {
    "грудь": ["Жим штанги лежа", "Сведение рук"],
    "спина": ["Тяга верхнего блока", "Тяга гантели в наклоне", "Горизонтальная тяга"],
    "квадрицепсы": ["Приседания со штангой", "Разгибания ног", "Выпады с гантелями"],
    "бицепс бедра": ["Сгибания ног лежа", "Румынская тяга"],
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

hernia_keywords = ("приседания", "выпады", "румынская тяга", "ягодичный мост", "скручивания", "подъем ног в висе")
back_keywords = ("присед", "румынская", "тяга штанги в наклоне")
baza_keywords = ("станов", "присед", "штанг") 

knee_injury_keywords = ("присед", "выпад", "разгибание ног")
shoulder_injury_keywords = (
    "жим штанги лежа",
    "махи гантелями",
    "тяга к подбородку",
    "жим гантелей сидя",
)

ELBOW_EXCLUDE_KEYWORDS = (
    "французский жим",
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
    thigh: float
    calves: float
    biceps: float
    training_status: str
    training_experience: str | None = None
    training_pause: str | None = None
    goal: str = ""
    contraindications: list[str] = field(default_factory=list)


def varicocele_note(contraindications: list[str] | None) -> str | None:
    if not contraindications:
        return None
    if "varicocele" in contraindications:
        return "При варикоцеле избегайте задержки дыхания и чрезмерного натуживания, работайте в умеренном режиме."
    return None


def normalize_profile_data(cleaned_data: dict) -> dict:
    """Map form payload to QuizProfile fields and normalize training period semantics."""
    data = dict(cleaned_data)

    # Support both old and new field names from forms.
    training_now = data.get("training_now")
    if "training_status" not in data:
        if training_now == "yes":
            data["training_status"] = "training"
        elif training_now == "no":
            data["training_status"] = "not_training"

    period = data.get("training_period")
    if data.get("training_status") == "training":
        if "training_experience" not in data:
            # Form values: lt2w, w2_4, gt1m
            data["training_experience"] = {
                "lt2w": "lt1m",
                "w2_4": "m1_3",
                "gt1m": "m3_6",
            }.get(period)
        data.setdefault("training_pause", None)
    elif data.get("training_status") == "not_training":
        if "training_pause" not in data:
            data["training_pause"] = {
                "lt2w": "lt2w",
                "w2_4": "w2_4",
                "gt1m": "gt4w",
            }.get(period)
        data.setdefault("training_experience", None)

    # Form field `injury` may be one or many values; engine expects a flat list.
    if "contraindications" not in data:
        injury = data.get("injury")
        if isinstance(injury, list):
            data["contraindications"] = [item for item in injury if item]
        elif injury:
            data["contraindications"] = [injury]
        else:
            data["contraindications"] = []
    elif isinstance(data["contraindications"], str):
        data["contraindications"] = [data["contraindications"]]

    # Remove form-specific fields that are not part of QuizProfile
    data.pop("injury", None)
    data.pop("training_now", None)
    data.pop("training_period", None)
    data.pop("goal", None)

    return data

def calculate_bmi(weight: float, height_cm: float) -> float:
    return round(weight / ((height_cm / 100) ** 2), 1)


def resolve_level(profile: QuizProfile) -> str:
    if profile.gender == "female":
        if profile.training_status == "training":
            if profile.training_experience == "lt1m":
                return "beginner"
            return "pro"

        if profile.training_status == "not_training":
            if profile.training_pause == "lt2w":
                return "pro"
            return "beginner"

    if profile.training_status == "training":
        if profile.training_experience == "lt1m":
            return "beginner"
        if profile.training_experience == "m1_3":
            return "fanat"
        if profile.training_experience == "m3_6":
            return "pro"
        if profile.training_experience == "gt6m":
            return "legend"

    if profile.training_status == "not_training":
        if profile.training_pause == "lt2w":
            return "pro"
        if profile.training_pause == "w2_4":
            return "fanat"
        if profile.training_pause == "gt4w":
            return "beginner"

    # Safe fallback for unknown/missing periods.
    return "beginner"

def resolve_program_type(profile: QuizProfile, level: str) -> str:
    if profile.gender == "female":
        if level == "beginner": 
            return "Фулбади" 
        return "Верх-низ"

    if level == "beginner":
        return "Фулбади"
    if level == "fanat":
        return "Тяни-толкай"
    if level == "pro":
        return "Тяни-толкай-ноги"
    return "Бро-сплит"


def circumference_focus(profile: QuizProfile, level: str) -> dict:
    weakest = []
    add_sets = {}

    # Новички работают без акцентов
    if level == "beginner":
        return {
            "weakest": weakest,
            "add_sets": add_sets,
        }

    chest_ref = profile.hips * (0.97 if profile.gender == "female" else 1.0)
    calves_ref = profile.thigh * 0.6
    hips_ref = profile.waist * (1.25 if profile.gender == "female" else 1.1)
    thigh_ref = profile.hips * 0.58
    biceps_ref = profile.chest * (0.34 if profile.gender == "female" else 0.36)

    if profile.chest < chest_ref:
        weakest.append("грудь")
        add_sets["грудь"] = add_sets.get("грудь", 0) + 1
        add_sets["спина"] = add_sets.get("спина", 0) + 1

    if profile.calves < calves_ref:
        weakest.append("икры")
        if level not in ("beginner", "fanat"):
            add_sets["икры"] = add_sets.get("икры", 0) + 1

    if profile.hips < hips_ref:
        weakest.append("бедра")
        if profile.gender == "female":
            add_sets["ягодицы"] = add_sets.get("ягодицы", 0) + 1

    if profile.thigh < thigh_ref:
        weakest.append("бедро")
        add_sets["бицепс бедра"] = add_sets.get("бицепс бедра", 0) + 1
        add_sets["квадрицепсы"] = add_sets.get("квадрицепсы", 0) + 1

    if profile.biceps < biceps_ref:
        weakest.append("бицепс")
        add_sets["бицепс"] = add_sets.get("бицепс", 0) + 1
        add_sets["трицепс"] = add_sets.get("трицепс", 0) + 1

    return {
        "weakest": sorted(set(weakest)),
        "add_sets": add_sets,
    }


def build_muscle_groups(level: str) -> list[str]:
    groups = beginner_muscles.copy()
    if level in ("fanat", "pro", "legend"):
        groups += fanat_only
    if level in ("pro", "legend"):
        groups += pro_only
    if level == "legend":
        groups += legend_only
    return groups


def apply_contra_filters(exercises: list[str], contraindications: list[str]) -> list[str]:
    if not contraindications:
        return exercises

    selected_contra = set(contraindications)
    has_axial_contra = bool(selected_contra & {"hernia", "spine_disc"})
    filtered = []
    for exercise in exercises:
        exercise_l = exercise.lower()

        # Осевая/грыжевая группа противопоказаний
        if has_axial_contra:
            if any(keyword in exercise_l for keyword in hernia_keywords):
                continue
            if any(keyword in exercise_l for keyword in back_keywords):
                continue
            if any(keyword in exercise_l for keyword in baza_keywords):
                continue

        # Локальные травмы суставов
        if "injury_knee" in selected_contra and any(k in exercise_l for k in knee_injury_keywords):
            continue
        if "injury_shoulder" in selected_contra and any(k in exercise_l for k in shoulder_injury_keywords):
            continue
        if "injury_elbow" in selected_contra and any(k in exercise_l for k in ELBOW_EXCLUDE_KEYWORDS):
            continue

        filtered.append(exercise)
    return filtered


def get_available_exercises_for_group(
    group: str,
    contraindications: list[str],
    count: int = 2
) -> list[str]:
    """
    Получить пригодные упражнения для группы мышц, учитывая противопоказания.

    Args:
        group: название мышечной группы
        contraindications: список противопоказаний пользователя
        count: количество упражнений для подбора

    Returns:
        Список упражнений размером до 'count', отфильтрованных по противопоказаниям
    """
    all_exercises = exercise_list.get(group, [])
    if not all_exercises:
        return []

    # Фильтруем ВСЕ упражнения группы по противопоказаниям
    available = apply_contra_filters(all_exercises, contraindications)

    # Возвращаем до 'count' пригодных упражнений
    return available[:count]


def resolve_load(profile: QuizProfile, level: str, bmi: float) -> dict:
    sets = 2
    reps = "10-15"
    cardio = "10-15 минут после силовой"

    if level == "beginner":
        sets = 2
        reps = "10-15"
    elif level == "fanat":
        sets = 3
        reps = "10-15"
    elif level == "pro":
        sets = 3
        reps = "8-12"
    elif level == "legend":
        sets = 4
        reps = "8-12"

    if profile.training_status == "not_training" and profile.training_pause == "w2_4":
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
            {"day": "День 1 (Пн)", "focus": "Тяни/Толкай (чередование)"},
            {"day": "День 2 (Ср)", "focus": "Толкай/Тяни (чередование)"},
            {"day": "День 3 (Пт)", "focus": "Тяни/Толкай (чередование)"},
        ]
    if program_type == "Верх-низ":
        return [
            {"day": "День 1 (Пн)", "focus": "Низ + ягодицы"},
            {"day": "День 2 (Ср)", "focus": "Верх"},
            {"day": "День 3 (Пт)", "focus": "Низ + ягодицы"},
        ]
    if program_type == "Тяни-толкай-ноги":
        return [
            {"day": "День 1 (Пн)", "focus": "Тяни"},
            {"day": "День 2 (Ср)", "focus": "Толкай"},
            {"day": "День 3 (Пт)", "focus": "Ноги"},
        ]
    return [
        {"day": "День 1 (Пн)", "focus": "Грудь+бицепс"},
        {"day": "День 2 (Вт)", "focus": "Спина+трицепс"},
        {"day": "День 3 (Ср)", "focus": "Ноги+плечи"},
    ]


def pick_exercises_for_day(
    focus: str,
    groups: list[str],
    contraindications: list[str],
    level: str,
    add_sets: dict[str, int] | None = None,
) -> list[str]:
    focus_l = focus.lower()

    # Подбираем мышечные группы под тип тренировочного дня
    if "тяни" in focus_l:
        requested_groups = ["спина", "бицепс", "средняя дельта", "задняя дельта"]
    elif "толкай" in focus_l:
        requested_groups = ["грудь", "трицепс", "передняя дельта", "пресс"]
    elif "ног" in focus_l or "низ" in focus_l:
        requested_groups = ["квадрицепсы", "бицепс бедра", "ягодицы", "икры", "пресс"]
    elif "груд" in focus_l:
        requested_groups = ["грудь", "трицепс"]
    elif "спина" in focus_l:
        requested_groups = ["спина", "бицепс", "задняя дельта"]
    elif "плеч" in focus_l:
        requested_groups = ["средняя дельта", "передняя дельта", "задняя дельта", "предплечья"]
    else:
        requested_groups = [group for group in groups if group in beginner_muscles]

    # Оставляем только группы, разрешенные для текущего уровня.
    selected_groups = [group for group in requested_groups if group in groups]

    max_exercises_per_group = 1 if level == "beginner" else 2
    exercises_for_day = []

    for group in selected_groups:
        # Получаем упражнения уже отфильтрованные по противопоказаниям
        base_exercises = get_available_exercises_for_group(
            group,
            contraindications,
            count=max_exercises_per_group
        )
        exercises_for_day.extend(base_exercises)

        # Акцент реализуется как дополнительный подход к первому упражнению группы.
        if add_sets and add_sets.get(group, 0) > 0 and base_exercises:
            exercises_for_day.append(f"{base_exercises[0]} (доп. подход на акцент)")

    return exercises_for_day

def generate_program(cleaned_data: dict) -> dict:
    normalized_data = normalize_profile_data(cleaned_data)
    profile = QuizProfile(**normalized_data)
    bmi = calculate_bmi(profile.weight, profile.height)
    level = resolve_level(profile)
    program_type = resolve_program_type(profile, level)
    load = resolve_load(profile, level, bmi)
    focus = circumference_focus(profile, level)
    groups = build_muscle_groups(level)
    week_plan = build_week_plan(program_type, profile.gender)

    exercises_by_day = []
    for day in week_plan:
        day_exercises = pick_exercises_for_day(
            day["focus"],
            groups,
            profile.contraindications,
            level,
            add_sets=focus.get("add_sets"),
        )
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
    training_period = normalized_data.get("training_period")
    if profile.training_status == "not_training" and training_period == "w2_4":
        recommendations.append("Первые 1-2 недели после перерыва держите нагрузку ниже обычной.")
    if profile.training_status == "not_training" and training_period == "gt1m":
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