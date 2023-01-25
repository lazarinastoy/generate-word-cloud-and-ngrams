import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache
def process_data(file, n):
    df = pd.read_excel(file)
    text = ' '.join(df.column.tolist())
    ngrams = []
    for i in range(len(text)-n+1):
        ngrams.append(text[i:i+n])
    return ngrams

def main():
    st.set_page_config(page_title="NGram Generator", page_icon=":guardsman:", layout="wide")
    st.title("NGram Generator")

    file = st.file_uploader("Upload your excel file", type=["xlsx"])
    if not file:
        st.error("Please upload a file.")
        return

    n = st.selectbox("Select N for N-grams", [2,3,4])

    if st.button("Generate"):
        ngrams = process_data(file, n)
        wordcloud = WordCloud().generate_from_frequencies(ngrams)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()
        if st.checkbox("Want to export the ngrams?"):
            st.write("Exported the ngrams to a spreadsheet.")
            export_file = st.file_uploader("Upload the excel file you want to export to", type=["xlsx"])
            if export_file:
                export_df = pd.DataFrame(ngrams,columns=['N-grams'])
                export_df.to_excel(export_file, index=False)

if __name__=='__main__':
    main()
