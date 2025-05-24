document.addEventListener("DOMContentLoaded", ()=>{

async function updating() {
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
};
updating();
async function homeCard(){
    const cardbody = document.getElementById("card");
    const successMsg = document.getElementById('successMsg');
    console.log('home page js is running ...')

        try {
            let response = await fetch("/audit_details");
            let data = await response.json();
            cardbody.innerHTML = "";
            console.log(data);
            data.forEach((item) => {
                let div1 = document.createElement("div");
                let div2 = document.createElement("div");
                let div3 = document.createElement("div");

                div2.innerHTML = `
                    <h2 class="text-xl font-bold mb-2"><span class="font-bold">Audit_Id:</span>${item.Audit_id}</h2>
                    <p><i class="fas fa-industry"></i> <span class="font-bold">Industry:</span> ${item.industry}</p>
                    <p><i class="fas fa-industry"></i> <span class="font-bold">Audit_type:</span> ${item.Audit_type}</p>
                    <p><i class="fas fa-calendar-alt"></i> <span class="font-bold">Date:</span> ${item.Date}</p>
                    <p><i class="fas fa-user"></i> <span class="font-bold">AuditAvenger per day:</span> ${item.Auditors_require}</p>
                    <p><i class="fas fa-clock"></i> <span class="font-bold">Day(s):</span> ${item.Days}</p>
                    <p><i class="fas fa-graduation-cap"></i> <span class="font-bold">Qualification:</span> ${item.Qualification}</p>
                    <p><i class="fas fa-laptop"></i> <span class="font-bold">Laptop:</span> ${item.equipment}</p>
                    <p><i class="fas fa-map-marker-alt"></i> <span class="font-bold text-red-500">Location:</span> ${item.loction}</p>
                    <p><i class="fas fa-dollar-sign"></i> <span class="font-bold">Compensation:</span> ${item.Amount}</p>
                `;

                div3.innerHTML = `
                    <button class="bg-yellow-500 text-black font-bold py-2 px-4 rounded w-full" >Apply Now</button>
               `;
               div3.addEventListener("click", async function () {
                    const data = {
                          audit_id: item.Audit_id,
                          whatsappLink: item.whatsappLink
                        };
                    try {
                        let response = await fetch('/apply/user_Details', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({data})
                        });
                        const contentType = response.headers.get('content-type');
                        if (contentType && contentType.includes('application/json')) {
                            const data = await response.json();
                            if (response.ok) {
                                console.log('Application Success:', data.message);
                                window.location.href = '/apply/user_Details';
                            } else {
                                console.error('Application Error:', data.error || data);
                                // You can redirect to login/register if needed here
                            }
                        } else {
                            const text = await response.text();
                            console.error('Unexpected response:', text);
                        }

                    } catch (err) {
                        console.error('Fetch failed:', err);
                    }
                })

               // Tailwind CSS classes
                div1.classList.add("flex", "flex-col", "justify-between", "bg-yellow-100", "rounded-lg", "shadow", "m-4", "overflow-hidden");
                div2.classList.add("p-4" ,"bg-gray-800");
                div3.classList.add("bg-gray-800", "p-4", "rounded-b-lg");

                // Nesting the elements properly
                div1.appendChild(div2);
                div1.appendChild(div3);
                cardbody.appendChild(div1);

            })
        }catch (error) {
            console.error("Error loading table data:", error);
        }

}
homeCard();

})