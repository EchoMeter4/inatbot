import aiohttp


# Gets the images of the wasp from the iNaturalist API
async def find(name):
    image_url = []

    api_version = 1
    api_base_url = f"https://api.inaturalist.org/v{api_version}/"
    endpoint_path = f"taxa?q={name}"
    endpoint = f"{api_base_url}{endpoint_path}"  # ?api_key={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            if response.status == 404:
                print("Something went wrong")
                return

            file = await response.json()

    result = file.get('results')
    count = 0
    id_ = result[0]['id']
    leng = len(result)

    for i in range(leng):
        for x in result[i]:
            if x == "default_photo" and count < 4:
                count = count + 1

    for i in range(count):
        body = result[i]
        default_photo = body['default_photo']
        id_ = body['id']
        url = default_photo['medium_url']
        image_url.append(url)
    return {'id': id_, 'image_list': image_url}
