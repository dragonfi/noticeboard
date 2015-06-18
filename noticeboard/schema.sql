drop table if exists Notes;
create table Notes (
    id integer primary key autoincrement,
    text text not null,
    created date not null,
    updated date
);
