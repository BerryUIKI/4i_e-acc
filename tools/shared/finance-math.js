/* Pure mathematical model: effective annual return, month-end contributions.
 * Source: ordinary-annuity formula; manuscript Ch5/Ch32, revised 2026-11-05.
 * No market data, taxes, fees or withdrawals. Rates are decimals, not percentages.
 */
(function (root) {
  'use strict';
  function annuityFactor(annualRate, years) {
    if (!Number.isFinite(annualRate) || annualRate <= -1 ||
        !Number.isFinite(years) || years < 0) throw new RangeError('Invalid rate or horizon');
    const months = Math.round(years * 12);
    const monthlyRate = Math.expm1(Math.log1p(annualRate) / 12);
    return Math.abs(monthlyRate) < 1e-14 ? months :
      Math.expm1(months * Math.log1p(monthlyRate)) / monthlyRate;
  }
  function futureValue(initial, monthly, annualRate, years) {
    const factor = annuityFactor(annualRate, years);
    return initial * Math.pow(1 + annualRate, Math.round(years * 12) / 12) + monthly * factor;
  }
  function requiredMonthly(target, initial, annualRate, years) {
    const factor = annuityFactor(annualRate, years);
    const gap = Math.max(0, target - futureValue(initial, 0, annualRate, years));
    return factor === 0 ? (gap === 0 ? 0 : Infinity) : gap / factor;
  }
  const api = {annuityFactor, futureValue, requiredMonthly};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.FinanceMath = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
