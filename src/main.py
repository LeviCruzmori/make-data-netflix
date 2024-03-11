#inicio do codigo
import pandas as pd
import os
import glob

# variavel folder-path caminho para ler os arquivos

folder_path = 'src\\data\\raw'

# vai listar todos os arquivos de exel
excel_files = glob.glob( os.path.join(folder_path,'*xlsx'))
if not excel_files:
    print('nunhum arquivo encontrado')
else:
    #data freme = tabela na memoria para quandar os arquivos
    dfs = []

    for excel_files in excel_files:

        try:
            #leio o arquivo de excel # teste par ver se esta lendo print(df_temp)
            df_temp = pd.read_excel(excel_files)            
            
            #pegar o nome do arquivo
            file_name = os.path.basename(excel_files)

            #coluna file_name
            df_temp['filename'] = file_name

            # criação de uma coluna chamada location
            if 'brasil'in file_name.lower():
                df_temp['location'] = 'br'
            elif 'france' in file_name.lower():
                df_temp['location'] = 'fr'
            elif 'italia' in file_name.lower():
                df_temp['location'] = 'it'

            #criação de coluna chamada campaign
            df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

            #quarda dados tratados dentro de uma dataframe comum
            dfs.append(df_temp)
            #print(df_temp)

        except Exception as e:
            print(f"Erro ao ler o arquivo {excel_files} : {e}")

    if dfs:
        #concatena todas as tabelas salvas no dfs em uma unica tabela
        result = pd.concat(dfs,ignore_index=True)
        
        #caminho de saida
        output_file = os.path.join('src','data','ready','clean.xlsx')
        
        # configurou motor de escrita
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
        
        # leva os dados do resultado a serem escritos no motor de exel configurado
        result.to_excel(writer, index=False)
        
        #salva o arquivo de excel
        writer._save()
    else:
        print('nunhum dado para ser salvo')