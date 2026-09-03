const $ = (id) => document.getElementById(id);

document.querySelectorAll('[data-panel]').forEach(button =>
  button.addEventListener('click', () => {
    document.querySelectorAll('.panel, .nav-item').forEach(el =>
      el.classList.remove('active'));
    $(button.dataset.panel).classList.add('active');
    document.querySelector(`.nav-item[data-panel="${button.dataset.panel}"]`)?.classList.add('active');
  })
);

function toast(message) {
  const el = $('toast');
  el.textContent = message;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2800);
}

$('runBtn').addEventListener('click', () => {
  const rain = Math.floor(100 + Math.random() * 48), soil = (0.68 + Math.random() * .22).toFixed(2);
  $('rainValue').textContent = `${rain} mm`;
  $('soilValue').textContent = soil;
  $('rainBar').style.width = `${Math.min(100, rain / 1.45)}%`;
  $('soilBar').style.width = `${soil * 100}%`;
  $('riskArea').textContent = `${(rain / 4.9).toFixed(1)} km²`;
  $('riskPeople').textContent = rain > 120 ? '1,284' : '942';
  toast('Assessment updated with current scenario inputs.');
});

$('exportBtn').addEventListener('click', () => toast('Brief prepared - browser download is ready to connect to your reporting system.'));

const inputs = ['stability', 'recharge', 'infra', 'density', 'load'];

function recalc() {
  const values = Object.fromEntries(inputs.map(id => [id, Number($(id).value)]));
  inputs.forEach(id => $(`${id}Out`).textContent = values[id].toFixed(2));
  const cci = (values.stability * values.recharge * values.infra) / (values.density * values.load);
  const shown = Math.min(1.5, cci).toFixed(2), unstable = cci < 1;
  $('cciNumber').textContent = shown;
  $('cciStatus').textContent = unstable ? 'Over-capacity / unstable' : 'Within carrying capacity';
  $('cciText').textContent = unstable ? 'Construction should be frozen and relocation planning initiated.' : 'Maintain monitoring and permit only resilient development.';
  $('cciNumber').style.color = unstable ? '#d06232' : '#16815b';
  $('cciMeter').style.left = `${Math.min(94, cci / 1.5 * 100)}%`;
}

inputs.forEach(id => $(id).addEventListener('input', recalc));
recalc();
