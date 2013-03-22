INSERT INTO `stats_instrument` (`id`, `metric_id`, `name`, `slug`, `annotations`, `aggregations`, `values`, `width`, `domain`, `units`)
VALUES
    (1, 1, 'Online Users', 'online-users', '[]', '[{\"name\":\"max\",\"func\":\"Max\",\"attr\":\"value\"}]', '[\"max\"]', 180, 86400, 'users'),
    (2, 7, 'Total Users', 'total-users', '[]', '[{\"name\":\"max\",\"func\":\"Max\",\"attr\":\"value\"}]', '[\"max\"]', 180, 86400, 'users'),
    (8, 10, 'Request Throughput', 'request-throughput', '[]', '[{\"name\":\"sum\",\"func\":\"Sum\",\"attr\":\"value\"}]', '[\"sum\"]', 180, 86400, 'requests'),
    (7, 9, 'Question Appears', 'question-appears', '[]', '[{\"name\":\"avg\",\"func\":\"Avg\",\"attr\":\"value\"}]', '[\"avg\"]', 180, 86400, 'ms'),
    (9, 11, 'API Response Time', 'api-response-time', '[]', '[{\"name\":\"avg\",\"func\":\"Avg\",\"attr\":\"value\"}]', '[\"avg\"]', 180, 86400, 'ms'),
    (10, 12, 'EPublisher Response Time', 'epublisher-response-time', '[]', '[{\"name\":\"avg\",\"func\":\"Avg\",\"attr\":\"value\"}]', '[\"avg\"]', 180, 86400, 'ms'),
    (12, 14, 'Daily Users', 'daily-users', '[]', '[{\"name\":\"max\",\"func\":\"Max\",\"attr\":\"value\"}]', '[\"max\"]', 86400, 31536000, 'users'),
    (13, 16, 'Monthly Users', 'monthly-users', '[]', '[{\"name\":\"max\",\"func\":\"Max\",\"attr\":\"value\"}]', '[\"max\"]', 2419200, 116121600, 'users'),
    (14, 13, 'Exceptions', 'exceptions', '[]', '[{\"name\":\"sum\",\"func\":\"Sum\",\"attr\":\"value\"}]', '[\"sum\"]', 180, 86400, 'exceptions');
