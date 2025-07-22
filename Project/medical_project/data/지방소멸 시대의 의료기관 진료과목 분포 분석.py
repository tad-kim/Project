# 1. 데이터 수집 및 구조 파악, EDA 기획 정리

import pandas as pd
import numpy as np
import matplotlib as plt


health = pd.read_csv("C:\\Users\\zkdlt\\Documents\\GitHub\\Project\\medical_project\\docs\\보건복지부_전국 지역보건의료기관 현황_20191231.csv", encoding='cp949')
medical = pd.read_csv("C:\\Users\\zkdlt\\Documents\\GitHub\\Project\\medical_project\\docs\\전국의료기관표준데이터.csv", encoding='cp949')
# CSV 불러오기

# 올바르게 불러온걸 확인하기 위한 작업

#print(health)
print(medical.columns)

# 병원 데이터의 주소 컬럼 기준으로 시도/시군구 분리
# 각 지역으로 나누기 위한 작업

# 주소에서 시도 추출 (예: 서울특별시, 경기도, 부산광역시 등)
medical['시도'] = medical['소재지전체주소'].str.extract(r'(\w+도|\w+시|\w+특별시|\w+광역시)')

# 주소에서 시군구 추출 (예: 강남구, 수원시, 고흥군 등)
medical['시군구'] = medical['소재지전체주소'].str.extract(r'\w+(?:도|시|특별시|광역시)\s+(\w+구|\w+시|\w+군)')

# 주소 분류 확인
print(medical[['소재지전체주소', '시도', '시군구']])
