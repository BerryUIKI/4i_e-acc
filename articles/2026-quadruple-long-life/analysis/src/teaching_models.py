"""Pure mathematical models for the manuscript, verified 2026-11-05.

Source: ordinary-annuity and unit-purchase arithmetic; no external market data.
Parameters: effective annual return, month-end contributions, no taxes/fees or
withdrawals. DCA uses the 12 hypothetical prices printed in chapter 27.
Update: change parameters explicitly and update manuscript and charts together.
"""
from math import expm1, log1p

DCA_PRICES = (1.0, .90, .78, .66, .60, .60, .68, .76, .84, .92, 1.0, 1.0)

def annuity_factor(annual_rate, years):
    months = round(years * 12)
    if annual_rate <= -1 or years < 0:
        raise ValueError('Invalid model inputs')
    monthly_rate = expm1(log1p(annual_rate) / 12)
    return months if abs(monthly_rate) < 1e-14 else expm1(months * log1p(monthly_rate)) / monthly_rate

def future_value(initial, monthly, annual_rate, years):
    return initial * (1 + annual_rate) ** years + monthly * annuity_factor(annual_rate, years)

if __name__ == '__main__':
    assert round(future_value(0, 500, .07, 35)) == 855707
    assert round(future_value(0, 4000, .07, 30)) == 4677810
    assert future_value(1000, 500, 0, 2) == 13000
    assert round(sum(100000 / 12 / p for p in DCA_PRICES), 2) == 127545.48
    print('Monthly annuity and DCA reference values verified.')
