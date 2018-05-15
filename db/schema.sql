drop table if exists news;
create table news (
  id integer primary key autoincrement,
  news_id char(20) not null UNIQUE,
  title char(100) not null,
  source_url char(50),
  source_name char(50),
  source_ico char(50),
  author char(50),
  read_count integer
);