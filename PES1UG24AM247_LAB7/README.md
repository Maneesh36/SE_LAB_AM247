# Lab 7 – Fuzz Testing for Input Validation Bugs

**Name:** Sanapala Venkata Maneesh  
**SRN:** PES1UG24AM247

## Objective
To identify input validation bugs in the bookstore trade-in application using property-based fuzz testing with Hypothesis.

## Functions Tested
1. `verify_isbn10_format()` – ISBN-10 input handling.
2. `calculate_depreciation_factor()` – Book age and lifespan input handling.
3. `lookup_condition_multiplier()` – Book condition lookup.

## Tools and Environment
- Python 3.11.9
- Pytest 9.2.0
- Hypothesis 6.112.1

## Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest test_processor.py -v
```

## Initial Findings
Fuzz testing identified crashes caused by invalid inputs, including empty strings, `None`, malformed values, and unknown condition codes.

## Fixes Implemented
- Added input type validation.
- Added ISBN length and character validation.
- Added safe handling of malformed depreciation inputs.
- Rejected invalid, negative, and non-finite depreciation values.
- Used safe dictionary lookup for unknown book conditions.

## Final Test Results

All three fuzz tests passed:

- `test_verify_isbn10_format_no_crash` – PASSED
- `test_calculate_depreciation_factor_safe` – PASSED
- `test_lookup_condition_multiplier_safe` – PASSED

**Final result: 3 passed**

## Conclusion
Fuzz testing helped identify input validation vulnerabilities. Appropriate validation and exception handling were implemented to make the three functions safer when handling unexpected inputs.