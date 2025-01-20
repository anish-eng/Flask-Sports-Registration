document.addEventListener('click', function (event) {

	// If the clicked element isn't our show password checkbox, bail
	if (event.target.id !== 'check') return;

	// Get the password field
	var password = document.querySelector('#password');
	if (!password) return;

	// Check if the password should be shown or hidden
	if (event.target.checked) {
		// Show the password
		password.type = 'text';
	} else {
		// Hide the password
		password.type = 'password';
	}

}, false);