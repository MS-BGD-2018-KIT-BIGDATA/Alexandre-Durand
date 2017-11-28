# ACER VS DELL sur Cdiscount
#   Quelle marque est la plus soldée ?

import requests
from bs4 import BeautifulSoup

# URL type = 'https://www.cdiscount.com/search/10/acer.html#_his_'

def getSoupFromURLbySearch(search):
    url = 'https://www.cdiscount.com/search/10/' + search + '.html#_his_'
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None


def getInfoFromOneProductSoup(soup_pdt):
    # Récupère le nom du produit
    pdtName = soup_pdt.find_all(class_ = 'prdtBTit')[0].text
    
    # Récupère le prix actuel du produit
    price = soup_pdt.find_all(class_ = 'price')[0].text
    price = float(price.replace('€', '.'))
    
    # S'il y en a un, récupère le prix barré (prix avant promo)
    old_price = price      #on set une variable 'old_price' avec la valeur du prix actuel
                           #et on updatera cette variable si on trouve effectivement un ancien prix
    if soup_pdt.find_all(class_ = 'prdtPrSt'):              #s'il y a une balise lié au prix barré:
        temp = soup_pdt.find_all(class_ = 'prdtPrSt')[0].text  #temp = valeur de cette balise
        if temp != '':                                         #et si cette balise n'est pas vide:
            old_price = float(temp.replace(',', '.'))               #alors on récupère l'ancien prix
    
    return (pdtName, price, old_price)


def PrintInfoForWholeSearchPage(search):
    soup = getSoupFromURLbySearch(search)
    SoupListByProduct = soup.find_all(class_ = 'prdtBloc')
    for soup_pdt in SoupListByProduct:
        pdtInf = getInfoFromOneProductSoup(soup_pdt)
        print()
        print(pdtInf[0])
        print('Prix =', pdtInf[1])
        if pdtInf[2] != pdtInf[1]:
            print('Ancien prix =', pdtInf[2])
        print('% DE REDUCTION =', \
              round(100*(pdtInf[2] - pdtInf[1])/pdtInf[2], 2), '%')


## TEST
#------
PrintInfoForWholeSearchPage('acer')
print('\n' + '=' * 50)
PrintInfoForWholeSearchPage('dell')


    


