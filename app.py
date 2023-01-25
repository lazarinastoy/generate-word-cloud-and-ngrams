import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache
def process_data(file, n):
    df = pd.read_excel(file, converters={'column': str})
    df['column'].fillna('', inplace=True)
    text = ' '.join(df.column.tolist())
    ngrams = []
    for i in range(len(text)-n+1):
        ngrams.append(text[i:i+n])
    return ngrams, df

def main():
    st.set_page_config(page_title="NGram Generator", page_icon=":guardsman:", layout="wide")
    st.title("NGram Generator")

    file = st.file_uploader("Upload your excel file", type=["xlsx"])
    if not file:
        st.error("Please upload a file.")
        return

    n = st.selectbox("Select N for N-grams", [2,3,4])

    if st.button("Generate"):
        ngrams, df = process_data(file, n)
        ngrams_series = pd.Series(ngrams)
        ngrams_dict = ngrams_series.value_counts().to_dict()
        wordcloud = WordCloud().generate_from_frequencies(ngrams_dict)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()
        st.write("Exported the ngrams to a spreadsheet.")
        # Automatic download of processed spreadsheet
        st.markdown('### Download the processed spreadsheet')
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download processed spreadsheet</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__=='__main__':
    main()
