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

/* Recherche dynamique des événements */
function normaliserTexte(value) {
  return value.toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-live-search]').forEach(function (input) {
    var table = document.querySelector(input.dataset.liveSearch);
    if (!table) return;

    var tbody = table.querySelector('tbody');
    var compteur = document.querySelector('.panel-head h2 .count');

    function rechercher() {
      var requete = normaliserTexte(input.value);
      var visibles = 0;

      tbody.querySelectorAll('tr').forEach(function (row) {
        if (row.classList.contains('empty-search-row')) return;
        var nom = normaliserTexte(row.dataset.eventName || '');
        var id = row.dataset.eventId || '';
        var correspond = !requete ||
          nom.indexOf(requete) > -1 ||
          id.indexOf(requete) > -1;
        row.style.display = correspond ? '' : 'none';
        if (correspond) visibles++;
      });

      var vide = tbody.querySelector('.empty-search-row');
      if (requete && visibles === 0) {
        if (!vide) {
          vide = document.createElement('tr');
          vide.className = 'empty-search-row';
          vide.innerHTML = '<td colspan="6" class="empty">Aucun événement ne correspond à votre recherche.</td>';
          tbody.appendChild(vide);
        }
        vide.style.display = '';
      } else if (vide) {
        vide.style.display = 'none';
      }

      if (compteur) compteur.textContent = requete ? visibles : tbody.querySelectorAll('tr:not(.empty-search-row)').length;
    }

    input.addEventListener('input', rechercher);
    rechercher();
  });
});

/* Nom du fichier choisi dans la zone de dépôt */
document.querySelectorAll('.drop input[type=file]').forEach(function (inp) {
  inp.addEventListener('change', function () {
    var label = inp.closest('.drop').querySelector('[data-file-name]');
    if (label && inp.files.length) label.textContent = inp.files[0].name;
  });
});
