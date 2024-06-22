<?php
// header('Content-Type: application/json');

$host = 'localhost';
$db = 'glot';
$user = 'postgres';
$pass = 'student';
$port = '5432';

$reg_name = $_GET['reg_name'] ?? '';

if (empty($reg_name)) {
    echo json_encode(['error' => 'Region name is required']);
    exit;
}

$conn = pg_connect("host=$host dbname=$db user=$user password=$pass port=$port");

if (!$conn) {
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

$query = "SELECT * FROM get_countries_after_reg($1)";
$result = pg_query_params($conn, $query, array($reg_name));

if (!$result) {
    echo json_encode(['error' => 'Query failed']);
    exit;
}

$data = pg_fetch_all($result);

if (is_array($data)) {
    echo json_encode($data);
} else {
    echo json_encode([]);
}

pg_close($conn);
