import pandas as pd
import re  # 匯入正規表達式模組
import opencc

# 【替換】設定檔案路徑，請改成你的檔案路徑
file_path = 'C:/Users/user/Desktop/lol_claer/LOL_MS/LOL_MS_Top.csv'

# 讀取 CSV 檔案成 DataFrame
df = pd.read_csv(file_path)


# 建立簡體轉繁體轉換器
converter = opencc.OpenCC('s2t')

# 把欄位名稱做簡轉繁

df.columns = [converter.convert(col) for col in df.columns]
  
# 把英雄名稱欄位裡的簡體字轉成繁體
df['英雄名稱'] = df['英雄名稱'].apply(converter.convert)


# 國服(簡體) -> 台服(繁體) 英雄名稱對照字典範例
cn_to_tw_name_map = {
    '德玛西亚之力': '嘉文四世',
    '正义天使': '凱爾',
    '炼金术士': '煉金術士',
    '狂战士': '沃利貝爾',
    '暮光之眼': '賽勒斯',
    '探险家': '伊澤瑞爾',
    '巨魔之王': '崔斯特',
    '时间刺客': '傑斯',
    '刀锋舞者': '菲歐拉',
    '疾风剑豪': '亞索',
    '放逐之刃': '瑞文',
    '复仇焰魂': '賽恩',
    '正义巨像': '墨爾本',
    '战争女神': '希瓦娜',
    '无极剑圣': '易大師',
    '暗裔剑魔': '亞托克斯',
    '机械公敌': '蘭博',
    '山隐之焰': '烏迪爾',
    '海洋之灾': '菲力歐',
    # ... 請自行補充完整
}


# 用字典做名稱替換
df['英雄名稱'] = df['英雄名稱'].apply(lambda x: cn_to_tw_name_map.get(x, x))


# 定義一個用 regex 處理百分比字串的函式
def percent_to_float_regex(x):
    # 如果是空值或 NaN，直接回傳 None
    if pd.isna(x):
        return None
    # 使用 regex 找出字串中數字和小數點的部分，忽略 % 和空白
    match = re.search(r'(\d+\.?\d*)', x)
    if match:
        # 找到後轉成浮點數並除以 100
        return float(match.group(1)) / 100
    else:
        # 若沒找到數字，回傳 None
        return None

# 用 regex 函式，將勝率、登場率、Ban率轉成浮點數
df['勝率'] = df['勝率'].apply(percent_to_float_regex)
df['登場率'] = df['登場率'].apply(percent_to_float_regex)
df['Ban率'] = df['Ban率'].apply(percent_to_float_regex)

# 檢查是否有重複的英雄名稱，若有會印出重複項
duplicate_heroes = df[df.duplicated(subset=['英雄名稱'], keep=False)]
if not duplicate_heroes.empty:
    print("發現重複英雄名稱：")
    print(duplicate_heroes)
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

# 若要轉換欄位名稱為英文，可用下面程式碼（非必須）
# df.rename(columns={'英雄名稱': 'Champion', '勝率': 'WinRate', '登場率': 'PickRate', 'Ban率': 'BanRate'}, inplace=True)


# 最後印出清理後的前五筆資料確認
print(df)
