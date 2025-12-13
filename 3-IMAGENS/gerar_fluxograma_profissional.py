from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def find_dot_executable() -> str:
    env_dot = os.environ.get("GRAPHVIZ_DOT")
    if env_dot and Path(env_dot).exists():
        return env_dot

    # If Graphviz is on PATH, use it
    for candidate in ["dot", "dot.exe"]:
        try:
            subprocess.run([candidate, "-V"], check=True, capture_output=True)
            return candidate
        except Exception:
            pass

    # Common Windows install locations
    candidates = [
        Path(os.environ.get("ProgramFiles", r"C:\\Program Files"))
        / "Graphviz"
        / "bin"
        / "dot.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\\Program Files (x86)"))
        / "Graphviz"
        / "bin"
        / "dot.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Graphviz" / "bin" / "dot.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError(
        "Graphviz 'dot' não encontrado. Instale Graphviz e/ou defina GRAPHVIZ_DOT apontando para dot.exe."
    )


def dot_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def html_label(lines: list[str], bold_first_line: bool = False) -> str:
    escaped = [dot_escape(x) for x in lines]
    if bold_first_line and escaped:
        escaped[0] = f"<B>{escaped[0]}</B>"
    return "<" + "<BR/>".join(escaped) + ">"


def render(dot_exe: str, dot_source: str, out_base: Path) -> None:
    out_base.parent.mkdir(parents=True, exist_ok=True)
    dot_path = out_base.with_suffix(".dot")
    dot_path.write_text(dot_source, encoding="utf-8")

    for fmt in ["png", "svg"]:
        out_path = out_base.with_suffix(f".{fmt}")
        subprocess.run(
            [
                dot_exe,
                f"-T{fmt}",
                str(dot_path),
                "-o",
                str(out_path),
            ],
            check=True,
        )


