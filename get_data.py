import requests, os
from tqdm import tqdm

# fetch clone urls from github api v3
def fetch_urls(language, fetch_star, save_file):
    print("start fetch_urls...")

    f = open(save_file, "a")
    token = open("github_token.txt", "r").read()
    current_star = 0
    headers = {"Authorization": f"token {token}"}

    print("fetch_star: ", fetch_star)

    for page in tqdm(range(10)):
        # fetch by most star github repos
        url = f"https://api.github.com/search/repositories?q=stars:<{fetch_star}+language:{language}&sort=stars&order=desc&per_page=100&page={page}"
        data = requests.get(url, headers=headers)
        obj = data.json()
        if obj.get("items"):
            for items in obj.get("items"):
                clone_url = items.get("clone_url")
                author = items.get("owner").get("login")
                name = items.get("name")
                current_star = items.get("stargazers_count")
                f.write(clone_url + "\t" + name + "\t" + author + "\n")
        else:
            break
    print(f"fetch done, current star: {current_star} saved to {save_file}")


# Keep only python file
def clean_repos(path):
    os.system(f"rm -rf {path}/.git")

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            if full_path.endswith(".py"):
                pass
                # print((f"Keeping {full_path}"))
            else:
                # print((f"Deleting {full_path}"))
                os.remove(full_path)


# download repos and clean
def fetch_repos(urls_file):
    f = open(urls_file, "r")
    line = 0
    for data in f:
        print("current line: ", line)
        url, name, author = data.strip().split("\t")
        os.system(f"git clone --depth 1 {url} repos/{author}/{name}")
        clean_repos(f"repos/{author}/{name}")
        line += 1

if __name__ == "__main__":
    # fetch_urls('python', 627 ,'github_repos.txt')
    fetch_repos("github_repos.txt")
