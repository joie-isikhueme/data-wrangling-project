import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

wikiurl = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
response= requests.get(wikiurl)
print(response.status_code)
soup= BeautifulSoup(response.text,'html.parser')
wikiTable=soup.find('table',{'class':"wikitable sortable"})

df=pd.read_html(str(wikiTable))
df=pd.DataFrame(df[0])
df.columns=[
            'Country','Area', 'Population', 'GDP per Capita','Population Density', 
            'Vehicle Ownership', 'Road Network Length', 'Total Road Deaths', 
            'Road deaths per Million', 'Number of People Killed per Billion', 
            'Number of Seriously Injured'
            ]
df.drop(['Number of People Killed per Billion',
        'Number of Seriously Injured','Road Network Length'],axis=1, 
        inplace=True)

df['Year']="2018"

df['GDP per Capita']=df['GDP per Capita'].str.replace(r'[^\d]+','')


df= df.sort_values("Road deaths per Million")
df.to_csv('Cleaned_European_Union_Safety_Facts_and_Figures.csv')

highestdeath=df.nlargest(10,['Total Road Deaths'])
mylabels= highestdeath['Country']
myexplode =[0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
highestdeath.groupby(['Country']).sum().plot(kind = 'pie',y= 'Total Road Deaths',
                                            autopct = '%1.0f%%',labels=mylabels,
                                            startangle=90,explode=myexplode,
                                            radius = 1.2,frame=False,
                                            shadow=True)


# highestdeath.plot(kind = 'pie',y= 'Total Road Deaths',autopct = '%1.0f%%',labels=mylabels,startangle=90,explode=myexplode,)
plt.legend(title= "Countries:",loc=2, prop={'size':6,},bbox_to_anchor =(-0.38,0.6,0,0.5),borderpad=2)
plt.ylabel("")
plt.title("Top 10 Countries With Highest Road Deaths(2018)",x=0.4,y=1.1)
plt.show()
mylabels
highestdeath
plt.scatter('Total Road Deaths','Population in thousands',data=highestdeath)