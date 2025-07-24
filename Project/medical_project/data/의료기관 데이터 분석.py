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
medical_df = medical[~medical['시도'].isin(exclude_sido)]

city_med = medical_df.groupby(['시도', '영업상태명']).size().unstack(fill_value=0)

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

# 폐업 병원 추출

colsed = medical[medical['영업상태명'] == '폐업']

# 진료과목 분해

# ','로 나누고 행마다 나열하기 위한 작업
closed_sub = closed['진료과목내용명'].dropna().str.split(',').explode()

# 공백 제거
closed_sub = closed_sub.str.strip()

# 진료 과목 집계
sub_count = closed_sub.value_counts()

# 진료과목별 TOP 15 그래프 도출

top_medical = sub_count.head(15)

top_medical.plot(kind='barh', figsize=(12, 6))
plt.title("폐업 병원 진료과목 TOP 15 (부수과목 포함)")
plt.xlabel("폐업된 병원 수")
plt.ylabel("진료과목")
plt.tight_layout()
plt.grid(axis='y')
plt.show()

# 특정 진료과목 지역별 공백 분석
#  정상 영업 병원 필터링

opened = medical[medical['영업상태명'] == '영업/정상']

sanbu_open = opened[opened['진료과목내용명'].str.contains('산부인과', na=False)]
# 산부인과 병원 수 확인
region_sanbu = sanbu_open.groupby(['시도', '시군구']).size().reset_index(name='산부인과수')

# 진료과목 분해 및 pivot 생성

open_sub = opened[['시도', '시군구', '진료과목내용명']].dropna()
open_sub = open_sub.assign(진료과목=open_sub['진료과목내용명'].str.split(',')).explode('진료과목')
open_sub['진료과목'] = open_sub['진료과목'].str.strip()

# .assign(). explode() 는 콤마로 합쳐진 진료과목을 하나하나의 행으로 풀어주는역할

province_groups = {
    "경기도": ["경기도"],
    "강원도": ["강원특별자치도"],
    "충청도": ["충청북도", "충청남도"],
    "전라도": ["전라북도", "전라남도"],
    "경상도": ["경상북도", "경상남도"]
}


# 산부인과 병원 수 집계 (시도+시군구)
sanbu_counts = open_sub[open_sub['진료과목'] == '산부인과'].groupby(['시도', '시군구']).size().reset_index(name='산부인과수')

# 시각화용 인덱스 추가
sanbu_counts['지역'] = sanbu_counts['시도'] + ' ' + sanbu_counts['시군구']
sanbu_counts = sanbu_counts.set_index('지역')

# 지역별 산부인과 병원 수 히트맵 (권역별로 나누기)
for g_name, sido_list in province_groups.items():
    # 해당 권역에 포함된 데이터만 필터링
    region_df = sanbu_counts[sanbu_counts.index.str.contains('|'.join(sido_list))]

    if not region_df.empty:
        plt.figure(figsize=(6, len(region_df) * 0.4 + 2))
        sns.heatmap(region_df[['산부인과수']], cmap='Reds', annot=True, fmt=".0f", linewidths=0.5, linecolor='gray')
        plt.title(f"{g_name} 산부인과 병원 수 (시도+시군구 기준)")
        plt.xlabel("산부인과")
        plt.ylabel("지역")
        plt.tight_layout()
        plt.show()


