async function sendMail() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('mail').value.trim();
    const message = document.getElementById('msg').value.trim();

    console.log("Sending Message:", message);

    if (!name || !email || !message) {
        alert("All fields are required!");
        return;
    }

    try {
        let response = await fetch('https://finalavengers.onrender.com/admin/report', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 'SenderName': name, "Email": email, "Message": message })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        let msg = await response.json();
        console.log("Server Response:", msg.message);
        alert(msg.message);

    } catch (error) {
        console.error("Error sending mail:", error);
        alert("Failed to send mail. Please try again later.");
    }
}

document.getElementById('mailBtn').addEventListener('click', sendMail);
