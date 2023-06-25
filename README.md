# Knitting Tools

A very simple knitting and crocheting web application created using Flask. I wanted to this application to be a helpful tool I would use regularly for my fiber arts projects.

## Run Locally

Clone the project

```bash
  git clone https://github.com/jackyFons/Knitting-Tools.git
```

Go to the project directory

```bash
  cd Knitting-Tools
```

Install dependencies

```bash
  pip install -r requirements.txt
```



## This webpage offers various useful features for knitting and crocheting enthusiasts:

- Comprehensive details on needle and hook sizes, yarn weights, and pattern abbreviations.
- A convenient search tool to find yarn substitutions.
- Row and stitch counters, accompanied by an optional table to track completed rows.
- A dedicated page for frequently used calculations in knitting and crocheting.
## Lessons Learned

For one of the web pages, my goal was to utilize an existing website to fetch yarn substitutions. This led me to explore web scraping using Python and the BeautifulSoup library.

My biggest obstacles came in the form of elements generated dynamically with JavaScript, which had a wait time before they could be scraped. After a bit of research and trial and error, I managed to overcome this challenge by implementing Selenium. This allowed me to effectively interact with the website and extract the necessary elements.