// Function for registration
async function register(event) {
    event.preventDefault();  // Prevent form reload if inside <form>

    const name = document.getElementById('name').value;
    const mail = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;

    if (!name || !mail || !phone) {
        alert("All fields are required.");
        return;
    }

    try {
        const response = await fetch('/apply/audit_application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: mail,
                phone: phone
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        alert(data['message']);
        window.location.href = data['link'];

    } catch (error) {
        console.error('Error during registration:', error);
        alert('Failed to register. Please try again.');
    }
}

// Calling function
document.getElementById('button').addEventListener('click', register);
