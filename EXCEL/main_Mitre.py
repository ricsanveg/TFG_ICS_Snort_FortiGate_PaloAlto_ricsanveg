import requests
from bs4 import BeautifulSoup
from datetime import date
import re
from pathlib import Path
import sys
from getMitre_old_versions import get_mitre_old_version
from getMitre_new_versions import get_mitre_new_version
from changes_TacTech import cambiosTecnicasTacticas
from table_TacTech import generarTablasAsociacion


# Se solicita al usuario si quiere comprobar las diferencias entre dos versiones o si quiere obtener la última versión
opcion = input('''\nIntroduce el número correspondiente a la opción deseada:
    0 - OBTENER una versión y comprobar diferencias con otra versión
    1 - OBTENER una versión y NO comprobar diferencias con otra versión
    2 - SOLO comprobar diferencias entre versiones

    Opción: ''')

if opcion not in ['0', '1', '2']:
    print("Opción no válida. Por favor, vuelve a ejecutar el script e introduce 0, 1 o 2.")
    sys.exit(1)

if opcion == '0':
    excel_old = input("\nIntroduce el nombre del fichero Excel con la versión a comparar: ")
    excel_old = f'TechniquesTacticsMitre/{excel_old}'
    if not Path(excel_old).exists():
        print(f"No se encontró el fichero {excel_old} para comparar las diferencias.\nPor favor, vuelve a ejecutar el script e introduce un nombre válido.")
        sys.exit(1)

