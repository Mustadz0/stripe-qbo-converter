#!/usr/bin/env python3
"""
Stripe → QuickBooks Web UI
Run: python web.py
"""

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.parser import StripeCSVParser
from core.transformer import QBOTransformer

app = FastAPI(title="Stripe → QBO Converter")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

PAGE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stripe → QuickBooks Converter</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0a0f; color: #e2e8f0; min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
  }}
  .card {{
    background: #14141f; border-radius: 20px; padding: 40px;
    width: 100%; max-width: 560px; margin: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,.5);
    border: 1px solid #1e1e2e;
  }}
  h1 {{ font-size: 24px; margin-bottom: 6px; }}
  .sub {{ color: #64748b; font-size: 14px; margin-bottom: 28px; }}
  .drop-zone {{
    border: 2px dashed #2a2a3e; border-radius: 14px; padding: 40px 20px;
    text-align: center; cursor: pointer; transition: all .25s;
    background: #0f0f1a;
  }}
  .drop-zone:hover, .drop-zone.dragover {{
    border-color: #3b82f6; background: #0f172a;
  }}
  .drop-zone.has-file {{
    border-color: #22c55e; border-style: solid;
  }}
  .drop-zone svg {{ width: 40px; height: 40px; stroke: #64748b; margin-bottom: 12px; }}
  .drop-zone p {{ color: #94a3b8; font-size: 14px; }}
  .file-name {{ color: #22c55e; font-size: 14px; margin-top: 8px; font-weight: 600; }}
  select, button {{
    width: 100%; padding: 12px 16px; border-radius: 10px;
    font-size: 14px; border: 1px solid #2a2a3e; background: #0f0f1a;
    color: #e2e8f0; margin-top: 16px; cursor: pointer;
    transition: all .2s; font-family: inherit;
  }}
  select:hover, select:focus {{ border-color: #3b82f6; outline: none; }}
  button {{
    background: #3b82f6; color: #fff; font-weight: 600; border: none;
    font-size: 15px; padding: 14px;
  }}
  button:hover {{ background: #2563eb; }}
  button:disabled {{ opacity: .5; cursor: not-allowed; }}
  .error {{ color: #ef4444; font-size: 13px; margin-top: 10px; display: none; }}
  .format-label {{ font-size: 12px; color: #64748b; margin-top: 20px; margin-bottom: -8px; display: block; }}
  .summary {{ margin-top: 20px; padding: 16px; background: #0f172a; border-radius: 10px; display: none; }}
  .summary table {{ width: 100%; font-size: 13px; }}
  .summary td {{ padding: 4px 8px; }}
  .summary td:last-child {{ text-align: right; font-weight: 600; }}
  .summary .label {{ color: #94a3b8; }}
  .divider {{ border: none; border-top: 1px solid #1e1e2e; margin: 12px 0; }}
</style>
</head>
<body>
<div class="card">
  <h1>⚡ Stripe → QBO</h1>
  <p class="sub">Convert Stripe CSV exports to QuickBooks-ready format</p>

  <form id="uploadForm">
    <div class="drop-zone" id="dropZone">
      <svg fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <p>Drop Stripe CSV here or click to upload</p>
      <div class="file-name" id="fileName"></div>
    </div>
    <input type="file" id="fileInput" accept=".csv" style="display:none">

    <span class="format-label">Output Format</span>
    <select name="format" id="formatSelect">
      <option value="bank">Bank Transactions (for QBO import)</option>
      <option value="sales_receipt">Sales Receipts (itemized)</option>
      <option value="journal">Journal Entries (double-entry)</option>
      <option value="combined">Combined (Bank + Fees)</option>
    </select>

    <button type="submit" id="convertBtn">Convert & Download</button>
    <div class="error" id="errorMsg"></div>
  </form>

  <div class="summary" id="summary">
    <hr class="divider">
    <p style="font-size:13px;font-weight:600;margin-bottom:8px">📊 Summary</p>
    <table><tbody id="summaryBody"></tbody></table>
  </div>
</div>

<script>
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const fileName = document.getElementById('fileName');
  const convertBtn = document.getElementById('convertBtn');
  const errorMsg = document.getElementById('errorMsg');
  const summary = document.getElementById('summary');
  const summaryBody = document.getElementById('summaryBody');
  let selectedFile = null;

  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('dragover', e => {{ e.preventDefault(); dropZone.classList.add('dragover'); }});
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
  dropZone.addEventListener('drop', e => {{ e.preventDefault(); dropZone.classList.remove('dragover'); handleFile(e.dataTransfer.files[0]); }});
  fileInput.addEventListener('change', e => handleFile(e.target.files[0]));

  function handleFile(file) {{
    if (!file || !file.name.endsWith('.csv')) {{ error('Please select a CSV file'); return; }}
    selectedFile = file;
    fileName.textContent = '✓ ' + file.name;
    dropZone.classList.add('has-file');
    errorMsg.style.display = 'none';
  }}

  document.getElementById('uploadForm').addEventListener('submit', async e => {{
    e.preventDefault();
    if (!selectedFile) {{ error('Select a CSV file first'); return; }}
    convertBtn.disabled = true; convertBtn.textContent = 'Converting...';
    errorMsg.style.display = 'none';

    const form = new FormData();
    form.append('file', selectedFile);
    form.append('format', document.getElementById('formatSelect').value);

    try {{
      const res = await fetch('/convert', {{ method:'POST', body: form }});
      if (!res.ok) {{ const err = await res.json(); throw new Error(err.detail || 'Conversion failed'); }}
      const data = await res.json();
      showSummary(data.summary);
      downloadCSV(data.csv, data.filename);
    }} catch(err) {{
      error(err.message);
    }} finally {{
      convertBtn.disabled = false; convertBtn.textContent = 'Convert & Download';
    }}
  }});

  function showSummary(s) {{
    summary.style.display = 'block';
    summaryBody.innerHTML = `
      <tr><td class="label">Transactions</td><td>${{s.transactions}}</td></tr>
      <tr><td class="label">Gross Charges</td><td>$${{(+s.charges).toFixed(2)}}</td></tr>
      <tr><td class="label">Fees</td><td>$${{(+s.fees).toFixed(2)}}</td></tr>
      <tr><td class="label">Refunds</td><td>$${{(+s.refunds).toFixed(2)}}</td></tr>
      <tr><td class="label">Net Revenue</td><td>$${{(+s.net_revenue).toFixed(2)}}</td></tr>
    `;
  }}

  function downloadCSV(csv, filename) {{
    const blob = new Blob(['\\uFEFF' + csv], {{ type: 'text/csv;charset=utf-8;' }});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = filename; a.click();
  }}

  function error(msg) {{ errorMsg.textContent = msg; errorMsg.style.display = 'block'; }}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return PAGE


@app.post("/convert")
async def convert(file: UploadFile = File(...), format: str = Form("bank")):
    if not file.filename.endswith(".csv"):
        from fastapi import HTTPException
        raise HTTPException(400, "Only CSV files accepted")

    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    parser = StripeCSVParser(text)
    transactions = parser.parse()

    if not transactions:
        from fastapi import HTTPException
        raise HTTPException(400, "No transactions found in CSV")

    transformer = QBOTransformer(transactions)

    format_map = {
        "bank": ("qbo_bank_transactions.csv", transformer.to_bank_transactions),
        "sales_receipt": ("qbo_sales_receipts.csv", transformer.to_sales_receipts),
        "journal": ("qbo_journal_entries.csv", transformer.to_journal_entries),
        "combined": ("qbo_combined.csv", transformer.to_combined),
    }

    filename, fn = format_map[format]
    csv_output = fn()
    summary_data = transformer.summary()

    return {
        "filename": filename,
        "csv": csv_output,
        "summary": summary_data,
    }


if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=8000, reload=True)
