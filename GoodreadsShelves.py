from bs4 import BeautifulSoup
from lxml import html
import mechanize

br = mechanize.Browser()

#Goodreads credentials
Email = raw_input('E-mail Address: ')
Password = raw_input('Password: ')

url = 'https://www.goodreads.com'
#Opens and grabs details at Goodreads URL
br.open(url)

#Filling the credentials
br.select_form('sign_in')
br.form['user[email]'] = Email
br.form['user[password]'] = Password
br.submit()

#Get the Welcome message
soup_welcome = BeautifulSoup(br.response().read().replace('&nbsp',''),'lxml')
p = soup_welcome.findAll('h2' , attrs={'class':'welcomeHeader'})

#Do stuff in review list
review_list_common_url = br.open('https://www.goodreads.com/review/list')
user_specific_all_bookshelves_url = review_list_common_url.geturl() + "?shelf=%23ALL%23"

#Get url of all the Books
soup_all_books = BeautifulSoup(br.response().read(),'lxml')
book_list = soup_all_books.findAll('td', attrs={'class':'field title'})
author_list = soup_all_books.findAll('td', attrs={'class':'field author'})
all_urls = soup_all_books.findAll('a', title=True)
ratings = soup_all_books.findAll('td',attrs={'class':'field avg_rating'})
reviews = soup_all_books.findAll('td',attrs={'class':'field num_ratings'})
pages = soup_all_books.findAll('td',attrs={'class':'field num_pages'})
book_urls = []
book_description = []
cover_page_urls = []

for i in all_urls:
	if '/book/show/' in i['href']:
		book_urls.append('https://www.goodreads.com' + i['href'])

#Get book description
for i in range(0,len(book_urls)):
	pr = mechanize.Browser()
	pr.open(book_urls[i])
	soup_of_a_book = BeautifulSoup(pr.response().read().replace('  ','').replace('\n',' '),'lxml')
	meta_prop_list = soup_of_a_book.findAll('meta', attrs={'property':'og:description'})
	cover_page_url = soup_of_a_book.findAll('img', attrs={'id':'coverImage'})
	for j in meta_prop_list:
		book_description.append(j['content'])

	for l in cover_page_url:
		cover_page_urls.append(l['src'])

final_Message = "\nList of your books:\n"

for k in range(0,len(book_urls)):
	final_Message += str(k+1) + ':)%s \n%s \nRatings: %s\nReview: %s \nNumber of pages: %s\nDescription: %s \n%s\n'%(book_list[k].get_text().replace('title','Title:').replace('  ','').replace('\n',''),author_list[k].get_text().replace('author','Author:').replace('  ','').replace('*','').replace('\n',''),ratings[k].get_text().replace('avg rating','').replace('  ',''),reviews[k].get_text().replace('num ratings','').replace('  ',''),pages[k].get_text().replace('num pages','').replace('pp',' ').replace('  ',''),book_description[k],cover_page_urls[k])

print final_Message

#Creating the CSS file
print "Creating css file"
css_file = open('main.css','w')
css_script = 'body{text-align: center;background-color: #fff;margin: 0;padding: 0;}img{margin-bottom: 10%;}#cover{width: 100%;height: 100%;border-radius: 0 7'+'%'+' 7% 0;}#book{width: 10%;margin-left: 17%;height: 21%;display: inline-block;float: left;margin-bottom: 10%;}.bookcontainer{width: 100%;height:100%;float: left;}.reveal-wrapper{position: relative;overflow: hidden;width: 100%;height: 100%;border-radius: 0 7' + '%' +'7% 0;}.reveal-wrapper:hover .reveal-top{left: -100%;}.reveal-content{box-shadow: 1px 1px 5px rgba(0,0,0,0.5) inset;width: inherit;overflow-x: hidden;height: inherit;color:#000;background: #fff;text-align: center;font-size: 0.82em;padding-top: 3px; }.reveal-top{background: #1F122C;width: 100%;height: 100%;position: absolute;top:0;left:0;transition: left 0.4s ease;}#numPages,#rating{font-size:0.8em}'
css_file.write(css_script)
css_file.close()
print "CSS file created : main.css\n\n"

#Creating the HTML file
print "Creating HTML file"
html_file = open('index.html','a')
html_script = '<html><head><link rel="stylesheet" type="text/css" href="./main.css"><title>GoodReads book list</title></head><body><img width="100%" height = "20%" src = "https://covenantcs.files.wordpress.com/2015/07/book-library-header-2109a.jpg">'

for m in range(0,len(book_urls)):
	html_script += '<div id="book"><div class = "bookcontainer" ><div class = "reveal-wrapper"><div class = "reveal-content">'+ u' '.join((book_description[m],'')).encode('utf-8').strip() +'</div><div class="reveal-top"><img id = "cover" src = "'+ u' '.join((cover_page_urls[m],'')).encode('utf-8').strip() +'"></div></div><br><span id="bookTitle"><b>'+ u' '.join((book_list[m].get_text().replace('title','').replace('  ','').replace('\n',''),'')).encode('utf-8').strip() +'</b><br><span id ="rating">'+ u' '.join((ratings[m].get_text().replace('avg rating','').replace('  ','').replace('\n',''),'')).encode('utf-8').strip() + ' Rating</span>, <span id="numPages">'+ u' '.join((pages[m].get_text().replace('num pages','').replace('pp','').replace('  ','').replace('\n',''),'')).encode('utf-8').strip() +' pages</span><br><span id = bookAuthor>'+ u' '.join((author_list[m].get_text().replace('author','').replace('  ','').replace('*','').replace('\n',''),'')).encode('utf-8').strip() +'</span></div></div>'

html_script += '</body></html>'
html_file.write(html_script)

html_file.close()

print "HTML file created : index.html\n\nOpen index.html that has been just created in your browser."
