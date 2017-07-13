import requests

def get_issue(owner="felipesilvadv", repo="tarea7", number=0, content=None,
              json=False):
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(
        owner=owner, repo=repo, number=number
    )
    r = requests.get(url)
    if json:
        return {"headers":r.headers, "json": r.json()}
    else:
        if r.headers["Status"] == "200 OK":
            dic = r.json()
            msg = """[{author}]
    [#{num_issue}-{titulo_issue}]
    {texto}
    [Link: {link_issue}]""".format(
                author=dic["user"]["login"],
                texto=dic["body"],
                titulo_issue=dic["title"],
                link_issue=dic["html_url"],
                num_issue=dic["number"])
            return msg
        else:
            return "No se pudo acceder a la issue"



if __name__ == "__main__":
    valor = get_issue("felipesilvadv", "tarea7", 1)
    print(valor)