-- is psql database
create TABLE allHeadlines (id int primary key, newsOrg varchar(8), title text unique, articleDate date, articleTime time);
create TABLE properNouns (id int primary key, fullName text unique, type varchar(10)); -- type can be place, person, or organization
create table acronyms(acronym text unique, id int);
create table abbreviations(abbrevation text unique, text fullName);
create table nicknames(nickname text unique, id int, foreign key(id) references properNouns(id));
create table NORPs(shortName text unique, id int, foreign key(id) references properNouns(id)); -- maps people of ethnicity ('NORPS' in spaCy) to their Countries/Cities
create table headlinePnouns(headlineId int , pNounId int, foreign key(headlineId) references allHeadlines(id), foreign key(pNounId) references properNouns(id));
create table Topics(clusterId Serial primary key, keywords text, numTweets int, avg_rating double precision);

