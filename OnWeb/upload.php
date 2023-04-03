<?php
if (isset($_FILES['image'])) {
    $uploadDirectory = '';
    $fileName = 'img.png';
    $filePath = $uploadDirectory . $fileName;
    if (move_uploaded_file($_FILES['image']['tmp_name'], $filePath)) {
        echo 'Image uploaded to server.';
    } else {
        echo 'An error has occurred';
    }
}
