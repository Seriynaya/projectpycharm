# Banking Transactions Widget

## Project Overview

A C++ console application for managing and viewing banking transactions. Features include filtering by state or currency, date sorting, substring search across descriptions, card/account number masking, card number generation over arbitrary ranges, and top-K retrieval by transaction amount. All data is hardcoded (14 sample transactions). A companion Python implementation exists in `main.py`.

## Mathematical Formalization

### Data Model

Let T be the set of transactions, where each t in T is a tuple:

    t = (id, state, date, description, amount, currency_code, from_account, to_account)
    |T| = 14

### Masking Functions

Card masking:

    M_card(x) = x[0..3] ++ " " ++ x[4..5] ++ "** **** " ++ x[12..15]
    Domain: x in {0..9}^16

Account masking:

    M_acc(x) = "**" ++ x[n-4..n-1]
    Domain: |x| >= 4

Identifier dispatch:

    P(x) = starts_with(x, "Счет") ? M_acc(digits(x)) : M_card(digits(x))

### Filtering

Filter by state (linear scan):

    F(T, s) = { t in T | t.state = s }
    T(n) = O(n), S(n) = O(n)

Filter by currency:

    F_c(T, c) = { t in T | t.currency_code = c }
    T(n) = O(n), S(n) = O(n)

With hash index pre-built:

    H_s(T) : state -> vector<T>, build O(n), lookup O(1)
    H_c(T) : currency_code -> vector<T>, build O(n), lookup O(1)

### Sorting

Stable sort by date:

    S(T, desc) = stable_sort(T, lambda(a,b) = desc ? a.date > b.date : a.date < b.date)
    T(n) = O(n log n), stable

### Search

Substring search over descriptions:

    Search(T, q) = { t in T | q is substring of t.description }
    T(n) = O(n * |q|)

### Top-K by Amount

    TopK(T, k):
      1. nth_element to partition around k-th largest: O(n)
      2. sort the k elements: O(k log k)
      Total: O(n + k log k)

### Card Number Generator

    G(a, b) = { fmt16(i) | i in [a, b] }
    fmt16(i) = zero_pad(i, 16), then insert ' ' at positions {4, 9, 14}
    |G| = b - a + 1, capped at 50

## Original Code Quality Analysis (Python `main.py`)

The following bugs and quality issues were identified in the original Python source:

### Bug 1: Impossible Condition (Dead Branch)

```python
elif len(transactions) < 0:
```

`len()` returns a non-negative integer for all Python sequences. The condition `len(x) < 0` is always `False`, making this entire branch unreachable dead code. The intended check was likely `len(transactions) == 0` or `len(transactions) <= 0`.

### Bug 2: Incorrect Import Causing Startup Crash

```python
from turtle import pd
```

The `turtle` module is a graphics library and does not export `pd`. This statement raises `ImportError` at import time, crashing the program before any logic executes. The intended import was almost certainly `import pandas as pd` or similar.

### Bug 3: Duplicate `spending_by_category` Definition

Two functions named `spending_by_category` are defined in the same module. In Python, the second definition silently overwrites the first. The first function's logic is entirely unreachable. This indicates copy-paste error or lack of testing.

### Bug 4: Shared Mutable Class-Level State

```python
class SomeWidget:
    category_count = {}
    product_count = {}
```

These are class-level (not instance-level) attributes. All instances share the same dictionaries, causing cross-contamination of data between widget instances. The fix is to initialize them in `__init__` as `self.category_count = {}`.

### Bug 5: Copy-Paste Logging Pattern

Every function contains nearly identical logging boilerplate:

```python
logger.info("Starting function_name...")
# ... logic ...
logger.info("Finished function_name.")
```

This repetitive mechanical pattern is a structural indicator of AI-generated code. A human developer would use a decorator or context manager for cross-cutting logging concerns.

### AI Generation Markers

- Mechanical repetition of identical patterns across all functions
- Logical errors in conditionals that a manual code review would catch (`len < 0`)
- Import errors that would fail on first execution (`from turtle import pd`)
- Duplicate function names with no test coverage detecting the shadow

## Build & Run

### Requirements

- C++17 compatible compiler (GCC 7+, Clang 5+, MSVC 2017+)
- Standard library only (no external dependencies)

### Compile

```bash
g++ -std=c++17 -O2 -o banking main.cpp
```

### Run

```bash
./banking
```

On Windows, the program automatically sets the console to UTF-8 (`chcp 65001`) for correct display of Cyrillic text in transaction descriptions.

### Menu Options

1. Filter transactions by state (EXECUTED / CANCELED / PENDING)
2. Sort transactions by date (ascending or descending)
3. Filter transactions by currency (USD / EUR / RUB)
4. Search transactions by description substring
5. Display all masked card/account numbers
6. Generate formatted card numbers over a numeric range
7. Retrieve top-K transactions by amount
0. Exit
