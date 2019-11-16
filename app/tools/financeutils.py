from app import cache
from app.sqldb.models import Transaction
from typing import List

# typing helper
Transactions = List[Transaction]

@cache.memoize(timeout=300)
def calc_balance(transactions : Transactions,
                 precision : float = 2) -> float:

    profits = sum(t.price for t in transactions if t.incoming)
    losses = sum(t.price for t in transactions if not t.incoming)
    result = round(profits - losses, precision) if precision else (profits - losses)
    return result