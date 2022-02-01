select   EqSt.id_point as id_point, m.id_legal as id_legal ,l."name" as servicename ,SUM(m.sum_income /100) as sumincome
 from equipment_status EqSt
left join points P on EqSt.id_point = P.id_point
left join operations.master m on EqSt.id_legal = m.id_legal 
left join legals l on m.id_legal = l.id_legal 
where m.state =60 and m.substate = 0 and P.point_type=0 and m.time_point between date_trunc('day', CURRENT_DATE -1) and date_trunc('day', CURRENT_DATE)
group by 1,2,3
order by 1
