import streamlit as st
from utils import auth
import requests
import json

url = 'http://stylishdao.csie.org:3000/api/1.0/products/create'
linebot = 'https://29b8-59-120-11-125.ngrok-free.app//test'
def getSheetRange(totalRow, totalCol):
    ALPHABETLIST = ALPHABETLIST = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    start = 'A1'
    if totalCol>=len(ALPHABETLIST):
        end = ALPHABETLIST[totalCol//26] + ALPHABETLIST[totalCol%26] + str(totalRow)
    else:
        end = ALPHABETLIST[totalCol%26] + str(totalRow)
    sheetRange = f'{start}:{end}'
    return sheetRange

def upload():
    st.header('STYLiSH 新增商品後台系統')
    st.markdown('若要直接上架商品，請按 **upload**；若要新增商品至清單中請按 **submit**')
    product_id  = st.text_input('product id')
    category    = st.text_input('category', 'men')
    title       = st.text_input('title', 'This is title')
    description = st.text_input('description', '這款「鬆身連帽外套」融合了時尚和舒適感，是你秋冬季節的必備單品。外套採用柔軟舒適的棉質面料製作，有著極高的透氣性和保暖性，讓你在寒冷的天氣中保持舒適。連帽設計不僅可以保護你的頭部和頸部不受寒風侵襲，還可以增添一份帥氣和潮流感。寬鬆的版型設計，可以讓你輕鬆地穿上多層衣服，讓你隨時保持暖和。此外，這款外套還有充足的口袋設計，可以輕鬆存放你的手機、財物等小物品。不管是在街頭、學校還是旅行途中，這款外套都能為你帶來出色的時尚體驗和舒適感受。')
    price       = st.text_input('price', 30)
    texture     = st.text_input('texture', 'This is texture')
    wash        = st.text_input('wash', 'This is wash')
    place       = st.text_input('place', 'This is place')
    note        = st.text_input('note', 'This is note')
    story       = st.text_input('story', 'This is story')
    main_image  = st.text_input('main image', 'https://gateway.pinata.cloud/ipfs/QmanQDr6bDTsw51t12kSe2EgCYVHCaMDEHkc4wR6ucPm2j?_gl=1*xrp1a7*rs_ga*M2ExODYwMTktMmZiNy00NjI3LTgwNWEtZjJmYzBmNmVhYjQz*rs_ga_5RMPXG14TE*MTY4MjQxMzE0OS4xMi4xLjE2ODI0MTM2MjcuNjAuMC4w')
    color_ids   = st.text_input('color ids', '1,3')
    sizes       = st.text_input('sizes', 'S,L')
    other_image = st.text_input('other images', 'https://gateway.pinata.cloud/ipfs/QmNRWpGwGkHAGbjQiC6hEaqb22bRU4cKkAGUuvyxYRaY5h?_gl=1*1cbydc1*rs_ga*M2ExODYwMTktMmZiNy00NjI3LTgwNWEtZjJmYzBmNmVhYjQz*rs_ga_5RMPXG14TE*MTY4MjQxMzE0OS4xMi4xLjE2ODI0MTM2MjcuNjAuMC4w,https://gateway.pinata.cloud/ipfs/Qmafotsa1sDseZ3pKSSUvtfm9tTW4QcCLaMnziu1nQa7eB?_gl=1*1cbydc1*rs_ga*M2ExODYwMTktMmZiNy00NjI3LTgwNWEtZjJmYzBmNmVhYjQz*rs_ga_5RMPXG14TE*MTY4MjQxMzE0OS4xMi4xLjE2ODI0MTM2MjcuNjAuMC4w,https://gateway.pinata.cloud/ipfs/QmeHZWNxTWT5KA2jedCXEXgN59ityJNAtWijcdtzL2y6A7?_gl=1*apds4s*rs_ga*M2ExODYwMTktMmZiNy00NjI3LTgwNWEtZjJmYzBmNmVhYjQz*rs_ga_5RMPXG14TE*MTY4MjQxMzE0OS4xMi4xLjE2ODI0MTM4MTkuNTEuMC4w')
    st.subheader('直接上架')
    uploadButton  = st.button('upload')
    st.subheader('加入清單中')
    sheetUrl      = st.text_input('sheet url', 'https://docs.google.com/spreadsheets/d/1XElQspBztCtSHUG6BXZVoWFetkhh9J_817rciOKcI18/edit#gid=0')
    submitButton  = st.button('submit')
    if uploadButton==True:
        if not product_id: st.error('please provide product id')
        else:
            data = {
                'product_id':   product_id,
                'category':     category,
                'title':        title,
                'description':  description,
                'price':        price,
                'texture':      texture,
                'wash':         wash,
                'place':        place,
                'note':         note,
                'story':        story,
                'main_image':   main_image,
                'color_ids':    color_ids,
                'sizes':        sizes,
                'other_images': other_image
            }
            
            response = requests.post(url, data=data)
            st.json(response.json())
            d = {
                'id': [product_id]
            }
            res = requests.post(linebot, data=json.dumps(d))
            uploadButton = False
    elif submitButton==True:
        if not product_id: st.error('please provide product id')
        else:
            sheet = auth.authenticate(sheetUrl)
            sh = sheet.worksheets()[0]
            content = sh.get_all_values()
            newItem = [product_id, category, title, description, price, texture, wash, place, note, story, main_image, color_ids, sizes, other_image]
            content.append(newItem)
            sheetRange = getSheetRange(len(content), 14)
            sh.update(sheetRange, content)
            st.snow()
    return



if __name__=='__main__':
    upload()