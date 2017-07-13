import requests
import json
def add_label(owner="felipesilvadv", repo="tarea7", number=0, content="",
              mensaje=True):
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{number}/" \
          "labels".format(owner=owner, repo=repo, number=number)
    with open("credentials") as file:
        credentials = tuple(file.read().splitlines())
    if isinstance(content, list):
        datos = json.dumps(content)
        r = requests.post(url, data=datos, auth=credentials)
        if mensaje:
            if len(content) == 1:
                valor = "el"
            else:
                valor = "los"
            return "A la issue #{num} se le agrego {largo} label {lista}\n" \
                   .format(num=number,
                                          largo=valor,
                                          lista=content)
        else:
            return {"headers": r.headers, "json": r.json()}
    elif isinstance(content, str):
        datos = json.dumps([content])
        r = requests.post(url, data=datos, auth=credentials)
        if mensaje:
            return "A la issue #{num} se le agrego el label {lista}" \
            .format(num=number, lista=content)
        else:
            return {"headers": r.headers, "json": r.json()}
    else:
        print("ERROR")

if __name__ == "__main__":
    a = add_label("felipesilvadv", "tarea7", 1, ["ERROR", "Tarea 7"])
    print(a)