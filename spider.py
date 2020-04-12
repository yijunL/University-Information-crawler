import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import time
 
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
        
    except:
        return ""

def findInfo(url):
    html=getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    bg_sez=soup.find("div",class_="bg_sez")
    if(bg_sez==None):
        return None,None
    h2=bg_sez.find("h2")
    if(h2==None):
        return None,None
    name=str(h2.contents[0]).strip()
    # infos["School"].append()    #获取校名

    lc=soup.find("ul",class_="left contact")
    if(lc==None):
        return None,None

    p=lc.find("p")
    if(p==None):
        return None,None
    loc=str(p.contents[0]).strip()
    loc=loc[loc.find("：")+1:]            #获取地址
    # infos["Location"].append(loc)
    return name,loc

def findStu(url):
    html=getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    jj=soup.find("div",class_="jj")
    if(jj==None):
        return None
    ps=jj("p")
    stu=""
    for p in ps:
        if(p.string):
            stu=str(p.string).strip()
            # stus["Student"].append(p.string)
            # print(p.string)
    if(stu==""):
        return "没有搜索到准确的在校生信息"
    return stu
     
def main():
    infoUrls=[]
    stuUrls=[]
    infos={"School":[],"Location":[],"Student":[]}
    url1 = 'http://college.gaokao.com/school/'
    url2= "http://college.gaokao.com/school/tinfo/"
    for i in range(1,2666):
        infoUrls.append(url1+str(i)+"/")
    for i in range(1,2666):
        stuUrls.append(url2+str(i)+"/zaixiao/")
    i=0

    

    for url1,url2 in zip(infoUrls,stuUrls):
        time.sleep(2)                        #休眠一下防止爬太快ip被封
        i+=1
        print("Search University Information: ",str(i)+"/2666")
        name,loc=findInfo(url1)
        stu=findStu(url2)
        retry=0
        while(not (name and loc and stu)):
            time.sleep(1)
            if(retry==5):
                print("Retried 5 times, give up")
                break
            print("Failed to access, try again!")
            name,loc=findInfo(url1)
            stu=findStu(url2)
            retry+=1
        if(name and loc and stu):
            print("name:",name)
            print("loc:",loc)
            print("stu:",stu)

            infos["School"].append(name)
            infos["Location"].append(loc)
            infos["Student"].append(stu)
        

    # i=0
    # for url in stuUrls:
    #     i+=1
    #     print("Search university student information: ",str(i)+"/2666")
    #     findStu(stus,url)

    data=pd.DataFrame(infos)
    print(data)
    data.to_csv("schoolData.csv",encoding='utf_8_sig')
    
main()





def findAllPages(pages,url):                #搜索出网站列表(弃用)
    while(True):
        end=1
        html=getHTMLText(url)
        soup = BeautifulSoup(html, "html.parser")
        ul=soup.find("ul",class_="fany")
        # print(ul)
        lis=ul("li")
        for li in lis:
            if(li.find("a")):
                if(li.find("a").string=="下一页 >>"):
                    pages.append(li.find("a").get("href"))
                    url=li.find("a").get("href")
                    print(li.find("a").get("href"))
                    end=0
        if(end==1):
            break

def fillUnivList(ulist, url):                    #搜索出某一网站上所有的高校地址（弃用）
    html=getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    for sc in soup.find("div",class_="scores_List").children:
        if isinstance(sc,bs4.element.Tag):
            if(sc.name=="dl"):
                dt=sc("dt")[0]
                ulist.append(dt.find("a").get("href"))
                print(dt.find("a").get("href"))
