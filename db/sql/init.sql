create table if not exists nav(
    navid integer primary key autoincrement,
    navname varchar(255) not null,
    navpath varchar(255) not null,
    picpath varchar(255),
    picbase64 varchar(2000),
    openstatus tinyint default 1, -- 1 - 打开；0 - 关闭
    navtype tinyint default 0 -- 0 - 内网；1 - 外网 
);
create table if not exists settings(
    set_id integer primary key autoincrement,
    set_name varchar(255) not null,
    set_content varchar(5000) not null
);

insert into settings(set_name, set_content) 
    select 'system' as set_name , '{ "hosts": ["127.0.0.1"], "version": "0.0.0" }' as set_content
    from settings where not exists(select set_id from settings where set_name = 'system');

insert or ignore into settings(set_name, set_content) values('system', '{ "hosts": ["127.0.0.1"], "version": "0.0.0" }')