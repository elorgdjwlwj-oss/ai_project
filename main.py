import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름')
b=st.selectbox('좋아하는 음식',['떡볶이','치킨','마라탕'])
if st.button('인사말 생성'):
  st.write(a+'님! 안녕하세요 !')
