from utils_excel import Write_Dic_to_Excel, Read_Excel_to_Dic, Read_Excel_to_List
import openpyxl

'''
Genera las tablas de asociación entre técnicas y tácticas, y entre subtécnicas y tácticas.
Se generan dos tablas en el archivo Excel "TechniquesTactics.xlsx" en las hojas "Tech_Tact" y "Subtech_Tact".
'''
def generarTablasAsociacion():
    # Se leen los datos del excel
    excel_name= "TechniquesTacticsMitre/TechniquesTactics.xlsx"
    sheets = ["Summary", "Tactics", "Techniques", "Subtechniques"]

    try:
        summary = Read_Excel_to_Dic(excel_name, sheets[0], "B2", "D5")

        tactics = Read_Excel_to_Dic(excel_name, sheets[1], "B2", f"E{summary['Tactics', 'Number']+2}")
        tactics_ids = Read_Excel_to_List(excel_name, sheets[1], "B3", f"B{summary['Tactics', 'Number']+2}")

        techniques = Read_Excel_to_Dic(excel_name, sheets[2], "B2", f"G{summary['Techniques', 'Number']+2}")
        techniques_ids = Read_Excel_to_List(excel_name, sheets[2], "B3", f"B{summary['Techniques', 'Number']+2}")

        subtechniques = Read_Excel_to_Dic(excel_name, sheets[3], "B2", f"F{summary['Subtechniques', 'Number']+2}")
        subtechniques_ids = Read_Excel_to_List(excel_name, sheets[3], "B3", f"B{summary['Subtechniques', 'Number']+2}")

    except FileNotFoundError:
        print(f"El archivo '{excel_name}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el excel: {e}")

    # Se crea un diccionario que marca con una X si la técnica está asociada a la táctica y con "" si no lo está
    tabla_techniques = {}
    for tech in techniques_ids:
        for tact in tactics_ids:
            if tact in techniques[tech, "Tactic IDs"]:
                tabla_techniques[tech, tact] = "X"
            else:
                tabla_techniques[tech, tact] = ""

    # Se crea un diccionario que marca con una X si la subtécnica está asociada a la táctica y con "" si no lo está
    tabla_subtechniques = {}
    for subtech in subtechniques_ids:
        for tact in tactics_ids:
            tech_of_subtech = subtechniques[subtech, "Technique ID"]
            if tact in techniques[tech_of_subtech, "Tactic IDs"]:
                tabla_subtechniques[subtech, tact] = "X"
            else:
                tabla_subtechniques[subtech, tact] = ""

    # Se escriben ambos diccionarios en el excel
    try:
            # Se abre el archivo excel
            libro_excel = openpyxl.load_workbook(excel_name)
            sheet1 = libro_excel['Tech_Tact']
            sheet2 = libro_excel['Subtech_Tact']
            # Se escriben los diccionarios en el archivo excel
            letra = chr(summary['Tactics', 'Number']+66)
            Write_Dic_to_Excel(libro_excel, excel_name, sheet1, tabla_techniques, 'B2', f'{letra}{summary["Techniques", "Number"]+2}', techniques_ids, tactics_ids)
            Write_Dic_to_Excel(libro_excel, excel_name, sheet2, tabla_subtechniques, 'B2', f'{letra}{summary["Subtechniques", "Number"]+2}', subtechniques_ids, tactics_ids)
            # Se cierra el archivo
            libro_excel.close()
    except FileNotFoundError:
        print(f"El archivo '{excel_name}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al escribir en excel: {e}")