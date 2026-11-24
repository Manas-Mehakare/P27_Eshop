import os, streamlit as st
from dotenv import load_dotenv
from groq import Groq
from PIL import Image
from core import PRODUCTS, answer, redact, catalogue_lines, handoff
from search import semantic, photo_search
from media import banner, speech
load_dotenv(); st.set_page_config(page_title='Mini E-Shop',page_icon='🛒'); st.title('Mini E-Shop Support')
key=os.getenv('GROQ_API_KEY') or st.sidebar.text_input('Groq API key',type='password')
st.sidebar.caption('Mock catalogue • 7-day returns • no real orders')
with st.expander('Catalogue'):
    st.table(PRODUCTS)
with st.expander('Find this item by photo'):
    file=st.file_uploader('Upload product photo',type=['png','jpg','jpeg'])
    if file and st.button('Find item'):
        try:
            p,score=photo_search(Image.open(file)); st.write(f'Closest match (similarity {score:.2f})'); st.write(catalogue_lines([p]) if score>=0.65 else handoff('low_image_similarity'))
        except Exception as e: st.error('Image search unavailable. Check model download and image format.')
with st.expander('Generate product banner'):
    p=st.selectbox('Product',PRODUCTS,format_func=lambda p:p['name'])
    if st.button('Generate banner'):
        b=banner(p); st.image(b); st.download_button('Save banner',b,'banner.png','image/png')
if 'history' not in st.session_state: st.session_state.history=[]
for role,msg in st.session_state.history:
    with st.chat_message(role): st.write(msg)
if q:=st.chat_input('Ask about products, orders or returns'):
    if not key: st.warning('Enter your Groq API key in the sidebar.')
    else:
        q=redact(q); st.session_state.history.append(('user',q))
        try: reply=answer(q,Groq(api_key=key),semantic)
        except Exception: reply=handoff('search_error')
        st.session_state.history.append(('assistant',reply)); st.rerun()
if st.session_state.history and st.button('Read latest reply aloud'):
    try: st.audio(speech(st.session_state.history[-1][1]),format='audio/mp3')
    except Exception: st.error('TTS requires internet access.')
