import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology, feature, filters, measure
from skimage.measure import regionprops, label
try:
    from skimage.feature import graycomatrix, graycoprops
except ImportError:
    from skimage.feature import greycomatrix as graycomatrix
    from skimage.feature import greycoprops as graycoprops
from scipy.ndimage import generic_filter
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

class MEVAnalyzer:
    """Morphometric analyzer for SEM images (Adapted from Review Article)"""

    def load_image(self, image_path):
        # Read with Windows/Unicode path support
        stream = open(image_path, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyarray, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(f"Error loading: {image_path}")
        
        # Normalize
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        return img

    def analyze_porosity(self, img):
        # Otsu Threshold
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # Calculate %
        porosity_pct = (np.sum(binary > 0) / img.size) * 100
        
        return binary, porosity_pct

    def analyze_structure(self, img):
        # Adaptive threshold for fibers
        binary = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Skeletonize
        skeleton = morphology.skeletonize(binary > 0)
        
        # Density
        density = np.sum(skeleton) / skeleton.size * 100
        
        return skeleton, density

    def analyze_roughness(self, img):
        # Local variance (roughness)
        local_var = generic_filter(img.astype(float), np.var, size=7)
        mean_roughness = np.mean(local_var)
        return local_var, mean_roughness

def create_comparative_panel():
    base_dir = Path(r"C:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC\MEV")
    
    # Image definitions (500x)
    # Adjust according to files found
    images_map = {
        "Untreated": base_dir / "NAO_TRATADAS" / "100_u_500.tif",
        "3% NaOH": base_dir / "3%" / "100_u_500.tif",
        "6% NaOH": base_dir / "6%" / "100_u_500.tif",
        "9% NaOH": base_dir / "9%" / "100_u_500.tif"
    }
    
    # Check existence
    for label, path in images_map.items():
        if not path.exists():
            print(f"ERROR: Image not found for {label}: {path}")
            # Try fallback for 9% if 503x doesn't exist
            if label == "9% NaOH":
                fallback = base_dir / "9%" / "505x.tif"
                if fallback.exists():
                    print(f"  -> Using fallback: {fallback}")
                    images_map[label] = fallback
                else:
                    return
            else:
                return

    analyzer = MEVAnalyzer()
    
    # Set up Grid: 4 Columns (Treatments) x 4 Rows (Original, Pores, Skeleton, Roughness)
    
    fig, axes = plt.subplots(4, 4, figsize=(20, 16))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    
    cols = ["Untreated", "3% NaOH", "6% NaOH", "9% NaOH"]
    rows = ["Original", "Porosity (Mask)", "Fibrillar Skeleton", "Roughness (Heatmap)"]
    
    # Column titles
    for ax, col in zip(axes[0], cols):
        ax.set_title(col, fontsize=14, fontweight='bold')

    # Row titles (in first column)
    for ax, row in zip(axes[:, 0], rows):
        ax.set_ylabel(row, fontsize=14, fontweight='bold')

    results_data = {}

    print("\n--- QUANTITATIVE RESULTS ---")
    print(f"{'Treatment':<20} | {'Porosity (%)':<15} | {'Density (%)':<15} | {'Roughness':<15}")
    print("-" * 75)

    for idx, (label_name, img_path) in enumerate(images_map.items()):
        print(f"Processing {label_name}...")
        img = analyzer.load_image(img_path)
        
        # 1. Original
        axes[0, idx].imshow(img, cmap='gray')
        axes[0, idx].axis('off')
        
        # 2. Porosity
        mask, porosity = analyzer.analyze_porosity(img)
        axes[1, idx].imshow(img, cmap='gray', alpha=0.7)
        axes[1, idx].imshow(mask, cmap='Reds', alpha=0.5)
        axes[1, idx].axis('off')
        axes[1, idx].text(0.5, -0.1, f"Porosity: {porosity:.1f}%", 
                         transform=axes[1, idx].transAxes, ha='center', fontsize=11, fontweight='bold')
        
        # 3. Skeleton
        skeleton, density = analyzer.analyze_structure(img)
        axes[2, idx].imshow(img, cmap='gray', alpha=0.6)
        axes[2, idx].imshow(skeleton, cmap='hot', alpha=0.7)
        axes[2, idx].axis('off')
        axes[2, idx].text(0.5, -0.1, f"Density: {density:.1f}%", 
                         transform=axes[2, idx].transAxes, ha='center', fontsize=11, fontweight='bold')
        
        # 4. Roughness
        roughness_map, mean_rough = analyzer.analyze_roughness(img)
        im = axes[3, idx].imshow(roughness_map, cmap='jet')
        axes[3, idx].axis('off')
        axes[3, idx].text(0.5, -0.1, f"Roughness: {mean_rough:.1f}", 
                         transform=axes[3, idx].transAxes, ha='center', fontsize=11, fontweight='bold')
        
        print(f"{label_name:<20} | {porosity:<15.2f} | {density:<15.2f} | {mean_rough:<15.2f}")

        # Add colorbar only in last column of roughness
        if idx == 3:
            cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.15])
            fig.colorbar(im, cax=cbar_ax)

    # Save
    output_path = base_dir.parent / "figura_painel_comparativo_500x_en.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Figure saved at: {output_path}")

if __name__ == "__main__":
    create_comparative_panel()
