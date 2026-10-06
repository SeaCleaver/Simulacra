# Adds src/ to sys.path so the test suite can import the engine modules
# (order, trade, order_book, portfolio, backtester, ...) which use bare imports.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
