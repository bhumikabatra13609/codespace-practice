const state = { name: '', target: '', currency: '₹', participants: [], editingIndex: null };
const $ = (id) => document.getElementById(id);

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
}

function showError(message) {
  const element = $('errorMessage');
  element.textContent = message;
  element.hidden = !message;
}

function payload() {
  return { name: state.name, target: state.target, currency: state.currency, participants: state.participants };
}

function money(value) { return `${state.currency || '₹'}${value}`; }

async function calculate() {
  state.name = $('poolName').value.trim();
  state.target = $('targetAmount').value;
  state.currency = $('currency').value.trim() || '₹';
  $('currencyPrefix').textContent = state.currency;
  $('paidPrefix').textContent = state.currency;
  $('pageTitle').textContent = state.name || 'Your shared expense, made fair.';
  try {
    const response = await fetch('/api/calculate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload()) });
    const result = await response.json();
    if (!response.ok) { showError(result.error); renderEmpty(); return; }
    showError('');
    render(result);
  } catch (error) { showError('The calculator is unavailable. Please try again.'); }
}

function renderEmpty() {
  $('targetMetric').textContent = money('0.00'); $('collectedMetric').textContent = money('0.00');
  $('shareMetric').textContent = money('0.00'); $('countMetric').textContent = state.participants.length;
  $('statusMetric').textContent = 'Not Started'; $('progressBar').style.width = '0%'; $('progressNote').textContent = '0% funded';
  $('remainingNote').textContent = 'Enter a valid target'; $('participantsBody').innerHTML = ''; $('settlementList').innerHTML = '<p class="settlement-empty">Add a valid pool and participants to generate settlements.</p>';
  $('transactionCount').textContent = '0'; $('emptyState').hidden = false; $('participantsTable').hidden = true;
}

function render(result) {
  $('targetMetric').textContent = money(result.target); $('collectedMetric').textContent = money(result.total_collected);
  $('shareMetric').textContent = money(result.fair_share); $('countMetric').textContent = result.participants.length;
  $('statusMetric').textContent = result.status; $('progressBar').style.width = `${result.progress}%`;
  $('progressNote').textContent = `${result.progress}% funded`;
  $('remainingNote').textContent = result.status === 'Overfunded' ? `${money((parseFloat(result.total_collected) - parseFloat(result.target)).toFixed(2))} over target` : `${money(result.remaining)} remaining`;
  $('participantCountLabel').textContent = `${result.participants.length} ${result.participants.length === 1 ? 'person' : 'people'}`;
  $('emptyState').hidden = result.participants.length > 0; $('participantsTable').hidden = result.participants.length === 0;
  $('participantsBody').innerHTML = result.participants.map((person, index) => {
    const balance = parseFloat(person.balance);
    const type = balance < 0 ? 'owing' : balance > 0 ? 'receiving' : 'settled';
    const status = type === 'owing' ? `Owes ${money(Math.abs(balance).toFixed(2))}` : type === 'receiving' ? `Gets ${money(balance.toFixed(2))}` : 'Settled';
    return `<tr><td><strong>${escapeHtml(person.name)}</strong></td><td>${money(person.share)}</td><td>${money(person.paid)}</td><td class="balance ${type}">${balance > 0 ? '+' : ''}${money(person.balance)}</td><td><span class="tag ${type}">${status}</span></td><td class="actions"><button class="icon-button" title="Edit participant" data-edit="${index}">Edit</button><button class="icon-button danger" title="Delete participant" data-delete="${index}">Delete</button></td></tr>`;
  }).join('');
  $('settlementList').innerHTML = result.settlements.length ? result.settlements.map((item) => `<div class="settlement-row"><div><strong>${escapeHtml(item.payer)}</strong><span>pays</span><strong>${escapeHtml(item.receiver)}</strong></div><b>${money(item.amount)}</b></div>`).join('') : '<p class="settlement-empty">Everyone is already settled. Nice work.</p>';
  $('transactionCount').textContent = result.settlements.length;
}

function resetForm() {
  state.name = ''; state.target = ''; state.currency = '₹'; state.participants = []; state.editingIndex = null;
  $('poolName').value = ''; $('targetAmount').value = ''; $('currency').value = '₹'; $('participantName').value = ''; $('paidAmount').value = '';
  calculate();
}

async function loadExample() {
  const response = await fetch('/api/example'); const result = await response.json();
  $('poolName').value = result.name; $('targetAmount').value = result.target; $('currency').value = result.currency;
  state.participants = result.participants.map((person) => ({ name: person.name, paid: person.paid }));
  calculate();
}

$('participantForm').addEventListener('submit', (event) => {
  event.preventDefault(); const name = $('participantName').value.trim(); const paid = $('paidAmount').value;
  if (!name) return showError('Participant name cannot be empty.');
  if (paid === '' || Number(paid) < 0 || !Number.isFinite(Number(paid))) return showError('Paid amount must be 0 or greater.');
  const duplicate = state.participants.some((person, index) => person.name.toLowerCase() === name.toLowerCase() && index !== state.editingIndex);
  if (duplicate) return showError('Participant names must be unique.');
  if (state.editingIndex === null) state.participants.push({ name, paid }); else state.participants[state.editingIndex] = { name, paid };
  state.editingIndex = null; $('participantName').value = ''; $('paidAmount').value = ''; showError(''); calculate();
});

$('participantsBody').addEventListener('click', (event) => {
  const edit = event.target.dataset.edit; const remove = event.target.dataset.delete;
  if (edit !== undefined) { state.editingIndex = Number(edit); $('participantName').value = state.participants[edit].name; $('paidAmount').value = state.participants[edit].paid; $('participantName').focus(); }
  if (remove !== undefined) { state.participants.splice(Number(remove), 1); calculate(); }
});

['poolName', 'targetAmount', 'currency'].forEach((id) => $(id).addEventListener('input', calculate));
$('resetButton').addEventListener('click', resetForm);
loadExample();