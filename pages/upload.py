import streamlit as st
from utils import auth
import requests
import json

url = 'http://stylishdao.csie.org:3000/api/1.0/products/create'

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
    category    = st.text_input('category', 'This is category')
    title       = st.text_input('title', 'This is title')
    description = st.text_input('description', 'This is description')
    price       = st.text_input('price', 30)
    texture     = st.text_input('texture', 'This is texture')
    wash        = st.text_input('wash', 'This is wash')
    place       = st.text_input('place', 'This is place')
    note        = st.text_input('note', 'This is note')
    story       = st.text_input('story', 'This is story')
    main_image  = st.text_input('main image', 'https://cdn.leonardo.ai/users/c621d88d-7acc-4fcb-9ccd-77dfa7226c81/generations/bf173785-9bfc-489f-94a6-b0539cbe86ba/Leonardo_Diffusion_The_stars_are_twinkling_and_filling_the_sk_0.jpg')
    color_ids   = st.text_input('color ids', '1,2,3,4,5')
    sizes       = st.text_input('sizes', 'S,S,S,S,S')
    other_image = st.text_input('other images', 'https://cdn.leonardo.ai/users/c621d88d-7acc-4fcb-9ccd-77dfa7226c81/generations/bf173785-9bfc-489f-94a6-b0539cbe86ba/Leonardo_Diffusion_The_stars_are_twinkling_and_filling_the_sk_0.jpg')
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