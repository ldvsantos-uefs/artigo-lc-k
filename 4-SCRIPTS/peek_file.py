import sys
from pathlib import Path

if len(sys.argv) < 2:
    print('Uso: python peek_file.py <caminho_para_arquivo>')
    raise SystemExit(1)

P = Path(sys.argv[1])
if not P.exists():
    print('Arquivo não encontrado:', P)
    raise SystemExit(1)

data = None
for enc in ('utf-8', 'latin1', 'cp1252'):
    try:
        with open(P, 'r', encoding=enc, errors='strict') as f:
            lines = [next(f) for _ in range(40)]
        print(f'--- Decodificado com {enc} ---')
        print(''.join(lines))
        data = True
        break
    except StopIteration:
        print(f'--- Decodificado com {enc} (menos de 40 linhas) ---')
        break
    except Exception as e:
        print(f'Falha com {enc}:', e)

if not data:
    print('Não foi possível decodificar com utf-8/latin1/cp1252; tentando leitura binária (primeiros 200 bytes)')
    with open(P, 'rb') as f:
        b = f.read(200)
        print(b)
