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
  // Messages are shown ON the page (not alert()) — in-app browsers like WhatsApp/Instagram silently block alerts.
  var form = document.getElementById('booking-form');
  if (form) {
    var errBox = document.getElementById('form-error'), okBox = document.getElementById('form-success');
    var showErr = function (msg) { errBox.textContent = msg; errBox.style.display = 'block'; errBox.scrollIntoView({ behavior: 'smooth', block: 'center' }); };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errBox.style.display = 'none';
      var a = form.querySelector('[name="arrival"]').value, d = form.querySelector('[name="departure"]').value;
      if (a && d && d < a) { showErr(MSG.dates); return; }
      var btn = form.querySelector('button[type="submit"]'), label = btn.textContent;
      btn.disabled = true; btn.textContent = MSG.sending;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data && String(data.success) === 'false') throw new Error(data.message || 'not sent');
          if (window.gtag) gtag('event', 'generate_lead', { tour: (form.querySelector('[name="tour"]') || {}).value || '', site_language: L });  // enquiry = lead in Analytics
          okBox.style.display = 'block';
          form.reset(); form.querySelectorAll('.row,.two,button').forEach(function (el) { el.style.display = 'none'; });
          okBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(function () { btn.disabled = false; btn.textContent = label; showErr(MSG.fail); });
    });
  }

  // Analytics: count clicks on the contact icons / email / Telegram / VK / Tripster links
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="mailto:"],a[href*="t.me/"],a[href*="vk.ru"],a[href*="clubok.travel"]');
    if (a && window.gtag) gtag('event', 'contact_click', { method: a.href.indexOf('mailto:') === 0 ? 'email' : a.href.indexOf('t.me') > -1 ? 'telegram' : a.href.indexOf('vk.ru') > -1 ? 'vk' : 'tripster' });
  });

  // cookie consent banner (works with Google Consent Mode defaults set in <head>)
  var CK = {
    en: { txt: 'We use cookies to see how visitors use our site, so we can make it better.', yes: 'Accept', no: 'Decline', more: 'Learn more', p: '/privacy/' },
    ru: { txt: 'Мы используем файлы cookie, чтобы понимать, как посетители пользуются сайтом, и делать его лучше.', yes: 'Принять', no: 'Отклонить', more: 'Подробнее', p: '/ru/privacy/' },
    es: { txt: 'Usamos cookies para ver cómo se usa nuestro sitio y así mejorarlo.', yes: 'Aceptar', no: 'Rechazar', more: 'Más información', p: '/es/privacy/' }
  }[L] || null;
  function getConsent() { try { return localStorage.getItem('ut_consent'); } catch (e) { return null; } }
  function setConsent(v) {
    try { localStorage.setItem('ut_consent', v); } catch (e) {}
    if (window.gtag) gtag('consent', 'update', { analytics_storage: v === 'yes' ? 'granted' : 'denied' });
    if (v !== 'yes') document.cookie.split(';').forEach(function (c) {           // declining removes Analytics cookies already set
      var n = c.split('=')[0].trim();
      if (n.indexOf('_ga') === 0) ['', '.' + location.hostname.replace(/^www\./, '')].forEach(function (dm) {
        document.cookie = n + '=; Max-Age=0; path=/' + (dm ? '; domain=' + dm : '');
      });
    });
  }
  function showBanner() {
    if (!CK || document.getElementById('cookie-banner')) return;
    var d = document.createElement('div');
    d.id = 'cookie-banner'; d.setAttribute('role', 'region'); d.setAttribute('aria-label', 'Cookies');
    d.innerHTML = '<p>' + CK.txt + ' <a href="' + CK.p + '">' + CK.more + '</a></p>' +
      '<div class="ck-btns"><button type="button" class="btn btn-outline ck-no">' + CK.no + '</button>' +
      '<button type="button" class="btn btn-orange ck-yes">' + CK.yes + '</button></div>';
    document.body.appendChild(d);
    d.querySelector('.ck-yes').addEventListener('click', function () { setConsent('yes'); d.remove(); });
    d.querySelector('.ck-no').addEventListener('click', function () { setConsent('no'); d.remove(); });
  }
  if (!getConsent()) showBanner();
  document.querySelectorAll('.cookie-settings,.cookie-settings-page').forEach(function (b) { b.addEventListener('click', showBanner); });

  // preselect tour from ?tour= on the contact page
  var sel = document.querySelector('select[name="tour"]'), q = new URLSearchParams(location.search).get('tour');
  if (sel && q) Array.prototype.forEach.call(sel.options, function (o) { if (o.value === q) o.selected = true; });
})();
