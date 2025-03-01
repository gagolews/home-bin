# Copyleft (C) 2024, Marek Gagolewski <https://www.gagolewski.com>
# Configuration file for IPython

# ln -s ~/bin/ipython_config.py ~/.ipython/profile_default/ipython_config.py

c.TerminalIPythonApp.exec_lines = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
print("Loaded module aliases: np, pd, plt, sns.", end="")
"""

c.TerminalIPythonApp.display_banner = False
c.TerminalIPythonApp.matplotlib = "qt6"
#c.TerminalInteractiveShell.history_load_length = 0
#c.TerminalInteractiveShell.history_length = 1000
c.TerminalInteractiveShell.autosuggestions_provider = None
