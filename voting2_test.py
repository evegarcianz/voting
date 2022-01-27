import voting
import openpyxl
wb=openpyxl.load_workbook('C:/Users/EDGAR/OneDrive/Documentos/MSc Data Science and AI/COMP517/COMP517_Assignment3/voting2.xlsx')
ws=wb.active

preferencia=voting.generatePreferences(ws)


## funciones para voting
def test_dictatorship_voting():
    res=[]
    for item in range(1,len(preferencia)+1):
        res.append(voting.dictatorship(preferencia,item))
    assert res==[2,1,4,3,4,1,5,1,5,5,1,1,4,1,3,4,1,2,2,3,1,2,3,2]

#lista para 
lista=[x for x in range(1,len(preferencia)+1)]
lista.append('max')
lista.append('min')

def test_plurality_voting():
    res=[]
    for item in lista :
        res.append(voting.plurality(preferencia,item))

    assert res==[1 for _ in range(0,26)]


def test_veto_voting():
    res=[]
    for item in lista :
        res.append(voting.veto(preferencia,item))
    assert res==[1 for _ in range(0,26)]

def test_borda_voting():
    res=[]
    for item in lista :
        res.append(voting.borda(preferencia,item))
    assert res==[1 for _ in range(0,26)]

def test_harmonic_voting():
    res=[]
    for item in lista :
        res.append(voting.harmonic(preferencia,item))
    assert res==[1 for _ in range(0,26)]



def test_scoringRule_voting():
    res=[]
    for item in lista :
        res.append(voting.scoringRule(preferencia,[.2,.25,.333,.5,1],item))
    assert res==[1 for _ in range(0,26)]

def test_rangeVoting_voting():
    res=[]
    for item in lista :
        res.append(voting.rangeVoting(ws,item))
    assert res==[1 for _ in range(0,26)]

def test_SVT_voting():
    res=[]
    for item in lista :
        res.append(voting.STV(preferencia,item))
    assert res==[1 for _ in range(0,26)]
