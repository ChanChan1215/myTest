import pandas as pd
import re  # 匯入正規表達式模組
import pymysql  # 匯入 pymysql
from pathlib import Path

# 讀取 CSV 檔案成 DataFrame
file_path = r'D:\lol_project\LOL_PROJECT\LOL_MS_Top.csv'  # 替換為您自己的檔案路徑
df = pd.read_csv(file_path)

# 國服(簡體) -> 台服(繁體) 英雄名稱對照字典
cn_to_tw_name_map = {
    '德玛西亚之力': '蓋倫',
    '正义天使': '凱爾',
    '齐天大圣': '悟空',
    '暮光之眼': '慎',
    '炼金术士': '辛吉德',
    '暗夜猎手': '汎',
    '狂战士': '歐拉夫',
    '迅捷斥候': '提摩',
    '狂暴之心': '凱能',
    '迷失之牙': '吶兒',
    '暗裔剑魔': '厄薩斯',
    '武器大师': '賈克斯',
    '祖安狂人': '蒙多醫生',
    '青钢影': '卡蜜兒',
    '腕豪': '賽特',
    '圣锤之毅': '波比',
    '符文法师': '雷茲',
    '刀锋舞者': '伊瑞莉雅',
    '无双剑姬': '菲歐拉',
    '蛮族之王': '泰達米爾',
    '铁铠冥魂': ' 魔鬥凱薩',
    '荒漠屠夫': '雷尼克頓 ',
    '无畏战车': '烏爾加特',
    '亡灵战神': '賽恩',
    '沙漠死神': '納瑟斯',
    '诺克萨斯之手': '達瑞斯',
    '深海泰坦': '納帝魯斯',
    '德玛西亚皇子': '嘉文四世',
    '熔岩巨兽': '墨菲特',
    '未来守护者': '杰西',
    '疾风剑豪': '犽宿',
    '猩红收割者': '弗拉迪米爾 ',
    '放逐之刃': '雷玟',
}

# 去除空白字符並確保大小寫一致性
df['英雄名稱'] = df['英雄名稱'].str.strip()  # 去除前後空格
df['英雄名稱'] = df['英雄名稱'].apply(lambda x: cn_to_tw_name_map.get(x.strip(), x.strip()))

# 定義一個用 regex 處理百分比字串的函式
def percent_to_float_regex(x):
    if pd.isna(x):
        return None
    match = re.search(r'(\d+\.?\d*)', x)
    if match:
        return float(match.group(1)) / 100
    else:
        return None

df['勝率'] = df['勝率'].apply(percent_to_float_regex)
df['登場率'] = df['登場率'].apply(percent_to_float_regex)
df['Ban率'] = df['Ban率'].apply(percent_to_float_regex)

# 檢查是否有重複的英雄名稱，若有會印出重複項
duplicate_heroes = df[df.duplicated(subset=['英雄名稱'], keep=False)]
if not duplicate_heroes.empty:
    print("發現重複英雄名稱：")
    print(duplicate_heroes)
    df = df.drop_duplicates(subset=['英雄名稱'], keep='first')
else:
    print("沒有發現重複的英雄名稱")

# 檢查勝率、登場率、Ban率是否有超出合理範圍（0~1之外）的數值
for col in ['勝率', '登場率', 'Ban率']:
    invalid_values = df[(df[col] < 0) | (df[col] > 1)]
    if not invalid_values.empty:
        print(f"在欄位 {col} 中發現異常數值：")
        print(invalid_values[['英雄名稱', col]])
    else:
        print(f"欄位 {col} 中沒有異常數值")

# 確認清理後的資料行數
print(f"清理後資料行數：{len(df)}")

# 匯入 MySQL 資料庫
# 資料庫連接資訊 - 以下參數需要根據您的實際資料庫進行替換：
db_config = {
    'host': '127.0.0.1',  # 替換為您的 MySQL 伺服器 IP 或域名
    'user': 'user',        # 替換為您的 MySQL 使用者名稱
    'password': 'password',  # 替換為您的 MySQL 密碼
    'database': 'lol_DB',  # 替換為您的資料庫名稱
    'port': 3307,  # 替換為您的 MySQL 端口（預設為 3306）
    'charset': 'utf8mb4',    # 確保支援中文
}

# 連接到資料庫
connection = pymysql.connect(**db_config)
cursor = connection.cursor()


# 放在 connection、cursor 建立之後、插入前
create_table_sql = """
CREATE TABLE IF NOT EXISTS LOL_MS_Top (
  英雄名稱 VARCHAR(100)   NOT NULL,
  勝率     DECIMAL(5,2)   NULL,
  登場率   DECIMAL(5,2)   NULL,
  Ban率    DECIMAL(5,2)   NULL,
  PRIMARY KEY (英雄名稱)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


insert_query = """
INSERT INTO LOL_MS_Top (英雄名稱, 勝率, 登場率, Ban率)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
  勝率   = VALUES(勝率),
  登場率 = VALUES(登場率),
  Ban率  = VALUES(Ban率);
"""

# 利用 Python 的 context manager (with 句) 來妥善管理資源
with pymysql.connect(**db_config) as connection:
    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)  # 保證表存在
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row['英雄名稱'],
                row['勝率'],
                row['登場率'],
                row['Ban率'],
            ))
        connection.commit()


# 儲存清理後的資料為 CSV
write_dir = Path("LOL_PROJECT")
write_dir.mkdir(exist_ok=True)
df.to_csv(write_dir/"LOL_MS_Top_clean.csv", header=True, index=False)