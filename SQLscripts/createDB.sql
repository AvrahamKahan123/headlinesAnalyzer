-- is psql database
create extension if not exists "uuid-ossp";
create TABLE allHeadlines (articleID UUID default uuid_generate_v1() primary key, newsOrg varchar(8), title text unique, articleDate date, articleTime time);
