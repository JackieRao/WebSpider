import requests
from pyquery import PyQuery as pq

dir='C:/Users/jackie.wujiang.rao/Desktop/Training/Python_Test/Book/'
urls=input("Input the book's url: ")#input the book url

#get the book name for file naming
def get_book_name(url):
	response=requests.get(url).text
	doc=pq(response)
	book_name=doc('.book-info h1 em').text() #the book name is under the class book-info, and in em point
	return book_name

#get the chapter url
def get_chapter_url(url):
	response=requests.get(url).text
	doc=pq(response)
	items=doc('.volume .cf li a').items()
	for item in items:
		yield 'https:'+item.attr.href

#get all the content in the chapter		
def get_content_url(url):
	response=requests.get(url).text
	doc=pq(response)
	items=doc('.main-text-wrap').items()
	for item in items:
		title=item.find('.j_chapterName').text()
		content=pq(item.find('.read-content.j_readContent').html()).text()
		return title,content

#download the content to your local		
def download_text(filename,content):
	bookname=dir+filename+'.txt'
	with open(bookname, 'a', encoding='utf-8') as file:
		file.write(content)

#the main process for the tool
if __name__=='__main__':
	bookname=get_book_name(urls)
	for url in get_chapter_url(urls):
		title,content=get_content_url(url)
		download_text(bookname,title)
		download_text(bookname,'\n')
		download_text(bookname,content)
		download_text(bookname,'\n\n\n')
		print (title, 'download completed')
	print ("Download successfully")