const trainingNowInputs = document.querySelectorAll('input[name="training_now"]');
const periodStepLabel = document.getElementById("period-step-label");

function syncTrainingLabel() {
    const selected = document.querySelector('input[name="training_now"]:checked');
    if (!selected || !periodStepLabel) {
        return;
    }

    if (selected.value === "yes") {
        periodStepLabel.textContent = "06 / Сколько времени тренируешься подряд";
    } else {
        periodStepLabel.textContent = "06 / Сколько не тренируешься";
    }
}

trainingNowInputs.forEach((input) => input.addEventListener("change", syncTrainingLabel));
syncTrainingLabel();

function smoothScrollToSection(targetId) {
    const target = document.getElementById(targetId);
    if (!target) {
        return;
    }

    const headerOffset = 110;
    const targetY = target.getBoundingClientRect().top + window.scrollY - headerOffset;
    window.scrollTo({ top: targetY, behavior: "smooth" });
}

document.addEventListener("click", (event) => {
    const link = event.target.closest('a[href="#how"], a[href="#start-cta"]');
    if (!link) {
        return;
    }

    event.preventDefault();
    smoothScrollToSection(link.getAttribute("href").slice(1));
});

if (document.getElementById("dashboard")) {
    document.getElementById("dashboard").scrollIntoView({ behavior: "smooth", block: "start" });
}
