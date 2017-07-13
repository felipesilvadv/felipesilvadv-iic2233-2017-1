import requests
import json
import datetime

def close_issue(owner="felipesilvadv", repo="tarea7", number=0, content=None,
                mensaje=True):
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(
        owner=owner, repo=repo, number=number
    )
    with open("credentials") as file:
        credentials = tuple(file.read().splitlines())
    #issue = requests.get(url).json()
    #print(issue)
    #datos = issue.update({"state":"close",
     #                     "closed_by":credentials[0],
     #                     "closed_at": str(datetime.datetime.now())
     #                     })
    datos = json.dumps({"state": "close"})
    r = requests.patch(url, data=datos, auth=credentials)
    if mensaje:
        if r.headers["Status"] == "200 OK":
            return "Se cerro la issue #{}\n[Link:{link}"\
                .format(number, link=r.json()["html_url"])
        else:
            return "No se pudo acceder a la issue #{}".format(number)
    return r

if __name__ == "__main__":
    valor =close_issue("felipesilvadv", "tarea7", 1, False)
    print(valor)
    print(isinstance(valor, str))