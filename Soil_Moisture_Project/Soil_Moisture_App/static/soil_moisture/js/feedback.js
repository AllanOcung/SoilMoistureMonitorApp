const feedbackopenButton = document.getElementById('feedbackbutton');
const feedbackcloseButton = document.getElementById('feedback-close');
const feedbackModal = document.getElementById('feedbackModal');

feedbackopenButton.addEventListener('click', () => {
  feedbackModal.classList.toggle('feedbackmodalon');
}
);

feedbackcloseButton.addEventListener('click', () => {
  feedbackModal.classList.toggle('feedbackmodalon');
}
);