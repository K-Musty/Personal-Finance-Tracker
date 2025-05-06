from app import create_app

app = create_app()

# Register blueprint after app creation
from app.routes import bp
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)