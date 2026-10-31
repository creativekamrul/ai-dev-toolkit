const filters = document.querySelector('#filters');
const buttons = [...filters.querySelectorAll('button')];
const cards = [...document.querySelectorAll('article[data-category]')];
const empty = document.querySelector('#empty');
function filterEvents(category) {
  let count = 0;
  for (const card of cards) {
    card.hidden = category !== 'all' && card.dataset.category !== category;
    if (!card.hidden) count++;
  }
  for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
  empty.hidden = count !== 0;
  document.querySelector('#count').textContent = `${count} ${count === 1 ? 'event' : 'events'} to make your month`;
}
for (const button of buttons) button.addEventListener('click', () => filterEvents(button.dataset.filter));
document.querySelector('#reset').addEventListener('click', () => {
  filterEvents('all');
  buttons[0].focus();
});
filters.hidden = false;
