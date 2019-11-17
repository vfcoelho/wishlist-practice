-- create database wishlist;

-- drop table items;

-- create table items(
-- 	id serial primary key,
-- 	name varchar(250) not null,
-- 	reserved boolean default false
-- );

-- insert into items ("name") values 
-- ('Fralda'),
-- ('Carrinho'),
-- ('Roupas'),
-- ('Brinquedo');

-- select * from items

-- drop table items;

--#########################################;


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

create table guest_list(
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
	item_name varchar(256)
);


insert into "user" (email,"name") values ('test@test.com','Coelho dos Testes');

insert into "user" (email,"name") values ('test2@test.com','Tartaruga dos Testes');
insert into "user" (email,"name") values ('cavalo@test.com','Cavalo dos Testes');
-- insert into "user" (email,"name") values ('cachoorro@test.com','Cachorro dos Testes');

insert into list (list_name, user_id) values ('Segunda lista',2);

insert into guest_list (user_id,list_id) values (1,1);
-- insert into guest_list (user_id,list_id) values (3,1);
-- insert into guest_list (user_id,list_id) values (3,2);
-- insert into guest_list (user_id,list_id) values (4,2);

insert into item (list_id,item_name) values (1,'Jogo de Copos');

select * from "user"

select * from list

select * from guest_list

select * from list as l join guest_list as g on l.id = g.list_id 

select 
	l.id, 
	l.list_name 
from list as l 
join guest_list as g on l.id = g.list_id 
where 
	g.user_id = 2
