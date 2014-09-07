drop table if exists entries;
drop table if exists menu;

create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

create table menu (
  id integer primary key autoincrement,
  name text not null,
  url text not null
);
