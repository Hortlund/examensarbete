import requests
from bs4 import BeautifulSoup 
import sys
import getopt
import time
import git

start = time.time()
repositories = []

def clone(clonePath):
    for x in range(len(repositories)):
        git.Repo.clone_from('https://github.com'+ repositories[x], clonePath+'/'+str(x))
    print("Done! - " + str(len(repositories)) + " repositories cloned to " + clonePath)
    end = time.time()
    print("Total time elapsed: " + str((round(end-start, 2))) + " seconds")
    

def scrape(search, clonePath):
    print("Scraping...")
    for x in range (100):
        if(search == "ansible"):
            response = requests.get(
                'https://github.com/search?l=&p='+str(x+1)+'&q=ansible+created%3A%3E%3D2019-01-01+extension%3A.yml&type=Repositories')
        elif(search == "puppet"):
            response = requests.get(
                'https://github.com/search?l=&p='+str(x+1)+'&q=puppet+created%3A%3E%3D2019-01-01+extension%3A.pp+language%3ARuby&type=Repositories')
        response_code = response.status_code
        if response_code != 200:
            print(response_code)
            print("Error code detected...\nExiting")
            sys.exit()
        html_content = response.content
        dom = BeautifulSoup(html_content, 'html.parser')
        reposSearch = dom.select("a.v-align-middle")
        time.sleep(10)
        end = time.time()
        print("Scraping... - Time elapsed: " + str((round(end-start,2))) + " seconds")
        for each_repository in reposSearch:
            repositories.append(each_repository.get('href'))
    end = time.time()
    print("Scraping finished - Time elapsed: " + str((round(end-start,2))) + " seconds")
    clone(clonePath)

def usage():
    print("Usage: scraper.py -c [--clonePath=Directory] -a [--ansible] || -p [--puppet]")

def main(argv):
    if len(sys.argv) == 1:
        usage()
        sys.exit(2)
    try:
      opts, args = getopt.getopt(argv, "hapc:", ["ansible", "puppet", "clonePath="])
    except getopt.GetoptError as error:
        print(error)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
         usage()
         print("Used to clone ansible or puppet repositories for static code analysis.\nCreated by Andreas Hortlund for bachelors thesis")
         sys.exit(2)
        elif opt in ("-c", "--clonePath"):
            clonePath = arg

        elif opt in ("-a","--ansible"):
            scrape("ansible", clonePath)

        elif opt in ("-p", "--puppet"):
            scrape("puppet", clonePath)

if __name__ == "__main__":
    main(sys.argv[1:])
