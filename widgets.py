# импортируем библиотеку streamlit
import streamlit as st

# импортируем библиотеку pandas
import pandas as pd

# Название
st.title("Песочница")

# Заголовок
st.header("Это заголовок")

# Подзаголовок
st.subheader("Это подзаголовок")

# Текст
st.text("Просто текст")

# Можно передавать параметры!
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))

# Инфомрационные сообщения 
st.success("Success")
st.info("Information")
st.warning("Warning")
st.error("Сообщение об ошибке")

# импортируем функцию Image, чтобы открывать картинки
from PIL import Image

# загружаем картинку
img = Image.open("DS_Methodology_chart.jpg")

# отображаем картинку используя streamlit
# st.image(img, width=400)
st.image(img)

# проверяем выбран ли чекбокс
if st.checkbox("Show/Hide"):
    # показываем текст если чекбокс выбран
    st.text("Showing the widget")
    
    
# радиобаттон
status = st.radio("Select Gender: ", ('Male', 'Female'))

if (status == 'Male'):
    st.success("Male")
else:
    st.success("Female")
    
