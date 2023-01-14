import pandas as pd
import pickle

class PREVISOES:
    def tratamento_dados(self):
        def vegetacao(i):
            switcher={
                'Porto': 82.99,
                'Leiria': 127.73,
                'Viana do Castelo': 71.85,
                'Coimbra': 233.07,
                'Aveiro': 80.53,
                'Lisboa': 36.26,
                'Braga': 40.35,
                'Guarda': 111.60,
                'Castelo Branco': 185.77,
                'Viseu': 138.88,
                'Santarém': 204.85,
                'Vila Real': 70.13,
                'Setúbal': 100,
                'Faro': 145.2,
                'Évora': 338.53,
                'Bragança': 144.49,
                'Beja': 244.67,
                'Portalegre': 255.37,
                'Grandola': 201.16,
                'Caldas da Rainha': 61.69,
                'Tomar': 153.86,
                'Penafiel': 58.84,
                'Guimarães': 45.13,
                'Chaves': 70.97
            }
            return switcher.get(i)

        df = pd.read_csv("datasets/fogos_tratados.csv")

        # Dados inseridos pelo utilizador
        hora = float(input('Hora: '))
        dia = float(input('Dia: '))
        mes = float(input('Mês: '))
        dsr = float(input('DSR: '))
        fwi = float(input('FWI: '))
        isi = float(input('ISI: '))
        dc = float(input('DC: '))
        dmc = float(input('DMC: '))
        ffmc = float(input('FFMC: '))
        bui = float(input('BUI: '))
        distrito = str(input('Distrito: '))
        area_vegetacao = vegetacao(distrito)

        # Valores máximos para a divisão para valores do SMOTE
        max_hora = df['Hora'].max()
        max_dia = df['Dia'].max()
        max_mes = df['Mes'].max()
        max_dsr = df['DSR'].max()
        max_fwi = df['FWI'].max()
        max_isi = df['ISI'].max()
        max_dc = df['DC'].max()
        max_dmc = df['DMC'].max()
        max_ffmc = df['FFMC'].max()
        max_bui = df['BUI'].max()
        max_area_vegetacao = df['AreaVegetacao'].max()

        # Dados com o SMOTE
        nova_hora = hora/max_hora
        novo_dia = dia/max_dia
        novo_mes = mes/max_mes
        novo_dsr = dsr/max_dsr
        novo_fwi = fwi/max_fwi
        novo_isi = isi/max_isi
        novo_dc = dc/max_dc
        novo_dmc = dmc/max_dmc
        novo_ffmc = ffmc/max_ffmc
        novo_bui = bui/max_bui
        novo_area_vegetacao = area_vegetacao/max_area_vegetacao

        # Array que vai ser dado para a previsão
        self.array = [novo_mes, novo_dia, nova_hora, novo_dsr, novo_fwi, novo_isi, novo_dc, 
        novo_dmc, novo_ffmc, novo_bui, novo_area_vegetacao]

    def previsoes(self):
        # Load the classifier
        with open('saved_clf/extremely_classifier.pkl', 'rb') as fid:
            clf_loaded = pickle.load(fid)

        previsao = clf_loaded.predict([self.array])

        print('Previsão de uma severidade', previsao[0], 'para este incêndio.')