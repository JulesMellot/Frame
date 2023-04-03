function toggleMode() {
    var body = document.querySelector('body');
    body.classList.toggle('dark-mode');
    var btn = document.querySelector('.toggle-mode-btn');
    if (btn.innerText === 'Dark Mode') {
      btn.innerText = 'Light Mode';
    } else {
      btn.innerText = 'Dark Mode';
    }
  }
  