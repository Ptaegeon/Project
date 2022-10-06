import matplotlib.pyplot as plt
import lxml
import requests
import pandas as pd
import html5lib
import os


def get_stock_code():
    # 종목코드 다운로드
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

    # 필요없는 column들은 제외
    stock_code = stock_code[['회사명', '종목코드']]

    # 한글 컬럼명을 영어로 변경
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    stock_code.code = stock_code.code.map('{:06d}'.format)

    return stock_code


def get_stock(code):
    df = pd.DataFrame()
    for page in range(1, 21):
        url = f'https://finance.naver.com/item/sise_day.naver?code={code}'
        url = f'{url}&page={page}'

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

        res = requests.get(url, headers=header)
        current_df = pd.read_html(res.text, header=0)[0]
        df = df.append(current_df, ignore_index=True)
    return df


def clean_data(df):
    df = df.dropna()
    df = df.rename(
        columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[
        ['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'], ascending=True)

    return df


company = '삼성전자'

stock_code = get_stock_code()
code = stock_code[stock_code.company == company].code.values[0].strip()
df = get_stock(code)
df = clean_data(df)
print(df)

plt.figure(figsize=(10, 4))
plt.plot(df['date'], df['close'])
plt.xlabel('date')
plt.ylabel('close')

chart_fname = os.path.join("res/stock_report", '{company}_chart.png'.format(company=company))
plt.savefig(chart_fname)
plt.show()

plt.figure(figsize=(15, 4))
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
df = df.sort_values(by=['date'], ascending=False)
pd.plotting.table(ax, df.head(10), loc='center', cellLoc='center', rowLoc='center')

table_fname = os.path.join("res/stock_report", '{company}_table.png'.format(company=company))
plt.savefig(table_fname)
