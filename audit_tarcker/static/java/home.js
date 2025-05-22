document.addEventListener("DOMContentLoaded", async function () {
    const Getbtn = document.getElementById("get");

    try {
        const response = await fetch("/user/home_page",{
            method: 'GET',
            credentials: 'include'  // ✅ This sends the session cookie!
        });
        let data = await response.json();
        let status = data['status'];
        console.log(status);
        if (status === 'logged_in') {
            Getbtn.innerText = 'Dashboard';  // <- fixed assignment
            Getbtn.setAttribute('href', '/admin/dashboard');
            console.log('Attribute changed...');
        } else {
            Getbtn.innerText = 'Get Started';  // <- fixed assignment
            Getbtn.setAttribute('href', '/signup_page');
        }
    } catch (error) {
        console.error("Error fetching user status:", error);
        Getbtn.innerText = 'Get Started';
        Getbtn.setAttribute('href', '/signup_page');
    }
});
