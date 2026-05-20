import requests
from bs4 import BeautifulSoup
from utils_excel import Write_Dic_to_Excel, Write_List_to_Excel
import time
import openpyxl
import re
            
def get_mitre_new_version(tactics, techniques, subtechniques, tactic_ids, technique_ids, subtechnique_ids, version_pedida, fecha):
    
    # Inicialización de las tácticas
    for tactic_id in tactic_ids:
        tactics[tactic_id, "Network Detection"] = 'NO'
        tactics[tactic_id, "Only Network Detection"] = 'YES'
    # Inicialización de las técnicas
    for technique_id in technique_ids:
        techniques[technique_id, "Network Detection"] = 'NO'
        techniques[technique_id, "Only Network Detection"] = 'YES'

    # Se comprueba si cada subtécnica tiene como fuente el tráfico de red
    for subtechnique_id in subtechnique_ids:
        subtechnique_name = subtechniques[subtechnique_id, "Subtechnique Name"]
        technique_id = subtechniques[subtechnique_id, "Technique ID"]
        subtechnique_id_part = subtechnique_id.split('.')[1]
        # Incicialización de las subtécnicas
        subtechniques[subtechnique_id, "Network Detection"] = 'NO'
        subtechniques[subtechnique_id, "Only Network Detection"] = 'YES'
        # Se hace la petición a la URL de la subtécnica
        url = f"https://attack.mitre.org/versions/{version_pedida[1]}/techniques/{technique_id}/{subtechnique_id_part}/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            det_ids = set()
            for a in soup.select('a[href*="/detectionstrategies/DET"]'):
                href = a.get("href", "")
                m = re.search(r"/detectionstrategies/(DET\d+)(?:/|#|$)", href)
                if m:
                    det_ids.add(m.group(1))
    
            if not det_ids:
                subtechniques[subtechnique_id, "Only Network Detection"] = 'NO'
                techniques[technique_id, "Only Network Detection"] = 'NO'

            for det_id in det_ids:
                url_det = f"https://attack.mitre.org/versions/{version_pedida[1]}/detectionstrategies/{det_id}/"
                response_det = requests.get(url_det)
                if response_det.status_code == 200:
                    soup_det = BeautifulSoup(response_det.text, 'html.parser')
                    components = []
                    for a in soup_det.select('a[href*="/datacomponents/DC"]'):
                        href = a.get("href", "")
                        text = a.get_text(strip=True)
                        m = re.search(r"/datacomponents/(DC\d+)(?:/|#|$)", href)
                        if m:
                            components.append(m.group(1))
                    components = list(set(components))
                    
                    for component in components:
                        if component == 'DC0082' or component == 'DC0085' or component == 'DC0078':
                            techniques[technique_id, "Network Detection"] = 'YES'
                            subtechniques[subtechnique_id, "Network Detection"] = 'YES'
                        else:
                            subtechniques[subtechnique_id, "Only Network Detection"] = 'NO'
                            techniques[technique_id, "Only Network Detection"] = 'NO'
                else:
                    raise Exception("Error al realizar la solicitud:", response_det.status_code)

            print(f"Subtechnique ID: {subtechnique_id}, Subtechnique Name: {subtechnique_name}, Technique ID: {technique_id}")
            # Se espera 3 segundos antes de hacer la siguiente petición y evitar ser detectados como un ataque
            time.sleep(3)
        else:
            print(url)
            raise Exception("Error al realizar la solicitud:", response.status_code)

    # Se comprueba si cada técnica tiene como fuente el tráfico de red
    for technique_id in technique_ids:
        technique_name = techniques[technique_id, "Technique Name"]
        # Se hace la petición a la URL de la técnica
        url = f"https://attack.mitre.org/versions/{version_pedida[1]}/techniques/{technique_id}/"
        response = requests.get(url)
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            det_ids = set()
            for a in soup.select('a[href*="/detectionstrategies/DET"]'):
                href = a.get("href", "")
                m = re.search(r"/detectionstrategies/(DET\d+)(?:/|#|$)", href)
                if m:
                    det_ids.add(m.group(1))
            
            if not det_ids:
                techniques[technique_id, "Only Network Detection"] = 'NO'

            for det_id in det_ids:
                url_det = f"https://attack.mitre.org/versions/{version_pedida[1]}/detectionstrategies/{det_id}/"
                response_det = requests.get(url_det)
                if response_det.status_code == 200:
                    soup_det = BeautifulSoup(response_det.text, 'html.parser')
                    components = []
                    for a in soup_det.select('a[href*="/datacomponents/DC"]'):
                        href = a.get("href", "")
                        text = a.get_text(strip=True)
                        m = re.search(r"/datacomponents/(DC\d+)(?:/|#|$)", href)
                        if m:
                            components.append(m.group(1))
                    components = list(set(components))
                    
                    if not components:
                        techniques[technique_id, "Only Network Detection"] = 'NO'

                    for component in components:
                        if component == 'DC0082' or component == 'DC0085' or component == 'DC0078':
                            techniques[technique_id, "Network Detection"] = 'YES'
                        else:
                            techniques[technique_id, "Only Network Detection"] = 'NO'
                else:
                    raise Exception("Error al realizar la solicitud:", response_det.status_code)
            
            # Se extraen los enlaces de las tácticas asociadas a la técnica
            div_elements = soup.find_all('div', class_='col-md-11 pl-0')
            combined_div = BeautifulSoup("", 'html.parser')
            for div_element in div_elements:
                combined_div.append(div_element)
            tactic_links = combined_div.find_all('a', href=lambda href: href and '/tactics/' in href)

            # Se crea una lista con los IDs y los nombres de las tácticas
            tactics_list = []
            for link in tactic_links:
                tactic_id = link['href'].split('/')[-1]
                if techniques[technique_id, "Network Detection"] == 'YES':
                    tactics[tactic_id, "Network Detection"] = 'YES'
                if techniques[technique_id, "Only Network Detection"] == 'NO':
                    tactics[tactic_id, "Only Network Detection"] = 'NO'
                tactic_name = link.text.strip()
                tactics_list.append((tactic_id, tactic_name))

            # Se obtienen los nombres y los IDs de las técnicas, para concatenarlos en una sola cadena
            tactic_ids2 = [tactic[0] for tactic in tactics_list]
            tactic_names = [tactic[1] for tactic in tactics_list]
            tactic_ids2 = " - ".join(tactic_ids2)
            tactic_names = " - ".join(tactic_names)

            # Se agrega al diccionario de técnicas
            techniques[technique_id, "Tactic IDs"] = tactic_ids2
            techniques[technique_id, "Tactic Names"] = tactic_names
            print(f"Technique ID: {technique_id}, Technique Name: {technique_name}, Tactic IDs: {tactic_ids2}, Tactic Names: {tactic_names}")

            # Se espera 3 segundos antes de hacer la siguiente petición y evitar ser detectados como un ataque
            time.sleep(3)

        else:
            raise Exception("Error al realizar la solicitud:", response.status_code)

    # Se calcula el número de técnicas de cada táctica
    for tactic_id in tactic_ids:
        tactic_name = tactics[tactic_id, "Tactic Name"]
        num_techniques = 0
        for technique_id in technique_ids:
            tactic_ids3 = techniques[technique_id, "Tactic IDs"]
            if tactic_id in tactic_ids3:
                num_techniques += 1
        tactics[tactic_id, "Number of Techniques"] = num_techniques
        #print(f"Tactic ID: {tactic_id}, Tactic Name: {tactic_name}, Number of Techniques: {num_techniques}")

    # Se crea un diccionario resumen
    summary = {}
    summary["Tactics", "Number"] = len(tactic_ids)
    num_nd1 = 0
    num_ond1 = 0
    for i in tactic_ids:
        if tactics[i, "Network Detection"] == 'YES':
            num_nd1 += 1
        if tactics[i, "Only Network Detection"] == 'YES':
            num_ond1 += 1
    summary["Tactics", "Network Detectable Items"] = num_nd1
    summary["Tactics", "Network Only Detectable Items"] = num_ond1
    summary["Techniques", "Number"] = len(technique_ids)

    num_nd2 = 0
    num_ond2 = 0
    for i in technique_ids:
        if techniques[i, "Network Detection"] == 'YES':
            num_nd2 += 1
        if techniques[i, "Only Network Detection"] == 'YES':
            num_ond2 += 1
    summary["Techniques", "Network Detectable Items"] = num_nd2
    summary["Techniques", "Network Only Detectable Items"] = num_ond2
    summary["Subtechniques", "Number"] = len(subtechnique_ids)

    num_nd3 = 0
    num_ond3 = 0
    for i in subtechnique_ids:
        if subtechniques[i, "Network Detection"] == 'YES':
            num_nd3 += 1
        if subtechniques[i, "Only Network Detection"] == 'YES':
            num_ond3 += 1
    summary["Subtechniques", "Network Detectable Items"] = num_nd3
    summary["Subtechniques", "Network Only Detectable Items"] = num_ond3

    # Se almacenan los diccionarios en un archivo excel
    try:
        excel_name = 'TechniquesTacticsMitre/TechniquesTactics.xlsx'
        # Se abre el archivo excel
        libro_excel = openpyxl.load_workbook(excel_name)
        sheet1 = libro_excel['Summary']
        columnas1 = ['Number', 'Network Detectable Items', 'Network Only Detectable Items']
        sheet2 = libro_excel['Tactics']
        columnas2 = ['Tactic Name', 'Number of Techniques', 'Network Detection', 'Only Network Detection']
        sheet3 = libro_excel['Techniques']
        columnas3 = ['Technique Name', 'Tactic IDs', 'Tactic Names', 'Number of Subtechniques', 'Network Detection', 'Only Network Detection']
        sheet4 = libro_excel['Subtechniques']
        columnas4 = ['Subtechnique Name', 'Technique ID', 'Technique Name', 'Network Detection', 'Only Network Detection']
        # Se escriben los diccionarios en el archivo excel
        Write_Dic_to_Excel(libro_excel, excel_name, sheet1, summary, 'B2', 'E5', ['Tactics', 'Techniques', 'Subtechniques'], columnas1)
        Write_List_to_Excel(libro_excel, excel_name, sheet1, fecha, 'B8', 'C8')
        Write_List_to_Excel(libro_excel, excel_name, sheet1, version_pedida, 'B9', 'C9')
        Write_Dic_to_Excel(libro_excel, excel_name, sheet2, tactics, 'B2', f'F{len(tactic_ids)+2}', tactic_ids, columnas2)
        Write_Dic_to_Excel(libro_excel, excel_name, sheet3, techniques, 'B2', f'H{len(technique_ids)+2}', technique_ids, columnas3)
        Write_Dic_to_Excel(libro_excel, excel_name, sheet4, subtechniques, 'B2', f'G{len(subtechnique_ids)+2}', subtechnique_ids, columnas4)
        # Cierra el archivo
        libro_excel.close()
    except FileNotFoundError:
        print(f"El archivo '{excel_name}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al escribir en excel: {e}")