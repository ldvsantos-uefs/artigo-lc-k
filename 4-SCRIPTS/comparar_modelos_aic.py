import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load data
file_path = r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC\processed_data\dados_spss_naoh_extraidos.csv"
df = pd.read_csv(file_path)

# Define models
def exponential_model(x, a, b):
    return a * np.exp(-b * x)

def power_model(x, a, b):
    return a * np.power(x, b)

def logarithmic_model(x, a, b):
    return a + b * np.log(x)

# Function to calculate AIC and BIC
def calculate_criteria(y_true, y_pred, n_params):
    n = len(y_true)
    rss = np.sum((y_true - y_pred) ** 2)
    
    # Avoid log(0) if perfect fit (unlikely)
    if rss == 0:
        rss = 1e-10
        
    aic = n * np.log(rss / n) + 2 * n_params
    bic = n * np.log(rss / n) + n_params * np.log(n)
    
    r_squared = 1 - (rss / np.sum((y_true - np.mean(y_true)) ** 2))
    
    return aic, bic, r_squared

# Analyze each treatment
results = []
treatments = df['treatment'].unique()

print(f"{'Treatment':<10} | {'Model':<12} | {'AIC':<10} | {'BIC':<10} | {'R²':<10}")
print("-" * 65)

for treatment in treatments:
    subset = df[df['treatment'] == treatment]
    x = subset['days'].values
    y = subset['stress'].values
    
    # Sort by x just in case
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]
    
    models = [
        ('Exponential', exponential_model),
        ('Power', power_model),
        ('Logarithmic', logarithmic_model)
    ]
    
    best_aic = float('inf')
    best_model_name = ""
    
    for name, func in models:
        try:
            # Initial guesses
            if name == 'Exponential':
                p0 = [max(y), 0.01]
            elif name == 'Power':
                p0 = [max(y), -0.5]
            elif name == 'Logarithmic':
                p0 = [max(y), -1.0]
                
            popt, _ = curve_fit(func, x, y, p0=p0, maxfev=10000)
            y_pred = func(x, *popt)
            
            # 2 parameters + 1 for variance = 3 parameters for AIC calculation in this context?
            # Usually k is number of estimated parameters in the model. Here 2.
            # Some definitions include variance as a parameter. Let's stick to k=2 for model params.
            # Actually, standard AIC formula for least squares regression implies estimating variance, so k = p + 1.
            # Let's use k=3 (a, b, sigma).
            k = 3 
            
            aic, bic, r2 = calculate_criteria(y, y_pred, k)
            
            print(f"{treatment:<10} | {name:<12} | {aic:.4f}     | {bic:.4f}     | {r2:.4f}")
            
            results.append({
                'Treatment': treatment,
                'Model': name,
                'AIC': aic,
                'BIC': bic,
                'R2': r2
            })
            
        except Exception as e:
            print(f"{treatment:<10} | {name:<12} | Failed: {e}")

print("-" * 65)
