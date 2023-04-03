<?php
// Read the JSON data sent in the request body
$data = json_decode(file_get_contents('php://input'), true);

// Check that the data sent is valid
if (isset($data['function']) && in_array($data['function'], ['DeviantArt', 'plex', 'fixed'])) {
	// Update JSON file
	file_put_contents('function.json', json_encode($data));
}

// Send a response
header('Content-Type: application/json');
echo json_encode(['success' => true]);
?>
