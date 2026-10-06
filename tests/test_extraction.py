from investment_docs.extractor import extract_pdf
from investment_docs.validator import validate

def test_extract_fixture():
    d=extract_pdf('examples/sample_fact_sheet.pdf')
    assert d['fund_name']=='Example Global Equity Fund'
    assert d['management_fee_pct']==0.65
    assert d['top_holdings'][0]['name']=='Example Technology Co'
    assert validate(d)['valid']
def test_validation_catches_bad_fee():
    d={'fund_name':'x','strategy':'y','management_fee_pct':101,'top_holdings':[]}
    result=validate(d)
    assert not result['valid'] and 'management_fee_pct_out_of_range' in result['errors']
def test_validation_catches_weight_sum():
    d={'fund_name':'x','strategy':'y','management_fee_pct':1,'top_holdings':[{'name':'A','weight_pct':70},{'name':'B','weight_pct':40}]}
    assert 'holding_weights_exceed_100_percent' in validate(d)['errors']
