// Signup: opens the visitor's email app with a ready-to-send request to join the list.
(function () {
  var TO = 'kjadhithya05@gmail.com';
  document.querySelectorAll('form[data-signup]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type=email]');
      var note = form.nextElementSibling;
      var email = (input.value || '').trim();
      if (!input.checkValidity() || !email) {
        input.reportValidity();
        return;
      }
      var subject = 'Ctrl+Curious signup: ' + email;
      var body = 'Hi,\n\nPlease add me to the Ctrl+Curious daily emails.\n\nEmail: ' + email + '\n';
      window.location.href = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      if (note) note.textContent = 'Your email app should open with the request ready. Hit send and you will be added.';
    });
  });
})();
