def routers(app):
    @app.route('/components/page/<string:name>', methods=['GET'])
    def page(name):
        print(name)
        return 'page'
    # return '111'