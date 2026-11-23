import pandas as pd

file_path = "역할1_2022_Baseline_실험결과.xlsx"

# 엑셀 시트 확인
excel = pd.ExcelFile(file_path)

print("===== 전체 시트 목록 =====")
print(excel.sheet_names)

# 주요 데이터 시트 확인
sheets = [
    "2022 지역별 발생량",
    "연도별 처리방식",
    "온실가스 배출량",
    "인프라"
]

for sheet in sheets:
    print("\n==========================")
    print("시트 이름:", sheet)

    df = pd.read_excel(file_path, sheet_name=sheet)

    print("데이터 크기:", df.shape)
    print("열 이름:", df.columns.tolist())
    print("\n데이터 미리보기:")
    print(df.head(5).to_string(index=False))