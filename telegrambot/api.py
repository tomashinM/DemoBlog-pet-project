import openapi_client.api as api_module


class API:
    def __init__(self, client):
        self.articles = api_module.ArticlesApi(client)
        self.profiles = api_module.ProfilesApi(client)
        self.tags = api_module.TagsApi(client)
        self.user = api_module.UserApi(client)
        self.users = api_module.UsersApi(client)
        self.search = api_module.SearchApi(client)
