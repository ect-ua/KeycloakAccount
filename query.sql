create table ectua_newusers(
	id  serial primary key,
	fullname  text,
   	email text not null,
	nmec int,
	ano_matricula int,
	register_token text not null unique,
	username text);

