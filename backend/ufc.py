import requests as req
from lxml import html
import datetime as dt
import random
from googlesearch import search

def safe_xpath(xml, xpath, default="Unknown"):
    result = xml.xpath(xpath)
    return result[0] if result else default

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
]

def parse_sherdog_fighter(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    htm = req.get(url, headers = headers)
    xml = html.document_fromstring(htm.content)
    
    
    wins_detailed = xml.xpath("//div[@class='wins']/div[@class='meter']/div[1]/text()")
    losses_detailed = xml.xpath("//div[@class='loses']/div[@class='meter']/div[1]/text()")
    bio = xml.xpath("//div[@class='fighter-info']")[0]
    
    try:
        other_wins = wins_detailed[3]
        other_losses = losses_detailed[3]
    except IndexError:
        other_wins = '0'
        other_losses = '0'

    fighter = {
        'name' : xml.xpath("//span[@class='fn']/text()")[0],
        'nationality' : bio.xpath("//strong[@itemprop='nationality']/text()")[0],
        'birthplace' : xml.xpath("//span[@class='locality']/text()")[0],
        'birthdate' : xml.xpath("//span[@itemprop='birthDate']/text()")[0],
        'age' : xml.xpath("//span[@itemprop='birthDate']/preceding-sibling::b/text()")[0],
        'height' : xml.xpath("//b[@itemprop='height']/text()")[0],
        'weight' : xml.xpath("//b[@itemprop='weight']/text()")[0],
        'weight_class' : xml.xpath("//div[@class='association-class']/a/text()")[0],

        'wins' : {
            'total': xml.xpath("//div[@class='winloses win']/span[2]/text()")[0],
            'ko/tko': wins_detailed[0],
            'submissions':wins_detailed[1],
            'decisions':wins_detailed[2],
            'others': other_wins
                },
        'losses' : {
            'total': xml.xpath("//div[@class='winloses lose']/span[2]/text()")[0],
            'ko/tko': losses_detailed[0],
            'submissions':losses_detailed[1],
            'decisions':losses_detailed[2],
            'others':other_losses
                },

        'fights' : []
    }
    return fighter

def get_ufc_stats(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    htm = req.get(url, headers = headers)
    xml = html.document_fromstring(htm.content)

    str_tds = []
    for item in xml.xpath("//dd"):
        if item.text is not None:
            str_tds.append(item.text)
        else:
            str_tds.append("0")

    distance = xml.xpath("//div[@class='c-stat-3bar__value']/text()")
    stats = xml.xpath("//div[@class='c-stat-compare__number']/text()")

    fighter = {
        'strikes': {
            'attempted': str_tds[1] if len(str_tds) > 1 else "0",
            'landed': str_tds[0] if len(str_tds) > 0 else "0",
            'standing': distance[0].split(" ")[0] if len(distance) > 0 else "0",
            'clinch': distance[1].split(" ")[0] if len(distance) > 1 else "0",
            'ground': distance[2].split(" ")[0] if len(distance) > 2 else "0",
            'striking defense': stats[4].strip() if len(stats) > 4 else "0",
            'strikes per minute': stats[0].strip() if len(stats) > 0 else "0"
        },
        'takedowns': {
            'attempted': str_tds[3] if len(str_tds) > 3 else "0",
            'landed': str_tds[2] if len(str_tds) > 2 else "0",
            'takedown defense': stats[5].strip() if len(stats) > 5 else "0",
            'subs per 15min': stats[3].strip() if len(stats) > 3 else "0"
        }
    }
    return fighter

def get_sherdog_link(query):
    possible_urls = search(query + " Sherdog fighter", num_results=10, sleep_interval=random.uniform(1, 4))
    for url in possible_urls:
        if "sherdog.com/fighter/" in url:
            return url
    
    print(f"Sherdog link not found for {query}")
    return None

def get_ufc_link(query):
    possible_urls = search(query + " ufc.com athlete", num_results=10, sleep_interval=random.uniform(1, 4))
    for url in possible_urls:
        if "ufc.com/athlete/" in url:
            return url
    
    print(f"UFC link not found for {query}")
    return None

def get_fighter(query):
    print(f"Searching for links for {query}...")
    sherdog_link = get_sherdog_link(query)
    ufc_link = get_ufc_link(query)
    

    if not sherdog_link:
        print(f"Could not retrieve Sherdog data for {query}. Aborting.")
        return None 
    
    print(f"Found Sherdog link: {sherdog_link}")
    fighter = parse_sherdog_fighter(sherdog_link)
    
    if not ufc_link:
        print(f"Sherdog data was found, but could not retrieve UFC.com stats for {query}.")
        return None
        
    print(f"Found UFC link: {ufc_link}")
    fighter.update(get_ufc_stats(ufc_link))
    return fighter