if opcion in ['0', '1']:
    # Se comprueba que existe el directorio TechniquesTactics.xlsx
    excel_name = 'TechniquesTacticsMitre/TechniquesTactics.xlsx'
    excel_path = Path(excel_name)
    if not excel_path.exists():
        print(
            f"No se encontró el fichero de salida '{excel_name}'. "
            "Asegúrate de haber creado la plantilla correctamente en esa ruta."
        )
        sys.exit(1)

    # --- CAMBIO A MATRIZ ICS ---
    url = "https://attack.mitre.org/matrices/ics/"
    response = requests.get(url)
    
    # Se extrae la versión actual de la matriz de técnicas de MITRE
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscamos la versión específicamente en la ruta de ICS
        tag_version = soup.find("a", href=re.compile(r"^/versions/v\d+/matrices/ics/?$"))
        if tag_version:
            href = tag_version["href"]
            numero_version = re.search(r"/versions/(v\d+)/", href).group(1)
            version_actual = ["Versión MITRE ATT&CK:", numero_version]
    else:
        print("Error al realizar la solicitud:", response.status_code)
        sys.exit(1)    

    version_pedida = input('''\nIntroduce la versión de la matriz de técnicas de MITRE que deseas obtener (por ejemplo, v17):
Si quieres obtener la última versión, introduce 'latest': ''')

    # Se valida el formato de la versión pedida
    if version_pedida != 'latest' and not re.match(r"^v\d+$", version_pedida):
        print("Formato de versión no válido.")
        sys.exit(1)

    # Gestión de versiones
    numero_version_actual = int(re.search(r"v(\d+)", numero_version).group(1))
    if version_pedida == 'latest':
        version_pedida = numero_version
        numero_version_pedida = numero_version_actual
    else:
        numero_version_pedida = int(re.search(r"v(\d+)", version_pedida).group(1))

    if version_pedida != 'latest' and (numero_version_pedida < 10 or numero_version_pedida > numero_version_actual):
        print(f"La versión {version_pedida} no está disponible.")
        sys.exit(1)

    if version_pedida != 'latest' and version_pedida != numero_version:
        # --- CAMBIO A URL DE VERSIÓN ICS ---
        url_version = f"https://attack.mitre.org/versions/{version_pedida}/matrices/ics/"
        response = requests.get(url_version)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tag_version = soup.find("a", href=re.compile(r"^/versions/v\d+/matrices/ics/?$"))
            if tag_version:
                href = tag_version["href"]
                version = ["Versión MITRE ATT&CK:", re.search(r"/versions/(v\d+)/", href).group(1)]
        else:
            print(f"No se pudo obtener la versión {version_pedida} de ICS.")
            sys.exit(1)
    else:
        version = ["Versión MITRE ATT&CK:", version_pedida]

    # Extracción de enlaces (ICS usa la misma estructura de rutas /tactics/ y /techniques/)
    tactic_links = soup.find_all('a', href=lambda href: href and '/tactics/T' in href)
    technique_links = soup.find_all('a', href=lambda href: href and '/techniques/T' in href)

    # Diccionarios para Tácticas
    tactic_ids = []
    tactics = {}
    for link in tactic_links:
        tactic_id = link['href'].split('/')[-1]
        tactic_name = link.text.strip()
        if tactic_id != '':
            tactics[tactic_id, "Tactic Name"] = tactic_name
            tactic_ids.append(tactic_id)

    # Diccionarios para Técnicas y Subtécnicas
    technique_ids = []
    subtechnique_ids = []
    techniques = {}
    subtechniques = {}
    for link in technique_links:
        technique_id = link['href'].split('/')[-1]
        technique_name = link.text.strip()
        
        if technique_id.startswith('T'):
            techniques[technique_id, "Technique Name"] = technique_name
            technique_ids.append(technique_id)
        else:
            esp_subtechnique_id = link['href'].split('/')[-1]
            if esp_subtechnique_id.isnumeric():
                technique_id = link['href'].split('/')[-2]
                subtechnique_id = f"{technique_id}.{esp_subtechnique_id}"
                subtechnique_name = link.text.strip()
                subtechniques[subtechnique_id, "Subtechnique Name"] = subtechnique_name
                subtechniques[subtechnique_id, "Technique ID"] = technique_id
                subtechnique_ids.append(subtechnique_id)
                
                # Asociar nombre de técnica a subtécnica
                for techniqueID in technique_ids:
                    if techniqueID == technique_id:
                        t_name = techniques[techniqueID, "Technique Name"]
                        if t_name.endswith(')'):
                            t_name = t_name[:t_name.rfind('(')].strip()
                        subtechniques[subtechnique_id, "Technique Name"] = t_name

    # Limpieza y ordenación
    tactic_ids = sorted(list(set(tactic_ids)))
    technique_ids = sorted(list(set(technique_ids)))
    subtechnique_ids = sorted(list(set(subtechnique_ids)))

    for t_id in technique_ids:
        t_name = techniques[t_id, "Technique Name"]
        if t_name.endswith(')'):
            techniques[t_id, "Number of Subtechniques"] = t_name[t_name.rfind('(')+1:t_name.rfind(')')].strip()
            techniques[t_id, "Technique Name"] = t_name[:t_name.rfind('(')].strip()
        else:
            techniques[t_id, "Number of Subtechniques"] = 0

    # Fecha de actualización
    if version_pedida == 'latest' or version_pedida == numero_version:
        today = date.today()
        fecha = ["Fecha de la última actualización:", today.strftime("%d/%m/%Y")]
    else:
        banner = soup.select_one("div.version-banner")
        if banner:
            texto_fecha = banner.get_text(" ", strip=True)
            m = re.search(r'between\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\s+and\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', texto_fecha)
            if m:
                inicio, fin = m.groups()
                fecha = ["Fechas de vigencia de la versión:", f"{inicio} - {fin}"]
            else:
                fecha = ["Fechas:", "No extraídas"]
        else:
            fecha = ["Fecha de la versión:", version_pedida]

    # Guardado de datos
    if version_pedida in ['v10', 'v11', 'v12', 'v13', 'v14', 'v15', 'v16', 'v17']:
        get_mitre_old_version(tactics, techniques, subtechniques, tactic_ids, technique_ids, subtechnique_ids, version, fecha)
    else:
        get_mitre_new_version(tactics, techniques, subtechniques, tactic_ids, technique_ids, subtechnique_ids, version, fecha)
        
    generarTablasAsociacion()

    if opcion == '0':
        cambiosTecnicasTacticas(excel_name, excel_old)

if opcion == '2':
    excel_n1 = input("\nIntroduce el nombre del primer fichero Excel: ")
    excel_n1 = f'TechniquesTacticsMitre/{excel_n1}'
    excel_n2 = input("Introduce el nombre del segundo fichero Excel: ")
    excel_n2 = f'TechniquesTacticsMitre/{excel_n2}'
    cambiosTecnicasTacticas(excel_n1, excel_n2)
