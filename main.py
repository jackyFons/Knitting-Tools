from flask import Flask, render_template, request
from yarn_scrape import search, details
import pandas as pd


# Reads data from file to display in the Home page
needle_df = pd.read_csv("data/needles.csv")
yarn_df = pd.read_csv("data/yarn.csv")
knit_df = pd.read_csv("data/knit_abbr.csv")
crochet_df = pd.read_csv("data/crochet_abbr.csv")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", needle_dfs=[needle_df.iloc[:12], needle_df[12:]], yarn_df=yarn_df,
                           knit_df=knit_df, crochet_df=crochet_df)


@app.route("/counter")
def counter():
    return render_template("counter.html", title="Counter")


@app.route("/calculators", methods=["GET", "POST"])
def calculators():
    return render_template("calculators.html")


@app.route("/yarn", methods=["GET", "POST"])
def yarn():
    if request.method == "POST":
        # Returns a list of potential yarns
        if request.form.get("search") == "search":
            yarn_name = request.form["yarn-name"]
            return render_template("yarn.html", name=yarn_name, yarn_list=search(yarn_name))
        # Returns current yarn and a list of substitute yarn
        elif request.form.get("details") == "Get Details":
            link = request.form.get("yarn")
            current_yarn, subs = details(link)
            return render_template("yarn-details.html", yarn=current_yarn, subs=subs)
    else:
        return render_template("yarn.html", name="red heart")


if __name__ == "__main__":
    app.run(debug=True)
