import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
try:
    import contextily as ctx
    HAS_CONTEXTILY = True
except ImportError:
    HAS_CONTEXTILY = False
    print("Aviso: 'contextily' não encontrado. O mapa será gerado sem fundo de satélite/rua.")

# Configurações de Fonte
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']

def add_north_arrow(ax, x, y, arrow_length=0.1):
    """Adiciona uma seta norte simples ao eixo."""
    ax.annotate('N', xy=(x, y + arrow_length), xytext=(x, y),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=12, xycoords=ax.transAxes)

def add_scale_bar(ax, length, location=(0.5, 0.05), linewidth=3):
    """
    Adiciona uma barra de escala simples.
    length: comprimento da barra em graus (aproximado) ou unidades do mapa.
    location: tupla (x, y) em coordenadas dos eixos (0-1).
    """
    x, y = location
    # Linha da escala
    ax.plot([x - length/2, x + length/2], [y, y], transform=ax.transAxes, 
            color='black', linewidth=linewidth)
    # Bordas verticais
    ax.plot([x - length/2, x - length/2], [y - 0.01, y + 0.01], transform=ax.transAxes, 
            color='black', linewidth=linewidth)
    ax.plot([x + length/2, x + length/2], [y - 0.01, y + 0.01], transform=ax.transAxes, 
            color='black', linewidth=linewidth)
    
    # Texto (precisa ajustar o valor do texto manualmente ou calcular geodésica se quiser precisão absoluta)
    # Aqui vamos deixar genérico ou pedir para o usuário ajustar o label
    ax.text(x, y + 0.02, "Graphic Scale", transform=ax.transAxes, 
            ha='center', va='bottom', fontsize=10)

