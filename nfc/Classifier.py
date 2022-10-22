# imports
import pandas as pd
import os
dir_list = os.listdir(os.getcwd())
print(dir_list)
#Cargar los datos
fold = './nfc/files/'
filenames = ['Catalogo_Giros.csv','Clientes_Descriptivo.csv','Transacciones_Clientes.csv']
cat_df = pd.read_csv(fold+filenames[0], sep="\t")
cli_df = pd.read_csv(fold+filenames[1], sep="\t")
trans_df = pd.read_csv(fold+filenames[2], sep="\t")

class Classifier:
    def __init__(self, client_id):
        self.client_id = client_id
        self.__type = "NORMAL"
        self.__mergeData()
        self.__getMayores()
        self.__getVulnerables()
    
    def __mergeData(self):
        self.gen_df = pd.merge(pd.merge(trans_df,cli_df,on='NU_CTE_COD'),cat_df,on='NU_AFILIACION')
        self.result_df = self.gen_df
    
    """
    ADULTOS MAYORES
        - POR LEY SE CONSIDERA ADULTO MAYOR A ALGUIEN CON MAS DE 60 AÑOS
    """
    def __getMayores(self):
        mayores_df = self.gen_df.loc[self.gen_df["EDAD"]>60] # POR LEY SE CONSIDERA ADULTO MAYOR A ALGUIEN CON MAS DE 60 AÑOS
        self.mayores = mayores_df['NU_CTE_COD'].unique()
        self.result_df = self.result_df.loc[~self.result_df["NU_CTE_COD"].isin(self.mayores)]
    
    """
    COLECTIVOS EN SITUACIÓN DE VULNERABILIDAD
        - TODAS LAS TRANSACCIONES SON DEBITO
        - NO TIENEN AL MENOS UN MOVIMIENTO AL MES
        - MENOS DE 1,000 EN MOVIMIENTOS MENSUALES
    """
    def __getVulnerables(self):
        credito_ids = self.result_df.loc[self.result_df['TIPO_TARJETA']=='CREDITO']['NU_CTE_COD'].unique()
        tend_df = self.result_df.loc[~self.result_df['NU_CTE_COD'].isin(credito_ids)]
        tend_df['FH_OPERACION'] = pd.to_datetime(tend_df['FH_OPERACION'])
        tend_df['year'] = tend_df['FH_OPERACION'].dt.year
        tend_df['month'] = tend_df['FH_OPERACION'].dt.month
        tend_df['day'] = tend_df['FH_OPERACION'].dt.day
        tend_df.drop('FH_OPERACION', axis = 1, inplace = True)
        mensual_df = tend_df.groupby(['NU_CTE_COD','month']).agg({'CD_GIRO':'count', 'IM_TRANSACCION': 'sum'}).reset_index()
        mensual_df['count'] = 1
        tend_df = mensual_df.groupby('NU_CTE_COD').sum().reset_index()
        vulnerables = tend_df.loc[tend_df['count'] < 12]
        mensual_df = mensual_df.loc[~mensual_df['NU_CTE_COD'].isin(vulnerables['NU_CTE_COD'])]
        mensual_df = mensual_df.loc[mensual_df['IM_TRANSACCION'] < 1000]
        self.vulnerables = mensual_df['NU_CTE_COD'].unique()
        self.result_df = self.result_df.loc[~self.result_df['NU_CTE_COD'].isin(self.vulnerables)]
    
    def __getType(self):
        if self.client_id in self.mayores:
            self.__type = "MAYOR"
            return
        if self.client_id in self.vulnerables:
            self.__type = "VULNERABLE"
            return
        """
        PERSONAS CON DISCAPACIDAD
            - AQUELLAS PERSONAS QUE EN SUS 5 SUBGIROS CON MAS GATOS ESTAN
                (droguerias, doctores, medicos o funerarios)
        """
        cli_df = self.result_df.loc[self.result_df['NU_CTE_COD'] == self.client_id]
        df_calculos = cli_df.groupby(['NB_GIRO', 'NB_SUBGIRO']).agg({'CD_GIRO':'count', 'IM_TRANSACCION': 'sum'}).reset_index()
        df_calculos = df_calculos.sort_values(by=["IM_TRANSACCION", "CD_GIRO"], ascending=False)
        top = ' '.join(df_calculos.head(5)['NB_SUBGIRO'].values.tolist())
        top = top.lower()
        if 'droguerias' in top:
            self.__type = "DISCAPACITADO"
            return
        if 'doctores' in top:
            self.__type = "DISCAPACITADO"
            return
        if 'medicos' in top:
            self.__type = "DISCAPACITADO"
            return
        if 'funerarios' in top:
            self.__type = "DISCAPACITADO"
            return
    
    def getClassification(self):
        self.__getType()
        return self.__type
    
    def getDataClient(self):
        return self.gen_df.loc[self.gen_df['NU_CTE_COD'] == self.client_id]
