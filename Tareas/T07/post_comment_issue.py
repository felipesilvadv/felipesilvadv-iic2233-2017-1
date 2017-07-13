import requests
import json

def comment_issue(owner="felipesilvadv", repo="tarea7", number=0, content="",
                  mensaje=True):
    with open("credentials") as file:
        credentials = tuple(file.read().splitlines())
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{number}/" \
          "comments".format(owner=owner, repo=repo, number=number)
    dic = {"body": content}
    msg = json.dumps(dic)
    r = requests.post(url, data=msg, auth=credentials)
    if mensaje:
        return "Se comento {msg} en la issue #{num}".format(
            msg=content, num=number
        )
    else:
        return {"headers":r.headers, "json": r.json()}

if __name__ == "__main__":
    print(comment_issue(number= 4 ,content="Estoy comentando la "
                                                      "issue"))