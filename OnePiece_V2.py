import os,time,requests
from selenium import webdriver
from pyquery import PyQuery as pq
from multiprocessing.pool import Pool
# from random import randint

ROOT_URL="http://ac.qq.com"
target_url=[ROOT_URL+"/Comic/comicInfo/id/505430"]#One Piece
DIR_PATH='C:/Users/jackie.wujiang.rao/Desktop/Training/Python_Test/Test/'#The file root path


def getUrls(comic_url,i):#get the chapter's url and i is the chapter number
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
	req=requests.get(comic_url,headers=headers).text
	doc=pq(req)
	items=doc('.chapter-page-all.works-chapter-list a').items()
	title=[]
	result={}
	for item in items:
		title.append(item.attr.title)
		result[item.attr.title]=item.attr.href
	Pagetitle=title[i]
	Pageresult=ROOT_URL+result[title[i]]
	print ("title:",Pagetitle)
	print ("Result:",Pageresult)
	return Pagetitle,Pageresult
	
def getImageUrls(comic_url):#get the images' url in the chapter
	urls=[]
	chrome_options=webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	# chrome_options=chrome_options
	browser=webdriver.Chrome(chrome_options=chrome_options)
	browser.get(comic_url)
	imgs=browser.find_elements_by_xpath("//div[@id='mainView']/ul[@id='comicContain']//img")
	for i in range(0,len(imgs)-1):
		if i==1:
			continue
		urls.append(imgs[i].get_attribute("src"))
		js='mainView.scrollTop='+str((i+1)*1280)#make the page can scroll down automatically
		browser.execute_script(js)
		time.sleep(20)
	browser.quit()
	print ("urls=",urls)
	return urls
	
def downloadComic(urls,path):#download the images
	i=0
	for url in urls:
		i+=1
		img=requests.get(url)
		with open(path+str(i)+'.jpg','wb') as comic:
			comic.write(img.content)

def main(i):
	title,result_url=getUrls(target_url[0],i)
	imgurl=getImageUrls(result_url)
	path=DIR_PATH+title+"/"
	if not os.path.exists(path):
		os.makedirs(path)
		print(path+'  创建成功')
	downloadComic(imgurl,path)
			
	
if __name__=="__main__":#multiple process to get the chapters at the same time
	pool=Pool()
	groups=[x*1 for x in range(-25,-33,-1)]
	pool.map(main, groups)
	pool.close()
	pool.join()