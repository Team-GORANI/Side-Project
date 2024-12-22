import reflex as rx
from pages.index import index

# Configure the application
config = rx.Config(
    app_name="HTP Analysis",
    app_title="HTP Analysis App",

    # Define the directory where your assets will be stored
    assets_dir="assets",
    port=3000,
    reload=True
)

# Create the app instance
app = rx.App(state=rx.State)

# Add pages to the app
app.add_page(
    route="/",
    component=index,
    title="HTP Analysis"
)

if __name__ == "__main__":
    app.compile()
