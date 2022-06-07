import streamlit as st


from PIL import Image
import pytesseract
from pytesseract import image_to_string
import io
import requests
import pandas as pd
from bs4 import BeautifulSoup
import pathlib


st.title("Detect Text in Images in Bulk")


alt_text_list = []
img_text_list = []
urls_list = []

img_list = []
df1 = pd.DataFrame(columns=["url", "img url", "alt text", "image text"])
img_formats = [".jpg", ".jpeg", ".png", ".webp"]
df1

df = pd.read_csv("urls.csv")
urls = df["urls"].tolist()
df


for y in urls:
    response = requests.get(y)

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    img_srcs = [img["src"] if img.has_attr("src") else "-" for img in img_tags]
    img_alts = [img["alt"] if img.has_attr("alt") else "-" for img in img_tags]


for count, x in enumerate(img_srcs):
    img_list.append(x)
    urls_list.append(y)


if x != "-":
    if pathlib.Path(x).suffix in img_formats:
        response = requests.get(x)
        img = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        if img_alts[count] != "-":
            alt_text_list.append(img_alts[count])
        else:
            alt_text_list.append("no alt")
        img_text_list.append(text)
    else:
        img_text_list.append("not supported")
        if img_alts[count] != "-":
            alt_text_list.append(img_alts[count])
        else:
            alt_text_list.append("no alt")
else:
    img_text_list.append("no src")
    if img_alts[count] != "-":
        alt_text_list.append(img_alts[count])
    else:
        alt_text_list.append("no alt")


st.write("what's in img_text_list?")
img_text_list

st.write("what's in alt_text_list?")
alt_text_list

df1["url"] = urls_list
df1["img url"] = img_list
df1["alt text"] = alt_text_list
df1["image text"] = img_text_list
df1