def build_flowchart(language: str) -> str:
    if language not in {"pt", "en"}:
        raise ValueError("language must be 'pt' or 'en'")

    if language == "pt":
        title_l1 = "Entradas do projeto\n/ qualificação"
        title_l2 = "Regras de decisão"
        title_l3 = "Tratamento recomendado"
        title_l4 = "Recomendação por objetivo"

        q0 = html_label(
            [
                "Ensaios rápidos",
                "(L/C, IC, FTIR;",
                "DRX/TGA)",
                "→ estimar VUF",
                "(P10)",
            ],
            bold_first_line=True,
        )
        i1 = html_label(["Vida útil", "alvo", "(VUF / P10)"])
        i2 = html_label(["Agressividade", "ambiental", "(UV: 0 / 0,5", "/ 1,0)"])
        i3 = html_label(["Ductilidade", "mínima", "(ε_max)"])

        d1 = html_label(["Uso temporário", "(VUF ≤ 60 dias)", "E UV ≤ 0,5?"], bold_first_line=True)
        d2 = html_label(
            ["UV ≥ 1,0 (exposição alta)", "OU exige ductilidade", "(ε_max ≥ 2,0%)?"],
            bold_first_line=True,
        )

        t0 = html_label(["T0 — Natural", "Aplicações temporárias", "(30–60 dias)"], bold_first_line=True)
        t2 = html_label(
            ["T2 — NaOH 6%", "Ponto de equilíbrio", "(VUF ~95 dias; ε_max ~2,8%)"],
            bold_first_line=True,
        )
        t3 = html_label(
            ["T3 — NaOH 9%", "Maior durabilidade", "(rigidez; ε_max < 2,0%)"],
            bold_first_line=True,
        )

        r0 = html_label(["Controle de erosão temporário", "/ revegetação (30–60 dias)"])
        r2 = html_label(["Bioengenharia de taludes tropicais", "(necessita deformabilidade)"])
        r3 = html_label(["Reforço/contensão rígida", "(deformação não crítica)"])

        n1 = html_label(
            [
                "Atenção: UV = 1,0",
                "→ erro pode atingir ~28%",
                "→ considerar correção não-linear",
                "/ validação local",
            ],
            bold_first_line=True,
        )
        s1 = html_label(
            [
                "Critérios sugeridos (especificação):",
                "R0 ≥ 20 kN/m; VUF ≥ 90 dias (P10);",
                "IC ≥ 60%; fim de vida: ε_max ≤ 2,0%",
            ],
            bold_first_line=True,
        )

        yes, no = "Sim", "Não"

    else:
        title_l1 = "Project inputs\n/ qualification"
        title_l2 = "Decision rules"
        title_l3 = "Recommended treatment"
        title_l4 = "Recommendation by project objective"

        q0 = html_label(
            [
                "Rapid assays",
                "(L/C, CI, FTIR;",
                "XRD/TGA)",
                "→ estimate FUL",
                "(P10)",
            ],
            bold_first_line=True,
        )
        i1 = html_label(["Target service", "life", "(FUL / P10)"])
        i2 = html_label(["Environmental", "aggressiveness", "(UV: 0 / 0.5", "/ 1.0)"])
        i3 = html_label(["Minimum", "ductility", "(ε_max)"])

        d1 = html_label(["Temporary use", "(VUF ≤ 60 days)", "AND UV ≤ 0.5?"], bold_first_line=True)
        d2 = html_label(
            ["UV ≥ 1.0 (high exposure)", "OR ductility required", "(ε_max ≥ 2.0%)?"],
            bold_first_line=True,
        )

        t0 = html_label(["T0 — Untreated", "Temporary applications", "(30–60 days)"], bold_first_line=True)
        t2 = html_label(
            ["T2 — 6% NaOH", "Balanced option", "(VUF ~95 days; ε_max ~2.8%)"],
            bold_first_line=True,
        )
        t3 = html_label(
            ["T3 — 9% NaOH", "Highest durability", "(stiffer; ε_max < 2.0%)"],
            bold_first_line=True,
        )

        r0 = html_label(["Temporary erosion control", "/ revegetation (30–60 days)"])
        r2 = html_label(["Tropical slope bioengineering", "(requires deformability)"])
        r3 = html_label(["Rigid reinforcement/containment", "(deformation not critical)"])

        n1 = html_label(
            [
                "Note: UV = 1.0",
                "→ error may reach ~28%",
                "→ consider non-linear correction",
                "/ local validation",
            ],
            bold_first_line=True,
        )
        s1 = html_label(
            [
                "Suggested specification targets:",
                "R0 ≥ 20 kN/m; FUL ≥ 90 days (P10);",
                "CI ≥ 60%; end-of-life: ε_max ≤ 2.0%",
            ],
            bold_first_line=True,
        )

        yes, no = "Yes", "No"

    # Graphviz DOT
    return f"""digraph G {{
  graph [
    charset="UTF-8",
    rankdir=LR,
    splines=ortho,
    nodesep=0.45,
    ranksep=0.65,
    pad=0.15,
    fontname="Arial",
    fontsize=12,
  ];

  node [
    fontname="Arial",
    fontsize=12,
    color="#111827",
    fontcolor="#111827",
    penwidth=1,
    style="rounded,filled",
    fillcolor="#ffffff",
    margin="0.12,0.08",
  ];

  edge [
    fontname="Arial",
    fontsize=11,
    color="#374151",
    fontcolor="#374151",
    penwidth=1,
    arrowsize=0.8,
  ];

  subgraph cluster_l1 {{
    label="{dot_escape(title_l1)}";
    labelloc=t;
    labeljust=l;
    color="#111827";
    penwidth=1;

          q0 [shape=parallelogram, fontsize=10, margin="0.08,0.05", label={q0}];
          i1 [shape=parallelogram, fontsize=10, margin="0.08,0.05", label={i1}];
          i2 [shape=parallelogram, fontsize=10, margin="0.08,0.05", label={i2}];
          i3 [shape=parallelogram, fontsize=10, margin="0.08,0.05", label={i3}];
  }}

  subgraph cluster_l2 {{
    label="{dot_escape(title_l2)}";
    labelloc=t;
    labeljust=l;
    color="#111827";
    penwidth=1;

    d1 [shape=diamond, style="filled", fillcolor="#ffffff", label={d1}];
    d2 [shape=diamond, style="filled", fillcolor="#ffffff", label={d2}];
  }}

  subgraph cluster_l3 {{
    label="{dot_escape(title_l3)}";
    labelloc=t;
    labeljust=l;
    color="#111827";
    penwidth=1;

    t0 [shape=box, label={t0}];
    t2 [shape=box, penwidth=3, label={t2}];
    t3 [shape=box, label={t3}];
  }}

  subgraph cluster_l4 {{
    label="{dot_escape(title_l4)}";
    labelloc=t;
    labeljust=l;
    color="#111827";
    penwidth=1;

    r0 [shape=box, label={r0}];
    r2 [shape=box, label={r2}];
    r3 [shape=box, label={r3}];
  }}

  n1 [shape=note, style="filled", fillcolor="#ffffff", label={n1}];
  s1 [shape=note, style="filled", fillcolor="#ffffff", label={s1}];

  // Primary flow
  q0 -> i1;
  i1 -> d1;
  i2 -> d1 [style=dashed, arrowhead=none];
    d1 -> t0 [xlabel="{yes}"];
    d1 -> d2 [xlabel="{no}"];
  i2 -> d2 [style=dashed, arrowhead=none];
  i3 -> d2 [style=dashed, arrowhead=none];
    d2 -> t2 [xlabel="{yes}"];
    d2 -> t3 [xlabel="{no}"];

  // Objective-oriented recommendations
  t0 -> r0;
  t2 -> r2;
  t3 -> r3;

  // Notes / boundaries
  i2 -> n1 [style=dashed, arrowhead=none];
  t2 -> s1 [style=dashed, arrowhead=none];
}}
"""


def main() -> int:
    dot_exe = find_dot_executable()

    pt_dot = build_flowchart("pt")
    en_dot = build_flowchart("en")

    render(dot_exe, pt_dot, ROOT / "fluxograma_decisorio_graphviz")
    render(dot_exe, en_dot, ROOT / "fluxograma_decisorio_en_graphviz")

    # Overwrite the manuscript-referenced PNGs to avoid touching the Markdown files
    (ROOT / "fluxograma_decisorio_graphviz.png").replace(ROOT / "fluxograma_decisorio.png")
    (ROOT / "fluxograma_decisorio_en_graphviz.png").replace(ROOT / "fluxograma_decisorio_en.png")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
