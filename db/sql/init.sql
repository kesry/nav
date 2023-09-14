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

insert or ignore into settings(set_name, set_content) values('system', '{ "hosts": [], "version": "0.0.0", "activehost": "" }')