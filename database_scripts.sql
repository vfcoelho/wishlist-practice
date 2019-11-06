create database wishlist;

drop table items;

create table items(
	id serial primary key,
	name varchar(250) not null,
	reserved boolean default false
);

insert into items ("name") values 
('Fralda'),
('Carrinho'),
('Roupas'),
('Brinquedo');

select * from items

--#########################################


create table "user"(
	id serial primary key,
	email varchar(256) not null,
	name varchar(256) not null
);

create table list(
	id serial primary key,
	user_id int
		references "user" on delete restrict,
    list_name varchar(256)
);

create table gest_list(
	id serial primary key,
	user_id int
		references "user" on delete restrict,
    list_id int
		references list on delete restrict
);

create table item(
	id serial primary key,
	guest_id int
		references "user" on delete restrict,
    list_id int
		references list on delete restrict,
	name varchar(256)
);

drop table items;
