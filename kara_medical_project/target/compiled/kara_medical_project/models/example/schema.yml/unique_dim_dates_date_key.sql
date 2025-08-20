
    
    

select
    date_key as unique_field,
    count(*) as n_records

from "kara_medical_db"."public_marts"."dim_dates"
where date_key is not null
group by date_key
having count(*) > 1


