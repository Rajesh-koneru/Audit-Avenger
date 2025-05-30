document.addEventListener("DOMContentLoaded", function () {
    const cardbody = document.getElementById("card");
    const successMsg = document.getElementById('successMsg');

    async function loadTableData() {
        try {
            let response = await fetch("/audit_details");
            let data = await response.json();
            cardbody.innerHTML = "";
            console.log(data);
            data.forEach((item) => {
                let div1 = document.createElement("div");
                let div2 = document.createElement("ul");
                let div3 = document.createElement("div");
                let Date=localDate(item.Date);
                let status=openAudits(item.Date);
                console.log('new date is :'+Date)

                div2.innerHTML = `
                    <h2 class=" flex justify-between text-xl font-bold mb-2 "><span class="font-bold mr-2 text-yellow-500">Audit Id: ${item.Audit_id} </span><span class="bg-green-700 text-white text-[10px] font-semibold px-2 py-[2px] rounded select-text  ${status === 'Urgent' ? 'bg-red-600 ' : 'bg-green-500 '}">${status}</span></h2>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-industry text-yellow-500 mr-2"></i>Industry:</span> <span> ${item.industry}</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-industry text-yellow-500 mr-2"></i>Audit Type:</span> <span>${item.Audit_type}</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-calendar-alt mr-2 text-yellow-500"></i> Date:</span><span> ${Date}</span></li>
                    <li class="flex justify-between" ><span class="font-bold"><i class="fas fa-user mr-2 text-yellow-500"></i>AuditAvenger per day:</span> <span>${item.Auditors_require} Auditor(s) require</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-clock mr-2 text-yellow-500"></i>Day(s):</span><span> For ${item.Days} day</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-graduation-cap mr-2 text-yellow-500"></i>Qualification:</span><span> ${item.Qualification}</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-laptop mr-2 text-yellow-500"></i>Laptop:</span> <span>${item.equipment}</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-map-marker-alt mr-2 text-yellow-500"></i> Location:</span><span> ${item.loction}</span></li>
                    <li class="flex justify-between"><span class="font-bold"><i class="fas fa-dollar-sign mr-2 text-yellow-500"></i>Compensation:</span><span> ${item.Amount}/- per Day</span></li>
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
                div2.classList.add("p-4" ,"bg-gray-800","space-y-2");
                div3.classList.add("bg-gray-800", "p-4", "rounded-b-lg");

                // Nesting the elements properly
                div1.appendChild(div2);
                div1.appendChild(div3);
                cardbody.appendChild(div1);


            });
        } catch (error) {
            console.error("Error loading table data:", error);
        }
    }



    loadTableData();
});


//function for loading correct date
function localDate(rawDate) {
  const date = new Date(rawDate);

  // Check if the date is valid
  if (isNaN(date.getTime()) || date.getFullYear() <= 1) {
    return "1/1/2023"; // fallback for bad or default .NET date
  }

  return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
}

//function for show urgent requirement status

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