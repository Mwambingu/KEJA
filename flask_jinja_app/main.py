#!/usr/bin/env python3
from website import create_app
from website.views import views
from website.auth import auth
app = create_app()
app.register_blueprint(views)
app.register_blueprint(auth)


if __name__ == "__main__":
    app.run(debug=True)
