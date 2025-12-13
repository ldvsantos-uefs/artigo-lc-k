import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gerar_graficos_simulacao as ggs

print("Generating English figures...")
ggs.plot_arrhenius('en')
ggs.plot_damage('en')
ggs.plot_validation_and_microstructure('en')
print("Done.")
