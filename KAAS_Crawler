#Cotton Z 2019.09.27
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import time
import os,sys
import re

'''
Automatically download KAAS pathway image result
Usage:
python3 this.py your_kaas_webpage_file.txt
'''
#sys.argv[1] kaas_webpage_file, one line one URL

headers_kaas = {
    'Host': 'www.genome.jp',
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',  #need change
}

def get_name_html_dict(kaas_url):
    name_html_dict = dict()
    try:
        response = requests.get(kaas_url, headers=headers_kaas)
        if response.status_code == 200:
            data = response.text
            soup =  BeautifulSoup(data,"lxml")
            for html_tag in soup.find_all('a', href=True, string="html"):
                html = html_tag["href"]
                organism_name = html_tag.parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text.strip()
                name_html_dict[organism_name] = "https://www.genome.jp/kaas-bin/"+html
            return name_html_dict
        else:
            print ('!!!status is wrong!!!'+kaas_url) 
    except requests.ConnectionError as e:
        print('Error',e.args,kaas_url)


def get_url_pathway_dict(html_url):
    url_pathway_dict = dict()
    try:
        response = requests.get(html_url, headers=headers_html)
        if response.status_code == 200:
            data = response.text
            soup =  BeautifulSoup(data,"lxml")
            for pathway_url_tag in soup.find_all('a', href=True, target="new"):
                pathway_url = pathway_url_tag["href"]
                pathway_acc = pathway_url_tag.text.strip()
                pathway_name = re.sub(' +', '_', pathway_url_tag.next_sibling.string.strip().split('(')[0].replace('/','').strip())
                url_pathway_dict[pathway_url] = [pathway_name,pathway_acc]
            return url_pathway_dict
        else:
            print ('!!!status is wrong!!!'+html_url) 
    except requests.ConnectionError as e:
        print('Error',e.args,html_url)


def get_pathway_image_url(pathway_url):
    try:
        response = requests.get(pathway_url, headers=headers_pathway)
        if response.status_code == 200:
            data = response.text
            soup =  BeautifulSoup(data,"lxml")
            pathway_image_url_tag =soup.find("img", attrs={'name':'pathwayimage'})
            pathway_image_url = "https://www.kegg.jp"+pathway_image_url_tag["src"]
            return pathway_image_url
        else:
            print ('!!!status is wrong!!!'+pathway_url) 
    except requests.ConnectionError as e:
        print('Error',e.args,pathway_url)




if __name__ == '__main__':
    os.makedirs('./KAAS_images/', exist_ok=True)
    url_list = []
    with open(sys.argv[1],'r') as kaas_webpage_file:
        for line in kaas_webpage_file.readlines():
            url_list.append(line.strip())
    for kaas_url in url_list:

        headers_html = {
            'Host': 'www.genome.jp',
            'Referer': kaas_url, #need change
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',  #need change
            }
        name_html_dict = get_name_html_dict(kaas_url)

        for organism_name in name_html_dict:
            html = name_html_dict[organism_name]
            url_pathway_dict = get_url_pathway_dict(html)
            for pathway_url in url_pathway_dict:
                pathway_name = '_'.join(url_pathway_dict[pathway_url][0].split(' '))
                pathway_acc = url_pathway_dict[pathway_url][1]
                
                headers_pathway = {
                'Host': 'www.genome.jp',
                'Referer': html, #need change
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',  #need change
                }

                pathway_image_url = get_pathway_image_url(pathway_url)
                time.sleep(3)
                r_image = requests.get(pathway_image_url, stream = True, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'})
                image_name = './KAAS_images/'+pathway_name+'_'+organism_name+'_'+pathway_acc+'.png'
                with open(image_name, 'wb') as output_file:
                    output_file.write(r_image.content)
                print('find one!')
