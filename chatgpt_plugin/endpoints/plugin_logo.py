from quart import send_file

@app.route('/logo.png')
async def plugin_logo():
    return await send_file('path/to/logo.png', mimetype='image/png')
