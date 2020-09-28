"""
-- 统计这个表中有多少行记录
select count(1) from tb_lemon_index;
-- 抽查：limit结果的限制
select * from tb_lemon_index LIMIT 800000,10;
-- id:主键，唯一标识  s_name:学生名  phone:手机号  c_name:班级名称
-- 800010  Tom_800010   13094524819  800010期
select * from tb_lemon_index where phone='13094524819';
-- 0.472s 这个是非常简单的查询语句：单表、单条件
select * from tb_lemon_index where id=800010;
-- 0.001 ：这个主键 --》主键索引--》最常使用的（查询、关联）

-- 手机号查询这种场景非常
-- 登录：输入手机号、密码--》数据库中匹配（查询）
-- 为phone字段建立一个索引
-- CREATE INDEX 索引名称 ON 表名(字段名);
create index idx_phone on tb_lemon_index(phone);

select * from tb_lemon_index where phone='13094524819';
-- 0.005s
-- 0.472s
-- select 0.472/0.005;

-- 800010  Tom_800010   13094524819  800010期
-- select * from tb_lemon_index where phone='13094524819' or s_name='Tom_800010';

-- 创建一个组合索引
create index idx_name_phone_cname on tb_lemon_index(s_name,phone,c_name);

DROP INDEX idx_phone ON tb_lemon_index;

select * from tb_lemon_index where phone='13094524819'; -- 有没有使用索引？？？
select * from tb_lemon_index where s_name='Tom_800010'; -- ？？？
-- 最左前缀
select * from tb_lemon_index where s_name='Tom_800010' and phone='13094524819';
select * from tb_lemon_index where c_name='800010期' and phone='13094524819';
select * from tb_lemon_index where s_name='Tom_800010' and c_name='800010期' and phone='13094524819';

-- 看一下sql语句的执行计划
EXPLAIN select * from tb_lemon_index where s_name='Tom_800010' and phone='13094524819';
EXPLAIN select * from tb_lemon_index where c_name='800010期' and phone='13094524819';
EXPLAIN select * from tb_lemon_index where s_name='Tom_800010' and c_name='800010期' and phone='13094524819';

"""
