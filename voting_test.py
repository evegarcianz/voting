import voting

import openpyxl
wb=openpyxl.load_workbook('C:/Users/EDGAR/OneDrive/Documentos/MSc Data Science and AI/COMP517/COMP517_Assignment3/voting.xlsx')
ws=wb.active
preferencia=voting.generatePreferences(ws)




def test_dictatorship_voting():
    """ This function runs dictatorship, from module voting,
    inside a loop and stores the results in a list. Then 
    compares the list of results to the list of known results 
    previously established.
    """
    res=[]
    for item in range(1,len(preferencia)+1):
        res.append(voting.dictatorship(preferencia,item))
    assert res==[4,4,4,1,2,1]

#lista para 
lista=[x for x in range(1,len(preferencia)+1)]
lista.append('max')
lista.append('min')

def test_plurality_voting():
    res=[]
    for item in lista :
        res.append(voting.plurality(preferencia,item))
    assert res==[4,4,4,4,4,4,4,4]


def test_veto_voting():
    res=[]
    for item in lista :
        res.append(voting.veto(preferencia,item))
    assert res==[4,4,4,1,3,1,4,1]

def test_borda_voting():
    res=[]
    for item in lista :
        res.append(voting.borda(preferencia,item))
    assert res==[4,4,4,4,4,4,4,4]

def test_harmonic_voting():
    res=[]
    for item in lista :
        res.append(voting.harmonic(preferencia,item))
    assert res==[4,4,4,4,4,4,4,4]


def test_scoringRule_voting():
    res=[]
    for item in lista :
        res.append(voting.scoringRule(preferencia,[30,90,80,100],item))
    assert res==[4,4,4,4,4,4,4,4]

def test_rangeVoting_voting():
    res=[]
    for item in lista :
        res.append(voting.rangeVoting(ws,item))
    assert res==[2,2,2,2,2,2,2,2]

def test_SVT_voting():
    res=[]
    for item in lista :
        res.append(voting.STV(preferencia,item))
    assert res==[4,4,4,4,4,4,4,4]
