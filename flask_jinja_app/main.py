#!/usr/bin/env python3
from website import create_app
from website.views import views

app = create_app()
app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True)