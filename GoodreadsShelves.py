from bs4 import BeautifulSoup
from lxml import html
import mechanize
import time

start_time = time.time()
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
book_urls = []
book_description = []

for i in all_urls:
	if '/book/show/' in i['href']:
		book_urls.append('https://www.goodreads.com' + i['href'])

#Get book description
for i in range(0,len(book_urls)):
	pr = mechanize.Browser()
	pr.open(book_urls[i])
	soup_of_a_book = BeautifulSoup(pr.response().read().replace('  ','').replace('\n',' '),'lxml')
	meta_prop_list = soup_of_a_book.findAll('meta', attrs={'property':'og:description'})
	for j in meta_prop_list:
		book_description.append(j['content'])


final_Message = "\nList of your books:\n"

for k in range(0,len(book_urls)):
	final_Message += str(k+1) + ':) %s \n%s \nDescription: %s \n\n'%(book_list[k].get_text().replace('title','Title:').replace('  ','').replace('\n',''),author_list[k].get_text().replace('author','Author:').replace('  ','').replace('*','').replace('\n',''),book_description[k])

print final_Message
print ("%s"%(time.time()-start_time))