import streamlit as st
from utils import auth
import requests
import json

entry   = 'http://stylishdao.csie.org:3000/api/1.0/products/create'
linebot = 'https://29b8-59-120-11-125.ngrok-free.app//test'

def handle_sheet(url='https://docs.google.com/spreadsheets/d/1XElQspBztCtSHUG6BXZVoWFetkhh9J_817rciOKcI18/edit#gid=0'):
    sheet = auth.authenticate(url)
    sh = sheet.worksheets()[0]
    content = sh.get_all_values()
    ids = []
    for i in range(len(content)):
        if not content[i][0]: break
        data = {
            'product_id':   content[i][0],
            'category':     content[i][1],
            'title':        content[i][2],
            'description':  content[i][3],
            'price':        content[i][4],
            'texture':      content[i][5],
            'wash':         content[i][6],
            'place':        content[i][7],
            'note':         content[i][8],
            'story':        content[i][9],
            'main_image':   content[i][10],
            'color_ids':    content[i][11],
            'sizes':        content[i][12],
            'other_images': content[i][13]
        }
        response = requests.post(entry, data=data)
        st.json(response.json())
        ids.append(content[i][0])
    sh.clear()
    d = {
        'id': ids
    }
    res = requests.post(linebot, data=json.dumps(d))
    return


def multi():
    st.header('批量上傳')
    url = st.text_input('url', 'https://docs.google.com/spreadsheets/d/1XElQspBztCtSHUG6BXZVoWFetkhh9J_817rciOKcI18/edit#gid=0')
    
    clicked = st.button('submit')
    if clicked: 
        handle_sheet(url)
        clicked = False
    return

if __name__=='__main__':
    multi()