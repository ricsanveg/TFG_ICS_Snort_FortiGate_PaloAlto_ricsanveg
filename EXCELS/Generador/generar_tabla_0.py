import pandas as pd
import os

def cargar_ods_robusto(path, version_label):
    if not os.path.exists(path):
        print(f"[-] No existe: {path}")
        return None
    
    print(f"[*] Analizando {version_label}...")
    try:
        # Cargamos el archivo completo
        xl = pd.ExcelFile(path, engine='odf')
        sheet = 'Techniques' if 'Techniques' in xl.sheet_names else xl.sheet_names[0]
        df_raw = xl.parse(sheet, header=None)

        idx_cabecera = None
        # Buscamos la fila de cabecera de forma segura
        for i, row in df_raw.iterrows():
            # Convertimos a string y quitamos nulos (NaN) para evitar el error de float
            valores_fila = [str(val).upper() for val in row.values if pd.notna(val)]
            fila_completa = " ".join(valores_fila)
            
            if 'TECHNIQUE ID' in fila_completa:
                idx_cabecera = i
                break
        
        if idx_cabecera is None:
            print(f"[-] Error: No se encontró 'Technique ID' en {version_label}")
            return None

        # Construimos el DataFrame
        df = df_raw.iloc[idx_cabecera + 1:].copy()
        df.columns = [str(c).strip() for c in df_raw.iloc[idx_cabecera]]
        
        # Limpiar nombres de columnas de saltos de línea
        df.columns = [c.replace('\n', ' ').strip() for c in df.columns]

        # Identificar columnas necesarias
        col_id = next((c for c in df.columns if 'ID' in c.upper() and 'TECH' in c.upper()), None)
        col_nombre = next((c for c in df.columns if 'NAME' in c.upper() and 'TECH' in c.upper()), None)
        col_red = next((c for c in df.columns if 'NETWORK' in c.upper() and 'DETECTION' in c.upper()), None)

        if not col_red or not col_id:
            print(f"[-] Columnas no encontradas en {version_label}. Vistas: {list(df.columns)}")
            return None

        # Filtrado de técnicas de Red
        df_red = df[df[col_red].astype(str).str.contains('YES', case=False, na=False)].copy()
        df_red = df_red[[col_id, col_nombre]]
        df_red[version_label] = 'SI'
        
        return df_red.rename(columns={col_id: 'Technique ID', col_nombre: 'Technique Name'})

    except Exception as e:
        print(f"[!] Error inesperado en {version_label}: {e}")
        return None

def main():
    folder = 'TechniquesTacticsMitre'
    rutas = {
        'v15': os.path.join(folder, 'V15TechniquesTactics.ods'),
        'v16': os.path.join(folder, 'V16TechniquesTactics.ods'),
        'v17': os.path.join(folder, 'V17TechniquesTactics.ods')
    }

    results = {}
    for v, path in rutas.items():
        df = cargar_ods_robusto(path, v)
        if df is not None:
            results[v] = df
            print(f"[+] {v} OK ({len(df)} técnicas)")

    if 'v17' not in results:
        print("\n[!] Error: No se pudo cargar v17. Revisa los archivos.")
        return

    # Unir versiones
    final = results['v17']
    for v in ['v16', 'v15']:
        if v in results:
            final = pd.merge(final, results[v][['Technique ID', v]], on='Technique ID', how='outer')

    # Formateo
    final = final.fillna('-').sort_values('Technique ID')
    final.insert(0, 'Nº', range(1, len(final) + 1))
    final.columns = ['Nº', 'ID Técnica', 'Nombre de la Técnica', 'v17 (ICS)', 'v16 (ICS)', 'v15 (ICS)']

    out = 'Tabla_0_ICS_Final.xlsx'
    final.to_excel(out, index=False)
    print(f"\n✅ PROCESO COMPLETADO: {out}")

if __name__ == "__main__":
    main()
