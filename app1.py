from flask import Flask, render_template, request
from scraper import scrape_events_with_selenium  # Import the updated scraper function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    events = []
    query = ""  # Initialize query variable
    
    if request.method == "POST":
        location = request.form.get("location")
        interests = request.form.get("interests")
        
        # Generate search query
        query = f"Find all non-profits related to {interests} in {location} (libraries, museums, hospitals, universities, parks, health centers, educational institutions, etc.)."
        
        # Scrape events and include the location for fallback images
        events = scrape_events_with_selenium(query, location)
        
    return render_template("index.html", events=events, search_query=query)

if __name__ == "__main__":
    app.run(debug=True)
