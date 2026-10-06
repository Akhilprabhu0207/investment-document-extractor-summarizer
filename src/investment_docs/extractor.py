from pathlib import Path
import re
import pdfplumber

def _first(pattern, text, flags=re.I):
    m=re.search(pattern,text,flags)
    return m.group(1).strip() if m else None

def extract_pdf(path: str | Path) -> dict:
    path=Path(path)
    with pdfplumber.open(path) as pdf:
        text='\n'.join(page.extract_text() or '' for page in pdf.pages)
    fund_name=_first(r'(?:Fund Name|Fund)\s*[:\-]\s*(.+)',text)
    strategy=_first(r'Strategy\s*[:\-]\s*(.+)',text)
    asset_class=_first(r'Asset Class\s*[:\-]\s*(.+)',text)
    fee_raw=_first(r'(?:Management Fee|Expense Ratio)\s*[:\-]\s*([0-9]+(?:\.[0-9]+)?)\s*%',text)
    holdings=[]
    for m in re.finditer(r'^\s*([A-Za-z0-9&.\- ]{3,60})\s+([0-9]+(?:\.[0-9]+)?)\s*%\s*$',text,re.M):
        name=m.group(1).strip()
        if name.lower() not in {'management fee','expense ratio','total'}: holdings.append({'name':name,'weight_pct':float(m.group(2))})
    return {'source_file':path.name,'fund_name':fund_name,'strategy':strategy,'asset_class':asset_class,'management_fee_pct':float(fee_raw) if fee_raw else None,'top_holdings':holdings[:10],'raw_text':text}
