document.addEventListener("DOMContentLoaded", async function () {
    const Getbtn = document.getElementById("get");

    try {
        const response = await fetch("/user/home_page",{
            method: 'GET',
            credentials: 'include'  // ✅ This sends the session cookie!
        });
        let data = await response.json();
        let status = data['status'];
        let role=data['role']
        console.log(status);
        alert(status)
        if (status === 'logged_in' && role == 'admin') {
            Getbtn.innerText = 'Dashboard';  // <- fixed assignment
            Getbtn.setAttribute('href', '/admin/dashboard');
            console.log('Attribute changed...');
        } else if( status === 'logged_in' && role =='auditor') {
            Getbtn.innerText = 'Dashboard';  // <- fixed assignment
            Getbtn.setAttribute('href', '/auditor_page/<username>');
            console.log('Attribute changed...');
        }else {
            Getbtn.innerText = 'Get Started';
            Getbtn.setAttribute('href', '/signup_page');

        }
    } catch (error) {
        console.error("Error fetching user status:", error);
        Getbtn.innerText = 'Get Started';
        Getbtn.setAttribute('href', '/signup_page');
    }
});
