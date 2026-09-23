// Uzbek Travel — site interactions
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var MSG = {
    en: { dates: 'Departure date must be after your arrival date.', sending: 'Sending…', fail: 'Sorry, something went wrong. Please email us directly at info.uzbektravelguide@gmail.com' },
    ru: { dates: 'Дата отъезда должна быть позже даты приезда.', sending: 'Отправляем…', fail: 'Извините, что-то пошло не так. Пожалуйста, напишите нам напрямую: info.uzbektravelguide@gmail.com' },
    es: { dates: 'La fecha de salida debe ser posterior a la de llegada.', sending: 'Enviando…', fail: 'Lo sentimos, algo salió mal. Escríbenos directamente a info.uzbektravelguide@gmail.com' }
  }[L] || null;
  if (!MSG) MSG = { dates: 'Departure date must be after your arrival date.', sending: 'Sending…', fail: 'Sorry, something went wrong. Please email info.uzbektravelguide@gmail.com' };
  // mobile nav
  var t = document.querySelector('.nav-toggle'), links = document.querySelector('.nav-links');
  if (t && links) t.addEventListener('click', function () {
    var open = links.classList.toggle('open'); t.setAttribute('aria-expanded', open);
  });

  // tour filter bar (tours page)
  var fb = document.querySelectorAll('.filters button');
  fb.forEach(function (b) {
    b.addEventListener('click', function () {
      fb.forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
      var f = b.dataset.filter;
      document.querySelectorAll('.cards [data-cat]').forEach(function (c) {
        c.style.display = (f === 'all' || c.dataset.cat.split(' ').indexOf(f) > -1) ? '' : 'none';
      });
    });
  });

  // booking form -> FormSubmit (emails info.uzbektravelguide@gmail.com)
  var form = document.getElementById('booking-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.querySelector('[name="_honey"]').value) return;           // spam trap
    var a = form.querySelector('[name="arrival"]').value, d = form.querySelector('[name="departure"]').value;
    if (a && d && d < a) { alert(MSG.dates); return; }
    var btn = form.querySelector('button[type="submit"]'), label = btn.textContent;
    btn.disabled = true; btn.textContent = MSG.sending;
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && String(data.success) === 'false') throw new Error(data.message || 'not sent');  // e.g. inbox not activated yet
        document.getElementById('form-success').style.display = 'block';
        form.reset(); form.querySelectorAll('.row,.two,button').forEach(function (el) { el.style.display = 'none'; });
        document.getElementById('form-success').scrollIntoView({ behavior: 'smooth', block: 'center' });
      })
      .catch(function () {
        btn.disabled = false; btn.textContent = label;
        alert(MSG.fail);
      });
  });

  // preselect tour from ?tour= on the contact page
  var sel = document.querySelector('select[name="tour"]'), q = new URLSearchParams(location.search).get('tour');
  if (sel && q) Array.prototype.forEach.call(sel.options, function (o) { if (o.value === q) o.selected = true; });
})();
