import pandas as pd
import re  # 匯入正規表達式模組
# import opencc

# 【替換】設定檔案路徑，請改成你的檔案路徑
file_path = r'C:\Users\user\Desktop\lol_claer\LOL_APEX\LOL_APEX_Sup.csv'

# 讀取 CSV 檔案成 DataFrame
df = pd.read_csv(file_path)

# 確認原始資料的行數
print(f"原始資料行數：{len(df)}")

# # 建立簡體轉繁體轉換器
# converter = opencc.OpenCC('s2t')

# # 把欄位名稱做簡轉繁
# df.columns = [converter.convert(col) for col in df.columns]

# # 把英雄名稱欄位裡的簡體字轉成繁體
# df['英雄名稱'] = df['英雄名稱'].apply(converter.convert)

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
    "灵罗娃娃":"關",
    "山隐之焰":"鄂爾",
    "机械公敌":"藍寶",
    "不灭狂雷":"弗力貝爾",
    "封魔剑魂":"犽凝",
    "星籁歌姬":"瑟菈芬",
    "蒸汽机器人":"布里茲",
    "荆棘之兴":"枷蘿",
    " 扭曲树精":"茂凱",
    "天启者":"卡瑪",
    "琴瑟仙女":"索娜",
    "众星之子":"索拉卡",
    "光辉女郎":"拉克絲",
    "明烛":"米里歐",
    "邪恶小法师":"維迦",
    "堕落天使":"魔甘娜",
    "唤潮鲛姬":"娜米",
    "风暴之怒":"珍娜",
    "血港鬼影":"派克",
    "复仇焰魂":"布蘭德",
    "诺克萨斯统领":"諾克薩斯",
    "牛头酋长":"亞歷斯塔",
    "弗雷尔卓德之心":"弗雷爾卓德",
    "曙光女神":"蕾歐娜",
    "幻翎":"幻翎洛",
    "仙灵女巫":"璐璐",
    "正义巨像":"加里奥",
    "涤魂圣枪":"赛娜",
    "魔法猫咪":"悠咪",
    "魂锁典狱长":"瑟雷西",
    "扭曲树精":"茂凱"   
}

# 去除空白字符並確保大小寫一致性
df['英雄名稱'] = df['英雄名稱'].str.strip()  # 去除前後空格
# 用字典做名稱替換，若對照字典中找不到則保留原名稱
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
    # 刪除重複的英雄名稱，只保留第一個
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

# 最後印出清理後的資料
print(df)