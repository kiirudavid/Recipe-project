import urllib.request,json
from .models import Recipe




# Getting api key
# api_key = None
# app_id = None

# Getting the recipe base url
base_url = None

def configure_request(app):
    global api_key, app_id, base_url
    api_key = app.config['RECIPE_API_KEY']
    app_id =app.config['APP_ID']
    base_url = app.config['RECIPE_API_BASE_URL']





def get_recipes():
    '''
    Function that gets the json responce to our url request
    '''
    get_recipes_url = "https://api.edamam.com/search?q=food&app_id=ee974c44&app_key=417ba80ca6f3032f407ccb1379e65325&from=0"

    with urllib.request.urlopen(get_recipes_url) as url:
        get_recipes_data = url.read()
        get_recipes_response = json.loads(get_recipes_data)

        recipe_results = None

        if get_recipes_response['hits']:
            recipe_results_list = get_recipes_response['hits']
            recipe_results = process_results(recipe_results_list)


    return recipe_results


def get_recipe(id):
    get_recipe_details_url = base_url.format(id,api_key)

    with urllib.request.urlopen(get_recipe_details_url) as url:
        recipe_details_data = url.read()
        recipe_details_response = json.loads(recipe_details_data)

        recipe_object = None
        if recipe_details_response:
            id = recipe_details_response.get('id')
            title = recipe_details_response.get('original_title')
            overview = recipe_details_response.get('overview')
            poster = recipe_details_response.get('poster_path')
            vote_average = recipe_details_response.get('vote_average')
            vote_count = recipe_details_response.get('vote_count')

            recipe_object = Recipe(id,title,overview,poster,vote_average,vote_count)

    return recipe_object



def search_recipe(recipe_name):
    # search_recipe_url = 'https://api.edamam.com/search?q={}&app_id=${}&app_key=${}'.format(api_key,recipe_name)
    search_recipe_url = "https://api.edamam.com/search?q=food&app_id=ee974c44&app_key=417ba80ca6f3032f407ccb1379e65325&from=0"
    with urllib.request.urlopen(search_recipe_url) as url:
        search_recipe_data = url.read()
        search_recipe_response = json.loads(search_recipe_data)

        search_recipe_results = None

        if search_recipe_response['hits']:
            search_recipe_list = search_recipe_response['hits']
            search_recipe_results = process_results(search_recipe_list)


    return search_recipe_results




def process_results(recipe_list):
    '''
    Function  that processes the recipe result and transform them to a list of Objects
    Args:
        recipe_list: A list of dictionaries that contain recipe details
    Returns :
        recipe_results: A list of recipe objects
    '''
    recipe_results = []
    for recipe_item in recipe_list:
        url = recipe_item['recipe'].get('url')
        label = recipe_item['recipe'].get('label')
        image = recipe_item['recipe'].get('image')
        source = recipe_item['recipe'].get('source')
        healthlabels = recipe_item['recipe'].get('healthlabels')
        ingredients = recipe_item['recipe'].get('ingredients')

        if image:
            recipe_object = Recipe(url,label,image,source,healthlabels,ingredients)
            recipe_results.append(recipe_object)
        # import pdb;pdb.set_trace()

    return recipe_results