library(tidyverse)
library(FactoMineR)
recap_RFM <- read_csv("C:/Users/mathu/OneDrive/Bureau/2023-2024/MAS/marketing/marketing/donneVerif/recap_RFM.csv")
recap_Segment_RFM <- read_csv("C:/Users/mathu/OneDrive/Bureau/2023-2024/MAS/marketing/marketing/donneVerif/recap_Segment_RFM.csv")
tableau_rfm <- read_csv("C:/Users/mathu/OneDrive/Bureau/2023-2024/MAS/marketing/marketing/donneVerif/tableau_rfm.csv")
rfm <- read_csv("C:/Users/mathu/OneDrive/Bureau/2023-2024/MAS/marketing/marketing/donneVerif/rfm.csv")
liste<-c()
for (i in tableau_rfm$Segment_Recence){
  if(!is.na(i)){
  if(i=='Haut'){liste<-c(liste,'Très peu récent')}
  else if(i=='Moyen'){liste<-c(liste, 'Peu récent')}
  else if(i=='Bas'){liste<-c(liste,'Récent')}}else{liste<-c(liste,NA)}
}
tabjoin<-rfm%>%left_join(tableau_rfm,by='ID_INDIVIDU')
tabjoin$CENTRE_VILLE<-sapply(tabjoin$CENTRE_VILLE,function(x) ifelse(x == "Centre Co", "Centre Commercial", x))
tabjoin$CENTRE_VILLE<-as.factor(tabjoin$CENTRE_VILLE)
tabjoin$SEXE<-factor(tabjoin$SEXE,levels=c(0,1,2),labels=c('Inconnu','Homme','Femme'))
ggplot(tabjoin)+aes(x=NB_CADEAUX,y=MONTANT_CUMULE.x,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Montant cumulé selon le nombre de cadeaux reçu",x="Nombre de cadeau",y="Montant cumulé")
ggplot(tabjoin)+aes(x=Segment_RFM,y=AGE,color=Segment_RFM)+geom_boxplot()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title='Age des clients selon leurs groupes',x="Groupe RFM",y="Age")
ggplot(tabjoin)+aes(x=CENTRE_VILLE,y=MONTANT_CUMULE.x)+geom_boxplot()+labs(title="Montant cumulé selon le lieu du magasin gestionnaire",x="Lieu",y="Montant cumulé")
ggplot(tabjoin)+aes(x=NB_MAG_DIFF,y=RECENCE.x,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title='Récence de la dernière visite selon\n le nombre de magasin visité',x="Nombre de magasin visité",y="Récence du dernier achat")
summary_data <- table(filter(tabjoin,SEXE=="Femme")$Segment_RFM)

# Convertir le résumé en un dataframe
summary_df <- as.data.frame(summary_data)

# Renommer les colonnes du dataframe
colnames(summary_df) <- c("Type de client", "count")
summary_df$percentage<-summary_df$count/sum(summary_df$count)*100
# Créer le camembert avec ggplot
ggplot(summary_df, aes(x = "", y = count, fill = `Type de client`)) +
  geom_bar(stat = "identity", width = 1)+
  scale_fill_manual(values=c("lightblue","purple","orange","blue","red")) +
  coord_polar("y", start = 0)+geom_text(aes(label = paste0(round(percentage), "%")), position = position_stack(vjust = 0.5)) +
  labs(title = "Répartition des client femmes selon\n les groupes RFM") +
  theme_void() +
  theme(legend.position = "right")
ggplot(tabjoin)+aes(x=NB_CADEAUX,y=RECENCE.x,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Récence selon le nombre de cadeaux reçu",x="Nombre de cadeau",y="Récence")
ggplot(tabjoin)+aes(x=Segment_RFM,y=ANCIENNETE,color=Segment_RFM)+geom_boxplot()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Ancienneté selon le segment RFM",x="Segment RFM",y="Ancienneté")
ggplot(tabjoin)+aes(x=Segment_RFM,y=tabjoin$PART_VIST_MAG_GEST,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Ancienneté selon le segment RFM",x="Segment RFM",y="Ancienneté")
ggplot(tabjoin)+aes(x=CA_MOY_VISITE,y=MONTANT_CUMULE.x,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Dépense totale selon le cout du panier moyen",x="Prix panier moyen",y="Dépense totale")
ggplot(tabjoin)+aes(x=Segment_RFM,y=NB_LIGNE_DIFF,color=Segment_RFM)+geom_point()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Ancienneté selon le segment RFM",x="Segment RFM",y="Ancienneté")
ggplot(tabjoin)+aes(x=Segment_RFM,y=NB_FAM_DIFF,color=Segment_RFM)+geom_boxplot()+scale_color_manual(values=c("lightblue","purple","orange","blue","red"), name = "Type de client")+labs(title="Nombre de famille d'article acheté\n selon le segment RFM",x="Segment RFM",y="Nombre de famille")
sum(summary_data)
summary_data2 <- table(tabjoin$Segment_RFM)
sum(summary_data2)
