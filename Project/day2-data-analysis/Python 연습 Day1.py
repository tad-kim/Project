import pandas as pd

# CSV 불러오기
df = pd.read_csv("https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv")
df.columns = df.columns.str.strip().str.replace('"', '')
# 데이터 프레임 확인
data = pd.DataFrame(df)
print(data.head())

# 컬럼이름 확인
print(data.columns)

# 기본통계 요약
print(data.describe())
# 행/열 개수 확인
print(data.shape)
# 데이터 타입 확인
print(data.dtypes)

#키가 70인치 이상인 사람들만 골라서 출력
tall_people = data[data['Height(Inches)'] >= 70]
print(tall_people)
# 몸무게가 높은 순서대로 정렬 TOP 5개 출력
sorted_wight = data.sort_values(by='Weight(Pounds)', ascending=False)
print(sorted_wight.head())
# 몸무게 기준으로 3개 구간으로 나눠서 평균 키 보기
print(data.groupby(pd.cut(data['Weight(Pounds)'], bins=3))['Height(Inches)'].mean())

print(data)
# 키가 70인치 이면서 몸무게가 130파운드 이상인 사람만 추려서 출력
big_people = data[(data['Height(Inches)'] >= 70) & (data['Weight(Pounds)'] >= 130)]
print(big_people)

# 가장 키가 큰사람 5명의 몸무게를 출력해봐
big_tall_people = data.sort_values(by='Height(Inches)', ascending=False).head(5)
print(big_tall_people[['Height(Inches)', 'Weight(Pounds)']])

# 몸무게를 4구간으로 나눠서 키의 평균과 개수를 각각 출력
weight_bins = pd.cut(data['Weight(Pounds)'], bins=4)
tall_weight_group = data.groupby(weight_bins)['Height(Inches)'].agg(['mean', 'count'])
print(tall_weight_group)
