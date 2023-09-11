import streamlit as st

from eda import * 

st.title('ДОМАШНЕЕ ЗАДАНИЕ ПО EDA + STREAMLIT')

st.header('Исходные файлы и статистика')

st.subheader('Список файлов')
# список файлов  
csv_list = get_csv_list()
st.write(csv_list)

st.subheader('Датафреймы')
# словарь с датафреймами
df_dct = make_df_dict(csv_list)
for name, item in df_dct.items():
    st.text(f'{name}:')
    st.write(item.head(3))
    
# финальный датафрейм     
df = make_fin_df(df_dct)
st.subheader('Итоговый датафрейм')
st.write(df.head()) 
st.text(f'{df.shape[0]} строк, {df.shape[1]} столбцов') 

# удоляем лишнее
del df_dct

# количество дубликатов и пропусков
st.text(f'Количество дубликатов: {len(df) - len(df.drop_duplicates())}')
st.text(f'Количество пропусков: {len(df) - len(df.dropna())}')

# удаляем дубликаты 
df.drop_duplicates(inplace=True)
st.text('После удаления дубликатов и пропусков:')
st.text(f'{df.shape[0]} строк, {df.shape[1]} столбцов') 

# статистики нек. признаков 
st.subheader('Некоторые статистики')
df_stat = stat(df) 
st.write(df_stat) 

# числовые характеристики  
df_ = df['SOCSTATUS_WORK_FL'].value_counts()
st.write(df_) 

df_ = df['SOCSTATUS_PENS_FL'].value_counts()
st.write(df_) 

st.subheader('Визуализация')

# первый графег: распределение отклика 
fig = target_dist(df)
st.pyplot(fig)

# распределение займов 
fig = loan_dist(df)
st.pyplot(fig)

# возраст ящик с усами 
fig = age_box(df)
st.pyplot(fig)

# возраст ящик с усами 
fig = age_bar(df)
st.pyplot(fig)

# матрица корреляций 
fig = corr_mtrx(df)
st.pyplot(fig)

# возраст vs отклик 
fig = age_vs_trg(df)
st.pyplot(fig) 

# доход vs отклик 
fig = income_vs_trg(df)
st.pyplot(fig) 


