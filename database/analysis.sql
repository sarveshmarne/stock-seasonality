CREATE VIEW seasonal_returns AS
WITH season_bounds AS (
    SELECT
        "Stock",
        season,
        EXTRACT(YEAR FROM "Date") AS year,
        MIN("Date") AS start_date,
        MAX("Date") AS end_date
    FROM stock_seasons
    GROUP BY "Stock", season, EXTRACT(YEAR FROM "Date")
),
prices AS (
    SELECT
        b."Stock",
        b.season,
        b.year,
        CAST(s1."Close" AS FLOAT) AS start_price,
        CAST(s2."Close" AS FLOAT) AS end_price
    FROM season_bounds b
    JOIN stock_seasons s1
        ON b."Stock" = s1."Stock"
        AND b.start_date = s1."Date"
    JOIN stock_seasons s2
        ON b."Stock" = s2."Stock"
        AND b.end_date = s2."Date"
)

SELECT
    "Stock",
    season,
    year,
    (end_price - start_price) / start_price AS season_return
FROM prices;

SELECT * FROM seasonal_returns LIMIT 10;

SELECT 
    "Stock",
    ROUND( (AVG(season_return) * 100)::NUMERIC, 2 ) AS avg_festive_return
FROM seasonal_returns
WHERE season = 'Festive'
GROUP BY "Stock"
ORDER BY avg_festive_return DESC;

SELECT season, "Stock", avg_return
FROM (
    SELECT 
        season,
        "Stock",
        ROUND( (AVG(season_return) * 100)::NUMERIC, 2 ) AS avg_return,
        RANK() OVER (PARTITION BY season ORDER BY AVG(season_return) DESC) AS rnk
    FROM seasonal_returns
    GROUP BY season, "Stock"
) t
WHERE rnk = 1;