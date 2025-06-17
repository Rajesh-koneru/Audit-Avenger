document.addEventListener("DOMContentLoaded", () => {
    async function updating() {
    const Getbtn = document.getElementsByClassName("toggle")[0];
        if (!Getbtn) {
            console.warn("Element with ID 'get' not found.");
            return;
        }

        try {
            const response = await fetch("/user/home_page", {
                method: 'GET',
                credentials: 'include'  // ✅ This sends the session cookie!
            });

            const data = await response.json();
            const status = data['status'];
            const role = data['role'];
            const username = data['username'];  // Ensure your backend sends this

            console.log(status);

            if (status === 'logged_in' && role === 'admin') {
                Getbtn.innerText = 'Dashboard';
                Getbtn.setAttribute('href', '/admin/dashboard');
                console.log('Redirect set to admin dashboard.');
            } else if (status === 'logged_in' && role === 'auditor') {
                Getbtn.innerText = 'Dashboard';
                Getbtn.setAttribute('href', `/auditor_page/${username}`);
                console.log('Redirect set to auditor page.');
            } else {
                Getbtn.innerText = 'Get Started';
                Getbtn.setAttribute('href', '/signup_page');
            }

        } catch (error) {
            console.error("Error fetching user status:", error);
            Getbtn.innerText = 'Get Started';
            Getbtn.setAttribute('href', '/signup_page');
        }
    }

    updating();
});
