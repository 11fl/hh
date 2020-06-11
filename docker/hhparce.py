import requests
from bs4 import BeautifulSoup
import unicodedata
from flask import Flask, Response
import re

app = Flask(__name__)

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
URL3 = f'https://hh.ru/search/vacancy?st=searchVacancy&text=devops&area=1&salary=&currency_code=RUR&only_with_salary=true&experience=doesNotMatter&order_by=publication_time&search_period=1&items_on_page=100&no_magic=true&L_save_area=true'
headers = {'User-Agent': useragent}

def reg(line):
    '''
    very bad regex function
    '''
    r = re.findall(r'\d+', line)
    if len(r) > 2:
        summ = [r[0]+r[1], r[2]+r[3]]
        div = True
    else:
        summ = [r[0] + r[1]]
        div = False
    summint = [int(x) for x in summ]
    return sum(summint)//2 if div else sum(summint)


def walk1() -> str:
    '''
    Get number of jobs for the last 24h with salary showed
    '''
    r = requests.get(URL3, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = soup.find('h1', class_="bloko-header-1").get_text()
    newcount = unicodedata.normalize('NFKD', count)
    fin = newcount.split(' ')[0]
    return f'num_of_jobs_now \t {fin}'

def getSalary() -> str:
    '''
    Getting salary from all positions
    '''
    tl =[]
    i = 0
    j = 0
    r = requests.get(URL3, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = soup.find_all(attrs={"data-qa":"vacancy-serp__vacancy-compensation"})
    for text in count:
        i += 1
        norm = unicodedata.normalize('NFKD', text.text)
        tl.append(norm)
    for payment in tl:
        j += reg(payment) 
    return f'avg_per_day \t {str(j//len(tl))}'

@app.route('/metrics')
def show():
    metrics =f'{walk1()}\n{getSalary()}\n'
    return Response(metrics, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
