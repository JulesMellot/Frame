const form = document.getElementById('json-form');

form.addEventListener('submit', function(event) {
	event.preventDefault();

	const data = {
		function: form.elements['function'].value
	};

        fetch('api/function', {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + window.FrameConfig.API_TOKEN
                },
                body: JSON.stringify(data)
        })
	.then(function(response) {
		return response.json();
	})
        .then(function(json) {
                console.log(json);
                Toastify({
                        text: t('functionUpdated'),
                        duration: 3000,
                        gravity: "top",
                        close: "true",
                        position: "right"
                  }).showToast();
        })
	.catch(function(error) {
		console.error(error);
	});
});

