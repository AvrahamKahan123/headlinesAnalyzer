-- is psql database
create TABLE allHeadlines (newsOrg varchar(8), title text unique, articleDate date, articleTime time, constraint primary key(newsOrg, title));
-- id is unused column; may be used later
create TABLE famouspeople(level int, lastname text, firstname text, description text, primary key(id, lastname, firstname));
create table countries(id int, cname varchar(33), primary key(cname));