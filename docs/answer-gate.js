// Behaviour for the "type an answer, then reveal" boxes used across worksheets.
// Enables the "Show answer" button once the student has typed something,
// then toggles the hidden answer div when the button is clicked.

document.addEventListener('input', function (e) {
  if (e.target.matches('.answer-input')) {
    const box = e.target.closest('.answer-box');
    box.querySelector('.reveal-btn').disabled = e.target.value.trim().length === 0;
  }
});

document.addEventListener('click', function (e) {
  if (e.target.matches('.reveal-btn') && !e.target.disabled) {
    const box = e.target.closest('.answer-box');
    const ans = box.querySelector('.answer');
    const showing = ans.style.display === 'block';
    ans.style.display = showing ? 'none' : 'block';
    e.target.textContent = showing ? 'Show answer' : 'Hide answer';
  }
});
