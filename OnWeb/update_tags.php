<?php
// Read the JSON data sent in the request body
$data = json_decode(file_get_contents('php://input'), true);

//Update JSON file
file_put_contents('tags.json', json_encode($data));

// Send a response
header('Content-Type: application/json');
echo json_encode(['success' => true]);
?>
