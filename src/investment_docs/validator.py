def validate(data,holding_sum_tolerance=1.0):
 errors=[]; warnings=[]; fee=data.get('management_fee_pct')
 if fee is not None and not 0<=fee<=100: errors.append('management_fee_pct_out_of_range')
 weights=[h.get('weight_pct') for h in data.get('top_holdings',[]) if h.get('weight_pct') is not None]
 if any(not 0<=w<=100 for w in weights): errors.append('holding_weight_out_of_range')
 if weights and sum(weights)>100+holding_sum_tolerance: errors.append('holding_weights_exceed_100_percent')
 if not data.get('fund_name'): warnings.append('fund_name_not_extracted')
 if not data.get('strategy'): warnings.append('strategy_not_extracted')
 return {'valid':not errors,'errors':errors,'warnings':warnings}
