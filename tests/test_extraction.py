from reportlab.pdfgen import canvas
from investment_docs.extractor import extract_pdf
from investment_docs.validator import validate

def test_extract_fixture(tmp_path):
    path=tmp_path/"sample_fact_sheet.pdf"
    c=canvas.Canvas(str(path))
    c.drawString(50,760,"Fund Name: Example Global Equity Fund")
    c.drawString(50,740,"Strategy: Global equity")
    c.drawString(50,720,"Asset Class: Equity")
    c.drawString(50,700,"Management Fee: 0.65%")
    c.drawString(50,660,"Example Technology Co 30%")
    c.drawString(50,640,"Example Finance Co 20%")
    c.save()
    d=extract_pdf(path)
    assert d["fund_name"]=="Example Global Equity Fund"
    assert d["management_fee_pct"]==0.65
    assert d["top_holdings"][0]["name"]=="Example Technology Co"
    assert validate(d)["valid"]

def test_validation_catches_bad_fee():
    assert not validate({"fund_name":"x","strategy":"y","management_fee_pct":101,"top_holdings":[]})["valid"]

def test_validation_catches_weight_sum():
    assert "holding_weights_exceed_100_percent" in validate({"fund_name":"x","strategy":"y","management_fee_pct":1,"top_holdings":[{"name":"A","weight_pct":70},{"name":"B","weight_pct":40}]})["errors"]
