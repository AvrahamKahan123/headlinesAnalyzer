-- is psql database
create TABLE allHeadlines (id SERIAL primary key, newsOrg varchar(8), title text unique, articleDate date, articleTime time);
-- id is unused column; may be used later
create TABLE famouspeople(level int, lastname text, firstname text, description text, primary key(id, lastname, firstname));
create table places(id SERIAL primary key, pname text, realName text); -- real name is in case of synonyms
create table properNouns(name text, level int, acronym VARCHAR(15), primary key(name, level));
create table lastnames(name text, ranking int);
create table firstNames(name text, ranking int);
create table organizations(id serial primary key, orgname text, abbreviation text);