def main():
    # 1. Carregar Dados
    try:
        br_uf = gpd.read_file("BR_UF_2024.shp")
        if len(br_uf) == 0:
            print("Aviso: BR_UF_2024.shp está vazio. Tentando baixar mapa mundi simplificado...")
            try:
                # Tentar URL direto do Natural Earth
                url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
                world = gpd.read_file(url)
                br_uf = world[world['NAME'] == 'Brazil']
            except Exception as e_download:
                print(f"Erro ao baixar mapa online: {e_download}")
                print("Criando geometria simplificada para o Brasil (fallback).")
                from shapely.geometry import box
                # Bounding box aproximado do Brasil
                br_poly = box(-74.0, -34.0, -34.0, 5.5)
                br_uf = gpd.GeoDataFrame({'geometry': [br_poly], 'NAME': ['Brazil']}, crs="EPSG:4326")
        
        se_mun = gpd.read_file("SE_Municipios_2024.shp")
    except Exception as e:
        print(f"Erro ao carregar shapefiles: {e}")
        return

    # Coordenadas Atualizadas (DMS para Decimal)
    # Povoado Tigre: 10°35'21.2"S 36°40'14.3"W
    tigre_lat = -(10 + 35/60 + 21.2/3600)
    tigre_lon = -(36 + 40/60 + 14.3/3600)
    tigre_coords = (tigre_lon, tigre_lat)
    
    # Lagoas de Typha: 10°35'23.8"S 36°40'14.5"W
    lagoa_lat = -(10 + 35/60 + 23.8/3600)
    lagoa_lon = -(36 + 40/60 + 14.5/3600)
    lagoa_coords = (lagoa_lon, lagoa_lat)

    tigre_point = Point(tigre_coords)
    lagoa_point = Point(lagoa_coords)
    
    gdf_tigre = gpd.GeoDataFrame({'geometry': [tigre_point], 'label': ['Povoado Tigre']}, crs="EPSG:4326")
    gdf_lagoa = gpd.GeoDataFrame({'geometry': [lagoa_point], 'label': ['Lagoas de Typha']}, crs="EPSG:4326")

    # Converter para SIRGAS 2000 / UTM zone 24S (EPSG:31984) para medidas métricas corretas se necessário
    # Mas para plotagem simples com lat/lon, manteremos WGS84 ou SIRGAS2000 Geográfico (4674)
    # Os arquivos parecem estar em coordenadas geográficas. Vamos garantir.
    if br_uf.crs is None: br_uf.set_crs(epsg=4674, inplace=True)
    if se_mun.crs is None: se_mun.set_crs(epsg=4674, inplace=True)
    
    # Filtrar Sergipe e Pacatuba
    # Como BR_UF_2024 não tem colunas de nome, vamos criar o contorno de Sergipe dissolvendo os municípios
    sergipe_boundary = se_mun.dissolve()
    pacatuba = se_mun[se_mun['NM_MUN'] == 'Pacatuba']

    # 2. Configurar Layout da Figura (A4 Paisagem)
    fig = plt.figure(figsize=(11.69, 8.27)) # A4 em polegadas
    gs = GridSpec(1, 2, width_ratios=[1, 3], figure=fig, wspace=0.05)

    # --- Coluna da Esquerda (Informações e Insets) ---
    # Usar subgridspec para criar subplots dentro da primeira coluna
    gs_left = gs[0].subgridspec(3, 1, height_ratios=[1, 1, 1], hspace=0.3)

    # Inset 1: Brasil com destaque para Sergipe
    ax_br = fig.add_subplot(gs_left[0])
    try:
        br_uf.plot(ax=ax_br, color='white', edgecolor='gray', linewidth=0.5, aspect=1)
        sergipe_boundary.plot(ax=ax_br, color='black', edgecolor='black', aspect=1)
    except ValueError:
        # Fallback se aspect falhar
        br_uf.plot(ax=ax_br, color='white', edgecolor='gray', linewidth=0.5)
        sergipe_boundary.plot(ax=ax_br, color='black', edgecolor='black')
    
    ax_br.set_title("Location in Brazil", fontsize=10)
    ax_br.axis('off')

    # Inset 2: Sergipe com destaque para Pacatuba
    ax_se = fig.add_subplot(gs_left[1])
    try:
        se_mun.plot(ax=ax_se, color='white', edgecolor='gray', linewidth=0.5, aspect=1)
        pacatuba.plot(ax=ax_se, color='black', edgecolor='black', aspect=1)
    except ValueError:
        se_mun.plot(ax=ax_se, color='white', edgecolor='gray', linewidth=0.5)
        pacatuba.plot(ax=ax_se, color='black', edgecolor='black')
        
    ax_se.set_title("Location in Sergipe", fontsize=10)
    ax_se.axis('off')

    # Texto / Legenda
    ax_text = fig.add_subplot(gs_left[2])
    ax_text.axis('off')
    text_content = (
        "LOCATION MAP\n\n"
        "Tigre Village\n"
        "Pacatuba Municipality - SE\n\n"
        "Coordinates:\n"
        f"Lat: {tigre_coords[1]:.4f} S\n"
        f"Lon: {tigre_coords[0]:.4f} W\n\n"
        "Reference System:\n"
        "SIRGAS 2000"
    )
    ax_text.text(0.5, 0.6, text_content, ha='center', va='center', fontsize=12)

    # --- Coluna da Direita (Mapa Principal) ---
    ax_main = fig.add_subplot(gs[1])
    
    # Plotar Pacatuba (Zoom)
    # Vamos dar um buffer ao redor de Pacatuba para mostrar os vizinhos
    bounds = pacatuba.total_bounds
    xlim = ([bounds[0]-0.1, bounds[2]+0.1])
    ylim = ([bounds[1]-0.1, bounds[3]+0.1])
    
    # Plotar municípios vizinhos (recorte)
    se_mun.cx[xlim[0]:xlim[1], ylim[0]:ylim[1]].plot(
        ax=ax_main, color='#f0f0f0', edgecolor='gray', linewidth=0.8, aspect=1
    )
    
    # Destaque Pacatuba
    # Adicionando hachura (hatch='///') para destaque
    pacatuba.plot(ax=ax_main, color='white', edgecolor='gray', linewidth=2.0, aspect=1, hatch='///')
    
    # Adicionar nome do Município
    # Ajuste manual da posição se necessário, ou usar centroide
    centroid = pacatuba.geometry.centroid.iloc[0]
    ax_main.text(centroid.x, centroid.y + 0.02, "Pacatuba", fontsize=12, ha='center', va='bottom', fontweight='bold', color='blue')

    # Plotar Ponto do Tigre
    gdf_tigre.plot(ax=ax_main, color='red', markersize=100, marker='*', label='Povoado Tigre', aspect=1)
    
    # --- Inset: Imagem de Satélite (Zoom no Tigre) ---
    # Criar um eixo inset no canto superior direito do mapa principal
    ax_ins = inset_axes(ax_main, width="35%", height="35%", loc='upper right', borderpad=1)
    
    # Definir extensão do zoom (aprox 1km ao redor do ponto)
    # 1 grau ~ 111km -> 1km ~ 0.009 graus. Raio de 500m ~ 0.0045
    delta = 0.0045
    xlim_ins = (tigre_coords[0] - delta, tigre_coords[0] + delta)
    ylim_ins = (tigre_coords[1] - delta, tigre_coords[1] + delta)
    
    # Plotar o ponto no inset
    gdf_tigre.plot(ax=ax_ins, color='yellow', markersize=100, marker='*', zorder=5, label='Povoado Tigre')
    gdf_lagoa.plot(ax=ax_ins, color='cyan', markersize=80, marker='D', zorder=5, label='Lagoas de Typha')
    
    # Adicionar Legenda no Inset
    # (Removido conforme solicitação - legenda movida para o painel esquerdo)
    
    # Configurar limites e remover eixos
    ax_ins.set_xlim(xlim_ins)
    ax_ins.set_ylim(ylim_ins)
    ax_ins.set_xticks([])
    ax_ins.set_yticks([])
    
    # Adicionar borda branca ao inset
    for spine in ax_ins.spines.values():
        spine.set_edgecolor('white')
        spine.set_linewidth(2)
        
    # Adicionar Basemap de Satélite no Inset
    if HAS_CONTEXTILY:
        try:
            # Usar Esri World Imagery para satélite
            # crs=se_mun.crs.to_string() assume que os limites do eixo estão no mesmo CRS do shapefile (que deve ser Lat/Lon ou UTM)
            # Como definimos xlim_ins com coordenadas Lat/Lon (tigre_coords), precisamos garantir que o CRS passado seja 4326
            # Se se_mun.crs for 4674 (SIRGAS 2000), é compatível com 4326 para fins de plotagem web (diferença mínima)
            # Mas para garantir, vamos passar explicitamente EPSG:4326 pois xlim_ins são Lat/Lon
            ctx.add_basemap(ax_ins, crs="EPSG:4326", source=ctx.providers.Esri.WorldImagery, attribution=False)
            ax_ins.set_title("Detail (Satellite)", fontsize=8, color='white', pad=2)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o basemap satélite: {e}")
            ax_ins.text(0.5, 0.5, "No Satellite", ha='center', va='center', fontsize=8)

    # Adicionar Basemap (opcional, requer internet e contextily)
    if HAS_CONTEXTILY:
        try:
            ctx.add_basemap(ax_main, crs=se_mun.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.3)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o basemap: {e}")

    # Adicionar Legenda no Mapa Principal (Canto Inferior Esquerdo)
    import matplotlib.lines as mlines
    star = mlines.Line2D([], [], color='red', marker='*', linestyle='None',
                          markersize=10, label='Tigre Village')
    diamond = mlines.Line2D([], [], color='cyan', marker='D', linestyle='None',
                          markersize=8, label='Typha Lagoons')
    
    ax_main.legend(handles=[star, diamond], loc='lower left', title="Legend", frameon=True, fontsize=10)

    # Configurações do Mapa Principal
    ax_main.set_xlim(xlim)
    ax_main.set_ylim(ylim)
    ax_main.set_title("Study Area Detail", fontsize=14)
    ax_main.set_xlabel("Longitude")
    ax_main.set_ylabel("Latitude")
    
    # Grid
    ax_main.grid(True, linestyle='--', alpha=0.5)
    
    # Norte e Escala (Manuais e simples)
    add_north_arrow(ax_main, 0.95, 0.90)
    # Escala aproximada visual (ajuste conforme necessário)
    # ax_main.text(0.95, 0.05, "Escala Gráfica", transform=ax_main.transAxes, ha='right')

    # Moldura
    for spine in ax_main.spines.values():
        spine.set_linewidth(2)

    plt.tight_layout()
    # Salvar diretamente na pasta de imagens
    import os
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../3-IMAGENS"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "mapa_tigre_python.png")
    
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Mapa salvo em: {output_file}")
    except MemoryError:
        print("Erro de memória ao salvar com 300 DPI. Tentando com 150 DPI...")
        try:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Mapa salvo em: {output_file} (150 DPI)")
        except MemoryError:
            print("Erro de memória ao salvar com 150 DPI. Tentando com 100 DPI...")
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"Mapa salvo em: {output_file} (100 DPI)")
    except Exception as e:
        print(f"Erro ao salvar o mapa: {e}")
    finally:
        plt.close(fig)

if __name__ == "__main__":
    main()
