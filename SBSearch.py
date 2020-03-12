import requests
from bs4 import BeautifulSoup

def getData(url):
    resinfo=[]
    result=""
    res=requests.get(url)
    eachsoup = BeautifulSoup(res.text, 'html.parser')
    title=eachsoup.find_all("h3")
    print("标题:"+title[0].text)
    num=eachsoup.find_all("span",style="color:#CC0000;")
    print("番号:"+num[0].text)
    infos=eachsoup.find_all("div", class_="col-md-3 info")
    for info in infos:
        pinfos=info.find_all("p")
        for pinfo in pinfos:
            spaninfos=pinfo.find_all("span")
            for spaninfo in spaninfos:
                ainfos=spaninfo.find_all("a")
                for ainfo in ainfos:
                    resinfo.append(ainfo.text)
    for ldata in resinfo:
        result=result+ldata+";"
    print("类别:"+result)
    print("磁力链接:")
    ans = eachsoup.select("body  script")
    para=""
    for an in ans:
        if("gid" in an.getText()):
            para=an.getText()
    para = para.replace('var','')
    paralist=para.split(";")
    para="&"+paralist[0]+"&"+paralist[1]+"&"+paralist[2]
    para=para.replace('\n', '').replace('\r', '').replace('\t','').replace(' ','').replace("'",'')
    finalurl="https://www.javbus.com/ajax/uncledatoolsbyajax.php?&lang=zh"+para
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "referer": "https://www.javbus.com/"+num[0].text
    }
    finalresult=requests.get(url=finalurl,headers=headers)
    finalsoup = BeautifulSoup(finalresult.text, 'html.parser')
    trs=finalsoup.find_all("tr")
    for tr in trs:
        fileinfo=''
        filemag=''
        tds=tr.find_all("td")
        for td in tds:
            aa=td.find_all("a",rel="nofollow")
            for a in aa:
                inf=''
                inf=a.text
                inf=inf.replace('\n', '').replace('\r', '').replace('\t','').replace(' ','')
                fileinfo=fileinfo+inf+" "
                filemag=a.get("href")
        print(fileinfo+"\n"+filemag+"\n")
    print("-------------------------------------------------------")




    
i=0
menu={"":""}
genre=requests.get("https://www.javbus.com/genre")
genresoup = BeautifulSoup(genre.text, 'html.parser')
gs=genresoup.find_all("a",class_="col-lg-2 col-md-2 col-sm-3 col-xs-6 text-center")
for g in gs:
    i=i+1
    print(str(i)+"."+g.text)
    menu[str(i)]=g.get("href")
inputnum=input("请输入序号:")
inputurl=menu[inputnum]
pages=input("请输入页数:")
for page in range(1,int(pages)):
	inputurl=inputurl+"/"+str(page)
	html_doc=requests.get(inputurl)
	soup = BeautifulSoup(html_doc.text, 'html.parser')
	links=soup.find_all("a", class_="movie-box")
	for link in links:
		getData(link.get('href'))
