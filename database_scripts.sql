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