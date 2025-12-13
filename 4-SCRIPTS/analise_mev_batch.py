
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from skimage import filters, morphology, measure, feature
from skimage.morphology import skeletonize
from scipy import ndimage
from pathlib import Path
import warnings
import json
from datetime import datetime

warnings.filterwarnings('ignore')

# Configurações de plotagem
plt.style.use('seaborn-v0_8-whitegrid')

class FiberAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, image_path):
        # Tenta carregar, suportando caminhos com caracteres especiais
        # cv2.imread não suporta bem caminhos com acentos/especiais no Windows
        # Solução: ler com numpy e decodificar
        stream = open(image_path, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(f"Não foi possível carregar: {image_path}")
        img_norm = img.astype(float) / 255.0
        return img, img_norm

    def analyze_surface_porosity(self, image_norm, sigma=2.0, threshold_factor=0.7):
        smoothed = filters.gaussian(image_norm, sigma=sigma)
        threshold = filters.threshold_otsu(smoothed)
        binary = smoothed < (threshold * threshold_factor)
        binary_clean = morphology.remove_small_objects(binary, min_size=20)
        binary_clean = morphology.remove_small_holes(binary_clean, area_threshold=10)
        
        labeled = measure.label(binary_clean)
        regions = measure.regionprops(labeled)
        
        total_area = image_norm.size
        pore_area = np.sum(binary_clean)
        porosity = (pore_area / total_area) * 100
        
        if regions:
            areas = [r.area for r in regions]
            results = {
                'porosity_percent': round(porosity, 2),
                'num_pores': len(regions),
                'mean_pore_area': round(np.mean(areas), 2)
            }
        else:
            results = {
                'porosity_percent': round(porosity, 2),
                'num_pores': 0,
                'mean_pore_area': 0
            }
        return results

    def analyze_fiber_orientation(self, image_norm, sigma=1.0):
        sobel_h = filters.sobel_h(filters.gaussian(image_norm, sigma=sigma))
        sobel_v = filters.sobel_v(filters.gaussian(image_norm, sigma=sigma))
        magnitude = np.sqrt(sobel_h**2 + sobel_v**2)
        orientation = np.arctan2(sobel_v, sobel_h)
        
        threshold = np.percentile(magnitude, 75)
        mask = magnitude > threshold
        
        if np.sum(mask) > 0:
            angles_deg = np.degrees(orientation[mask])
            angles_deg = (angles_deg + 180) % 180
            std_angle = np.std(angles_deg)
            orientation_index = 1 - (std_angle / 90.0)
            results = {
                'orientation_index': round(orientation_index, 3),
                'mean_angle_deg': round(np.mean(angles_deg), 2)
            }
        else:
            results = {'orientation_index': 0, 'mean_angle_deg': 0}
        return results

    def analyze_fiber_structure(self, image_norm, sigma=2.0):
        smoothed = filters.gaussian(image_norm, sigma=sigma)
        threshold = filters.threshold_otsu(smoothed)
        binary = smoothed > threshold
        skeleton = skeletonize(binary)
        
        fibril_density = np.sum(skeleton) / skeleton.size
        
        skeleton_float = skeleton.astype(float)
        corners = feature.corner_harris(skeleton_float, sigma=2.0)
        corner_threshold = np.percentile(corners, 99.9)
        junctions = corners > corner_threshold
        num_junctions = np.sum(junctions)
        
        results = {
            'fibril_density': round(fibril_density, 5),
            'num_junctions': int(num_junctions)
        }
        return results

    def analyze_surface_texture(self, image_norm, window_size=15):
        kernel = np.ones((window_size, window_size))
        local_mean = ndimage.convolve(image_norm, kernel / kernel.sum(), mode='reflect')
        local_var = ndimage.convolve(image_norm**2, kernel / kernel.sum(), mode='reflect') - local_mean**2
        local_std = np.sqrt(np.maximum(local_var, 0))
        roughness_std = np.mean(local_std)
        
        results = {'roughness_std': round(roughness_std, 5)}
        return results

    def process_image(self, image_path):
        try:
            img, img_norm = self.load_image(image_path)
            
            porosity_res = self.analyze_surface_porosity(img_norm)
            orient_res = self.analyze_fiber_orientation(img_norm)
            struct_res = self.analyze_fiber_structure(img_norm)
            texture_res = self.analyze_surface_texture(img_norm)
            
            return {
                'porosity': porosity_res['porosity_percent'],
                'orientation_index': orient_res['orientation_index'],
                'fibril_density': struct_res['fibril_density'],
                'roughness': texture_res['roughness_std']
            }
        except Exception as e:
            print(f"Erro ao processar {image_path}: {e}")
            return None

def main():
    base_dir = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC\MEV")
    output_dir = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC\processed_data\MEV_BATCH")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    analyzer = FiberAnalyzer(output_dir)
    
    groups = {
        "Natural (T0)": base_dir / "NAO_TRATADAS",
        "NaOH 6% (T2)": base_dir / "6%",
        "NaOH 9% (T3)": base_dir / "9%"
    }
    
    results = []
    
    print("Iniciando análise em lote...")
    
    for group_name, group_path in groups.items():
        if not group_path.exists():
            print(f"Aviso: Pasta não encontrada: {group_path}")
            continue
            
        print(f"\nProcessando grupo: {group_name}")
        # Buscar imagens (tif, png, jpg)
        images = list(group_path.glob("*.tif")) + list(group_path.glob("*.png")) + list(group_path.glob("*.jpg"))
        
        if not images:
            print(f"  Nenhuma imagem encontrada em {group_path}")
            continue
            
        for img_path in images:
            print(f"  Analisando: {img_path.name}")
            metrics = analyzer.process_image(img_path)
            
            if metrics:
                metrics['Group'] = group_name
                metrics['Filename'] = img_path.name
                results.append(metrics)
    
    if not results:
        print("Nenhum resultado obtido.")
        return
        
    df = pd.DataFrame(results)
    
    # Salvar CSV bruto
    csv_path = output_dir / "mev_batch_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nResultados salvos em: {csv_path}")
    
    # Calcular médias e desvios
    numeric_cols = ['porosity', 'orientation_index', 'fibril_density', 'roughness']
    summary = df.groupby('Group')[numeric_cols].agg(['mean', 'std']).round(4)
    print("\nRESUMO ESTATÍSTICO:")
    print(summary)
    
    # Salvar resumo
    summary.to_csv(output_dir / "mev_batch_summary.csv")
    
    # Gerar gráficos comparativos
    metrics_to_plot = ['porosity', 'orientation_index', 'fibril_density', 'roughness']
    titles = ['Porosity (%)', 'Orientation Index', 'Fibril Density', 'Roughness (std)']
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics_to_plot):
        sns.boxplot(x='Group', y=metric, data=df, ax=axes[i], palette="Set2")
        sns.stripplot(x='Group', y=metric, data=df, ax=axes[i], color='black', alpha=0.5, jitter=True)
        axes[i].set_title(titles[i], fontweight='bold')
        axes[i].set_xlabel('')
        
    plt.tight_layout()
    plot_path = output_dir / "mev_comparativo_batch.png"
    plt.savefig(plot_path, dpi=300)
    print(f"Gráfico comparativo salvo em: {plot_path}")

if __name__ == "__main__":
    main()
