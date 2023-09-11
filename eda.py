import pandas as pd
import requests

import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('ggplot')


GITHUB_URL = "https://github.com/aiedu-courses/stepik_linear_models/tree/main/datasets"
GITHUB_URL_RAW = "https://raw.githubusercontent.com/aiedu-courses/stepik_linear_models/main/datasets/"


def get_csv_list(url=GITHUB_URL):

    r = requests.get(url)
    csv_list = str(r.text)
    csv_list = csv_list.split('"')
    csv_list = [i for i in csv_list if '.csv' in i and 'D_' in i and 'dataset' not in i]
    
    return csv_list 


def make_df_dict(csv_list_, url_raw_=GITHUB_URL_RAW):
    dataframes = {}

    for file in csv_list_:    
     # Создание имени датафрейма с приставкой "df_"
        dataframe_name = f"df_{file.replace('.csv', '').replace('D_', '')}"
        # Чтение файла CSV в датафрейм
        file_path = ''.join([url_raw_, file])
        df_temp = pd.read_csv(file_path)
        df_temp = df_temp.drop_duplicates()
        dataframes[dataframe_name] = df_temp

    # Вывод созданных датафреймов
    return dataframes 
    
    
def make_fin_df(dataframes):

    # Собираем итоговый датафрейм 
    df_fin = pd.DataFrame()
    df_fin[['AGREEMENT_RK', 'ID_CLIENT', 'TARGET']] = dataframes['df_target'][['AGREEMENT_RK', 'ID_CLIENT', 'TARGET']]
    df_fin = df_fin.merge(dataframes['df_clients'], how='left', left_on='ID_CLIENT', right_on='ID')
    
    df_fin = df_fin[['AGREEMENT_RK', 'TARGET', 'ID_CLIENT', 'AGE', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS']]
    df_fin = df_fin.merge(dataframes['df_salary'], how='left', left_on='ID_CLIENT', right_on='ID_CLIENT')

    # Промежуточный датафрейм с займами
    df_loans = pd.merge(dataframes['df_loan'], dataframes['df_close_loan'], how='left', left_on='ID_LOAN', right_on='ID_LOAN')

    # Второй промежуточный датафрейм: соединяем клиентов с займами
    merged_df = df_fin.merge(df_loans, how='left', left_on='ID_CLIENT', right_on='ID_CLIENT')
    
    # Подсчитываем общее количество займов
    merged_df['LOAN_NUM_TOTAL'] = merged_df.groupby('ID_CLIENT')['ID_LOAN'].transform('count')
    # Подсчитываем количество закрытых займов
    merged_df['LOAN_NUM_CLOSED'] = merged_df.groupby('ID_CLIENT')['CLOSED_FL'].transform('sum')

    # Сборка
    df_fin = df_fin.merge(merged_df[['ID_CLIENT', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED']], on='ID_CLIENT')
    df_fin = df_fin[['AGREEMENT_RK', 'TARGET', 'AGE', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS', 'PERSONAL_INCOME', 'LOAN_NUM_TOTAL','LOAN_NUM_CLOSED']]
    
    del df_loans, merged_df
    
    return df_fin 
    
    
def target_dist(df):

    fig, ax = plt.subplots()
    sns.histplot(df, x='TARGET', bins=2, ax=ax)
    ax.set_title(label='Распределение отклика')
    
    return fig 
    
    
def loan_dist(df):

    fig, ax = plt.subplots()
    sns.histplot(df['LOAN_NUM_TOTAL'], ax=ax, label='Все кредиты')
    sns.histplot(df['LOAN_NUM_CLOSED'], ax=ax, label='Закрытые кредиты')
    ax.legend()

    ax.set_title(label='Распределение количества кредитов')
    return fig 
    
    
def age_box(df):
    fig, ax = plt.subplots()
    df['AGE'].plot(kind='box', title='Возраст')
    return fig 
    
    
def age_bar(df):
    fig, ax = plt.subplots()
    df['AGE'].plot(kind='hist', bins=df['AGE'].max() - df['AGE'].min() + 1, title='Возраст')
    return fig 
    
    
def corr_mtrx(df):

    corr_matrix = df[['TARGET', 'AGE', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS', 'PERSONAL_INCOME', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    ax.set_title(label='Матрица корреляций')

    return fig 
    

def age_vs_trg(df):

    fig, ax = plt.subplots()
    sns.boxplot(data=[df[df['TARGET'] == 0]['AGE'], df[df['TARGET'] == 1]['AGE']], palette=['#a1c9f4', '#ff9f9b'], ax=ax)
    ax.set_xticklabels(labels=['Нет отклика', 'Есть отклик'])
    ax.set_title(label='Возраст / Отклик')
    
    return fig 
    

def income_vs_trg(df):

    fig, ax = plt.subplots()
    sns.stripplot(x = "TARGET", y = "PERSONAL_INCOME", data = df, palette=['#a1c9f4', '#ff9f9b'])
    ax.set_xticklabels(labels=['Нет отклика', 'Есть отклик'])
    ax.set_title(label='Личный доход / Отклик')
    
    return fig 


def stat(df):

    df_stat = df[['AGE', 'PERSONAL_INCOME', 'DEPENDANTS']].describe()[1:].T[['mean', 'min', 'max', '50%', 'std']]
    df_stat['mean'] = df_stat['mean'].round()
    df_stat['std'] = df_stat['std'].round(2)

    df_stat.rename(columns={'mean':'Среднее', 'min':'Минимум', 'max':'Максимум', '50%':'Медиана', 'std':'Ст. отклонение'}, 
                   index={'AGE':'Возраст', 'PERSONAL_INCOME':'Личный доход', 'DEPENDANTS':'Иждивенцы'}, 
                   inplace=True)

    return df_stat