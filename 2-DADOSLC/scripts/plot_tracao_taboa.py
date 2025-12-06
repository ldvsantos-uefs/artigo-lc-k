#!/usr/bin/env python3
"""
Plota curvas tensão x deformação a partir do CSV combinado gerado por `import_tracao_taboa.py`.
Gera PNGs em `../processed_data/plots/` para os dias solicitados (30 e 90 por default).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / "processed_data" / "tracao_taboa_combined.csv"
OUT_DIR = ROOT / "processed_data" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def interp_series(strain, stress, grid):
    # ensure monotonic strain for interpolation
    order = np.argsort(strain)
    s = np.array(strain)[order]
    t = np.array(stress)[order]
    # remove duplicates in s
    s_unique, idx = np.unique(s, return_index=True)
    t_unique = t[idx]
    return np.interp(grid, s_unique, t_unique, left=np.nan, right=np.nan)


def plot_for_day(df, day, out_dir):
    df_day = df[df['days'] == day]
    if df_day.empty:
        print(f"Nenhum dado para {day} dias")
        return

    treatments = sorted(df_day['treatment'].dropna().unique())
    if not treatments:
        treatments = [None]

    n = len(treatments)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 4), squeeze=False)

    for i, tr in enumerate(treatments):
        ax = axes[0, i]
        if tr is None:
            sel = df_day
            title = f"All treatments - {day} dias"
        else:
            sel = df_day[df_day['treatment'] == tr]
            title = f"{tr} - {day} dias"

        specimens = sel['specimen'].unique()
        # determine common strain grid
        max_str = 0.0
        series = []
        for sp in specimens:
            s = sel[sel['specimen'] == sp]['strain'].values
            t = sel[sel['specimen'] == sp]['stress'].values
            if len(s) < 2:
                continue
            max_str = max(max_str, np.nanmax(s))
            series.append((s, t))
            ax.plot(s, t, color='gray', linewidth=0.8, alpha=0.8)

        if not series:
            ax.set_title(title + ' (sem séries válidas)')
            continue

        grid = np.linspace(0, max_str, 300)
        interp_vals = []
        for s, t in series:
            y = interp_series(s, t, grid)
            interp_vals.append(y)

        arr = np.vstack(interp_vals)
        mean = np.nanmean(arr, axis=0)
        std = np.nanstd(arr, axis=0)

        ax.plot(grid, mean, color='C0', linewidth=2.0, label='média')
        ax.fill_between(grid, mean-std, mean+std, color='C0', alpha=0.3, label='±1σ')
        ax.set_xlabel('Deformação')
        ax.set_ylabel('Tensão / Esforço')
        ax.set_title(title)
        ax.legend()

    out_path = out_dir / f"tracao_{day}dias_summary.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Salvo: {out_path}")


def main():
    if not IN_FILE.exists():
        print(f"Arquivo combinado não encontrado: {IN_FILE}")
        return
    df = pd.read_csv(IN_FILE)
    # ensure numeric
    df['strain'] = pd.to_numeric(df['strain'], errors='coerce')
    df['stress'] = pd.to_numeric(df['stress'], errors='coerce')
    days_to_plot = [30, 90]
    for d in days_to_plot:
        plot_for_day(df, d, OUT_DIR)


if __name__ == '__main__':
    main()
