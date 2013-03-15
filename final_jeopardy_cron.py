import urllib2
import pprint
from bs4 import BeautifulSoup
import re
import os
import datetime
import time
import MySQLdb

def get_html_from_season(season_number,offline):
	''' Takes season number and whether or not you're working offline.
	Returns BeautifulSoup object of a season HTML page.
	'''
	if offline:
		f = open('season.html', 'r')
		jarchive_html = f.read()
		f.close()	
		bs = BeautifulSoup(jarchive_html)
	else:
		url = 'http://www.j-archive.com/showseason.php?season={0}'.format(season_number)
		response = urllib2.urlopen(url)
		jarchive_html = response.read()
		bs =  BeautifulSoup(jarchive_html)
	return bs

def get_episode_urls_from_season(season_bs):
	episode_links = season_bs.findAll('a', attrs={'href': re.compile("game_id")})
	episodes = {}
	for row in episode_links:
		episode_info = row.string.encode('utf-8')
		episode_number = episode_info[1:5]
		air_date =  episode_info[14:]	
		#print episode_links[0]
		episode = {			
			'air_date': air_date,
			'url': row['href'],
			'episode_info': episode_info,
			'episode_number': episode_number
		}	
		episodes[episode_number] = episode
	return episodes

def get_final_jeopardy_from_episode(episodes):
	#i = 0 
	#while i < 20:
	for episode in episodes:
		url = episodes[episode]['url']	
		response = urllib2.urlopen(url)
		jarchive_html = response.read()
		bs_html =  BeautifulSoup(jarchive_html)
		print "getting fj from: ", url
		fj_clue = get_final_jeopardy(bs_html)
		episodes[episode]['clue'] = fj_clue		
		print episodes[episode]['clue']
		#{'category': u'OLYMPIC HOST CITIES', 'correct_answer': u'Sarajevo', 
		#'clue_text': u'When this city hosted the XIV Winter Olympics, it was located in \
		#a different nation than today', 'round': 'FJ'}		
		time.sleep(3)
		#print episodes
		#i = i + 1
			#if i == 100:
				#return episodes
	return episodes

def get_final_jeopardy(bs_html):
	""" Grab the Final Jeopardy clue from BeautifulSoup objectand return a clue dicionary to be added to the 
	clue dictionary.
	"""	
	#insert try catch in case the season isn't ready...
	try:
		bs_html.find("td",{"id": "clue_FJ"})
	except AttributeError:
		#no fj for this round
		clue_text = "bad"

	clue_text = bs_html.find("td",{"id": "clue_FJ"}).text
	finalj = bs_html.find("div", {"id": "final_jeopardy_round"})
	div = finalj.find("div")	
	mouseover_js = div['onmouseover'].split(",",2)
	answer_soup = BeautifulSoup(mouseover_js[2]) 
	answer = answer_soup.find('em').text
	category = finalj.find("td", {"class":"category_name"}).text
	category_comments = finalj.find("td", {"class":"category_comments"}).text

	#TODO: Grab incorrect answers and add them to the clue info
	# This could be helpful for users who want a hint or to
	# rule out what they think might be a right answer.	
	#  It's all in the answer soup, just have to get it out....
	#incorrect_answer = answer_soup.findAll("td", {"rowspan":"2"})
	
	clue_info = {
		"round" : "FJ",
		"category" : category,
		"category_comments": category_comments,		
		"clue_text" : clue_text,
		"correct_answer": answer,	
		}
	return clue_info

def insert_into_database(episodes):

	for episode in episodes:
		print episode
		conn = MySQLdb.connect(host="localhost",
		user="admin",
		passwd="theR3dbu11",
		db="djeopardy")
		print conn
		x = conn.cursor()
		print x
		print episodes[episode]['clue']['category']
		add_final_jeopardy = ("INSERT INTO djeo_finaljeopardy "
	               "(category, clue_text, correct_answer, game_number, game_id, air_date, game_round, category_comments, game_url, scrape_date) "
	               "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

		final_jeopardy_data = ( 
			episodes[episode]['clue']['category'].encode('utf-8'), 
			episodes[episode]['clue']['clue_text'].encode('utf-8'), 
			episodes[episode]['clue']['correct_answer'].encode('utf-8'),
			episodes[episode]['episode_number'],
			episodes[episode]['episode_info'],
			episodes[episode]['air_date'],
			'FJ',
			episodes[episode]['clue']['category_comments'],
			episodes[episode]['url'],
			datetime.datetime.now().strftime("%Y-%m-%d") )
		x.execute(add_final_jeopardy,final_jeopardy_data)
		conn.commit()
		x.close
		conn.close()
		time.sleep(2)
		print episode

#d = datetime.datetime.today()#datetime.datetime.now()
#print datetime.datetime.now().strftime("%Y-%m-%d")
#print d.isoformat()
season_bs = get_html_from_season(25,False)
episode_urls = get_episode_urls_from_season(season_bs)
#for key in episode_urls:
#	print "key:", key, "value:", episode_urls[key]

#print "#############################################"
final_jeopardy_info = get_final_jeopardy_from_episode(episode_urls)
import csv
w = csv.writer(open("fj.txt", "w"))
for key, val in final_jeopardy_info.items():
    w.writerow([key, val])
#w.write(final_jeopardy_info)


#for key in final_jeopardy_infob:

#	print "key:", key, "value:", final_jeopardy_info[key]	
#insert_into_database(final_jeopardy_info)
print "done"


##### Loop to grab all FJ from Season 29 for variety's sake



# How should the cron work?
'''
1. Grab the season page
2. Check the db to see what the last game was
3. If there's a new game, grab the url
4. 
'''
