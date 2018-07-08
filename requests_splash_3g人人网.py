import requests
cookie = "3g人人网的cookie，由Chrome手动截取"

script = """
splash.images_enabled = false
splash:set_custom_headers{
    ["Cookie"] = (args.cookie)
    }
splash:go(args.url)
return splash:html()
"""
resp = requests.post('http://localhost:8050/run', json={
    'lua_source': script,
    'url': url,
    'cookie':cookie
})
png_data = resp.text


id = '7738342928'
if id in str(png_data):
    print('ok')
else:
    print('not in html source')
