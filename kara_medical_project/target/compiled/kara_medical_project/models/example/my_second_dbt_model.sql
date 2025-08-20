-- Use the `ref` function to select from other models

select *
from "kara_medical_db"."public"."my_first_dbt_model"
where id = 1