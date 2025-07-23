# 1. 데이터 수집 및 구조 파악, EDA 기획 정리

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors



health = pd.read_csv("C:\\Users\\zkdlt\\Documents\\GitHub\\Project\\medical_project\\docs\\보건복지부_전국 지역보건의료기관 현황_20191231.csv", encoding='cp949')
medical = pd.read_csv("C:\\Users\\zkdlt\\Documents\\GitHub\\Project\\medical_project\\docs\\전국의료기관표준데이터.csv", encoding='cp949')
# CSV 불러오기

# 올바르게 불러온걸 확인하기 위한 작업

#print(health)
print(medical.columns)

# 미션 1. 전국 병원의 영업상태(정상/폐업/휴업) 분포를 분석 도출

# 우선 영업상태명 컬럼으로 정상,폐업,휴업 등 영업상태를 확인
medical_ = medical['영업상태명'].value_counts(normalize=True)

medical_df = medical_ * 100
print(medical_df)

plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(12, 6))
medical_df.plot(kind='pie', autopct='%.1f%%', startangle=90)
plt.title("전국 의료기관 영업상태")
plt.ylabel("") # 원형 그래프에선 y축 라벨 필요없음
plt.tight_layout()
plt.show()


