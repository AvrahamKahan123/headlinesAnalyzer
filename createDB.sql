create extension if not exists "uuid-ossp";
create TABLE allHeadlines (articleID UUID default uuid_generate_v1() primary key, newsOrg varchar(8), title text, articleDate date, articleTime time);
