-- is psql database
create TABLE allHeadlines (id SERIAL primary key, newsOrg varchar(8), title text unique, articleDate date, articleTime time);
create TABLE famouspeople(id serial primary key, level int, lastname text, firstname text, description text);
create table places(id SERIAL primary key, pname text, realName text unique); -- real name is for case of synonyms (ex. America, USA, United States
create table organizations(id serial primary key, orgname text unique, abbreviation text);
create table headlinePlaces(headlineId int , placeId int, foreign key(headlineId) references allHeadlines(id), foreign key(placeId) references places(id));
create table headlinepeople(headlineId int , personId int, foreign key(headlineId) references allHeadlines(id), foreign key(personId) references famouspeople(id));
create table headlineOrgs(headlineId int , orgId int, foreign key(headlineId) references allHeadlines(id), foreign key(orgId) references organizations(id));
create table Clusters(clusterId Serial primary key, keywords text, numTweets int, avg_rating double precision);


--create table properNouns(name text, level int, acronym VARCHAR(15), primary key(name, level));
create table lastnames(name text unique, ranking int);
create table firstNames(name text unique, ranking int);
