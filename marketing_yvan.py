import datetime
import numpy as np
import pandas as pd
R_complement_individu_2016=pd.read_csv("donnee/R_COMPLEMENT_INDIVIDU_2016.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'DATE_NAISS_A':'str','DATE_NAISS_M':'str','DATE_NAISS_J':'str','EAN':'str'})
R_individu_2016=pd.read_csv("donnee/R_INDIVIDU_2016.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'DATE_NAISS_A':'str','DATE_NAISS_M':'str','DATE_NAISS_J':'str','EAN':'str'})
R_magasin=pd.read_csv("donnee/R_MAGASIN.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'EAN':'str'})
R_referentiel=pd.read_csv("donnee/R_REFERENTIEL.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'EAN':'str'})
R_tickets_2016=pd.read_csv("donnee/R_TICKETS_2016.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'EAN':'str'})
R_typo_produit=pd.read_csv("donnee/R_TYPO_PRODUIT.csv",delimiter=";",encoding= 'iso-8859-1',dtype={'EAN':'str'})

'''print(R_complement_individu_2016)'''
'''print(R_individu_2016)'''
'''print(R_magasin)'''
'''print(R_referentiel)'''
'''print(R_tickets_2016)'''
'''print(R_typo_produit)'''



DF_INDIVIDU = pd.merge(R_individu_2016,R_complement_individu_2016,on='ID_INDIVIDU',how='left')
'''print(type(DF_INDIVIDU.iloc[1]['DATE_CREATION_CARTE']))'''
DF_INDIVIDU['date_naissance']=pd.to_datetime(DF_INDIVIDU[['DATE_NAISS_A','DATE_NAISS_M','DATE_NAISS_J']].astype(str).apply(lambda x: '-'.join(x),axis=1),format='%Y-%m-%d',errors='coerce')
DF_INDIVIDU['AGE']=(datetime.datetime.strptime('2016-08-31','%Y-%m-%d')-DF_INDIVIDU['date_naissance'])//datetime.timedelta(days=365.2425)
DF_INDIVIDU['Anciennete']=[(datetime.datetime.strptime('2016-08-31','%Y-%m-%d'))-datetime.datetime.strptime(i,'%d/%m/%Y') for i in DF_INDIVIDU['DATE_CREATION_CARTE']]
DF_INDIVIDU.loc[(DF_INDIVIDU['AGE'] > 90) | (DF_INDIVIDU['AGE'] < 18) | (np.isnan(DF_INDIVIDU['AGE'])), 'TRANCHE_AGE'] = None
DF_INDIVIDU.loc[(DF_INDIVIDU['AGE'] >= 18) | (DF_INDIVIDU['AGE'] <= 25), 'TRANCHE_AGE'] = 'Tranche 18-25'
DF_INDIVIDU.loc[(DF_INDIVIDU['AGE'] >= 26) | (DF_INDIVIDU['AGE'] <= 45), 'TRANCHE_AGE'] = 'Tranche 26-45'
DF_INDIVIDU.loc[(DF_INDIVIDU['AGE'] >= 46) | (DF_INDIVIDU['AGE'] <= 90), 'TRANCHE_AGE'] = 'Tranche 46-90'
'''print(DF_INDIVIDU)'''
'''print(R_tickets_2016.columns)
print(R_tickets_2016.iloc[1])
print(R_magasin.columns)
print(R_magasin.iloc[1])
print(R_referentiel.columns)
print(R_referentiel.iloc[1])
print(R_typo_produit.columns)
print(R_typo_produit.iloc[1])'''
R_tickets_2016['DATE_ACHAT']=[(datetime.datetime.strptime(i,'%d/%m/%Y')) for i in R_tickets_2016['DATE_ACHAT']]
R_tickets_2016_2=R_tickets_2016.query('DATE_ACHAT>=datetime.datetime.strptime("2014-09-01","%Y-%m-%d")')
'''print(R_tickets_2016_2.shape)'''
df_matrice_travail= R_tickets_2016_2.merge(R_magasin,on='CODE_BOUTIQUE',how='left').merge(R_referentiel,on='EAN',how='left').merge(R_typo_produit,on='MODELE',how='left')
'''print(df_matrice_travail)'''
df_matrice_travail['PRIX_OK']= df_matrice_travail.apply(lambda x : 0 if x['MODELE']in ['FAVO','FAVORI'] else x['PRIX_AP_REMISE'], axis=1)
df_matrice_travail['CENTRE_VILLE']=df_matrice_travail.apply(lambda x : 'Centre ville' if x['CENTRE_VILLE'] in ['Centre ville'] else 'Centre commercial' if x['CENTRE_VILLE'] in ['Centre Co','Centre Commercial'] else 'NC',axis=1)
matrice_travail_ok=df_matrice_travail
'''print(matrice_travail_ok.columns)'''
dfparindiv=matrice_travail_ok.groupby(['ID_INDIVIDU', 'DATE_ACHAT', 'CODE_BOUTIQUE', 'NUM_TICKET'],as_index=False)
df_visite=dfparindiv.agg({'QUANTITE':sum,'PRIX_OK':sum})
df_visite=df_visite.rename(columns={'QUANTITE': 'NB_PRODUITS','PRIX_OK':'CA_VISITE'})
df_visite['PRIX_MOYEN']=df_visite['CA_VISITE']/df_visite['NB_PRODUITS']
'''print(df_matrice_travail.loc[df_matrice_travail['ID_INDIVIDU']==4])
print(df_visite.loc[df_visite['ID_INDIVIDU']==4])'''
'''print(df_visite)'''
df_visite_moy=df_visite.groupby(['ID_INDIVIDU'],as_index=False).agg({'NUM_TICKET':len,'CA_VISITE':sum,'NB_PRODUITS':np.average}).rename(columns={'NUM_TICKET': 'NB_VISITES','NB_PRODUITS':'NB_PRDT_MOY_VISITE','CA_VISITE':'MONTANT_CUMULE'})
df_visite_moy['CA_MOY_VISITE']=df_visite_moy['MONTANT_CUMULE']/df_visite_moy['NB_VISITES']
'''print(df_visite_moy)'''
def nombre_elements_distincts(liste):
    # Utilisation d'un ensemble pour stocker les éléments uniques
    elements_uniques = set(liste)
    # Retourne la taille de l'ensemble, qui correspond au nombre d'éléments distincts
    return len(elements_uniques)
def repere_cado(liste):
    compt=0
    for i in liste:
        if(i=='FAVO'or'FAVORI'):
            compt+=1
    return compt
df_indiv=matrice_travail_ok.groupby(['ID_INDIVIDU'],as_index=False).agg({'DATE_ACHAT':max,'CODE_BOUTIQUE':nombre_elements_distincts,'Ligne':nombre_elements_distincts,'Famille':nombre_elements_distincts,'MODELE':repere_cado})
df_indiv=df_indiv.rename(columns={'CODE_BOUTIQUE':'NB_MAG_DIFF','Ligne':'NB_LIGNES_DIFF','Famille':'NB_FAM_DIFF','MODELE':'NB_CADEAUX'})
df_indiv['RECENCE']=df_indiv['DATE_ACHAT'].apply(lambda x: (datetime.datetime.strptime('2016-08-31','%Y-%m-%d')-x).days)
df_indiv=df_indiv.drop(columns=['DATE_ACHAT'])
#a refaire pour trouver CODE_MAGASIN qui n'est pas dans matrice travail ok
dictpersmag={}
for i,j in zip(R_complement_individu_2016['ID_INDIVIDU'],R_complement_individu_2016['CODE_MAGASIN']):
    dictpersmag[i]=j
matrice_travail_ok_copy=df_visite[['ID_INDIVIDU','CODE_BOUTIQUE']]
matrice_travail_ok_copy['CODE_MAGASIN']=matrice_travail_ok_copy['ID_INDIVIDU'].apply(lambda x : dictpersmag[x])
matrice_travail_ok_copy['SAME']=[int(i==j) for i,j in zip(matrice_travail_ok_copy['CODE_MAGASIN'],matrice_travail_ok_copy['CODE_BOUTIQUE'])]
matrice_travail_ok_copy=matrice_travail_ok_copy.groupby(['ID_INDIVIDU'],as_index=False).agg({'SAME':sum})
df_indiv['PART_VIST_MAG_GEST']=[i/j for i,j in zip(matrice_travail_ok_copy['SAME'],df_visite_moy['NB_VISITES'])]
df_Matrice_finale=pd.merge(df_visite_moy,df_indiv,on='ID_INDIVIDU',how='left')
print(df_Matrice_finale)
df_Matrice_finale.to_csv('mon_fichier.csv', index=False)