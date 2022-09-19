from request2postman.collection import Collection


def request_to_postman_hook(collection: Collection):
    def hook(response, *args, **kwargs):
        collection.add_request(response.request)
        return response
    return hook
