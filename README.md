# headlinesAnalyzer
Currently incomplete (~75% done). News and Twitter analyzer using python Natural Language Processing Modules and ElasticSearch. Attempts to create over time a tracker for topics, how many articles there are about that topic, and how people are tweeting about that topic
# explanation
Flow chart for program can be found by clicking by viewing flow_chart.pdf
See overview.txt for full explanation of program structure module by module and explanation of design decisions
This program attempts to understand the interaction between the news, news sites and social media. 
First, it scrapes several news-sites using BeautifulSoup and saves these results to a PostgreSQL db. The programs are then parsed and analyzed with the help of the spaCy machine learning module and precreated postgres tables to extract related names, places, and organizations. Then, the program extracts topics with the help of the Latent Dirchet Allocation algorithm from Scikit-learn. The topics are then indexed by elasticsearch. The article headlines are then mapped to the topics by searching against the topics. Elasticsearch is used to do this, instead of just seeing how LDA constructed its topics, because Elasticsearch is more capable of providing similarity scores and determining whether a document truly belongs to a topic cluster. At this point the Twitter API is used to generate streams of tweets filtered on keywords in the topics (ex. "BLM", "Police" and "Portland" could be keywords for one topic). These tweets are then sentiment analyzed (ie. are the tweets positive or negative) with the help of the TextBlob module. These results are then stored in postgreSQL for easy retrieval whenever desired. 
New topics are generated from scratch every set time interval, and during that interval new headlines can be classified by searching their titles against the topics index
The program makes use of a great deal of data to parse the Headlines for names and places. This data is stored mostly in postgreSQL tables. This data is neccesary since testing showed that Machine Learning modules are usually not very good at telling the difference between last names, organizations, and places (ex. in one test, "Biden" was characterized as a 'geopolitical entity')
The program adds values and names to the database by scraping the web (this feature is complete for names already) automatically
The program also indexes title names so to make them searchable. Signifigant modification to the DB schema has been done recently, so some small bits of the code may still be illogical

# current state
Most of the code to complete every individual task (parse the headlines, extract the topics with LDA, index the Topics, search the headlines against the topics, get the tweets with the Twitter API, extract places, people and organizations from the Headlines) is complete, yet they are not yet linked together to complete the pipeline. Basic unit tests have verified some components

# current Issues 
Work will be done to make addditons to postgres thread-safe (now it relies on just grabbing the next highest available integer for id before a bulk insert, which is dangerous, for obvious reasons, unless the query for the next available integer is coupled with the inserts which is not always possible). Testing will begin in rigor soon on the whole project

