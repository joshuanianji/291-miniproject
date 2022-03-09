drop table if exists editors;
drop table if exists follows;
drop table if exists watch;
drop table if exists sessions;
drop table if exists customers;
drop table if exists recommendations;
drop table if exists casts;
drop table if exists movies;
drop table if exists moviePeople;

PRAGMA foreign_keys = ON;

create table moviePeople (
  pid		char(4),
  name		text,
  birthYear	int,
  primary key (pid)
);
create table movies (
  mid		int,
  title		text,
  year		int,
  runtime	int,
  primary key (mid)
);
create table casts (
  mid		int,
  pid		char(4),
  role		text,
  primary key (mid,pid),
  foreign key (mid) references movies,
  foreign key (pid) references moviePeople
);
create table recommendations (
  watched	int,
  recommended	int,
  score		float,
  primary key (watched,recommended),
  foreign key (watched) references movies,
  foreign key (recommended) references movies
);
create table customers (
  cid		char(4),
  name		text,
  pwd		text,
  primary key (cid)
);
create table sessions (
  sid		int,
  cid		char(4),
  sdate		date,
  duration	int,
  primary key (sid,cid),
  foreign key (cid) references customers
	on delete cascade
);
create table watch (
  sid		int,
  cid		char(4),
  mid		int,
  duration	int,
  primary key (sid,cid,mid),
  foreign key (sid,cid) references sessions,
  foreign key (mid) references movies
);
create table follows (
  cid		char(4),
  pid		char(4),
  primary key (cid,pid),
  foreign key (cid) references customers,
  foreign key (pid) references moviePeople
);
create table editors (
  eid		char(4),
  pwd		text,
  primary key (eid)
);
