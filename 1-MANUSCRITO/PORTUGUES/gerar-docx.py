#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo Word da revisão de escopo a partir do Markdown.

Uso: python gerar-docx.py

Gera o arquivo revisao_artigo.docx a partir do modelar_LC_K.md.
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def gerar_docx(md_file, output_file, bib_file, csl_file, apendices_file=None):
    """
    Gera arquivo DOCX usando Pandoc.
    
    Args:
        md_file: Arquivo Markdown de entrada
        output_file: Arquivo DOCX de saída
        bib_file: Arquivo de bibliografia
        csl_file: Arquivo de estilo de citação
        apendices_file: Arquivo de apêndices (opcional)
    
    Returns:
        0 se sucesso, 1 se erro
    """
    print(f"\nGerando {output_file.name}...")
    
    # Remover arquivo antigo se existir
    # Em Windows/OneDrive, é comum o DOCX estar bloqueado se estiver aberto.
    # Se não for possível apagar, gera com sufixo "_novo".
    if output_file.exists():
        print(f"[INFO] Removendo arquivo antigo: {output_file.name}")
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                output_file.unlink()
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    print(f"[AVISO] Tentativa {attempt + 1}/{max_attempts}: Arquivo em uso, aguardando...")
                    time.sleep(0.6)
                else:
                    novo_output = output_file.with_name(f"{output_file.stem}_novo{output_file.suffix}")
                    print(f"[AVISO] Não foi possível remover '{output_file.name}' (arquivo em uso).")
                    print(f"[INFO] Gerando em arquivo alternativo: {novo_output.name}")
                    output_file = novo_output
                    break
    
    # Comando Pandoc
    cmd = [
        "pandoc",
        str(md_file),
    ]
    
    # Adicionar apêndices ANTES do --citeproc
    if apendices_file and apendices_file.exists():
        cmd.append(str(apendices_file))
        print(f"[INFO] Incluindo apendices: {apendices_file.name}")
    
    # Adicionar resource-path para encontrar figuras (compatível com Windows via os.pathsep)
    md_dir = md_file.parent.resolve()
    repo_root = Path(__file__).resolve().parent.parent.parent
    resource_paths = [
        str(md_dir),
        str(repo_root),
        str(repo_root / "1-MANUSCRITO" / "PORTUGUES"),
        str(repo_root / "1-MANUSCRITO" / "INGLES"),
        str(repo_root / "3-IMAGENS" / "PORTUGUES"),
        str(repo_root / "3-IMAGENS" / "INGLES"),
    ]
    cmd.extend([
        "--resource-path", os.pathsep.join(resource_paths),
    ])
    
    # Adicionar processamento de citações
    cmd.extend([
        "--citeproc",
        "--bibliography", str(bib_file),
        "--csl", str(csl_file),
    ])
    
    # Adicionar modelo de formatação se existir (padroniza PT/EN)
    # Preferir o template canônico em 1-MANUSCRITO/PORTUGUES para manter o mesmo estilo.
    modelo_canonico = (repo_root / "1-MANUSCRITO" / "PORTUGUES" / "modelo_formatacao.docx").resolve()
    modelo_local = (md_dir / "modelo_formatacao.docx").resolve()

    modelo = modelo_canonico if modelo_canonico.exists() else (modelo_local if modelo_local.exists() else None)
    if modelo is not None:
        print(f"[INFO] Usando modelo de formatação: {modelo}")
        cmd.extend(["--reference-doc", str(modelo)])
    
    cmd.extend(["-o", str(output_file)])
    
    print("Executando Pandoc...")
    
    try:
        # Executar Pandoc
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=str(md_dir),
        )
        
        # Mostrar warnings/erros do Pandoc
        if result.stderr:
            print(f"\nAvisos do Pandoc para {output_file.name}:")
            print(result.stderr)
        
        # Verificar código de saída do Pandoc
        if result.returncode != 0:
            print(f"\nErro: Pandoc retornou código {result.returncode} ao gerar {output_file.name}.")
            if result.stdout:
                print("Saída:", result.stdout)
            return 1
        
        # Verificar se o arquivo foi criado
        if output_file.exists():
            print(f"\nArquivo {output_file.name} gerado com sucesso.")
            print(f"Localização: {output_file.absolute()}")
            print(f"Tamanho: {output_file.stat().st_size / 1024:.1f} KB")
            return 0
        else:
            print(f"\nErro: o arquivo {output_file.name} não foi gerado.")
            if result.stdout:
                print("Saída:", result.stdout)
            return 1
            
    except FileNotFoundError:
        print("\nErro: Pandoc não está instalado ou não está no PATH do sistema.")
        print("Instale o Pandoc em: https://pandoc.org/installing.html")
        return 1
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        return 1

