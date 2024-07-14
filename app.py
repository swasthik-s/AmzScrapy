from flask import Flask
from modules.routes import index, download_file  # Import the routes

app = Flask(__name__)
app.secret_key = 'your_secret_key'  #Required for session management

# Register routes
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/download', view_func=download_file)

if __name__ == '__main__':
    app.run(debug=True)
