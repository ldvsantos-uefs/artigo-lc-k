import zipfile
import xml.etree.ElementTree as ET
import re

def ler_docx(caminho_arquivo):
    """
    Lê o texto de um arquivo .docx extraindo o XML interno.
    """
    try:
        with zipfile.ZipFile(caminho_arquivo) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            texto_completo = []
            for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                textos = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                if textos:
                    texto_completo.append(''.join(textos))
            
            return '\n'.join(texto_completo)
    except Exception as e:
        return f"Erro ao ler docx: {e}"

if __name__ == "__main__":
    texto = ler_docx("manuscrito_degradacao.docx")
    # Salvar em txt para facilitar leitura
    with open("conteudo_manuscrito.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("Texto extraído para conteudo_manuscrito.txt")
    
    # Mostrar as primeiras linhas para ver se funcionou
    print(texto[:2000])
