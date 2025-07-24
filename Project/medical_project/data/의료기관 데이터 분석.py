# 1. 데이터 수집 및 구조 파악, EDA 기획 정리

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors


medical = pd.read_csv("C:\\Users\\zkdlt\\Documents\\GitHub\\Project\\medical_project\\docs\\전국의료기관표준데이터.csv", encoding='cp949')
# CSV 불러오기

# 올바르게 불러온걸 확인하기 위한 작업

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

# 지역(특별, 광역, 도, 시) 기준으로 병원 영업 상태 비교 도출

# 우선 지역 전처리 (시도 , 시군구)
# 공백을 기준으로 쪼개기
# pandas 메서드 이용
medical['시도'] = medical['소재지전체주소'].str.extract(r'(\w+도|\w+특별시|\w+광역시|\w+자치도|\w+자치시)')
medical['시군구'] = medical['소재지전체주소'].str.extract(r'(\w+구|\w+시|\w+군)')


# 쪼갠 후 첫번째 값은 시도, 두번째는 시군구 할당



# 광역지역 (시도) 영업상태 분석
exclude_sido = ['죽도', '상도']
medical = medical[~medical['시도'].isin(exclude_sido)]

city_med = medical.groupby(['시도', '영업상태명']).size().unstack(fill_value=0)

city_med = city_med.loc[city_med.sum(axis=1).sort_values(ascending=False).index]


city_med.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title("광역지역(시도)별 병원 영업상태 분석")
plt.ylabel("병원 수")
plt.xlabel("시도")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')
plt.show()

# 서울 제외 각 지역군으로 합친 후 분석

province_group = {
    "경기도": ["경기도"],
    "강원도": ["강원특별자치도"],
    "충청도": ["충청북도", "충청남도"],
    "전라도": ["전라북도", "전라남도"],
    "경상도": ["경상북도", "경상남도"]
}

# 반복문을 이용해보자

for group_name, sido in province_group.items():
    # 해당 도 그룹에 해당하는 데이터만 추출
    target = medical[medical['시도'].isin(sido)]
    # 폐업 병원만 필터링 작업
    closed = target[target['영업상태명'] == '폐업']
    # 시군구별 폐업 병원 수 집계
    count_closed = closed['시군구'].value_counts().reset_index()
    count_closed.columns = ['시군구', '폐업병원수']

    #시각화

    plt.figure(figsize=(12, 6))
    sns.barplot(data=count_closed, x='시군구', y='폐업병원수')
    plt.title(f"{group_name} 시군구별 폐업 병원 수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    # 진료과목별 폐업 현황 분석




