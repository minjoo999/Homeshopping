import numpy as np
import pandas as pd
import collections
import plotly.express as px

# 엑셀파일 입력받기 -> df 만들기 -> 시간이 가로, 날짜가 세로로 바꾸기
fileno = int(input("넣을 파일의 수를 쓰시오: " ))
files = []
for i in range(fileno):
    hsf = input("파일의 경로를 넣으세요: " )
    hs = pd.read_excel(hsf)
    hs = hs.set_index('시간대').transpose()
    # hs = hs.reset_index()
    # hs.rename(columns={'index':'날짜'}, inplace=True)
    files.append(hs)

# print(files)

# 입력받은 엑셀파일들을 다 합쳐서 df 1개로 만들기 & csv 파일 저장 (날짜 보존!)
df = pd.concat(files)
df = df.reset_index()
df.rename(columns={'index':'날짜'}, inplace=True)
# print(df)

while True:
    ans = input("CSV 파일을 만드시겠습니까? Y or N ")
    if ans == 'Y' or ans == 'y':
        df_path = input("파일명을 .csv 형태로 입력해주세요: ")
        df.to_csv(df_path, sep=',')
        print("완료되었습니다")
        break
    elif ans == 'N' or ans == 'n':
        break
    else:
        continue


# 문자열 가공 (날짜 지우는 옵션)
df.drop(['날짜'], axis=1, inplace=True)
text_df = df.to_string(header=False, index=False)
text_df = text_df.strip()
text_df1 = text_df.split('\\n')
# print(text_df1)

# 가공된 문자열 리스트 뽑기
text_final = []
for text in text_df1:
    hs = text.split()
    for i in hs:
        if hs.index(i) % 2 == 1:
            text_final.append(i)

# print(text_final)

# 리스트를 방송국과 성분으로 분리하기
vendor = []
medicine = []
for text in text_final:
    a = text.replace('(', ' ').replace(')', '')
    hs = a.split(' ')
    for i in hs:
        if hs.index(i) == 0:
            medicine.append(i)
        else:
            vendor.append(i)

# print(vendor)
# print(medicine)



# 결과 분석 뽑기
medicine_words = {}
vendor_words = {}

medicine_words = collections.Counter(medicine).most_common()
vendor_words = collections.Counter(vendor).most_common()

# print(medicine_words)

# dictionary -> dataframe -> 시각화
# 결과 분석 시각화
# 튜플 왼쪽과 오른쪽을 별개의 컬럼으로 매긴 df -> 얘를 plotly 막대그래프로 뽑기
medicine_df = pd.DataFrame(medicine_words, columns=['성분', '횟수'])
vendor_df = pd.DataFrame(vendor_words, columns=['방송국', '횟수'])

# print(medicine_df)
# print(vendor_df)

while True:
    qna = input("성분과 방송국 중 보고 싶은 것을 골라주세요: ")
    if qna == "성분":
        med_fig_name = input("그래프 제목을 적어주세요: ")
        med_fig = px.bar(medicine_df, x='성분', y='횟수', title=med_fig_name)
        med_fig.show()
        break
    elif qna == "방송국":
        vend_fig_name = input("그래프 제목을 적어주세요: ")
        vend_fig = px.bar(vendor_df, x='방송국', y='횟수', title=vend_fig_name)
        vend_fig.show()
        break
    else:
        continue
