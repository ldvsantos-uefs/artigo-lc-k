import geopandas as gpd

try:
    br_uf = gpd.read_file("BR_UF_2024.shp")
    print("Columns in BR_UF_2024.shp:", br_uf.columns)
    
    se_mun = gpd.read_file("SE_Municipios_2024.shp")
    print("Columns in SE_Municipios_2024.shp:", se_mun.columns)
except Exception as e:
    print(e)
