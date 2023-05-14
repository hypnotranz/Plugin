from quart import send_file

@app.route('/logo.png')
async def plugin_logo():
    return await send_file('logo.png', mimetype='image/png')
