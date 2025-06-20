from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

# Tambahkan endpoint GraphQL
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)