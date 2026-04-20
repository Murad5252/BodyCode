from django import forms

_PARAM = {"class": "param-input__el"}


class QuizForm(forms.Form):
    gender = (
        ("male", "Мужчина"),
        ("female", "Женщина"),
    )

    traning_status = (
        ("yes", "Да"),
        ("no", "Нет"),
    )
    experience = (
        ("lt2w", "< 2 недель"),
        ("w2_4", "2-4 недели"),
        ("gt1m", "> 1 месяца"),
    )

    goal = (
        ("cut", "Похудение"),
        ("bulk", "Набор массы"),
        ("maintenance", "Поддержание"),
    )

    contraindications = (
        ("protrusion", "Протрузии / грыжа позвоночника"),
        ("hernia_inguinal", "Паховая грыжа"),
        ("hernia_umbilical", "Пупочная грыжа"),
        ("hernia_femoral", "Бедренная грыжа"),
        ("hernia_linea_alba", "Грыжа белой линии живота"),
        ("injury_knee", "Травма колена"),
        ("injury_elbow", "Травма локтя"),
        ("injury_shoulder", "Травма плеча"),
        ("varicocele", "Варикоцеле"),
    )

    gender = forms.ChoiceField(
        label="Пол",
        choices=gender,
        widget=forms.RadioSelect,
    )

    age = forms.IntegerField(
        label="Возраст",
        min_value=12,
        max_value=90,
        widget=forms.NumberInput(
            attrs={**_PARAM, "placeholder": "28", "min": "12", "max": "90"}),
    )

    weight = forms.FloatField(
        label="Вес (кг)",
        min_value=30,
        max_value=250,
        widget=forms.NumberInput(
            attrs={**_PARAM, "placeholder": "75", "step": "0.1", "min": "30", "max": "250"}),
    )

    height = forms.FloatField(
        label="Рост (см)",
        min_value=120,
        max_value=230,
        widget=forms.NumberInput(
            attrs={**_PARAM, "placeholder": "178", "step": "0.1", "min": "120", "max": "230"}),
    )

    chest = forms.FloatField(
        label="Обхват груди (см)",
        min_value=40,
        max_value=200,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )

    waist = forms.FloatField(
        label="Обхват талии (см)",
        min_value=40,
        max_value=200,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )
    
    hips = forms.FloatField(
        label="Обхват бедер (см)",
        min_value=40,
        max_value=220,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )

    forearm = forms.FloatField(
        label="Обхват предплечья (см)",
        min_value=15,
        max_value=60,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )

    calves = forms.FloatField(
        label="Обхват икры (см)",
        min_value=20,
        max_value=70,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )

    biceps = forms.FloatField(
        label="Обхват бицепса (см)",
        min_value=15,
        max_value=70,
        widget=forms.NumberInput(attrs={**_PARAM, "step": "0.1"}),
    )

    training_now = forms.ChoiceField(
        label="Тренируется ли сейчас",
        choices=traning_status,
        widget=forms.RadioSelect,
    )

    training_period = forms.ChoiceField(
        label="Период тренировок / перерыва",
        choices=experience,
        widget=forms.RadioSelect,
    )

    goal = forms.ChoiceField(
        label="Цель", 
        choices=goal, 
        widget=forms.RadioSelect,
        )

    contraindications = forms.MultipleChoiceField(
        label="Противопоказания", 
        choices=contraindications,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        )
