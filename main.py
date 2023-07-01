import re

import requests
from bs4 import BeautifulSoup


def get_batch_details(row) -> tuple:
    row_mx_auto = row.find("div", class_="col-12 mb-4").find("div", class_="card shadow-sm").find("div", class_="card-body").find("div", class_="row mx-auto")


    batch_name = row_mx_auto.find("div", class_="col-12 col-lg-2").find("div", class_="text-center text-lg-left").get_text().replace("\n", "")
    batch_title = row_mx_auto.find("div", class_="col-12 col-lg-7 text-justify").find("a").find("h5").get_text()
    batch_url = row_mx_auto.find("div", class_="col-12 col-lg-2").find("a")["href"]

    return batch_name, batch_title, batch_url

def get_detail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    body = soup.find("body", id="topo")
    detail_batch = body.find("div", id="content").find("div", class_="container detalhes-lote")
    title = detail_batch.find("div", class_="px-1 text-center").find_all("h4")[1].get_text()
    print("Title:", title)
    
    

    info_batch = detail_batch.find("div", class_="col-12 col-lg-8 p-1 float-left").find("div").find("div", class_="mb-3 p-2 border rounded text-justify")
 
    print(info_batch)
    
    
    address = info_batch.find("div", class_="informacoes-adicionais").find("div")
    print(address)
    
    
    return {"title": title , "address": ""}


page = 1
search = "https://agostinholeiloes.com.br/lotes/search"
while True:
    params = {
        "tipo": "",
        "data_leilao_ini": "",
        "data_leilao_fim": "",
        "lance_inicial_ini": "",
        "lance_inicial_fim": "",
        "address_uf": "",
        "address_cidade_ibge": "",
        "address_logradouro": "",
        "comitente_id": "",
        "search": "",
        "page": page
    }
    response = requests.get(search, params)
    # For debug, uncomment
    # def save_html_response(response, page):
    #     with open(f"agostinho_{page}.html", "wb") as f:
    #         f.write(response.content)
    # save_html_response(response)

    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find("body", id="topo")
    batch_list = body.find("div", id="content").find("div", class_="container").find("div", class_="lista-lotes")

    # For debug, uncomment
    # def get_batches_len(batch_list) -> int:
    #     return int(re.search(r"\b\d+\b", batch_list.find("div", class_="mt-2 mb-2").get_text()).group())
    # batches_len = get_batches_len(batch_list)
    # pages = batches_len // 30
    # print("batches_len", batches_len)
    # print("pages", pages)

    if not batch_list.find("div", class_="row"):
        break

    rows = batch_list.find("div", class_="row").find_all("div", class_="lote")
    for i, row in enumerate(rows, start=1):
        name, title, url = get_batch_details(row)
        print(f"{i} {name=} {title=} {url=}")
        print(f"calling get_detail({url})")
        details = get_detail(url)
    page += 1