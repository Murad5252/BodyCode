// Animated Quiz Logic
class AnimatedQuiz {
  constructor() {
    this.currentQuestion = 1;
    this.totalQuestions = 8;
    this.form = document.getElementById('animated-quiz-form');
    this.questions = document.querySelectorAll('.quiz-question');
    this.nextBtn = document.getElementById('next-btn');
    this.prevBtn = document.getElementById('prev-btn');
    this.submitBtn = document.getElementById('submit-btn');
    this.progressBar = document.querySelector('.progress-bar');
    this.currentQuestionSpan = document.getElementById('current-question');
    this.trainingNowInputs = document.querySelectorAll('input[name="training_now"]');

    this.init();
  }

  init() {
    this.showQuestion(1);
    this.attachEventListeners();
    this.syncTrainingLabel();
  }

  attachEventListeners() {
    this.nextBtn.addEventListener('click', () => this.nextQuestion());
    this.prevBtn.addEventListener('click', () => this.prevQuestion());
    this.trainingNowInputs.forEach(input => {
      input.addEventListener('change', () => this.syncTrainingLabel());
    });

    // Prevent form submission on Enter in input fields
    this.form.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
        e.preventDefault();
        this.nextQuestion();
      }
    });
  }

  showQuestion(questionNum) {
    // Hide all questions
    this.questions.forEach(q => {
      q.classList.remove('active', 'exit-left', 'exit-right');
    });

    // Show current question
    const currentQ = document.querySelector(`[data-question="${questionNum}"]`);
    if (currentQ) {
      currentQ.classList.add('active');
    }

    // Update progress bar
    const progress = (questionNum / this.totalQuestions) * 100;
    this.progressBar.style.setProperty('--progress', progress + '%');
    const progressAfter = this.progressBar.querySelector('::after');
    if (progressAfter || this.progressBar) {
      this.progressBar.style.setProperty('width', progress + '%', 'important');
    }
    // Update progress using pseudo-element
    this.updateProgressBar();

    this.currentQuestionSpan.textContent = questionNum;

    // Update button visibility
    if (questionNum === 1) {
      this.prevBtn.style.display = 'none';
      this.nextBtn.style.display = 'flex';
      this.submitBtn.style.display = 'none';
    } else if (questionNum === this.totalQuestions) {
      this.prevBtn.style.display = 'flex';
      this.nextBtn.style.display = 'none';
      this.submitBtn.style.display = 'flex';
    } else {
      this.prevBtn.style.display = 'flex';
      this.nextBtn.style.display = 'flex';
      this.submitBtn.style.display = 'none';
    }

    // Focus on first focusable element in the question
    const firstInput = currentQ?.querySelector('input, textarea, select');
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
  }

  updateProgressBar() {
    const percentage = (this.currentQuestion / this.totalQuestions) * 100;
    const style = document.createElement('style');
    style.textContent = `.progress-bar::after { width: ${percentage}% !important; }`;

    // Remove old style if exists
    const oldStyle = document.querySelector('style[data-quiz-progress]');
    if (oldStyle) oldStyle.remove();

    style.setAttribute('data-quiz-progress', 'true');
    document.head.appendChild(style);
  }

  nextQuestion() {
    if (this.currentQuestion < this.totalQuestions) {
      const currentQ = document.querySelector(`[data-question="${this.currentQuestion}"]`);
      currentQ.classList.add('exit-left');

      setTimeout(() => {
        this.currentQuestion++;
        this.showQuestion(this.currentQuestion);
      }, 300);
    }
  }

  prevQuestion() {
    if (this.currentQuestion > 1) {
      const currentQ = document.querySelector(`[data-question="${this.currentQuestion}"]`);
      currentQ.classList.add('exit-right');

      setTimeout(() => {
        this.currentQuestion--;
        this.showQuestion(this.currentQuestion);
      }, 300);
    }
  }

  syncTrainingLabel() {
    const selected = document.querySelector('input[name="training_now"]:checked');
    const trainingPeriodLabel = document.querySelector('[data-question="6"] .quiz-question__title');

    if (!selected || !trainingPeriodLabel) {
      return;
    }

    if (selected.value === 'yes') {
      trainingPeriodLabel.textContent = 'Сколько времени тренируешься подряд?';
    } else {
      trainingPeriodLabel.textContent = 'Сколько не тренируешься?';
    }
  }
}

// Initialize quiz when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new AnimatedQuiz();
  const resultOverlay = document.getElementById('quiz-result-overlay');
  const closeButton = document.getElementById('quiz-result-close');

  if (resultOverlay) {
    document.body.classList.add('modal-open');

    const closeOverlay = () => {
      resultOverlay.classList.remove('is-visible');
      document.body.classList.remove('modal-open');
    };

    if (closeButton) {
      closeButton.addEventListener('click', closeOverlay);
    }

    resultOverlay.addEventListener('click', (event) => {
      if (event.target === resultOverlay) {
        closeOverlay();
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && resultOverlay.classList.contains('is-visible')) {
        closeOverlay();
      }
    });
  }
});
