from flask import Flask, request, jsonify
from search import search
import html
from filter import Filter
from storage import DBstorage
app = Flask(__name__)

styles = """
<style>
.site{
    font-size: .8rem;
    color: green;
}
.snippet{
    font-size: .9rem;
    color: gray;
    margin-bottom: 30px;
    
}

.rel-button{
    cursor: pointer;
    color: blue;
    
}
</style>

<script>

const relevant = function (query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "query": query,
            "link": link
        })
    });
}
</script>

"""

search_template =  styles + """

<form actions= "/" method="post">
    <input type="text" name="query">
    <input type="submit" value="Search">
</form>

"""

result_template = """
<p class="site">{rank}: {link} <span class="rel-button"  onclick='relevant("{query}", "{link}");'>Relevant </span></p>
<a href = "{link}">{title}</a>
<p class ="snippet">{snippet}</p>

"""

# Our deafult route
# Get methods gets the html data and post send data
@app.route("/", methods=["GET", "POST"])

def search_form():
    if request.method == "POST":
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()
    
def run_search(query):
    results = search(query)
    fi = Filter(results)
    results = fi.filter()
    renderd = search_template
    results["snippet"] = results["snippet"].apply(lambda x : html.escape(x))
    for index, row in results.iterrows():
        renderd += result_template.format(**row)
    return renderd

def show_search_form():
    return search_template


# this method shows the relevancy 
@app.route("/relevant", methods = ["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data ["link"]
    storage = DBstorage()
    storage.update_relevance(query, link,10)
    return jsonify(sucess= True)
    
    