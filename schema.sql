drop table if exists entries;
drop table if exists menu;

create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  published bit not null,
  author tinyint not null,
  published_time timestamp not null
);

create table authors (
	id interger primary key autoincrement,
	name text not null
);

create table menu (
  id integer primary key autoincrement,
  name text not null,
  url text not null
);
