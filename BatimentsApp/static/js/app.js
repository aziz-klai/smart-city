/* Smart City — interactions de base (modales, confirmation, recherche instantanée) */
document.addEventListener('click', function (e) {
  var open = e.target.closest('[data-open]');
  if (open) {
    e.preventDefault();
    var m = document.getElementById(open.dataset.open);
    if (m) {
      var t = m.querySelector('[data-modal-title]');
      if (t && open.dataset.title) t.textContent = open.dataset.title;
      m.classList.add('open');
    }
  }
  var close = e.target.closest('[data-close]');
  if (close) { e.preventDefault(); close.closest('.modal').classList.remove('open'); }
  if (e.target.classList.contains('modal')) e.target.classList.remove('open');

  var del = e.target.closest('[data-confirm]');
  if (del && !window.confirm(del.dataset.confirm)) e.preventDefault();

  var chip = e.target.closest('[data-fill]');
  if (chip) {
    var target = document.querySelector(chip.dataset.fill);
    if (target) { target.value = chip.textContent.trim(); target.focus(); }
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') document.querySelectorAll('.modal.open').forEach(function (m) { m.classList.remove('open'); });
});

/* Recherche instantanée côté client (maquettes) — en Django la recherche se fait côté serveur via ?q= */
document.querySelectorAll('[data-live-search]').forEach(function (input) {
  var table = document.querySelector(input.dataset.liveSearch);
  if (!table) return;
  input.addEventListener('input', function () {
    var q = input.value.toLowerCase();
    table.querySelectorAll('tbody tr').forEach(function (row) {
      row.style.display = row.textContent.toLowerCase().indexOf(q) > -1 ? '' : 'none';
    });
  });
});

/* Nom du fichier choisi dans la zone de dépôt */
document.querySelectorAll('.drop input[type=file]').forEach(function (inp) {
  inp.addEventListener('change', function () {
    var label = inp.closest('.drop').querySelector('[data-file-name]');
    if (label && inp.files.length) label.textContent = inp.files[0].name;
  });
});
