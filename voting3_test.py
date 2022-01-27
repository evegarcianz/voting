import voting
import openpyxl
wb=openpyxl.load_workbook('C:/Users/EDGAR/OneDrive/Documentos/MSc Data Science and AI/COMP517/COMP517_Assignment3/voting3.xlsx')
ws=wb.active

preferencia=voting.generatePreferences(ws)


## funciones para voting
def test_dictatorship_voting():
    res=[]
    for item in range(1,len(preferencia)+1):
        res.append(voting.dictatorship(preferencia,item))
    assert res==[4,4,1,2,3,1,1,2,2,1,1,5,2,5,5,1,1]

#lista para 
lista=[x for x in range(1,len(preferencia)+1)]
lista.append('max')
lista.append('min')

def test_plurality_voting():
    res=[]
    for item in lista :
        res.append(voting.plurality(preferencia,item))

    assert res==[1 for _ in range(0,19)]


def test_veto_voting():
    res=[]
    for item in lista :
        res.append(voting.veto(preferencia,item))
    assert res==[1 for _ in range(0,19)]

def test_borda_voting():
    res=[]
    for item in lista :
        res.append(voting.borda(preferencia,item))
    assert res==[1 for _ in range(0,19)]

def test_harmonic_voting():
    res=[]
    for item in lista :
        res.append(voting.harmonic(preferencia,item))
    assert res==[1 for _ in range(0,19)]