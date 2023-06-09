import requests
import time

# dunijet
token = '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'

# amir00462
# token = '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'

search_url = 'https://api.github.com/search/repositories'
star_url = 'https://api.github.com/user/starred/<owner>/<repo>'
params = {
    'q': 'android+language:kotlin+stars:>5500',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 70
}

def starProjects():
    # empty list
    repositories_to_star = []

    # Send a GET request to the API endpoint with the search query parameters and the personal access token as the authentication header
    response = requests.get(search_url, params=params, headers={'Authorization': 'token ' + token})

    # Check the response status code
    if response.status_code == 200:

        results = response.json()['items']
        for result in results:
            owner = result['owner']['login']
            repo = result['name']
            repositories_to_star.append((owner, repo))
            print(f'{owner}/{repo}')

        # Loop through the list of repositories to star and send a PUT request to the API endpoint for each one
        for owner, repo in repositories_to_star:
            # Replace <owner> and <repo> with the owner and name of the repository you want to star
            url = star_url.replace('<owner>', owner).replace('<repo>', repo)

            # Send a PUT request to the API endpoint with the personal access token as the authentication header
            response = requests.put(url, headers={'Authorization': 'token ' + token})

            # Check the response status code
            if response.status_code == 204:
                print(f'{owner}/{repo} starred successfully!')
                time.sleep(1)

            else:
                print(f'Failed to star {owner}/{repo}')
                time.sleep(1)

    else:
        print('Failed to search repositories')


if __name__ == '__main__':
    starProjects()


