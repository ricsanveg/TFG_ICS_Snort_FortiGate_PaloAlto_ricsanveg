from utils_excel import Read_Excel_to_Dic, Read_Excel_to_List
from datetime import date

'''
Función que compara dos excels y muestra las diferencias entre ellos.
Se comparan los siguientes aspectos:
- Tácticas: nombre, número de técnicas asociadas, detección en red y detección solo en red.
- Técnicas: nombre, tácticas asociadas, número de subtécnicas asociadas, detección en red y detección solo en red.
- Subtécnicas: nombre, detección en red y detección solo en red.
'''
def cambiosTecnicasTacticas(excel_n1, excel_n2):
    # Se almacenan las diferencias entre los dos excels
    diferencias = []
    today = date.today()
    diferencias.append(f"Fecha de la comparación: {today.strftime('%d/%m/%Y')}\n\n")
    #print("CAMBIOS RESPECTO A LA ÚLTIMA VERSIÓN:\n")
    diferencias.append("CAMBIOS ENTRE VERSIONES:\n")
    # Se leen los datos de los dos excels
    sheets = ["Summary", "Tactics", "Techniques", "Subtechniques"]
    Range1 = "B2"
    Range2 = "H5" 

    try:
        version_n1 = Read_Excel_to_List(excel_n1, sheets[0], "C9", "C9")[0]
        version_n2 = Read_Excel_to_List(excel_n2, sheets[0], "C9", "C9")[0]
        summary_n1   = Read_Excel_to_Dic(excel_n1, sheets[0], Range1, Range2)
        summary_n2   = Read_Excel_to_Dic(excel_n2, sheets[0], Range1, Range2)
        
    except FileNotFoundError:
        print(f"El archivo '{excel_n1}' o '{excel_n2}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el excel: {e}")

    # Se comprueban las diferencias entre los dos resúmenes
    for i in ["Tactics", "Techniques", "Subtechniques"]:
        for j in ["Number", 'Internet Scan Detectable Items', 'Network Share Detectable Items', 'Network Traffic Detectable Items', "Network Detectable Items", "Network Only Detectable Items"]:
            if summary_n1[i, j] != summary_n2[i, j]:
                diff = f"{j} of {i} in {version_n2}: {summary_n2[i,j]} ----- {j} of {i} in {version_n1}: {summary_n1[i,j]}"
                diferencias.append(diff + "\n")

    # Se leen los datos de las tácticas, técnicas y subtécnicas
    Range3_n1 = f"I{summary_n1['Tactics', 'Number']+2}"
    Range3_n2 = f"I{summary_n2['Tactics', 'Number']+2}"
    Range4_n1 = f"B{summary_n1['Tactics', 'Number']+2}"
    Range4_n2 = f"B{summary_n2['Tactics', 'Number']+2}"
    Range5_n1 = f"K{summary_n1['Techniques', 'Number']+2}" 
    Range5_n2 = f"K{summary_n2['Techniques', 'Number']+2}"    
    Range6_n1 = f"B{summary_n1['Techniques', 'Number']+2}"
    Range6_n2 = f"B{summary_n2['Techniques', 'Number']+2}"
    Range7_n1 = f"J{summary_n1['Subtechniques', 'Number']+2}"
    Range7_n2 = f"J{summary_n2['Subtechniques', 'Number']+2}"
    Range8_n1 = f"B{summary_n1['Subtechniques', 'Number']+2}"
    Range8_n2 = f"B{summary_n2['Subtechniques', 'Number']+2}"

    try:
        tactics_n1   = Read_Excel_to_Dic(excel_n1, sheets[1], Range1, Range3_n1)
        tactics_n2   = Read_Excel_to_Dic(excel_n2, sheets[1], Range1, Range3_n2)
        tactics_ids_n1 = Read_Excel_to_List(excel_n1, sheets[1], "B3", Range4_n1)
        tactics_ids_n2 = Read_Excel_to_List(excel_n2, sheets[1], "B3", Range4_n2)

        techniques_n1 = Read_Excel_to_Dic(excel_n1, sheets[2], Range1, Range5_n1)
        techniques_n2 = Read_Excel_to_Dic(excel_n2, sheets[2], Range1, Range5_n2)
        techniques_ids_n1 = Read_Excel_to_List(excel_n1, sheets[2], "B3", Range6_n1)
        techniques_ids_n2 = Read_Excel_to_List(excel_n2, sheets[2], "B3", Range6_n2)

        subtechniques_n1 = Read_Excel_to_Dic(excel_n1, sheets[3], Range1, Range7_n1)
        subtechniques_n2 = Read_Excel_to_Dic(excel_n2, sheets[3], Range1, Range7_n2)
        subtechniques_ids_n1 = Read_Excel_to_List(excel_n1, sheets[3], "B3", Range8_n1)
        subtechniques_ids_n2 = Read_Excel_to_List(excel_n2, sheets[3], "B3", Range8_n2)

    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el excel: {e}")

    #############################################################################################
    ######################################### TÁCTICAS ##########################################
    #############################################################################################
    diferencias.append("\n")
    # Se comprueba si hay alguna táctica en el excel 1 y no en el excel 2
    for i in tactics_ids_n1:
        if i not in tactics_ids_n2:
            diff = f"Tactic {i} - {tactics_n1[i, 'Tactic Name']} IN {version_n1} and NOT IN {version_n2}."
            diferencias.append(diff + "\n")
    # Se comprueba si hay alguna táctica en el excel 2 y no en el excel 1
    for i in tactics_ids_n2:
        if i not in tactics_ids_n1:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} IN {version_n2} and NOT IN {version_n1}."
            diferencias.append(diff + "\n")
    
    # Obtenemos los ids iguales para comprobar sus diferencias
    tactics_ids = list(set(tactics_ids_n1) & set(tactics_ids_n2))

    # Se comprueban las diferencias entre las tácticas
    for i in tactics_ids:
        # Se comprueba si ha cambiado el nombre de la táctica
        if tactics_n1[i, "Tactic Name"] != tactics_n2[i, "Tactic Name"]:
            diff = f"Tactic {i} has changed its name -> In {version_n2}: {tactics_n2[i, 'Tactic Name']} --- In {version_n1}: {tactics_n1[i, 'Tactic Name']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado el número de técnicas asociadas
        if tactics_n1[i, "Number of Techniques"] != tactics_n2[i, "Number of Techniques"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed the number of techniques -> In {version_n2}: {tactics_n2[i, 'Number of Techniques']} --- In {version_n1}: {tactics_n1[i, 'Number of Techniques']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Internet Scan'
        if tactics_n1[i, "Internet Scan"] != tactics_n2[i, "Internet Scan"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed its Internet Scan -> In {version_n2}: {tactics_n2[i, 'Internet Scan']} --- In {version_n1}: {tactics_n1[i, 'Internet Scan']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Share'
        if tactics_n1[i, "Network Share"] != tactics_n2[i, "Network Share"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed its Network Share -> In {version_n2}: {tactics_n2[i, 'Network Share']} --- In {version_n1}: {tactics_n1[i, 'Network Share']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Traffic'
        if tactics_n1[i, "Network Traffic"] != tactics_n2[i, "Network Traffic"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed its Network Traffic -> In {version_n2}: {tactics_n2[i, 'Network Traffic']} --- In {version_n1}: {tactics_n1[i, 'Network Traffic']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado la detección en red de la táctica
        if tactics_n1[i, "Network Detection"] != tactics_n2[i, "Network Detection"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed its network detection -> In {version_n2}: {tactics_n2[i, 'Network Detection']} --- In {version_n1}: {tactics_n1[i, 'Network Detection']}"
            diferencias.append(diff + "\n")
        if tactics_n1[i, "Only Network Detection"] != tactics_n2[i, "Only Network Detection"]:
            diff = f"Tactic {i} - {tactics_n2[i, 'Tactic Name']} has changed its only network detection -> In {version_n2}: {tactics_n2[i, 'Only Network Detection']} --- In {version_n1}: {tactics_n1[i, 'Only Network Detection']}"
            diferencias.append(diff + "\n")

    #############################################################################################
    ######################################### TÉCNICAS ##########################################
    #############################################################################################
    diferencias.append("\n")
    # Se comprueba si hay alguna técnica en el excel 1 y no en el excel 2
    for i in techniques_ids_n1:
        if i not in techniques_ids_n2:
            diff = f"Technique {i} - {techniques_n1[i, 'Technique Name']} IN {version_n1} and NOT IN {version_n2}."
            diferencias.append(diff + "\n")
    # Se comprueba si hay alguna técnica en el excel 2 y no en el excel 1
    for i in techniques_ids_n2:
        if i not in techniques_ids_n1:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} IN {version_n2} and NOT IN {version_n1}."
            diferencias.append(diff + "\n")

    # Obtenemos los ids iguales para comprobar sus diferencias
    techniques_ids = list(set(techniques_ids_n1) & set(techniques_ids_n2))
    
    # Se comprueban las diferencias entre las técnicas
    for i in techniques_ids:
        # Se comprueba si ha cambiado el nombre de la técnica
        if techniques_n1[i, "Technique Name"] != techniques_n2[i, "Technique Name"]:
            diff = f"Technique {i} has changed its name -> In {version_n2}: {techniques_n2[i, 'Technique Name']} --- In {version_n1}: {techniques_n1[i, 'Technique Name']}"
            diferencias.append(diff + "\n")
        # Se comprueba si han cambiado las tácticas asociadas
        if techniques_n1[i, "Tactic IDs"] != techniques_n2[i, "Tactic IDs"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its associated tactics -> In {version_n2}: {techniques_n2[i, 'Tactic IDs']} --- In {version_n1}: {techniques_n1[i, 'Tactic IDs']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado el número de subtécnicas asociadas
        if techniques_n1[i, "Number of Subtechniques"] != techniques_n2[i, "Number of Subtechniques"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed the number of subtechniques -> In {version_n2}: {techniques_n2[i, 'Number of Subtechniques']} --- In {version_n1}: {techniques_n1[i, 'Number of Subtechniques']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Internet Scan'
        if techniques_n1[i, "Internet Scan"] != techniques_n2[i, "Internet Scan"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its Internet Scan -> In {version_n2}: {techniques_n2[i, 'Internet Scan']} --- In {version_n1}: {techniques_n1[i, 'Internet Scan']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Share'
        if techniques_n1[i, "Network Share"] != techniques_n2[i, "Network Share"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its Network Share -> In {version_n2}: {techniques_n2[i, 'Network Share']} --- In {version_n1}: {techniques_n1[i, 'Network Share']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Traffic'
        if techniques_n1[i, "Network Traffic"] != techniques_n2[i, "Network Traffic"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its Network Traffic -> In {version_n2}: {techniques_n2[i, 'Network Traffic']} --- In {version_n1}: {techniques_n1[i, 'Network Traffic']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado la detección en red de la técnica
        if techniques_n1[i, "Network Detection"] != techniques_n2[i, "Network Detection"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its network detection -> In {version_n2}: {techniques_n2[i, 'Network Detection']} --- In {version_n1}: {techniques_n1[i, 'Network Detection']}"
            diferencias.append(diff + "\n")
        if techniques_n1[i, "Only Network Detection"] != techniques_n2[i, "Only Network Detection"]:
            diff = f"Technique {i} - {techniques_n2[i, 'Technique Name']} has changed its only network detection -> In {version_n2}: {techniques_n2[i, 'Only Network Detection']} --- In {version_n1}: {techniques_n1[i, 'Only Network Detection']}"
            diferencias.append(diff + "\n")

    #############################################################################################
    ####################################### SUBTÉCNICAS #########################################
    #############################################################################################
    diferencias.append("\n")
    # Se comprueba si hay alguna subtécnica en el excel 1 y no en el excel 2
    for i in subtechniques_ids_n1:
        if i not in subtechniques_ids_n2:
            diff = f"Subtechnique {i} - {subtechniques_n1[i, 'Subtechnique Name']} IN {version_n1} and NOT IN {version_n2}."
            diferencias.append(diff + "\n")
    # Se comprueba si hay alguna subtécnica en el excel 2 y no en el excel 1
    for i in subtechniques_ids_n2:
        if i not in subtechniques_ids_n1:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} IN {version_n2} and NOT IN {version_n1}."
            diferencias.append(diff + "\n")
    
    # Obtenemos los ids iguales para comprobar sus diferencias
    subtechniques_ids = list(set(subtechniques_ids_n1) & set(subtechniques_ids_n2))
    # Se comprueban las diferencias entre las subtécnicas
    
    for i in subtechniques_ids:
        # Se comprueba si ha cambiado el nombre de la subtécnica
        if subtechniques_n1[i, "Subtechnique Name"] != subtechniques_n2[i, "Subtechnique Name"]:
            diff = f"Subtechnique {i} has changed its name -> In {version_n2}: {subtechniques_n2[i, 'Subtechnique Name']} --- In {version_n1}: {subtechniques_n1[i, 'Subtechnique Name']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Internet Scan'
        if subtechniques_n1[i, "Internet Scan"] != subtechniques_n2[i, "Internet Scan"]:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} has changed its Internet Scan -> In {version_n2}: {subtechniques_n2[i, 'Internet Scan']} --- In {version_n1}: {subtechniques_n1[i, 'Internet Scan']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Share'
        if subtechniques_n1[i, "Network Share"] != subtechniques_n2[i, "Network Share"]:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} has changed its Network Share -> In {version_n2}: {subtechniques_n2[i, 'Network Share']} --- In {version_n1}: {subtechniques_n1[i, 'Network Share']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado 'Network Traffic'
        if subtechniques_n1[i, "Network Traffic"] != subtechniques_n2[i, "Network Traffic"]:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} has changed its Network Traffic -> In {version_n2}: {subtechniques_n2[i, 'Network Traffic']} --- In {version_n1}: {subtechniques_n1[i, 'Network Traffic']}"
            diferencias.append(diff + "\n")
        # Se comprueba si ha cambiado la detección en red de la subtécnica
        if subtechniques_n1[i, "Network Detection"] != subtechniques_n2[i, "Network Detection"]:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} has changed its network detection -> In {version_n2}: {subtechniques_n2[i, 'Network Detection']} --- In {version_n1}: {subtechniques_n1[i, 'Network Detection']}"
            diferencias.append(diff + "\n")
        if subtechniques_n1[i, "Only Network Detection"] != subtechniques_n2[i, "Only Network Detection"]:
            diff = f"Subtechnique {i} - {subtechniques_n2[i, 'Subtechnique Name']} has changed its only network detection -> In {version_n2}: {subtechniques_n2[i, 'Only Network Detection']} --- In {version_n1}: {subtechniques_n1[i, 'Only Network Detection']}"
            diferencias.append(diff + "\n")

    # Se escriben las diferencias en un archivo
    with open("TechniquesTacticsMitre/changes.txt", "w") as file:
        for diff in diferencias:
            file.write(diff)