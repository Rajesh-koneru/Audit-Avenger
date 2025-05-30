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

                let Date=localDate(item.Date);
                let status=openAudits(item.Date);
                console.log('new date is :'+status);

                div2.innerHTML = `
                    <h2 class="flex justify-between text-xl font-bold mb-2 "><span class="font-bold mr-2">Audit_Id: ${item.Audit_id} </span><span class="bg-green-700 text-white text-[10px] font-semibold px-2 py-[2px] rounded select-text  ${status === 'Urgent' ? 'bg-red-600 ' : 'bg-green-500 '}">${status}</span></h2>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-industry text-yellow-500 mr-2"></i>Industry:</span> <span class="text-xs md:text-base lg:text-lg"> ${item.industry}</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-industry text-yellow-500 mr-2"></i>Audit_type:</span> <span class="text-xs md:text-base lg:text-lg">${item.Audit_type}</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-calendar-alt mr-2 text-yellow-500"></i> Date:</span><span class="text-xs md:text-base lg:text-lg"> ${Date}</span></li>
                    <li class="flex justify-between" ><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-user mr-2 text-yellow-500"></i>AuditAvenger per day:</span class="text-xs md:text-base lg:text-lg"> <span>${item.Auditors_require} Auditor(s) require</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-clock mr-2 text-yellow-500"></i>Day(s):</span><span class="text-xs md:text-base lg:text-lg"> For ${item.Days} day</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-graduation-cap mr-2 text-yellow-500"></i>Qualification:</span><span class="text-xs md:text-base lg:text-lg"> ${item.Qualification}</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-laptop mr-2 text-yellow-500"></i>Laptop:</span> <span class="text-xs md:text-base lg:text-lg">${item.equipment}</span></li>
                    <li class="flex justify-between"><span class="font-bold text-xs md:text-base lg:text-lg"><i class="fas fa-map-marker-alt mr-2 text-yellow-500"></i> Location:</span><span class="text-xs md:text-base lg:text-lg text-right"> ${item.loction}</span></li>
                    <li class="flex justify-between"><span class="font-bold text-sm md:text-base lg:text-lg"><i class="fas fa-dollar-sign mr-2 text-yellow-500"></i>Compensation:</span><span class="text-xs md:text-base lg:text-lg"> ${item.Amount}/- per Day</span></li>
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
                div1.classList.add("flex", "flex-col", "justify-between", "bg-yellow-100", "rounded-lg", "shadow", "m-4", "overflow-hidden","border-t-[10px]","border-t-yellow-500");
                div2.classList.add("p-4" ,"bg-gray-800" ,"space-y-2");
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

});

function openAudits(auditDateStr){

    const auditDate = new Date(auditDateStr);
    const today = new Date();

    const diffTime = today - auditDate;
    const diffDays = diffTime / (1000 * 60 * 60 * 24); // milliseconds to days

    const status =  Math.trunc(diffDays) <= 0 ? "Urgent" : "Open";

    console.log(diffDays)

    console.log("Status:", status);
    return status
}
function localDate(rawDate) {
  const date = new Date(rawDate);

  // Check if the date is valid
  if (isNaN(date.getTime()) || date.getFullYear() <= 1) {
    return "1/1/2023"; // fallback for bad or default .NET date
  }

  return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
}