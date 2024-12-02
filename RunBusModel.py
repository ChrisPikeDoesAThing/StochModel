import pandas as pd
from BusModel import BusModel
def RunStoch():
    Q1dfcolumns = ["L","W","Wc1","Wc2","Wc3","pi0","pi1","pi2","pi3","pi4","pi5","pi6","pi7","pi8","pi9","pi10"]
    Q2dfcolumns = ["L","W","Wc1","Wc2","Wc3","pi0","pi1","pi2","pi3","pi4","pi5","pi6","pi7","pi8","pi9","pi10"]
    Q1 = pd.DataFrame(columns=Q1dfcolumns)
    Q2 = pd.DataFrame(columns=Q1dfcolumns)
    N = 300
    for n in range(N):
        lam = [.028*60,.113*60,.169*60]
        mu1 = [.341*60,.355*60,.449*60]
        mu2 = [.407*60,.372*60]
        Stats = BusModel(lam, mu1, mu2)
        
        Q1data=[Stats[0][0],Stats[0][1],Stats[0][2][0][0],Stats[0][2][1][0],Stats[0][2][2][0],Stats[0][3][0],Stats[0][3][1],Stats[0][3][2],Stats[0][3][3],Stats[0][3][4],Stats[0][3][5],Stats[0][3][6],Stats[0][3][7],Stats[0][3][8],Stats[0][3][9],Stats[0][3][10]]
        Q2data=[Stats[1][0],Stats[1][1],Stats[1][2][0][0],Stats[1][2][1][0],Stats[1][2][2][0],Stats[1][3][0],Stats[1][3][1],Stats[1][3][2],Stats[1][3][3],Stats[1][3][4],Stats[1][3][5],Stats[1][3][6],Stats[1][3][7],Stats[1][3][8],Stats[1][3][9],Stats[1][3][10]]
        Q1.loc[len(Q1)] = Q1data
        Q2.loc[len(Q2)] = Q2data
    Q1.to_csv('Q1-Real.csv', index=False)
    Q2.to_csv('Q2-Real.csv', index=False)
    return()

RunStoch()