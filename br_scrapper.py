import pandas as pd
from bs4 import BeautifulSoup
import urllib
import re
from calendar import month_abbr

def br_scrapper(player, year):
    url = "https://www.baseball-reference.com/players/gl.fcgi?id={}&t=b&year={}".format(player, year)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    
    header = soup.find('table', id="batting_gamelogs").find('thead').find('tr').text.split('\n')
    #header = soup.find('table', id="batting_gamelogs").find('tr').text.split('\n')
    header = header[2:-1] # drop first and last item
    header = ['team_homeORaway' if x=='' else x for x in header]
    
    table = soup.find('table', id="batting_gamelogs")
    table_rows = table.find('tbody').find_all('tr', id=re.compile("batting_gamelogs.\d{4}"))
    #table_rows
    
    data = []
    for row in table_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    player_name = soup.find('div', itemtype='https://schema.org/Person').find('h1').text
    bats = soup.find('div', itemtype = 'https://schema.org/Person').text.split('\n')[8].split(':')[1].strip()
    
    data = pd.DataFrame(data=data, columns = header)
    
    data['Yr'] = year
    data['Player'] = player_name
    data['Bats'] = bats
    data['Month'] = data['Date'].str.split(" ").str[0]
    data['Day'] = data['Date'].str.split(" ").str[1]
    
    month_dict = dict((v,k) for k,v in enumerate(month_abbr))
    
    mth = []
    for i in data['Month']:
        mth.append(month_dict[i])
    
    data['Month'] = mth
    data['Day'] = data['Day'].astype(str).astype(int)
    
    data['dt'] = pd.to_datetime(data['Yr']*10000+data['Month']*100+data['Day'], format = '%Y%m%d')
    
    data = data.drop(["Yr", "Month", "Day"], axis=1)
    
    data = data.set_index('dt')
    
    return(data)