def gerar_pdf(md_file, output_file, bib_file, csl_file, pdf_engine="xelatex"):
    """
    Gera arquivo PDF usando Pandoc com um motor LaTeX (xelatex por padrão).

    Args:
        md_file: Arquivo Markdown de entrada
        output_file: Arquivo PDF de saída
        bib_file: Arquivo de bibliografia
        csl_file: Arquivo de estilo de citação
        pdf_engine: Motor de conversão para PDF (xelatex, lualatex, pdflatex)

    Returns:
        0 se sucesso, 1 se erro
    """
    print(f"\nGerando {output_file.name}...")

    # Remover arquivo antigo se existir
    if output_file.exists():
        print(f"📝 Removendo arquivo antigo: {output_file.name}")
        try:
            output_file.unlink()
        except PermissionError:
            print(f"Erro: não foi possível remover '{output_file.name}'. Verifique se está aberto.")
            return 1

    cmd = [
        "pandoc",
        str(md_file),
        "--citeproc",
        "--bibliography", str(bib_file),
        "--csl", str(csl_file),
        "-o", str(output_file),
        "--pdf-engine", pdf_engine,
    ]

    print("Executando Pandoc para PDF...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stderr:
            print("Avisos do Pandoc (PDF):")
            print(result.stderr)
        if result.returncode != 0:
            print(f"Erro: Pandoc retornou código {result.returncode} ao gerar {output_file.name}.")
            return 1
        if output_file.exists():
            print(f"Arquivo {output_file.name} gerado com sucesso.")
            return 0
        else:
            print(f"Erro: o arquivo {output_file.name} não foi gerado.")
            return 1
    except FileNotFoundError:
        print("Erro: Pandoc não encontrado. Instale Pandoc antes de continuar.")
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1

def main():
    # Estrutura atual do repositório: <root>/1-MANUSCRITO/{PORTUGUES,INGLES}
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    os.chdir(repo_root)
    print(f"[INFO] Diretório de trabalho definido para: {repo_root}")
    
    print("=" * 70)
    print("GERADOR DE REVISÃO DE ESCOPO - WORD")
    print("=" * 70)
    
    # Arquivos comuns
    bib_file = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "referencias_lc.bib"
    csl_file = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "apa.csl"
    apendices_pt = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "apendices.md"
    
    # Verificar arquivos necessários
    arquivos_necessarios = [bib_file, csl_file]
    arquivos_faltando = [f for f in arquivos_necessarios if not f.exists()]
    
    if arquivos_faltando:
        print("\nErro: arquivos necessários não encontrados:")
        for arquivo in arquivos_faltando:
            print(f"   - {arquivo}")
        return 1
    
    # Contador de sucesso
    sucessos = 0
    total = 0
    
    # ========================================================================
    # GERAR REVISÃO DE ESCOPO
    # ========================================================================
    # Versão PT
    md_pt = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "modelar_LC_K.md"
    docx_pt = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "modelo_LC_K.docx"
    result_pt = 1

    if not md_pt.exists():
        print(f"\nArquivo {md_pt} não encontrado!")
        return 1
    else:
        total += 1
        result_pt = gerar_docx(md_pt, docx_pt, bib_file, csl_file)
        if result_pt == 0:
            sucessos += 1
    
    # Versão EN (inglês)
    md_en = repo_root / "1-MANUSCRITO" / "INGLES" / "modelar_LC_K_EN.md"
    docx_en = repo_root / "1-MANUSCRITO" / "INGLES" / "modelo_LC_K_EN.docx"
    
    if md_en.exists():
        print(f"\n[INFO] Encontrado {md_en.name} - gerando DOCX em inglês...")
        total += 1
        result_en = gerar_docx(md_en, docx_en, bib_file, csl_file)
        if result_en == 0:
            sucessos += 1
    else:
        print(f"\n[AVISO] Arquivo {md_en.name} não encontrado. Pulando geração da versão em inglês.")

    # ========================================================================
    # GERAR MATERIAL SUPLEMENTAR
    # ========================================================================
    md_suplementar = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "material_suplementar.md"
    docx_suplementar = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "material_suplementar.docx"
    
    if md_suplementar.exists():
        print(f"\n[INFO] Encontrado {md_suplementar.name} - gerando DOCX...")
        total += 1
        result_suplementar = gerar_docx(md_suplementar, docx_suplementar, bib_file, csl_file)
        if result_suplementar == 0:
            sucessos += 1
    else:
        print(f"\n[AVISO] Arquivo {md_suplementar.name} não encontrado. Pulando geração do material suplementar.")

    # Material Suplementar EN (inglês)
    md_suplementar_en = repo_root / "1-MANUSCRITO" / "INGLES" / "material_suplementar_EN.md"
    docx_suplementar_en = repo_root / "1-MANUSCRITO" / "INGLES" / "material_suplementar_EN.docx"
    
    if md_suplementar_en.exists():
        print(f"\n[INFO] Encontrado {md_suplementar_en.name} - gerando DOCX em inglês...")
        total += 1
        result_suplementar_en = gerar_docx(md_suplementar_en, docx_suplementar_en, bib_file, csl_file)
        if result_suplementar_en == 0:
            sucessos += 1
    else:
        print(f"\n[AVISO] Arquivo {md_suplementar_en.name} não encontrado. Pulando geração do material suplementar em inglês.")

    # Gerar PDF opcionalmente
    # Use argumento de linha de comando: python gerar-docx.py --pdf
    if len(sys.argv) > 1 and sys.argv[1] in ("--pdf", "-p"):
        pdf_output = repo_root / "1-MANUSCRITO" / "PORTUGUES" / "revisao_artigo.pdf"
        print("\n[INFO] Opcao de PDF detectada - gerando PDF com xelatex...")
        if md_pt.exists():
            total += 1
            result_pdf = gerar_pdf(md_pt, pdf_output, bib_file, csl_file, pdf_engine="xelatex")
            if result_pdf == 0:
                sucessos += 1
        else:
            print("[AVISO] Arquivo Markdown não encontrado para gerar PDF")
    
    # ========================================================================
    # RESUMO FINAL
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 RESUMO DA GERAÇÃO")
    print("=" * 70)
    print(f"[OK] Arquivos gerados com sucesso: {sucessos}/{total}")
    
    if sucessos == total:
        print("\nTodos os arquivos foram gerados com sucesso.")
        return 0
    elif sucessos > 0:
        print(f"\nAlguns arquivos não foram gerados ({total - sucessos} falharam).")
        return 1
    else:
        print("\nNenhum arquivo foi gerado.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
