-- is psql database
create TABLE allHeadlines (newsOrg varchar(8), title text unique, articleDate date, articleTime time, constraint primary key(newsOrg, title));
