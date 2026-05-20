import openpyxl

# Se lee una tabla de Excel y se guarda en un diccionario
def Read_Excel_to_Dic(name, sheet, Range1, Range2):
    
    excel_doc=openpyxl.load_workbook(name,data_only=True)
    sheet=excel_doc[sheet]
    
    dict1={}
    multiple_cells = sheet[Range1:Range2]
    Aux={}
    Aux.update({0:'Empty'})

    Column=0
    for cell in multiple_cells[0]:
        if Column >=1:
            Aux.update({Column:cell.value})
        Column=Column+1
  
    RowNumber=len(multiple_cells)
    for Row in range(1,RowNumber):
        dict2 = {}
        Column=0
        key = multiple_cells[Row][Column].value
        for cell in multiple_cells[Row]:
            if Column>=1:
                dict2.update({Aux[Column]:cell.value})
            Column=Column+1
        dict1.update({key:dict2})

    Data={}
    for i in dict1:
        for j in dict1[i]:
            Data[i,j]=dict1[i][j]
            
    return Data

# Se guarda un diccionario en una tabla de Excel
def Write_Dic_to_Excel(WB, name, sheet, auxdic, Range1, Range2, filas, columnas):

    multiple_cells = sheet[Range1:Range2]
    aux1=filas
    aux2=columnas

    Column=0
    for cell in multiple_cells[0]:
        if Column==0:
            cell.value=' '
        if Column >=1:
            cell.value=aux2[Column-1]
        Column=Column+1

    RowNumber=len(multiple_cells)
    ColNumber=len(multiple_cells[0])
    for Row in range(1,RowNumber):
        multiple_cells[Row][0].value=aux1[Row-1]
        for j in range(1,ColNumber):
            a1=aux1[Row-1]
            a2=aux2[j-1]
            #print(auxdic[a1,a2])
            multiple_cells[Row][j].value=auxdic[a1,a2]
    WB.save(name)

def getList(dictt):
    lista = []
    for key in dictt.keys():
        lista.append(key)
    return lista

# Se lee una tabla de Excel y se guarda en una lista
def Read_Excel_to_List(name, sheet, Range1, Range2):
    excel_doc=openpyxl.load_workbook(name,data_only=True)
    sheet=excel_doc[sheet]
    listaAux = []
    multiple_cells = sheet[Range1:Range2]
    for row in multiple_cells:
        for cell in row:
            listaAux.append(cell.value)
    return listaAux

# Se guarda una lista en una tabla de Excel
def Write_List_to_Excel(wb, name, sheet, List1, Range1, Range2):
    multiple_cells = sheet[Range1:Range2]
    k=0
    for row in multiple_cells:
        for cell in row:
            cell.value=List1[k]
            k=k+1
    wb.save(name)