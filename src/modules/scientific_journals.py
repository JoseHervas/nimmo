from scholarly import scholarly, ProxyGenerator
import requests, copy, time
from bs4 import BeautifulSoup

def get_latest_papers(journal_name):
    print("[+] Preparing proxy")
    pg = ProxyGenerator()
    pg.ScraperAPI("efa0d2d95f1f374785d6ea3f653d38bf")
    scholarly.use_proxy(pg)

    print("[+] Extracting papers from", journal_name)
    template_query = 'source:{0}'
    query = template_query.format(requests.utils.quote(journal_name))
    template_url = '/scholar?hl=en&q={0}&scisbd=1&num=10&as_sdt=0,5'
    url = template_url.format(requests.utils.quote(query))
    search = scholarly.search_pubs_custom_url(url)
    summary = []
    for i, result in enumerate(search):
        if i >= 10:
            break  
        print("\t- Extracting paper features number", i+1, "of", 10)
        paper = extract_paper_features(result)
        summary.append(paper)
    return(summary)

def extract_abstract_from_nature(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    abstract = soup.find('div', {'class': 'c-article-section__content'})
    return(abstract.text.strip())

def extract_paper_features(paper):
    to_print = copy.deepcopy(paper)
    article_obj = {
        'title': to_print["bib"]['title'],
        'venue': to_print["bib"]['venue'],
        'num_citations': to_print['num_citations'],
        'pub_url': to_print['pub_url'],
    }
    try:
        # TODO: This only works for Nature. Need to generalize this.
        article_obj['abstract'] = extract_abstract_from_nature(to_print['pub_url'])
    except:
        article_obj['abstract'] = "No abstract was found."
    return(article_obj)