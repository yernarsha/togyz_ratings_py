import requests
from bs4 import BeautifulSoup as bs
import csv

def get_html(url):
    r = requests.get(url)
    if r.ok: # 200, not 403, 404
        return r.text
    print(r.status_code)

def process_page(url, save_name):
    html = get_html(url)
    soup = bs(html, 'lxml')
    trs = soup.find('table', class_='MsoNormalTable').find_all('tr')
    
    for tr in trs:
        line = ''
        tds = tr.find_all('td')
        
        i = 0
        for td in tds:
            line += td.text.strip()
            i += 1
        if i > 6:
            print(line)

        data = {'num': tds[0].text.strip(),
                'name': tds[1].text.strip(),
                'region': tds[2].text.strip(),
                'title': tds[3].text.strip(),
                'before': tds[4].text.strip(),
                'diff': tds[5].text.strip(),
                'after': tds[6].text.strip()}
        export_to_csv(data, save_name)

def export_to_csv(data, save_name):
    with open(save_name, 'a') as file:
        writer = csv.writer(file)
        if data['diff'] == '':
            data['diff'] = '0'
        writer.writerow((data['num'], data['name'], data['region'], data['title'], data['before'], data['diff'], data['after']))

url_men = 'http://9kumalak.com/index.php/2012-04-10-18-56-53/reiting-uldar/624-rejting-ldar-01-01-2023-t-zetulermen'
url_women = 'http://9kumalak.com/index.php/2012-04-10-18-56-53/yzdar/626-rejting-yzdar-01-01-2023-t-zetulermen'

def main():
    process_page(url_men, 'men.csv')
    process_page(url_women, 'women.csv')
    print('Done!')

if __name__ == '__main__':
    main()
