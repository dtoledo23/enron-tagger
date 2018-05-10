SELECT
	date_trunc('day', tags.datetime) AS day,
	SUM(tags.case) AS points
FROM (
	SELECT
	datetime,
	CASE WHEN tag='positive' THEN 1
		WHEN tag='negative' THEN -1
		ELSE 0
    END
    FROM sentiment_timeline
)  AS tags
GROUP BY day
ORDER BY day;
