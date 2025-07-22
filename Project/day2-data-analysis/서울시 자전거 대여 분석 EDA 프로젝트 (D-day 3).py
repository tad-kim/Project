# 서울시 자전거 대여 분석 EDA 프로젝트 (D-day 3)


from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 불러오기

data = pd.read_csv("C:\\Users\\zkdlt\\Desktop\\프로젝트 과제\\서울특별시 공공자전거 대여이력 정보_2412.csv", encoding='cp949')
print(data.head())
# 컬럼명 확인하기
print(data.columns)

df = pd.DataFrame(data)
df.columns = df.columns.str.strip()

# 날짜 데이터 처리


df['대여일시'] = pd.to_datetime(df['대여일시'])
df['요일'] = df['대여일시'].dt.weekday
df['시간'] = df['대여일시'].dt.hour
df['날짜'] = df['대여일시'].dt.date
print(df.head())

# 대여소 위치별 분석
top_df = df.groupby('대여 대여소명').size().sort_values(ascending=False).head(10)
print(top_df)
#한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
# 그래프 그리기
plt.figure(figsize=(12, 6))
sns.barplot(x=top_df.index, y=top_df.values, palette='viridis')
plt.title('Top 10 대여 대여소명')
plt.xlabel('대여 대여소명')
plt.ylabel('대여 횟수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

