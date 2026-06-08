<div align="center">

# Stripe → QuickBooks Converter

### Transform Stripe CSV exports into QuickBooks-ready files in seconds

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mustadz0/stripe-qbo-converter/pulls)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://github.com/Mustadz0/stripe-qbo-converter)
[![Donate](https://img.shields.io/badge/Donate-TRON-darkgreen?logo=tron&logoColor=white)](https://github.com/Mustadz0/stripe-qbo-converter#donate)
[![CI](https://github.com/Mustadz0/stripe-qbo-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/Mustadz0/stripe-qbo-converter/actions)

---

[🇬🇧 English](#english) &nbsp;•&nbsp; [🇸🇦 العربية](#arabic) &nbsp;•&nbsp; [🇫🇷 Français](#francais) &nbsp;•&nbsp; [🇪🇸 Español](#espanol) &nbsp;•&nbsp; [🇩🇪 Deutsch](#deutsch) &nbsp;•&nbsp; [🇹🇷 Türkçe](#turkce)

---

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="80" alt="FastAPI"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="70" alt="Python"/>

</div>

---

<a name="english"></a>
## 🇬🇧 English

**Stripe → QuickBooks Converter** is a free, open-source tool that converts Stripe CSV exports into QuickBooks-compatible formats. Built for freelancers, bookkeepers, and SaaS founders who waste hours every month manually reformatting transaction data.

### The Problem

Every month, thousands of bookkeepers spend **1–3 hours per client** manually reformatting Stripe CSV exports to match QuickBooks Online (QBO) import requirements. Stripe's date format doesn't match QBO's. Fees aren't separated. Refunds break the workflow. Columns don't align.

**This tool eliminates that friction entirely.**

### Features

- **4 Output Formats** — Bank Transactions, Sales Receipts, Journal Entries, or Combined
- **Auto-Detection** — Works with any Stripe CSV (Balance History, Payouts, Charges)
- **Smart Fee Handling** — Automatically separates Stripe processing fees
- **Refund Reconciliation** — Properly marks refunds as negative amounts
- **Date Normalization** — Converts all dates to QBO-friendly `MM/DD/YYYY`
- **Web UI** — Drag-and-drop interface for non-technical users
- **CLI** — Command-line tool for automation & scripting
- **Multi-Currency** — Works with any currency Stripe supports
- **100% Private** — Runs locally, no data leaves your machine
- **Free & Open Source** — MIT license

### Quick Start

```bash
# 1. Clone & install
git clone https://github.com/Mustadz0/stripe-qbo-converter.git
cd stripe-qbo-converter
pip install -r requirements.txt

# 2. Generate a summary of your CSV
python cli.py your_stripe_export.csv --summary

# 3. Convert to QuickBooks format
python cli.py your_stripe_export.csv -f bank -o qbo_ready.csv
```

### CLI Usage

```bash
# Show transaction summary
python cli.py export.csv --summary

# Convert to Bank Transactions (default)
python cli.py export.csv -f bank -o bank.csv

# Convert to Sales Receipts (itemized per customer)
python cli.py export.csv -f sales_receipt -o receipts.csv

# Convert to Journal Entries (double-entry accounting)
python cli.py export.csv -f journal -o journal.csv

# Combined format (bank + fees)
python cli.py export.csv -f combined -o combined.csv

# Preview first 10 rows without saving
python cli.py export.csv -f bank --preview
```

### Web UI

```bash
python web.py
# Open http://localhost:8000
```

Upload your Stripe CSV, select format, and download the converted file — no terminal needed.

### Output Formats

| Format | Description | Best For |
|--------|-------------|----------|
| `bank` | Date, Description, Amount, Memo | Direct QBO bank import |
| `sales_receipt` | Per-customer charges + fees | Detailed sales records |
| `journal` | Debit/Credit double entries | Full accounting integration |
| `combined` | Bank + fee rows in one file | Complete monthly overview |

### How It Works

```
Stripe CSV → Parser (auto-detect columns) → Transformer (4 formats) → QBO-ready CSV
```

1. **Export** your data from Stripe Dashboard → Reports → Balance History
2. **Run** the converter with one command
3. **Import** the result into QuickBooks Online via Banking → Import

### Roadmap

- [ ] Stripe API direct integration (sync without CSV)
- [ ] Xero format support
- [ ] Recurring auto-sync
- [ ] Desktop app (PyInstaller bundle)
- [ ] Docker deployment

### Why This Exists

Built because every third-party Stripe→QBO tool charges **$80+/month** for what is essentially a CSV transformation. This does the same job for free.

---

<a name="arabic"></a>
## 🇸🇦 العربية

**محول Stripe → QuickBooks** أداة مجانية مفتوحة المصدر لتحويل ملفات CSV من Stripe إلى صيغ متوافقة مع QuickBooks. صممت للمحاسبين، وأصحاب المتاجر الإلكترونية، ومؤسسي الشركات الناشئة الذين يضيعون ساعات كل شهر في إعادة تنسيق البيانات يدويًا.

### المشكلة

كل شهر، آلاف المحاسبين يقضون **1–3 ساعات لكل عميل** في إعادة تنسيق تصدير CSV من Stripe ليتوافق مع QuickBooks. تنسيق التاريخ مختلف. الرسوم غير مفصولة. المبالغ المستردة تعطل سير العمل.

**هذه الأداة تزيل هذه المشكلة تمامًا.**

### المميزات

- **4 صيغ إخراج** — معاملات بنكية، إيصالات مبيعات، قيود يومية، أو مجمعة
- **كشف تلقائي** — يعمل مع أي تصدير CSV من Stripe
- **معالجة ذكية للرسوم** — يفصل رسوم المعالجة تلقائيًا
- **تسوية المبالغ المستردة** — يضع علامة على المبالغ المستردة كقيم سالبة
- **توحيد التواريخ** — يحول كل التواريخ إلى صيغة QBO
- **واجهة ويب** — سحب وإفلات للمستخدمين غير التقنيين
- **واجهة أوامر** — للأتمتة والبرمجة النصية
- **مجاني تمامًا** — رخصة MIT مفتوحة المصدر

### بداية سريعة

```bash
pip install -r requirements.txt
python cli.py ملفك.csv --summary
python cli.py ملفك.csv -f bank -o qbo_ready.csv
python web.py  # فتح http://localhost:8000
```

### أوامر CLI

```bash
python cli.py export.csv --summary                    # عرض الملخص
python cli.py export.csv -f bank -o bank.csv          # معاملات بنكية
python cli.py export.csv -f journal -o journal.csv    # قيود يومية
python cli.py export.csv -f bank --preview            # معاينة
```

### صيغ الإخراج

| الصيغة | الوصف | الأفضل لـ |
|--------|-------|-----------|
| `bank` | التاريخ، الوصف، المبلغ، ملاحظة | استيراد بنكي مباشر |
| `sales_receipt` | رسوم كل عميل | سجلات مبيعات مفصلة |
| `journal` | قيود مدينة/دائنة | تكامل محاسبي كامل |
| `combined` | بنك + رسوم في ملف واحد | نظرة شهرية شاملة |

### طريقة العمل

```
Stripe CSV → محلل (يكشف الأعمدة تلقائيًا) → محول (4 صيغ) → CSV جاهز لـ QBO
```

1. **صدّر** بياناتك من Stripe Dashboard → Reports → Balance History
2. **شغّل** المحول بأمر واحد
3. **استورد** النتيجة إلى QuickBooks Online

### لماذا هذه الأداة؟

لأن كل أدوات الطرف الثالث تحاسب بـ **$80+/شهر** مقابل عملية تحويل CSV بسيطة. هذه الأداة تفعل نفس الشيء مجانًا.

---

<a name="francais"></a>
## 🇫🇷 Français

**Convertisseur Stripe → QuickBooks** — Un outil gratuit et open-source qui transforme les exports CSV Stripe en formats compatibles QuickBooks. Conçu pour les comptables, les freelances et les fondateurs SaaS.

### Fonctionnalités

- **4 formats de sortie** : Transactions bancaires, Reçus de vente, Écritures de journal, Combiné
- **Détection automatique** du type de CSV Stripe
- **Séparation intelligente des frais** de traitement Stripe
- **Gestion des remboursements** en montants négatifs
- **Interface Web** glisser-déposer
- **Interface CLI** pour l'automatisation
- **100% gratuit** sous licence MIT

### Démarrage rapide

```bash
pip install -r requirements.txt
python cli.py votre_export.csv -f bank -o pret_pour_qbo.csv
python web.py  # ouvrir http://localhost:8000
```

### Formats de sortie

| Format | Description |
|--------|-------------|
| `bank` | Date, Description, Montant, Mémo |
| `sales_receipt` | Ventes détaillées par client |
| `journal` | Écritures comptables Débit/Crédit |
| `combined` | Transactions bancaires + frais |

### Pourquoi cet outil ?

Les alternatives facturent **80$+/mois** pour une simple transformation CSV. Cet outil fait le même travail gratuitement.

---

<a name="espanol"></a>
## 🇪🇸 Español

**Convertidor Stripe → QuickBooks** — Herramienta gratuita de código abierto que convierte exportaciones CSV de Stripe a formatos compatibles con QuickBooks.

### Características

- **4 formatos de salida** : Transacciones bancarias, Recibos de venta, Asientos contables, Combinado
- **Detección automática** del tipo de CSV
- **Separación inteligente de comisiones** de Stripe
- **Manejo de reembolsos** como montos negativos
- **Interfaz web** de arrastrar y soltar
- **Interfaz CLI** para automatización
- **100% gratuito** licencia MIT

### Inicio rápido

```bash
pip install -r requirements.txt
python cli.py tu_exportacion.csv --summary
python cli.py tu_exportacion.csv -f bank -o listo_qbo.csv
```

### Formatos de salida

| Formato | Descripción |
|---------|-------------|
| `bank` | Fecha, Descripción, Monto, Memo |
| `sales_receipt` | Ventas detalladas por cliente |
| `journal` | Asientos contables Débito/Crédito |
| `combined` | Transacciones + comisiones |

---

<a name="deutsch"></a>
## 🇩🇪 Deutsch

**Stripe → QuickBooks Konverter** — Ein kostenloses Open-Source-Tool zum Konvertieren von Stripe CSV-Exporten in QuickBooks-kompatible Formate.

### Funktionen

- **4 Ausgabeformate** : Banktransaktionen, Verkaufsbelege, Buchungssätze, Kombiniert
- **Automatische Erkennung** des Stripe CSV-Typs
- **Intelligente Gebührentrennung** der Stripe-Verarbeitungsgebühren
- **Rückerstattungsverwaltung** als negative Beträge
- **Web-Oberfläche** per Drag & Drop
- **CLI-Schnittstelle** für Automatisierung
- **100% kostenlos** unter MIT-Lizenz

### Schnellstart

```bash
pip install -r requirements.txt
python cli.py dein_export.csv -f bank -o bereit_fuer_qbo.csv
```

### Ausgabeformate

| Format | Beschreibung |
|--------|-------------|
| `bank` | Datum, Beschreibung, Betrag, Notiz |
| `sales_receipt` | Detailierte Verkäufe pro Kunde |
| `journal` | Doppelte Buchführung (Soll/Haben) |
| `combined` | Bank + Gebühren in einer Datei |

---

<a name="turkce"></a>
## 🇹🇷 Türkçe

**Stripe → QuickBooks Dönüştürücü** — Stripe CSV dosyalarını QuickBooks uyumlu formatlara dönüştüren ücretsiz, açık kaynaklı bir araç.

### Özellikler

- **4 çıktı formatı** : Banka İşlemleri, Satış Makbuzları, Yevmiye Kayıtları, Birleşik
- **Otomatik algılama** — Herhangi bir Stripe CSV ile çalışır
- **Akıllı ücret yönetimi** — Stripe işlem ücretlerini otomatik ayırır
- **İade yönetimi** — İadeleri negatif tutar olarak işaretler
- **Web arayüzü** — Sürükle-bırak ile kullanım
- **CLI arayüzü** — Otomasyon için
- **Tamamen ücretsiz** — MIT lisansı

### Hızlı Başlangıç

```bash
pip install -r requirements.txt
python cli.py dosyan.csv --summary
python cli.py dosyan.csv -f bank -o qbo_hazir.csv
```

### Çıktı Formatları

| Format | Açıklama |
|--------|----------|
| `bank` | Tarih, Açıklama, Tutar, Not |
| `sales_receipt` | Müşteri bazında satışlar |
| `journal` | Çift taraflı muhasebe kaydı |
| `combined` | Banka + ücretler tek dosyada |

---

---

<a name="donate"></a>
## 💛 Support / دعم التطوير / Soutenir / Apoyar / Unterstützen / Destek

If this tool saved you time, consider supporting its development:

> **TRON (TRC20):** `TSQt2sV6NypuXFK3mqtPCgzHeoXug6pQp4`

<div align="center">

```
TSQt2sV6NypuXFK3mqtPCgzHeoXug6pQp4
```

</div>

---

| | | |
|---|---|---|
| 🇬🇧 | **Support Development** | Every donation helps keep this tool free and updated. Thank you! |
| 🇸🇦 | **ادعم التطوير** | كل تبرع يساعد في إبقاء هذه الأداة مجانية ومطورة. شكرًا لك! |
| 🇫🇷 | **Soutenir le développement** | Chaque don aide à maintenir cet outil gratuit et à jour. Merci ! |
| 🇪🇸 | **Apoyar el desarrollo** | Cada donación ayuda a mantener esta herramienta gratuita. ¡Gracias! |
| 🇩🇪 | **Entwicklung unterstützen** | Jede Spende hilft, dieses Tool kostenlos zu halten. Danke! |
| 🇹🇷 | **Geliştirmeyi destekle** | Her bağış bu aracı ücretsiz tutmaya yardımcı olur. Teşekkürler! |

---

<div align="center">

**Made with ❤️ by [Mustadz0](https://github.com/Mustadz0)**

Contributions, issues, and feature requests are welcome!

[![GitHub stars](https://img.shields.io/github/stars/Mustadz0/stripe-qbo-converter?style=social)](https://github.com/Mustadz0/stripe-qbo-converter/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Mustadz0/stripe-qbo-converter?style=social)](https://github.com/Mustadz0/stripe-qbo-converter/network/members)

</div>
