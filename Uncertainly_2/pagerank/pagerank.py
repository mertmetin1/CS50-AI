import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

""" 
    crawl(directory): 
    Belirli bir dizindeki HTML sayfalarını analiz eder ve bu sayfalar arasındaki bağlantıları bulur.
    Bu bağlantıları bir sözlükte saklar, her bir sayfa için diğer sayfalara olan bağlantıları içerir.

    transition_model(corpus, page, damping_factor):
    Verilen bir sayfadan diğer sayfalara geçme olasılıklarını hesaplar.
    Sayfanın bağlantılarına tıklama olasılığı 
    ve rastgele bir sayfaya gitme olasılığı dahil olmak üzere iki farklı olasılığı dikkate alır.

    sample_pagerank(corpus, damping_factor, n):
    Örnekleme yöntemini kullanarak belirli bir sayıda (n) örnek alır 
    ve bu örnekler üzerinden sayfa sıralaması hesaplar. Rastgele başlayarak, 
    belirli bir sayfadan diğer sayfalara geçme olasılıklarını kullanarak örnekler alır 
    ve bu örnekler üzerinden PageRank değerlerini tahmin eder.

    iterate_pagerank(corpus, damping_factor): 
    Tekrarlayan yöntemi kullanarak sayfa sıralamasını hesaplar. 
    Başlangıçta her sayfanın PageRank değerini eşit bir şekilde başlatır 
    ve ardından bu değerleri güncellemek için belirli bir iterasyon sayısında tekrar tekrar günceller.

"""
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    If a page has no outgoing links, returns an equal probability for all pages in the corpus
    """

    #corpus Setinde bulunan tüm sayfalar için olasılığı 0 olan bir set daha oluşturduk:prob_dist
    prob_dist = {page_name : 0 for page_name in corpus}
    """
    
            corpus = {
                'page1': ['page2', 'page3'],
                'page2': ['page1', 'page3'],
                'page3': ['page2']
            }
            prob_dist = {'page1': 0, 'page2': 0, 'page3': 0}


    """
    # sayfada hiç link yok ise sayfa dizininin olasılığını döndür 
    if len(corpus[page]) == 0:     #if len("page1") == 0              
        for page_name in prob_dist:   # for "page1" in prob_dist
            prob_dist[page_name] = 1 / len(corpus)     #prob_dist["page1"] = 1/len(corpus)(3)
        return prob_dist

    # Probability of picking any page at random:
    """ 
    random_prob değişkeni, herhangi bir sayfanın rastgele seçilme olasılığını hesaplar. 
    Eğer bir kullanıcı mevcut sayfadaki bağlantılardan birine tıklamazsa, 
    tüm sayfalar arasında eşit olarak rastgele bir sayfaya gitme olasılığını ifade eder.
    """
    random_prob = (1 - damping_factor) / len(corpus)       

    # Probability of picking a link from the page:
    """
    link_prob değişkeni ise, belirli bir sayfanın bağlantılarına tıklama olasılığını hesaplar. 
    Bu, kullanıcının mevcut sayfadaki bağlantılardan birine tıklama olasılığını belirler. 
    Eğer kullanıcı mevcut sayfadaki bir bağlantıya tıklarsa,
    bu olasılıkla bir bağlantı seçer.
    """
    link_prob = damping_factor / len(corpus[page])
    
    
    """  prob_dist = {'page1': 1/3, 'page2': 1/3, 'page3': 1/3}
    """
    # Add probabilities to the distribution:
    for page_name in prob_dist:
        prob_dist[page_name] += random_prob                #rasgele seçilme olasılığını  olasılık dağılımına ekle 

        if page_name in corpus[page]:                  
            prob_dist[page_name] += link_prob         # sayfadaki bağlantıya tıklanma olasılığını olasılık dağılımına ekle 

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visits = {page_name: 0 for page_name in corpus} # dizindeki dosyaların tıklanma sayısını sıfır olarak belirle ve bir set oluştur

    # First page choice is picked at random:
    curr_page = random.choice(list(visits))     #random bir sayfa seç
    visits[curr_page] += 1              #seçilen sayfanın tıklanma sayısını arttır 

    # For remaining n-1 samples, pick the page based on the transistion model:
    for i in range(0, n-1):

        trans_model = transition_model(corpus, curr_page, damping_factor) # return olasılık dağılımı prob_dist:("page_name":probability(int))

        # Pick next page based on the transition model probabilities:
        rand_val = random.random()                       
        total_prob = 0

        for page_name, probability in trans_model.items(): 
            total_prob += probability        #her sayfasının tıklanma olasılığını total  olasılık dağılımınna ekle 
            if rand_val <= total_prob:          #olasılık dağılımı  random bir değerden fazla olan bir sayfa var ise 
                curr_page = page_name           # current page e ata
                break

        visits[curr_page] += 1             #current page in tıklanma sayısını arttır 

    # Normalise visits using sample number: 
    #sayfaları tıklanma sayılarını toplam sayfa sayısına oranla ve sayfa seviyleri seti oluştur
    page_ranks = {page_name: (visit_num/n) for page_name, visit_num in visits.items()}
    

    print('Sum of sample page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Calculate some constants from the corpus for further use:
    num_pages = len(corpus) # dizindeki toplam sayfa sayısı 
    init_rank = 1 / num_pages  #ilk seviye 
    random_choice_prob = (1 - damping_factor) / len(corpus)  #sayfanın seçilme olasığı/total sayfa sayısı 
    iterations = 0

    # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    page_ranks = {page_name: init_rank for page_name in corpus} # ilk olasılıkların atamasını yap
    new_ranks = {page_name: None for page_name in corpus}   # olsalık dağılımları için boş bir olasılık seti oluştur
    max_rank_change = init_rank 

    # Iteratively calculate page rank until no change > 0.001
    while max_rank_change > 0.001:

        iterations += 1
        max_rank_change = 0

        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] * init_rank
                # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
            # Calculate new page rank
            new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
            new_ranks[page_name] = new_rank

        # Normalise the new page ranks:
        norm_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

        # Find max change in page rank:
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change

        # Update page ranks to the new ranks:
        page_ranks = new_ranks.copy()

    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks


if __name__ == "__main__":
    main()
