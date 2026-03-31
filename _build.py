"""
Script de construcción del sistema de certificados REVEM.
Genera generator.html y verify.html con los logos embebidos.
Diseño HORIZONTAL (landscape) basado en el modelo oficial.
Código = REV-YYYYMMDD-CEDULA
Firmas pre-embebidas si existen firma_calderon.png y firma_guaman.png
"""
import base64
import os

BASE = "F:/Documentos/Certificados"

with open(f"{BASE}/_logo_color.b64") as f:
    LOGO_COLOR = f.read().strip()
with open(f"{BASE}/_logo_white.b64") as f:
    LOGO_WHITE = f.read().strip()
with open(f"{BASE}/_sig1.b64") as f:
    SIG1_DATA = "data:image/png;base64," + f.read().strip()
with open(f"{BASE}/_sig2.b64") as f:
    SIG2_DATA = "data:image/png;base64," + f.read().strip()
with open(f"{BASE}/_fondo.b64") as f:
    FONDO_DATA = "data:image/png;base64," + f.read().strip()

print("Firma Calderón: EMBEBIDA")
print("Firma Guamán:   EMBEBIDA")
print("Fondo:          EMBEBIDO")

# ============================================================
# GENERATOR HTML
# ============================================================
GENERATOR = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Generador de Certificados · REVEM</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Playfair+Display:ital,wght@0,700;1,400;1,700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.6/dist/JsBarcode.all.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --green: #6BBE2E;
  --green-dark: #4e9120;
  --green-light: #e8f7d8;
  --dark: #2D3436;
  --gray: #636E72;
  --light: #F8F9FA;
  --border: #DFE6E9;
}}

body {{
  font-family: "Montserrat", sans-serif;
  background: #ECEFF1;
  color: var(--dark);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}

.app-header {{
  background: var(--dark);
  padding: 11px 22px;
  display: flex; align-items: center; gap: 13px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  flex-shrink: 0;
}}
.app-header img {{ height: 28px; }}
.app-header h1 {{ color: #fff; font-size: 13px; font-weight: 600; flex: 1; }}
.badge {{ background: var(--green); color: white; font-size: 9px; font-weight: 700; padding: 3px 8px; border-radius: 20px; letter-spacing: 1px; text-transform: uppercase; }}

.app-body {{ display: flex; flex: 1; overflow: hidden; min-height: 0; }}

/* SIDEBAR */
.sidebar {{
  width: 300px; min-width: 300px;
  background: #fff;
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  overflow-y: auto;
}}
.sb-section {{ padding: 14px 16px; border-bottom: 1px solid var(--border); }}
.sb-title {{ font-size: 9px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gray); margin-bottom: 10px; }}

.form-group {{ margin-bottom: 8px; }}
.form-label {{ display: block; font-size: 10px; font-weight: 600; color: var(--dark); margin-bottom: 3px; }}
.form-input {{
  width: 100%; padding: 7px 10px;
  border: 1.5px solid var(--border); border-radius: 6px;
  font-family: "Montserrat", sans-serif; font-size: 12px; color: var(--dark);
  transition: border-color 0.2s; outline: none; background: #fff;
}}
.form-input:focus {{ border-color: var(--green); }}
.form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }}
.form-row-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }}

