insert into lastNames select lastname from famouspeople on conflict do nothing; -- may create duplicate entries, which is fine since lastNames is to be treated as a set
insert into firstNames select firstname from famouspeople on conflict do nothing;
