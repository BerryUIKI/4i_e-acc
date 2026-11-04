"""Current chapter 1/5 teaching checks, not historical data verification.
Source: teaching_models ordinary-annuity formula, effective annual return .07,
month-end contributions, no fees/taxes/withdrawals. Updated 2026-11-05.
Old untraceable terminal/CPI assertions have been retired; use references.md for
the separately sourced observations actually retained in the current manuscript.
"""
from teaching_models import future_value
for years,expected in [(25,391521),(30,584726),(35,855707)]:
 result=future_value(0,500,.07,years)
 assert round(result)==expected
 print(f'{years} years, 500 per month, 7% effective: {result:.2f}')