/* Sig status */
.sig-status {{
  display: flex; align-items: center; gap: 6px;
  font-size: 10px; padding: 5px 8px; border-radius: 5px; margin-top: 4px;
}}
.sig-ok {{ background: var(--green-light); color: var(--green-dark); border: 1px solid var(--green); }}
.sig-missing {{ background: #fff3cd; color: #856404; border: 1px solid #ffc107; }}
.sig-upload {{
  border: 2px dashed var(--border); border-radius: 5px;
  padding: 6px; text-align: center; cursor: pointer;
  transition: all 0.2s; background: var(--light); margin-top: 4px;
  position: relative; overflow: hidden;
}}
.sig-upload:hover {{ border-color: var(--green); background: var(--green-light); }}
.sig-upload input {{ position: absolute; inset: 0; opacity: 0; cursor: pointer; }}
.sig-upload img {{ max-height: 36px; max-width: 100%; object-fit: contain; }}
.sig-hint {{ font-size: 9px; color: var(--gray); }}

/* Participants */
.add-row {{ display: flex; gap: 6px; margin-bottom: 7px; }}
.add-row .form-input {{ flex: 1; margin: 0; }}

.btn {{
  padding: 7px 12px; border: none; border-radius: 6px;
  font-family: "Montserrat", sans-serif; font-size: 11px; font-weight: 600;
  cursor: pointer; transition: all 0.2s;
  display: inline-flex; align-items: center; gap: 4px; white-space: nowrap;
}}
.btn-green {{ background: var(--green); color: white; }}
.btn-green:hover {{ background: var(--green-dark); }}
.btn-dark {{ background: var(--dark); color: white; }}
.btn-dark:hover {{ background: #1a1a2e; }}
.btn-outline {{ background: #fff; color: var(--dark); border: 1.5px solid var(--border); }}
.btn-outline:hover {{ border-color: var(--dark); }}
.btn-red {{ background: #e74c3c; color: white; padding: 3px 7px; font-size: 9px; }}
.btn-full {{ width: 100%; justify-content: center; margin-bottom: 5px; font-size: 11px; padding: 9px 12px; }}

.part-list {{ max-height: 200px; overflow-y: auto; }}
.part-item {{
  display: flex; align-items: center; gap: 6px;
  padding: 6px 7px; border: 1px solid var(--border); border-radius: 5px;
  margin-bottom: 4px; background: var(--light); cursor: pointer; transition: all 0.15s;
}}
.part-item:hover, .part-item.active {{
  border-color: var(--green); background: var(--green-light);
}}
.pnum {{ width: 18px; height: 18px; background: var(--green); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 8px; font-weight: 700; flex-shrink: 0; }}
.pinfo {{ flex: 1; min-width: 0; }}
.pname {{ font-size: 11px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.pcode {{ font-size: 9px; color: var(--gray); font-family: monospace; }}

.actions-section {{ padding: 12px 16px; background: var(--light); }}
.progress-bar {{ height: 3px; background: var(--border); border-radius: 2px; margin-top: 6px; overflow: hidden; display: none; }}
.progress-fill {{ height: 100%; background: var(--green); transition: width 0.3s; width: 0%; }}
.status-msg {{ font-size: 9px; color: var(--gray); text-align: center; margin-top: 4px; min-height: 12px; }}

/* PREVIEW */
.preview-area {{
  flex: 1; display: flex; flex-direction: column;
  align-items: center; padding: 20px; overflow-y: auto; gap: 12px;
}}
.preview-top {{
  width: 100%; max-width: 1060px;
  display: flex; align-items: center; justify-content: space-between;
}}
.preview-label {{ font-size: 11px; color: var(--gray); font-weight: 500; }}
.preview-wrapper {{
  width: 100%; max-width: 1060px;
  background: white; border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.15);
  overflow: hidden; position: relative; flex-shrink: 0;
}}

/* ===== CERTIFICATE — Landscape A4: 1056×748px ===== */
#cert-template {{
  width: 1056px;
  height: 748px;
  position: relative;
  background: #FFFFFF;
  font-family: "Montserrat", sans-serif;
  overflow: hidden;
}}

/* Fondo completo del certificado */
.c-wm {{
  position: absolute;
  width: 100%; height: 100%;
  top: 0; left: 0;
  opacity: 1;
  pointer-events: none;
  object-fit: cover;
  object-position: center center;
  z-index: 0;
}}

/* Todos los elementos encima del fondo */
.c-top, .c-bot, .c-logo, .c-confiere, .c-title, .c-title-line, .c-name, .c-desc, .c-footer {{
  position: relative;
  z-index: 1;
}}

/* Color bars */
.c-top {{ position: absolute; top: 0; left: 0; right: 0; height: 10px; background: linear-gradient(90deg, #4e9120, #6BBE2E, #4e9120); z-index: 1; }}
.c-bot {{ position: absolute; bottom: 0; left: 0; right: 0; height: 10px; background: linear-gradient(90deg, #4e9120, #6BBE2E, #4e9120); z-index: 1; }}

/* Logo centered top */
.c-logo {{
  position: absolute;
  top: 34px; left: 50%;
  transform: translateX(-50%);
  height: 64px;
}}

/* "Revem Ecuador confiere el presente:" */
.c-confiere {{
  position: absolute;
  top: 162px; left: 0; right: 0;
  text-align: center;
  font-size: 13px; font-weight: 400; color: #888; letter-spacing: 0.3px;
}}

/* "Certificado de Participación a:" */
.c-title {{
  position: absolute;
  top: 188px; left: 60px; right: 60px;
  text-align: center;
  font-size: 30px; font-weight: 800; color: var(--dark); letter-spacing: 0.5px;
}}

/* Underline on title */
.c-title-line {{
  position: absolute;
  top: 234px; left: 50%; transform: translateX(-50%);
  width: 70px; height: 3px; background: #6BBE2E; border-radius: 2px;
}}

/* Recipient name */
.c-name {{
  position: absolute;
  top: 248px; left: 60px; right: 60px;
  text-align: center;
  font-family: "Playfair Display", serif;
  font-size: 38px; font-weight: 400; font-style: italic;
  color: var(--dark); line-height: 1.15;
}}

/* Description */
.c-desc {{
  position: absolute;
  top: 352px; left: 90px; right: 90px;
  text-align: center;
  font-family: "Playfair Display", serif;
  font-size: 14px; font-weight: 400; font-style: italic;
  color: #444; line-height: 1.7;
}}

/* Footer */
.c-footer {{
  position: absolute;
  bottom: 28px; left: 52px; right: 52px;
  display: flex; align-items: flex-end; justify-content: space-between;
}}

/* Signature */
.c-sig {{ text-align: center; width: 210px; }}
.c-sig-img {{ height: 68px; max-width: 200px; object-fit: contain; display: block; margin: 0 auto 3px; }}
.c-sig-ph {{ height: 46px; border-bottom: 1.5px solid #ccc; margin-bottom: 3px; }}
.c-sig-line {{ width: 100%; height: 1px; background: #bbb; margin-bottom: 5px; }}
.c-sig-italic {{ font-family: "Playfair Display", serif; font-style: italic; font-size: 12px; color: var(--dark); }}
.c-sig-cargo {{ font-size: 10px; color: var(--gray); margin-top: 2px; font-weight: 500; }}

/* QR + code center */
.c-codes {{ text-align: center; display: flex; flex-direction: column; align-items: center; gap: 4px; }}
.c-qr {{ width: 90px; height: 90px; }}
.c-qr img, .c-qr canvas {{ width: 90px !important; height: 90px !important; }}
.c-barcode {{ max-width: 200px; height: 32px; display: block; margin: 0 auto; }}
.c-code-id {{ font-size: 7.5px; color: var(--gray); letter-spacing: 0.5px; font-weight: 600; font-family: monospace; }}
.c-verify-txt {{ font-size: 7px; color: #aaa; }}

/* Toast */
.toast {{
  position: fixed; bottom: 16px; right: 16px;
  background: var(--dark); color: white;
  padding: 9px 15px; border-radius: 7px; font-size: 11px; font-weight: 500;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  transform: translateY(60px); opacity: 0; transition: all 0.3s; z-index: 9999;
}}
.toast.show {{ transform: translateY(0); opacity: 1; }}
.toast.success {{ border-left: 3px solid var(--green); }}
.toast.error {{ border-left: 3px solid #e74c3c; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
</style>
</head>
<body>

<header class="app-header">
  <img src="data:image/png;base64,{LOGO_WHITE}" alt="REVEM">
  <h1>Generador de Certificados · REVEM Ecuador</h1>
  <span class="badge">MVP</span>
</header>

<div class="app-body">
  <aside class="sidebar">

    <!-- Evento -->
    <div class="sb-section">
      <div class="sb-title">&#9881; Evento</div>
      <div class="form-group">
        <label class="form-label">Nombre del evento / taller</label>
        <input class="form-input" id="evName" value="Taller de cumplimiento técnico en Alumbrado Público: Criterios y Evaluación">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Fecha</label>
          <input class="form-input" id="evDate" type="date" value="2026-03-31">
        </div>
        <div class="form-group">
          <label class="form-label">Ciudad</label>
          <input class="form-input" id="evCity" value="Ibarra">
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">URL verificación (GitHub Pages)</label>
        <input class="form-input" id="verifyBase" value="https://diegoqprobst.github.io/revem-certs/verify.html" readonly style="background:#f0f7ea;color:#4e9120;font-size:10px;cursor:default">
        <div style="font-size:9px;color:var(--gray);margin-top:2px">&#10003; URL configurado · github.com/diegoqprobst</div>
      </div>
    </div>

    <!-- Firmantes -->
    <div class="sb-section">
      <div class="sb-title">&#9998; Firmantes</div>
      <div class="form-row">
        <div>
          <div class="form-group">
            <label class="form-label">Nombre 1</label>
            <input class="form-input" id="s1Name" value="Ing. Carlos Calderón">
          </div>
          <div class="form-group">
            <label class="form-label">Cargo 1</label>
            <input class="form-input" id="s1Title" value="Gerente de Operaciones">
          </div>
          <div class="sig-status sig-ok">&#10003; Firma cargada</div>
        </div>
        <div>
          <div class="form-group">
            <label class="form-label">Nombre 2</label>
            <input class="form-input" id="s2Name" value="Ing. Susana Guamán">
          </div>
          <div class="form-group">
            <label class="form-label">Cargo 2</label>
            <input class="form-input" id="s2Title" value="Jefe Dpt. Técnico">
          </div>
          <div class="sig-status sig-ok">&#10003; Firma cargada</div>
        </div>
      </div>
    </div>

    <!-- Participantes -->
    <div class="sb-section">
      <div class="sb-title">&#128100; Participantes &nbsp;<span id="partCount" style="color:var(--green);font-weight:800">0</span></div>

      <!-- CSV import row -->
      <div style="display:flex;gap:5px;margin-bottom:8px">
        <button class="btn btn-outline" style="flex:1;font-size:10px;padding:6px 8px" onclick="downloadCsvTemplate()">
          &#11123; Descargar formato CSV
        </button>
        <label class="btn btn-outline" style="flex:1;font-size:10px;padding:6px 8px;justify-content:center;cursor:pointer;display:flex;align-items:center;gap:4px">
          &#11014; Cargar CSV
          <input type="file" accept=".csv" style="display:none" onchange="loadCsv(this)">
        </label>
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:8px"></div>

      <div class="form-group">
        <label class="form-label">Nombre completo</label>
        <input class="form-input" id="newName" placeholder="Nombre completo"
          onkeydown="if(event.key==='Enter')document.getElementById('newCed').focus()">
      </div>
      <div class="add-row">
        <input class="form-input" id="newCed" placeholder="Cédula (10 dígitos)"
          maxlength="10"
          onkeydown="if(event.key==='Enter')addParticipant()">
        <button class="btn btn-green" onclick="addParticipant()" title="Agregar (Enter)">&#43; Agregar</button>
      </div>
      <div class="part-list" id="partList"></div>
    </div>

    <!-- Acciones -->
    <div class="actions-section">
      <button class="btn btn-green btn-full" onclick="downloadOne()" id="btnOne" disabled>
        &#11123;&nbsp; Descargar seleccionado
      </button>
      <button class="btn btn-dark btn-full" onclick="downloadAll()" id="btnAll" disabled>
        &#128230;&nbsp; Descargar todos (ZIP)
      </button>
      <button class="btn btn-outline btn-full" onclick="exportJson()" id="btnJson" disabled>
        &#128196;&nbsp; Exportar certs.json → GitHub
      </button>
      <div class="progress-bar" id="progBar"><div class="progress-fill" id="progFill"></div></div>
      <div class="status-msg" id="statusMsg"></div>
    </div>
  </aside>

  <!-- PREVIEW -->
  <main class="preview-area">
    <div class="preview-top">
      <span class="preview-label" id="previewLabel">Agrega un participante para ver la vista previa</span>
      <button class="btn btn-outline" onclick="refreshPreview()" style="font-size:10px">&#8635; Actualizar</button>
    </div>
    <div class="preview-wrapper" id="previewWrap">
      <div id="certScaler" style="transform-origin:top left">

        <!-- CERTIFICATE TEMPLATE -->
        <div id="cert-template">
          <img class="c-wm" src="{FONDO_DATA}" alt="">
          <div class="c-top"></div>
          <div class="c-bot"></div>

          <!-- Logo removed as requested -->

          <div class="c-confiere">Revem Ecuador confiere el presente:</div>
          <div class="c-title">Certificado de Participación a:</div>
          <div class="c-title-line"></div>

          <div class="c-name" id="cName">NOMBRE DEL PARTICIPANTE</div>

          <div class="c-desc" id="cDesc">
            Por su participación en el evento, realizado en la ciudad de <em>Ciudad</em> el día <em>fecha</em>
          </div>

          <div class="c-footer">
            <!-- Firmante 1 -->
            <div class="c-sig">
              <img id="cSig1" class="c-sig-img" src="{SIG1_DATA}" alt="" style="display:block">
              <div id="cSig1Ph" class="c-sig-ph" style="display:none"></div>
              <div class="c-sig-line"></div>
              <div class="c-sig-italic" id="cSig1Name">Ing. Carlos Calderón</div>
              <div class="c-sig-cargo" id="cSig1Title">Gerente de Operaciones</div>
            </div>

            <!-- Códigos centro -->
            <div class="c-codes">
              <div id="cQR" class="c-qr"></div>
              <svg id="cBarcode" class="c-barcode"></svg>
              <div class="c-code-id" id="cCodeId">REV-YYYYMMDD-CEDULA</div>
              <div class="c-verify-txt">Escanea para verificar autenticidad</div>
            </div>

            <!-- Firmante 2 -->
            <div class="c-sig">
              <img id="cSig2" class="c-sig-img" src="{SIG2_DATA}" alt="" style="display:block">
              <div id="cSig2Ph" class="c-sig-ph" style="display:none"></div>
              <div class="c-sig-line"></div>
              <div class="c-sig-italic" id="cSig2Name">Ing. Susana Guamán</div>
              <div class="c-sig-cargo" id="cSig2Title">Jefe Dpt. Técnico</div>
            </div>
          </div>
        </div>
        <!-- end cert-template -->
      </div>
    </div>
  </main>
</div>

<div class="toast" id="toast"></div>

<script>
// ===== PRE-LOADED STATE =====
const S = {{
  participants: [],
  sel: -1,
  sig1: {repr(SIG1_DATA)} || null,
  sig2: {repr(SIG2_DATA)} || null,
  counter: 1
}};

window.addEventListener('load', () => {{
  scalePreview();
  window.addEventListener('resize', scalePreview);
  updateCert();
}});

function scalePreview() {{
  const wrap = document.getElementById('previewWrap');
  const scaler = document.getElementById('certScaler');
  const scale = wrap.clientWidth / 1056;
  scaler.style.transform = `scale(${{scale}})`;
  wrap.style.height = (748 * scale) + 'px';
}}

function esc(s) {{ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}

function formatDate(d) {{
  if (!d) return 'fecha';
  const dt = new Date(d + 'T12:00:00');
  const m = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  return `${{dt.getDate()}} de ${{m[dt.getMonth()]}} de ${{dt.getFullYear()}}`;
}}

function genCode(cedula, dateStr) {{
  // REV-YYYYMMDD-CEDULA
  const d = dateStr ? dateStr.replace(/-/g,'') : new Date().toISOString().slice(0,10).replace(/-/g,'');
  return `REV-${{d}}-${{cedula}}`;
}}

let toastT;
function toast(msg, type='success') {{
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `toast ${{type}} show`;
  clearTimeout(toastT);
  toastT = setTimeout(() => el.className='toast', 3000);
}}
function setStatus(msg) {{ document.getElementById('statusMsg').textContent = msg; }}

// ===== PARTICIPANTS =====
function addParticipant() {{
  const nameEl = document.getElementById('newName');
  const cedEl = document.getElementById('newCed');
  const name = nameEl.value.trim();
  const cedula = cedEl.value.trim();

  if (!name) {{ toast('Ingresa el nombre del participante','error'); nameEl.focus(); return; }}
  if (!cedula || cedula.length < 6) {{ toast('Ingresa la cédula (mínimo 6 dígitos)','error'); cedEl.focus(); return; }}
  if (!/^\\d+$/.test(cedula)) {{ toast('La cédula solo debe tener números','error'); cedEl.focus(); return; }}

  // Check for duplicate cedula
  if (S.participants.find(p => p.cedula === cedula)) {{
    toast('Ya existe un participante con esa cédula','error'); cedEl.focus(); return;
  }}

  const evDate = document.getElementById('evDate').value;
  const id = genCode(cedula, evDate);
  S.participants.push({{ id, name, cedula }});
  nameEl.value = ''; cedEl.value = '';
  nameEl.focus();
  renderList();
  select(S.participants.length - 1);
  updateBtns();
  toast('Participante agregado');
}}

function removePart(i, e) {{
  e.stopPropagation();
  S.participants.splice(i, 1);
  if (S.sel >= S.participants.length) S.sel = S.participants.length - 1;
  renderList();
  if (S.sel >= 0) select(S.sel); else S.sel = -1;
  updateBtns();
}}

function renderList() {{
  document.getElementById('partCount').textContent = S.participants.length;
  document.getElementById('partList').innerHTML = S.participants.map((p,i) => `
    <div class="part-item ${{i===S.sel?'active':''}}" onclick="select(${{i}})">
      <div class="pnum">${{i+1}}</div>
      <div class="pinfo">
        <div class="pname">${{esc(p.name)}}</div>
        <div class="pcode">${{p.id}}</div>
      </div>
      <button class="btn btn-red" onclick="removePart(${{i}},event)">✕</button>
    </div>`).join('');
}}

function select(i) {{ S.sel = i; renderList(); updateCert(); }}

function updateBtns() {{
  document.getElementById('btnOne').disabled = S.sel < 0;
  document.getElementById('btnAll').disabled = !S.participants.length;
  document.getElementById('btnJson').disabled = !S.participants.length;
}}

// ===== SIGNATURES =====
function loadSig(input, n) {{
  const f = input.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = e => {{
    if (n===1) {{ S.sig1 = e.target.result; document.getElementById('s1Prev').innerHTML = `<img src="${{e.target.result}}" style="max-height:36px;max-width:100%;object-fit:contain">`; }}
    else {{ S.sig2 = e.target.result; document.getElementById('s2Prev').innerHTML = `<img src="${{e.target.result}}" style="max-height:36px;max-width:100%;object-fit:contain">`; }}
    if (S.sel >= 0) updateCert();
  }};
  r.readAsDataURL(f);
}}

// ===== CERTIFICATE UPDATE =====
function updateCert() {{
  const p = S.participants[S.sel];
  const evName = document.getElementById('evName').value || 'el evento';
  const evDate = document.getElementById('evDate').value;
  const city = document.getElementById('evCity').value || 'la ciudad';
  const verifyBase = document.getElementById('verifyBase').value || '#';

  document.getElementById('cName').textContent = p ? p.name.toUpperCase() : 'NOMBRE DEL PARTICIPANTE';

  const evTxt = evName ? `"${{evName}}"` : 'el evento';
  document.getElementById('cDesc').innerHTML =
    `Por su participación en el ${{evTxt}},<br>realizado en la ciudad de <em>${{city}}</em> el día <em>${{formatDate(evDate)}}</em>`;

  document.getElementById('cSig1Name').textContent = document.getElementById('s1Name').value || 'Firmante 1';
  document.getElementById('cSig1Title').textContent = document.getElementById('s1Title').value || 'Cargo';
  document.getElementById('cSig2Name').textContent = document.getElementById('s2Name').value || 'Firmante 2';
  document.getElementById('cSig2Title').textContent = document.getElementById('s2Title').value || 'Cargo';

  const s1i=document.getElementById('cSig1'), s1p=document.getElementById('cSig1Ph');
  const s2i=document.getElementById('cSig2'), s2p=document.getElementById('cSig2Ph');
  if (S.sig1) {{ s1i.src=S.sig1; s1i.style.display='block'; s1p.style.display='none'; }}
  else {{ s1i.style.display='none'; s1p.style.display='block'; }}
  if (S.sig2) {{ s2i.src=S.sig2; s2i.style.display='block'; s2p.style.display='none'; }}
  else {{ s2i.style.display='none'; s2p.style.display='block'; }}

  if (!p) {{ document.getElementById('cCodeId').textContent = 'REV-YYYYMMDD-CEDULA'; return; }}

  document.getElementById('cCodeId').textContent = p.id;

  // Barcode CODE128
  try {{
    JsBarcode('#cBarcode', p.id, {{
      format: 'CODE128', width: 1.3, height: 30,
      displayValue: false, margin: 0, background: 'transparent'
    }});
  }} catch(e) {{}}

  // QR
  const qrEl = document.getElementById('cQR');
  qrEl.innerHTML = '';
  const verifyUrl = verifyBase.includes('?') ? verifyBase+'&id='+p.id : verifyBase+'?id='+p.id;
  try {{
    new QRCode(qrEl, {{ text: verifyUrl, width:90, height:90, colorDark:'#2D3436', colorLight:'#FFFFFF', correctLevel: QRCode.CorrectLevel.M }});
  }} catch(e) {{}}

  document.getElementById('previewLabel').textContent = `Vista previa: ${{p.name}} · ${{p.id}}`;
}}

function refreshPreview() {{ updateCert(); scalePreview(); }}

// ===== PDF GENERATION =====
async function capture(participant) {{
  S.sel = S.participants.indexOf(participant);
  updateCert();
  await new Promise(r => setTimeout(r, 350));
  const scaler = document.getElementById('certScaler');
  const prev = scaler.style.transform;
  scaler.style.transform = 'scale(1)';
  await new Promise(r => setTimeout(r, 60));
  const canvas = await html2canvas(document.getElementById('cert-template'), {{
    scale: 2, width: 1056, height: 748,
    useCORS: true, allowTaint: true, logging: false,
    backgroundColor: '#FFFFFF'
  }});
  scaler.style.transform = prev;
  return canvas;
}}

async function downloadOne() {{
  const p = S.participants[S.sel]; if (!p) return;
  setStatus('Generando PDF...');
  try {{
    const canvas = await capture(p);
    const imgData = canvas.toDataURL('image/jpeg', 0.97);
    const {{ jsPDF }} = window.jspdf;
    const pdf = new jsPDF({{ orientation:'landscape', unit:'mm', format:'a4' }});
    pdf.addImage(imgData, 'JPEG', 0, 0, 297, 210);
    pdf.save(`Certificado_${{p.name.replace(/\\s+/g,'_')}}_${{p.cedula}}.pdf`);
    toast('PDF descargado');
  }} catch(e) {{ toast('Error: '+e.message,'error'); }}
  setStatus('');
}}

async function downloadAll() {{
  if (!S.participants.length) return;
  const pb=document.getElementById('progBar'), pf=document.getElementById('progFill');
  pb.style.display='block'; pf.style.width='0%';
  const zip = new JSZip();
  const {{ jsPDF }} = window.jspdf;
  for (let i=0; i<S.participants.length; i++) {{
    const p = S.participants[i];
    setStatus(`Generando ${{i+1}}/${{S.participants.length}}: ${{p.name}}`);
    pf.style.width = ((i/S.participants.length)*100)+'%';
    try {{
      const canvas = await capture(p);
      const imgData = canvas.toDataURL('image/jpeg', 0.95);
      const pdf = new jsPDF({{ orientation:'landscape', unit:'mm', format:'a4' }});
      pdf.addImage(imgData, 'JPEG', 0, 0, 297, 210);
      zip.file(`Certificado_${{p.name.replace(/\\s+/g,'_')}}_${{p.cedula}}.pdf`, pdf.output('blob'));
    }} catch(e) {{ console.error(p.name,e); }}
  }}
  pf.style.width='100%'; setStatus('Comprimiendo...');
  const blob = await zip.generateAsync({{type:'blob'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href=url; a.download=`Certificados_REVEM_${{new Date().toISOString().slice(0,10)}}.zip`;
  a.click(); URL.revokeObjectURL(url);
  pb.style.display='none'; setStatus('');
  toast(`${{S.participants.length}} certificados descargados`);
}}

// ===== CSV =====
function downloadCsvTemplate() {{
  const csv = 'nombre,cedula\\nEjemplo Nombre Apellido,1234567890';
  const blob = new Blob([csv], {{type:'text/csv;charset=utf-8;'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'formato_participantes.csv';
  a.click(); URL.revokeObjectURL(url);
  toast('Formato CSV descargado');
}}

function loadCsv(input) {{
  const file = input.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {{
    const lines = e.target.result.split('\\n').map(l => l.trim()).filter(l => l);
    if (!lines.length) {{ toast('CSV vacío','error'); return; }}

    // Detect header row (nombre, cedula)
    const firstLine = lines[0].toLowerCase().replace(/['"]/g,'');
    const hasHeader = firstLine.includes('nombre') || firstLine.includes('cedula') || firstLine.includes('name');
    const dataLines = hasHeader ? lines.slice(1) : lines;

    const evDate = document.getElementById('evDate').value;
    let added = 0, skipped = 0, errors = [];

    dataLines.forEach((line, i) => {{
      if (!line) return;
      // Support comma or semicolon separator
      const sep = line.includes(';') ? ';' : ',';
      const parts = line.split(sep).map(p => p.trim().replace(/^["']|["']$/g,''));
      const name = parts[0] || '';
      const cedula = (parts[1] || '').replace(/\\D/g,'');

      if (!name) {{ errors.push(`Fila ${{i+1+(hasHeader?1:0)}}: nombre vacío`); skipped++; return; }}
      if (!cedula || cedula.length < 6) {{ errors.push(`Fila ${{i+1+(hasHeader?1:0)}}: cédula inválida`); skipped++; return; }}
      if (S.participants.find(p => p.cedula === cedula)) {{ skipped++; return; }}

      S.participants.push({{ id: genCode(cedula, evDate), name, cedula }});
      added++;
    }});

    renderList();
    if (added > 0) select(S.participants.length - 1);
    updateBtns();
    input.value = '';

    if (errors.length) {{
      toast(`${{added}} agregados, ${{skipped}} omitidos`, 'error');
      console.warn('CSV errors:', errors);
    }} else {{
      toast(`${{added}} participantes cargados desde CSV`);
    }}
  }};
  reader.readAsText(file, 'UTF-8');
}}

function exportJson() {{
  const data = {{
    event: {{ name: document.getElementById('evName').value, date: document.getElementById('evDate').value, city: document.getElementById('evCity').value }},
    generated: new Date().toISOString(),
    certificates: S.participants.map(p => ({{
      id: p.id, name: p.name, cedula: p.cedula,
      event: document.getElementById('evName').value,
      date: document.getElementById('evDate').value,
      city: document.getElementById('evCity').value,
      issuedAt: new Date().toISOString()
    }}))
  }};
  const blob = new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href=url; a.download='certs.json'; a.click(); URL.revokeObjectURL(url);
  toast('certs.json exportado — súbelo a GitHub');
}}

['evName','evDate','evCity','verifyBase','s1Name','s1Title','s2Name','s2Title'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) el.addEventListener('input', updateCert);
}});
</script>
</body>
</html>"""

with open(f"{BASE}/generator.html", "w", encoding="utf-8") as f:
    f.write(GENERATOR)
print(f"generator.html: {len(GENERATOR):,} bytes")

# ============================================================
# VERIFY HTML
# ============================================================
VERIFY = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verificación de Certificado · REVEM</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.6/dist/JsBarcode.all.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --green: #6BBE2E; --dark: #2D3436; --gray: #636E72; --light: #F8F9FA; --border: #DFE6E9; }}
body {{
  font-family: "Montserrat", sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #2D3436 60%, #1a3a1a 100%);
  min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px;
}}
.card {{ background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); max-width: 500px; width: 100%; overflow: hidden; position: relative; z-index: 10; }}
.card-header {{ background: var(--dark); padding: 20px 26px; display: flex; align-items: center; gap: 13px; }}
.card-header img {{ height: 30px; }}
.htext h1 {{ color: white; font-size: 13px; font-weight: 600; }}
.htext p {{ color: rgba(255,255,255,0.4); font-size: 10px; margin-top: 2px; }}
.card-body {{ padding: 26px; }}
.spinner {{ width: 34px; height: 34px; border: 3px solid var(--border); border-top-color: var(--green); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 10px; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.loading {{ text-align: center; color: var(--gray); font-size: 11px; padding: 16px 0; }}
.valid-badge {{ display: flex; align-items: center; gap: 10px; background: #e8f7d8; border: 2px solid var(--green); border-radius: 10px; padding: 12px 15px; margin-bottom: 20px; }}
.check {{ width: 32px; height: 32px; background: var(--green); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 15px; flex-shrink: 0; }}
.valid-badge strong {{ font-size: 12px; font-weight: 700; color: var(--dark); display: block; }}
.valid-badge span {{ font-size: 10px; color: var(--gray); }}
.field {{ margin-bottom: 12px; }}
.field-label {{ font-size: 9px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gray); margin-bottom: 3px; }}
.field-value {{ font-size: 14px; font-weight: 600; color: var(--dark); }}
.field-value.name {{ font-family: "Playfair Display", serif; font-style: italic; font-size: 18px; }}
.divider {{ height: 1px; background: var(--border); margin: 16px 0; }}
.code-box {{ background: var(--light); border-radius: 7px; padding: 10px 13px; display: flex; align-items: center; justify-content: space-between; }}
.code-label {{ font-size: 9px; color: var(--gray); font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }}
.code-val {{ font-size: 11px; font-weight: 700; color: var(--dark); font-family: monospace; }}
.invalid {{ text-align: center; padding: 14px 0; }}
.x-icon {{ width: 50px; height: 50px; background: #fdecea; border: 2px solid #e74c3c; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; margin: 0 auto 10px; }}
.invalid-title {{ font-size: 14px; font-weight: 700; color: #c0392b; margin-bottom: 7px; }}
.invalid-sub {{ font-size: 11px; color: var(--gray); line-height: 1.7; }}
.card-footer {{ background: var(--light); padding: 11px 26px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 8px; }}
.footer-logo {{ height: 16px; opacity: 0.5; }}
.footer-text {{ font-size: 9px; color: var(--gray); }}

/* Boton Descargar */
.btn-dl {{ display: flex; align-items: center; justify-content: center; width: 100%; background: var(--dark); color: white; padding: 12px; border-radius: 8px; font-weight: 600; font-size: 13px; font-family: inherit; margin-top: 20px; text-decoration: none; cursor: pointer; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.15); transition: background 0.2s; }}
.btn-dl:hover {{ background: #1a1a2e; }}

/* HIDDEN CERT TEMPLATE FOR PDF */
#hidden-cert {{ position: fixed; top: 0; left: 0; z-index: -9999; opacity: 0; pointer-events: none; overflow: hidden; }}
#cert-template {{ width: 1056px; height: 748px; position: relative; background: #FFFFFF; font-family: "Montserrat", sans-serif; overflow: hidden; }}
.c-wm {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: 0; }}
.c-top {{ position: absolute; top: 0; left: 0; right: 0; height: 10px; background: linear-gradient(90deg, #4e9120, #6BBE2E, #4e9120); z-index: 1; }}
.c-bot {{ position: absolute; bottom: 0; left: 0; right: 0; height: 10px; background: linear-gradient(90deg, #4e9120, #6BBE2E, #4e9120); z-index: 1; }}
.c-confiere {{ position: absolute; top: 162px; left: 0; right: 0; text-align: center; font-size: 13px; font-weight: 400; color: #888; z-index: 1; }}
.c-title {{ position: absolute; top: 188px; left: 60px; right: 60px; text-align: center; font-size: 30px; font-weight: 800; color: var(--dark); z-index: 1; }}
.c-title-line {{ position: absolute; top: 234px; left: 50%; transform: translateX(-50%); width: 70px; height: 3px; background: var(--green); border-radius: 2px; z-index: 1; }}
.c-name {{ position: absolute; top: 248px; left: 60px; right: 60px; text-align: center; font-family: "Playfair Display", serif; font-size: 38px; font-style: italic; color: var(--dark); z-index: 1; }}
.c-desc {{ position: absolute; top: 352px; left: 90px; right: 90px; text-align: center; font-family: "Playfair Display", serif; font-size: 14px; font-style: italic; color: #444; line-height: 1.7; z-index: 1; }}
.c-footer {{ position: absolute; bottom: 28px; left: 52px; right: 52px; display: flex; align-items: flex-end; justify-content: space-between; z-index: 1; }}
.c-sig {{ text-align: center; width: 210px; }}
.c-sig-img {{ height: 68px; max-width: 200px; object-fit: contain; display: block; margin: 0 auto 3px; }}
.c-sig-line {{ width: 100%; height: 1px; background: #bbb; margin-bottom: 5px; }}
.c-sig-italic {{ font-family: "Playfair Display", serif; font-style: italic; font-size: 12px; color: var(--dark); }}
.c-sig-cargo {{ font-size: 10px; color: var(--gray); margin-top: 2px; font-weight: 500; }}
.c-codes {{ text-align: center; display: flex; flex-direction: column; align-items: center; gap: 4px; }}
.c-qr {{ width: 90px; height: 90px; }}
.c-qr img, .c-qr canvas {{ width: 90px !important; height: 90px !important; }}
.c-barcode {{ max-width: 200px; height: 32px; display: block; margin: 0 auto; }}
.c-code-id {{ font-size: 7.5px; color: var(--gray); font-weight: 600; font-family: monospace; }}
.c-verify-txt {{ font-size: 7px; color: #aaa; }}
</style>
</head>
<body>
<div class="card">
  <div class="card-header">
    <img src="data:image/png;base64,{LOGO_WHITE}" alt="REVEM">
    <div class="htext">
      <h1>Verificador de Certificados</h1>
      <p>Sistema oficial · REVEM Ecuador</p>
    </div>
  </div>
  <div class="card-body" id="cardBody">
    <div class="loading"><div class="spinner"></div>Verificando...</div>
  </div>
  <div class="card-footer">
    <img class="footer-logo" src="data:image/png;base64,{LOGO_COLOR}" alt="REVEM">
    <span class="footer-text">REVEM · Energía Ilimitada &nbsp;|&nbsp; Verificación oficial</span>
  </div>
</div>

<!-- HIDDEN CERTIFICATE FOR PDF EXPORT -->
<div id="hidden-cert">
  <div id="cert-template">
    <img class="c-wm" src="{FONDO_DATA}" alt="">
    <div class="c-top"></div><div class="c-bot"></div>
    <div class="c-confiere">Revem Ecuador confiere el presente:</div>
    <div class="c-title">Certificado de Participación a:</div>
    <div class="c-title-line"></div>
    <div class="c-name" id="cName">NOMBRE</div>
    <div class="c-desc" id="cDesc">Descripción</div>
    <div class="c-footer">
      <div class="c-sig">
        <img class="c-sig-img" src="{SIG1_DATA}" alt="">
        <div class="c-sig-line"></div>
        <div class="c-sig-italic">Ing. Carlos Calderón</div>
        <div class="c-sig-cargo">Gerente de Operaciones</div>
      </div>
      <div class="c-codes">
        <div id="cQR" class="c-qr"></div>
        <svg id="cBarcode" class="c-barcode"></svg>
        <div class="c-code-id" id="cCodeId">ID</div>
      </div>
      <div class="c-sig">
        <img class="c-sig-img" src="{SIG2_DATA}" alt="">
        <div class="c-sig-line"></div>
        <div class="c-sig-italic">Ing. Susana Guamán</div>
        <div class="c-sig-cargo">Jefe Dpt. Técnico</div>
      </div>
    </div>
  </div>
</div>

<script>
let globalCert = null;

async function downloadPDF() {{
  const btn = document.getElementById('dlBtn');
  btn.innerHTML = '<div class="spinner" style="width:14px;height:14px;border-width:2px;margin:0 8px 0 0"></div> Generando PDF...';
  btn.style.pointerEvents = 'none';
  
  try {{
    const canvas = await html2canvas(document.getElementById('cert-template'), {{
      scale: 2, width: 1056, height: 748,
      useCORS: true, allowTaint: true, logging: false, backgroundColor: '#FFFFFF'
    }});
    const imgData = canvas.toDataURL('image/jpeg', 0.97);
    const {{ jsPDF }} = window.jspdf;
    const pdf = new jsPDF({{ orientation:'landscape', unit:'mm', format:'a4' }});
    pdf.addImage(imgData, 'JPEG', 0, 0, 297, 210);
    pdf.save(`Certificado_${{globalCert.name.replace(/\\s+/g,'_')}}_${{globalCert.id}}.pdf`);
  }} catch(e) {{
    alert('Hubo un error al generar el PDF. Asegúrate de estar en un navegador moderno.');
  }}
  
  btn.innerHTML = '📥 Descargar mi Certificado (PDF)';
  btn.style.pointerEvents = 'auto';
}}

(async () => {{
  const body = document.getElementById('cardBody');
  const params = new URLSearchParams(window.location.search);
  const certId = params.get('id');
  if (!certId) {{
    body.innerHTML = `<div style="text-align:center;padding:14px 0;font-size:12px;color:#636E72">
      Escanea el código QR de un certificado REVEM para verificar su autenticidad.</div>`;
    return;
  }}
  
  let data = {{ certificates: [] }};
  let successFetch = false;
  
  // 1. Local
  try {{ 
    const resLocal = await fetch('./certs.json'); 
    if (resLocal.ok) {{
       const localData = await resLocal.json();
       if(localData.certificates) {{ data.certificates.push(...localData.certificates); successFetch = true; }}
    }}
  }} catch(e) {{}}
  
  // 2. Nube Google Sheets
  try {{
     const scriptURL = 'https://script.google.com/macros/s/AKfycbzjTgTY1FXQZhDIjTcRd2Uj0My5K_76FRdfmM4ApeOCFd84Tpl2aQeymH7wqrzUdfqk/exec';
     const resCloud = await fetch(scriptURL);
     if (resCloud.ok) {{
        const cloudData = await resCloud.json();
        if(cloudData.certificates) {{ data.certificates.push(...cloudData.certificates); successFetch = true; }}
     }}
  }} catch(e) {{}}

  if (!successFetch) {{
    body.innerHTML = `<div class="invalid"><div class="x-icon">&#9888;</div>
      <div class="invalid-title">No se pudo verificar</div>
      <div class="invalid-sub">La base de datos no está disponible. Contacta a REVEM.</div></div>`;
    return;
  }}
  
  const cert = data.certificates && data.certificates.find(c => c.id === certId);
  if (!cert) {{
    body.innerHTML = `<div class="invalid"><div class="x-icon">&#10007;</div>
      <div class="invalid-title">Certificado no encontrado</div>
      <div class="invalid-sub">El código <strong>${{certId}}</strong> no corresponde a ningún certificado emitido por REVEM.</div></div>`;
    return;
  }}
  
  globalCert = cert;
  const months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
  let dateStr = cert.date;
  try {{ const d = new Date(cert.date+'T12:00:00'); dateStr = `${{d.getDate()}} de ${{months[d.getMonth()]}} de ${{d.getFullYear()}}`; }} catch(e) {{}}
  if (cert.city) dateStr = cert.city + ', ' + dateStr;
  
  // Render verified view
  body.innerHTML = `
    <div class="valid-badge">
      <div class="check">&#10003;</div>
      <div><strong>Certificado Auténtico</strong><span>Verificado por el sistema oficial REVEM</span></div>
    </div>
    <div class="field"><div class="field-label">Participante</div><div class="field-value name">${{cert.name}}</div></div>
    <div class="divider"></div>
    <div class="field"><div class="field-label">Evento</div><div class="field-value">${{cert.event}}</div></div>
    <div class="field" style="margin-top:10px"><div class="field-label">Fecha y lugar</div><div class="field-value">${{dateStr}}</div></div>
    <div class="divider"></div>
    <div class="code-box">
      <div><div class="code-label">Código de certificado</div><div class="code-val">${{cert.id}}</div></div>
      <span style="font-size:18px">&#128274;</span>
    </div>
    <button class="btn-dl" id="dlBtn" onclick="downloadPDF()">📥 Descargar mi Certificado (PDF)</button>
  `;
  
  // POPULATE HIDDEN CANVAS TEMPLATE
  document.getElementById('cName').innerHTML = cert.name.toUpperCase();
  document.getElementById('cCodeId').innerHTML = cert.id;
  document.getElementById('cDesc').innerHTML = `Por su participación en <em>${{cert.event}}</em>,<br>con fecha de expedición <em>${{dateStr}}</em>`;
  
  const verifyUrl = 'https://diegoqprobst.github.io/revem-certs/verify.html?id=' + cert.id;
  new QRCode(document.getElementById('cQR'), {{ text: verifyUrl, width:90, height:90, colorDark:'#2D3436', colorLight:'#FFFFFF', correctLevel: QRCode.CorrectLevel.M }});
  try {{ JsBarcode('#cBarcode', cert.id, {{ format: 'CODE128', width: 1.3, height: 30, displayValue: false, margin: 0, background: 'transparent' }}); }} catch(e) {{}}

}})();
</script>
</body>
</html>"""

with open(f"{BASE}/verify.html", "w", encoding="utf-8") as f:
    f.write(VERIFY)
print(f"verify.html: {len(VERIFY):,} bytes")
print("Done!")
