import streamlit as st
import pandas as pd 
import re 
import streamlit.components.v1 as components

pkl_file_path = "Formosan-Mandarin_sent_pairs_139023entries.pkl"

def read_pickle_file(file_path):
  try:
    df = pd.read_pickle(file_path)
    return df 
  except Exception as e:
    st.error(f"Error reading .pkl file: {e}")
    return None

def main():
  st.title("臺灣南島語-華語句庫資料集")
  st.subheader("Dataset of Formosan-Mandarin sentence pairs")
  st.markdown(
        """
### 資料概要 Data Overview
- 🎢 資料集合計約13萬筆台灣南島語-華語句對
- ⚠️ 此查詢系統僅供教學與研究之用，內容版權歸原始資料提供者所有

### 資料來源 Data Sources
- 以下資料經由網路爬蟲取得。
   + 🥅 九階教材: [族語E樂園](http://web.klokah.tw)
   + 💬 生活會話: [族語E樂園](http://web.klokah.tw)
   + 🧗 句型: [族語E樂園](http://web.klokah.tw)
   + 🔭 文法: [臺灣南島語言叢書](https://alilin.apc.gov.tw/tw/)
- 詞典資料使用`PDFMiner` 將2019版的PDF檔轉成HTML，再用`BeautifulSoup`抓取句對，偶爾會出現族語跟華語對不上的情形。若發現錯誤，請[聯絡我📩](https://howard-haowen.rohan.tw/)。詞典中重複出現的句子已從資料集中刪除。
   + 📚 [原住民族語言線上詞典](https://e-dictionary.apc.gov.tw/Index.htm?fbclid=IwAR18XBJPj2xs7nhpPlIUZ-P3joQRGXx22rbVcUvp14ysQu6SdrWYvo7gWCc)
- 其他辭典資料來源:
   + 📚 [阿美族語辭典 Facidol Dict](https://lab.mirusausiliq.com/facidol-dict/)
   + 📚 [阿美族語辭典 Facidol Project](https://lab.mirusausiliq.com/facidolproject/)


### 查詢方法 How to Use
- 🔭 過濾：使用左側欄功能選單可過濾資料來源(可多選)與語言，也可使用華語或族語進行關鍵詞查詢。
  - 🔍 關鍵詞查詢支援[正則表達式](https://zh.wikipedia.org/zh-tw/正则表达式)。
  - 🥳 族語範例: 
    + 使用`cia *`查詢布農語，能找到包含`danumcia`、`luduncia`或`siulcia`等詞的句子。
    + 使用`[a-z]{15,}`查詢任何族語，能找到包含15個字母以上單詞的句子，方便過濾長詞。
  - 🤩 華語範例: 
    + 使用`^有一`查詢華語，能找到使用`有一天`、`有一塊`或`有一晚`等詞出現在句首的句子。
    + 使用`[0-9]{1,}`查詢華語，能找到包含羅馬數字的句子，如`我今年16歲了`。
- 📚 排序：點選標題列。例如點選`族語`欄位標題列內的任何地方，資料集便會根據族語重新排序。
- 💬 更多：文字長度超過欄寬時，將滑鼠滑到欄位上方即可顯示完整文字。
- 🥅 放大：點選表格右上角↘️進入全螢幕模式，再次點選↘️返回主頁。
        """
  )

  df = read_pickle_file(pkl_file_path)

  zh_columns = {
    "Lang_En": "Language",
    "Lang_Ch": "語言_方言",
    "Ab": "族語",
    "Ch": "華語",
    "From": "來源",
  }
  df.rename(columns=zh_columns, inplace=True)
  source_set = df['來源'].unique()
  sources = st.sidebar.multiselect(
    "請選擇資料來源",
    options=source_set,
    default='詞典',
  )
  langs = st.sidebar.selectbox(
    "請選擇語言",
    options=[
      '阿美', '泰雅', '布農', '卡那卡那富', '噶瑪蘭',
      '排灣', '魯凱', '撒奇萊雅', '賽夏', '賽德克',
      '邵', '卑南', '鄒', '達悟', '太魯閣',
      '達悟'
    ],
  )
  texts = st.sidebar.radio(
    "請選擇關鍵詞查詢文字類別",
    options=['華語', '族語'],
  )

  s_filt = df['來源'].isin(sources)

  # select a language 
  if langs == "噶瑪蘭":
    l_filt = df['Language'] == "Kavalan"
  elif langs == "阿美":
    l_filt = df['Language'] == "Amis"
  elif langs == "撒奇萊雅":
    l_filt = df['Language'] == "Sakizaya"
  elif langs == "魯凱":
    l_filt = df['Language'] == "Rukai"
  elif langs == "排灣":
    l_filt = df['Language'] == "Paiwan"
  elif langs == "卑南":
    l_filt = df['Language'] == "Puyuma"
  elif langs == "賽德克":
    l_filt = df['Language'] == "Seediq"
  elif langs == "邵":
    l_filt = df['Language'] == "Thao"
  elif langs == "拉阿魯哇":
    l_filt = df['Language'] == "Saaroa"
  elif langs == "達悟":
    l_filt = df['Language'] == "Yami"
  elif langs == "泰雅":
    l_filt = df['Language'] == "Atayal"
  elif langs == "太魯閣":
    l_filt = df['Language'] == "Truku"
  elif langs == "鄒":
    l_filt = df['Language'] == "Tsou"
  elif langs == "卡那卡那富":
    l_filt = df['Language'] == "Kanakanavu"
  elif langs == "賽夏":
    l_filt = df['Language'] == "Saisiyat"
  elif langs == "布農":
    l_filt = df['Language'] == "Bunun"

  text_box = st.sidebar.text_input('在下方輸入華語或族語，按下ENTER後便會自動更新查詢結果')

  t_filt = df[texts].str.contains(text_box, flags=re.IGNORECASE)

  filt_df = df[(s_filt) & (l_filt) & (t_filt)]

  st.markdown(
    """
### 查詢結果 Result
    """
  )

  st.dataframe(filt_df, 800, 400)

  st.markdown(
    """
### 版權聲明 License
- 這個 repo 中的程式碼是基於並修改自 [howard-haowen/Formosan-languages](https://github.com/howard-haowen/Formosan-languages/) 原始碼，由 [howard-haowen](https://github.com/howard-haowen/) 所創建，對於原作者的貢獻表示感謝。
- 因原網站程式許久未更新，導致錯誤發生，原 repo 中的程式碼已無法正常運作，因此我將其修改為可正常運作的版本。 
- The code in this repository is based on and modified from the original source available on [howard-haowen/Formosan-languages](https://github.com/howard-haowen/Formosan-languages/). The original code is the work of [howard-haowen](https://github.com/howard-haowen/), and I would like to express my appreciation for their contributions.
- Due to the prolonged lack of updates to the original website's code, errors have occurred, rendering the code in the original repository unable to function properly. Therefore, I have modified it to a version that functions correctly.
- 2023-2024 Create by [Mirusa Usiliq](https://github.com/mirusausiliq/) & [Repo](https://github.com/mirusausiliq/Formosan-languages-new/)
    """
  )


if __name__ == "__main__":
    main()

