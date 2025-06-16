import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv('mon_fichier.csv')
data2=data[['ID_INDIVIDU']]
data2=pd.concat([data2,pd.qcut(data['MONTANT_CUMULE'],q=[0, .33, .66, 1.],labels=['Pas Depensier','Moyennement Depensier','Depensier'])],axis=1).rename(columns={'MONTANT_CUMULE':'MONTANT'})
data2=pd.concat([data2,pd.qcut(data['RECENCE'],q=[0, .33, .66, 1.],labels=['Recent','Moyennement Recent','Ancien'])],axis=1).rename(columns={'RECENCE':'RECENCE'})
data2=pd.concat([data2,pd.qcut(data['NB_VISITES'],q=[0, .38, .66, 1.],labels=['Peu Frequent','Moyennement Frequent','Tres Frequent'])],axis=1).rename(columns={'NB_VISITES':'FREQUENCE'})
print(data2)
data3=data.merge(data2,on='ID_INDIVIDU',how='left')
data3.to_csv('rfm.csv', index=False)