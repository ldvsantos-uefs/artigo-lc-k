
import cv2
import numpy as np
from skimage import filters, morphology, measure, feature
from skimage.morphology import skeletonize
from scipy import ndimage
import matplotlib.pyplot as plt
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

class FiberAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, image_path):
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
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
        return results, binary_clean

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
        return results, magnitude

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
        return results, skeleton

    def analyze_surface_texture(self, image_norm, window_size=15):
        kernel = np.ones((window_size, window_size))
        local_mean = ndimage.convolve(image_norm, kernel / kernel.sum(), mode='reflect')
        local_var = ndimage.convolve(image_norm**2, kernel / kernel.sum(), mode='reflect') - local_mean**2
        local_std = np.sqrt(np.maximum(local_var, 0))
        roughness_std = np.mean(local_std)
        
        results = {'roughness_std': round(roughness_std, 5)}
        return results, local_std

    def process_image(self, image_path, label):
        print(f"Processando: {image_path}")
        img, img_norm = self.load_image(image_path)
        
        porosity_res, binary = self.analyze_surface_porosity(img_norm)
        orient_res, magnitude = self.analyze_fiber_orientation(img_norm)
        struct_res, skeleton = self.analyze_fiber_structure(img_norm)
        texture_res, roughness = self.analyze_surface_texture(img_norm)
        
        # Plotting
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Análise Morfométrica MEV - {label}', fontsize=16, fontweight='bold')
        
        # Original
        axes[0,0].imshow(img, cmap='gray')
        axes[0,0].set_title('Imagem Original')
        axes[0,0].axis('off')
        
        # Porosidade
        axes[0,1].imshow(binary, cmap='gray')
        axes[0,1].set_title(f'Porosidade: {porosity_res["porosity_percent"]}%')
        axes[0,1].axis('off')
        
        # Orientação
        axes[0,2].imshow(magnitude, cmap='jet')
        axes[0,2].set_title(f'Orientação (IO={orient_res["orientation_index"]})')
        axes[0,2].axis('off')
        
        # Esqueleto
        axes[1,0].imshow(skeleton, cmap='gray')
        axes[1,0].set_title(f'Estrutura (D={struct_res["fibril_density"]})')
        axes[1,0].axis('off')
        
        # Rugosidade
        axes[1,1].imshow(roughness, cmap='hot')
        axes[1,1].set_title(f'Rugosidade (σ={texture_res["roughness_std"]})')
        axes[1,1].axis('off')
        
        # Resumo
        axes[1,2].axis('off')
        summary = f"""
        RESUMO - {label}
        
        Porosidade: {porosity_res["porosity_percent"]}%
        N° Poros: {porosity_res["num_pores"]}
        
        Orientação (IO): {orient_res["orientation_index"]}
        Ângulo Médio: {orient_res["mean_angle_deg"]}°
        
        Densidade Fibrilar: {struct_res["fibril_density"]}
        Junções: {struct_res["num_junctions"]}
        
        Rugosidade (σ): {texture_res["roughness_std"]}
        """
        axes[1,2].text(0.1, 0.5, summary, fontsize=10, verticalalignment='center', family='monospace')
        
        plt.tight_layout()
        output_file = self.output_dir / f"analise_mev_{label}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Salvo em: {output_file}")

if __name__ == "__main__":
    # Caminhos absolutos
    input_image = r"C:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC\MEV\T1.300x.tif"
    output_folder = r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS"
    
    analyzer = FiberAnalyzer(output_folder)
    try:
        analyzer.process_image(input_image, "Typha_Domingensis_Natural")
    except Exception as e:
        print(f"Erro: {e}")
