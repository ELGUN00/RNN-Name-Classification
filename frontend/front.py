import streamlit as st
import requests
import time
import pandas as pd

st.set_page_config(
    page_title="Name classification",page_icon=':person:',initial_sidebar_state="expanded"
)



  

with open('./frontend/style.css') as f:
    st.markdown(f'<style>{f.read()}/<style>', unsafe_allow_html=True)

with st.container():
    st.write("""# ML name classification project """)
    st.write('---')
    st.write(' ')
    st.write('### Test data metrics:')
    df = pd.read_csv('./frontend/report.csv')
    # df = pd.DataFrame(
    # [
    #     {"metric": "Precision", "score": '95%'},
    #     {"metric": "Recall", "score": '95%'},
    #     {"metric": "F1", "score": '95%'},
    # ])
    st.dataframe(df, use_container_width=True)
    st.write(' ')


c1 = st.container()
c2 = st.container()


def test(name):
    if name:
        try:
            with st.spinner('Wait for it...'):
                time.sleep(1)
            r = requests.get(f'http://api:8080/{name}')
            data = r.json().get('data')
            with c2:
                st.write(""" ### The result of nationality in percentage""")
                columns = st.columns(5)
                for i, col in enumerate(columns):
                    col.metric(data[i][1], f'{data[i][0]}%')
        except Exception as e:
            st.error(e, icon="🚨")
    else:
        st.error('Please write name', icon="🚨")

with c1:
    with st.form(key='Search name nationality'):
        st.write('Name Information')
        name = st.text_input(label="Name ")
        submit_form = st.form_submit_button(label="Find nationality", help="Click to search name nationality!", on_click=test(name))



