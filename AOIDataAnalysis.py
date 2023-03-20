import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.header("Defect rate analysis system")
with st.sidebar:
    uploaded_files = st.file_uploader('Upload your files',accept_multiple_files=True)

data_list = [] 
for f in uploaded_files: 
    data = pd.read_csv(f) 
    data_list.append(data)
try:
    if data_list[1] is not None: 
        df = data_list[0].T
        
        df.columns = ['Unnamed: 1','OVAL','CUT','BOT','SIDE1','SIDE2','NECKOUT','.','-Total-','-Good-','-Bad-','-Rate(%)-']
        df = df.drop(['ITEM'])
        with st.sidebar:
            st.write(df.head(5))
   
        count = len(df)
        df.reset_index(drop=True, inplace=True)
        df_time = df['Unnamed: 1']
        df['OVAL'] = pd.to_numeric(df['OVAL'])
        df['CUT'] = pd.to_numeric(df['CUT'])
        df['BOT'] = pd.to_numeric(df['BOT'])
        df['SIDE1'] = pd.to_numeric(df['SIDE1'])
        df['SIDE2'] = pd.to_numeric(df['SIDE2'])
        df['NECKOUT'] = pd.to_numeric(df['NECKOUT'])
        df['-Total-'] = pd.to_numeric(df['-Total-'])
        df['-Good-'] = pd.to_numeric(df['-Good-'])
        df['-Bad-'] = pd.to_numeric(df['-Bad-'])
        df['-Rate(%)-'] = pd.to_numeric(df['-Rate(%)-'])
        
        df_flaw = df['OVAL'] + df['CUT'] + df['BOT'] + df['SIDE1'] + df['SIDE2'] + df['NECKOUT']
        df_flaw_machine = df['-Bad-']
            
        list = ''
        ture = 0
        false = 0
        df1 = df

        for i in range(count):
            if df_flaw[i] == df_flaw_machine[i]:
                ture = ture + 1
            else:
                false = false + 1
                    #list = list + df_time[i] + '\n'
                df1 = df1.drop([i], axis = 0)

        list = ''
        df2 = df
        for i in range(count):
            if df_flaw_machine[i] < 400:
                    #list = list + df_time[i] + '\n'
                df2 = df2.drop([i], axis = 0)

        flaw_number = 0
        flaw_number1 = 0
        flaw_number2 = 0
        flaw_number3 = 0
        flaw_number4 = 0
        flaw_number5 = 0
        flaw_number6 = 0
        flaw_number7 = 0
        flaw_number8 = 0
        flaw_number9 = 0
        
        A = 0
        time_count = 0
        count_A = len(data_list[1])
        
        name = data_list[1]['name']
        time_start = data_list[1]['start time']
        time_finish = data_list[1]['finish time']
        
        df_time = pd.to_datetime(df['Unnamed: 1'])
        time_start = pd.to_datetime(time_start)
        time_finish = pd.to_datetime(time_finish)
        
        list_q = name.tolist()
        
        ddd = pd.DataFrame(columns=['OVAL','CUT','BOT','SIDE1','SIDE2','NECKOUT','-Total-','-Good-','-Bad-','-Rate(%)-'])
        #st.write(ddd)
        for j in range(count_A):
            start = time_start[j]
            finish = time_finish[j]
            #st.write(df['OVAL'])
            for i in range(count):
                if df_time[i] == start:
                    A = 1
                if A == 1:
                    time_count = time_count + 1
                    flaw_number = flaw_number + df['OVAL'][i]
                    flaw_number1 = flaw_number1 + df['CUT'][i]
                    flaw_number2 = flaw_number2 + df['BOT'][i]
                    flaw_number3 = flaw_number3 + df['SIDE1'][i]
                    flaw_number4 = flaw_number4 + df['SIDE2'][i]
                    flaw_number5 = flaw_number5 + df['NECKOUT'][i]
                    flaw_number6 = flaw_number6 + df['-Total-'][i]
                    flaw_number7 = flaw_number7 + df['-Good-'][i]
                    flaw_number8 = flaw_number8 + df['-Bad-'][i]
                    flaw_number9 = flaw_number9 + df['-Rate(%)-'][i]
                if df_time[i] == finish:
                    A = 0

            flaw_number9 = flaw_number9/time_count
            ddd.loc[j] = [flaw_number,flaw_number1,flaw_number2,flaw_number3,flaw_number4,flaw_number5,flaw_number6,flaw_number7,flaw_number8,flaw_number9]
            flaw_number = 0
            flaw_number1 = 0
            flaw_number2 = 0
            flaw_number3 = 0
            flaw_number4 = 0
            flaw_number5 = 0
            flaw_number6 = 0
            flaw_number7 = 0
            flaw_number8 = 0
            flaw_number9 = 0
            time_count = 0

        st.header('實驗數據')
        st.write(ddd) 
        list_d = []
        
        flaw = ddd['OVAL'].values.tolist()
        flaw1 = ddd['CUT'].values.tolist()
        flaw2 = ddd['BOT'].values.tolist()
        flaw3 = ddd['SIDE1'].values.tolist()
        flaw4 = ddd['SIDE2'].values.tolist()
        flaw5 = ddd['NECKOUT'].values.tolist()
        flaw6 = ddd['-Total-'].values.tolist()
        flaw7 = ddd['-Good-'].values.tolist()
        flaw8 = ddd['-Bad-'].values.tolist()
        flaw9 = ddd['-Rate(%)-'].values.tolist()
        list_d = list_d + [flaw] + [flaw1]+ [flaw2]+ [flaw3]+ [flaw4]+ [flaw5]+ [flaw6]+ [flaw7]+ [flaw8]+ [flaw9]
        
        ddd_new = ddd[['-Good-', '-Bad-']]
        st.header('卡方統計檢定結果')
        
        qqqq = pd.DataFrame(columns=list_q, index = list_q)
        #st.write(qqqq)
        for j in range(count_A):
            for i in range(count_A):
                observed = ddd_new.loc[[j, i]]
                out=stats.chi2_contingency(observed=observed,correction=False)
                B = list_q[j]
                if out[1] >= 0.05:
                    qqqq.iat[j, i] = out[1]
                if out[1] < 0.05:
                    qqqq.iat[j, i] = out[1]
        st.write(qqqq)
        
except:
    st.write()




