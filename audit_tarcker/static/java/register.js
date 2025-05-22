// Function for registration
async function register() {
    let name = document.getElementById('name').value;
    let mail = document.getElementById('email').value;
    let phone = document.getElementById('phone').value;

    try {
        let response = await fetch('/apply/audit_application', {
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
        let data = await response.json();
        alert(data['message']);
        window.location.href =data['link'];
    } catch (error) {
        console.error('Error during registration:', error);
        alert('Failed to register. Please try again.');
    }
}

// Calling function
document.getElementById('button').addEventListener('click', register);
