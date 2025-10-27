select
    zip_code,
    population
from {{ source('raw', 'zip_population') }}
