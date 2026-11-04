// Reference values: independently iterated monthly cash flows, not market data.
const assert = require('node:assert/strict');
const {futureValue, requiredMonthly} = require('./finance-math.js');
function reference(initial, monthly, annual, years) {
  let amount = initial;
  const rate = Math.pow(1 + annual, 1 / 12) - 1;
  for (let m = 0; m < years * 12; m++) amount = amount * (1 + rate) + monthly;
  return amount;
}
for (const annual of [0, 0.07, -0.1]) {
  const actual = futureValue(10000, 500, annual, 30);
  assert.ok(Math.abs(actual - reference(10000, 500, annual, 30)) < 0.0001);
  const monthly = requiredMonthly(6000000, 100000, annual, 30);
  assert.ok(Math.abs(reference(100000, monthly, annual, 30) - 6000000) < 0.001);
}
assert.equal(futureValue(1000, 500, 0, 2), 13000);
assert.equal(requiredMonthly(1000, 2000, 0, 2), 0);
assert.equal(requiredMonthly(1000, 0, 0, 0), Infinity);
assert.equal(Math.round(futureValue(0, 500, 0.07, 35)), 855707);
assert.equal(Math.round(requiredMonthly(6000000, 0, 0.07, 30)), 5131);
console.log('Effective annual returns and month-end cash flows verified.');
