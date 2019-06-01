import json

import aiohttp
from sanic import Sanic
from sanic import response

app = Sanic()


@app.route('/api/login', methods=frozenset({"GET"}))
async def login(request):
    return response.redirect("https://github.com/login/oauth/authorize?client_id=910b187636bfb3f33ac9&redirect_uri=http://127.0.0.1:8000/oauth/redirect")


@app.route("/oauth/redirect")
async def oauth_code(request):
    code = request.args['code'][0]
    token_url = "https://github.com/login/oauth/access_token"
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, json={"client_id": "910b187636bfb3f33ac9",
                                                 "client_secret": "b426ca8d5a34cdc744566c1d6a331d44efbb41dd",
                                                 "code": code}) as resp:

            token = await resp.text()
            rsp_json = {each.split('=')[0]: each.split('=')[1] for each in token.split('&')}
            return response.json(rsp_json)

if __name__ == "__main__":
    app.run()
