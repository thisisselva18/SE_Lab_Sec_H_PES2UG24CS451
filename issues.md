# Known Issue Table — `recruitment_tracker.py`

Line numbers refer to the original file. Reports: `before/` (original) and `after/` (fixed).

Baseline: Pylint **4.47/10**, Bandit **3 issues** (2 Medium, 1 Low), Flake8 **8 issues**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection — Bandit B608 (Medium) | Security | 8 | The `INSERT` query is built with an f-string from `name`, `role`, `expected_salary` and `status`. A name such as `O'Brien` breaks the query, and a crafted value can run arbitrary SQL. | Use a parameterised query with `?` placeholders and pass the values as a tuple, so SQLite treats them as data, never as SQL. |
| Use of `eval` — Bandit B307 (Medium), Pylint W0123 | Security | 14 | `eval(salary_rule)` executes whatever string is passed in, so a caller can run arbitrary Python code (e.g. `__import__('os').system(...)`). | Remove `eval`. `shortlist()` now takes a numeric `salary_limit` and the caller passes the number. (`ast.literal_eval` is not enough here: since Python 3.8 it rejects `"500000 + 150000"`.) |
| `try`/`except`/`pass` with broad exception — Bandit B110 (Low), Pylint W0718 | Security / Bug | 28–29 | `except Exception: pass` swallows every error, so a failed status update fails silently and hides real bugs. | Catch only `sqlite3.Error` and report the failure instead of discarding it. |
| Inconsistent return statements — Pylint R1710 | Bug | 12, 20–21 | `shortlist()` returns a list when there are matches but implicitly returns `None` otherwise, so callers have to handle two types. | Always return a list (empty when nothing matches), built with a list comprehension. |
| Resource not managed with `with` / no encoding — Pylint R1732, W1514 | Bug | 32–35 | The file is opened with `open()` and closed manually. If a write raises, the handle leaks. No encoding is given, so output depends on the platform's default encoding. | Use `with open(path, "w", encoding="utf-8") as f:` so the file is always closed and written as UTF-8. |
| Unused variable — Pylint W0612, Flake8 F841 | Code quality | 15 | `total_seen = len(rows)` is computed but never used. | Remove the line. |
| Non-snake_case function names — Pylint C0103 | Style | 7, 24, 31, 38 | `addApplicant`, `updateStatus`, `exportReport` and `countByStatus` break PEP 8 naming. | Rename to `add_applicant`, `update_status`, `export_report` and `count_by_status`, and update every call in `main()`. |
| Missing docstrings — Pylint C0114, C0116 | Documentation | 1, 7, 12, 24, 31, 38, 42 | The module and all six functions have no docstring. | Add a module docstring and a one-line docstring to each function. |
| Line too long — Flake8 E501, Pylint C0301 | Style | 4, 8, 13, 26, 39 | Lines are 93–140 characters (Flake8 limit 79, Pylint limit 100). | Wrap the SQL strings with implicit string concatenation inside parentheses and split long calls over several lines. |
| Trailing whitespace — Flake8 W291, Pylint C0303 | Style | 15 | Extra spaces at the end of the line. | Removed (the line was deleted along with the unused variable). |
| Expected 2 blank lines — Flake8 E302 | Style | 31 | Only one blank line before `def exportReport`. | Add a second blank line between the top-level functions. |
