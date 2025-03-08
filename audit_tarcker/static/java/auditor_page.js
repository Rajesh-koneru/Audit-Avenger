document.addEventListener("DOMContentLoaded"  ,async function(){
        let name=document.querySelector('.name');
        let tableBody=document.querySelector('.tbody');



        let response=await fetch("https://finalavengers.onrender.com/auditor/auditor_details")
        let data=await response.json()


        auditorName=data['username']

        name.innerText=auditorName;
        async function fetchData(){
            try{
                response=await fetch("https://finalavengers.onrender.com/auditor/data" ,{
                       method:'POST',
                       headers: {
                        "Content-Type": "application/json"
                    },
                    body :JSON.stringify({ "name": auditorName})
                })

                // checking if response is okay or not
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
                }

                // getting response
                   data= await response.json()


                   tableBody.innerHTML = ""; // Clear table before loading new data
                   data.forEach((item) => {
                        let row = document.createElement("tr");

                        // If in Update Mode, make 'audit_status' editable
                        row.innerHTML = `
                            <td class="py-2 px-4">${item.Audit_id}</td>
                            <td class="py-2 px-4">${item.auditor_name}</td>
                            <td class="py-2 px-4">${item.planned_date}</td>
                            <td class="py-2 px-4">${item.state}</td>
                            <td class="py-2 px-4">${item.city}</td>
                             <td class="py-2 px-4">${item.client_name}</td>
                             <td class="py-2 px-4">${item.auditor_contact}</td>
                            <td class="py-2 px-4">${item.audit_status}</td>
                            <td class="py-2 px-4">${item.payment_amount}</td>
                            <td class="py-2 px-4">${item.payment_status}</td>

                            `;
                        tableBody.append(row);

                   })

            }catch(error){
                console.error("Error fetching audit data:", error);
            }
        }
        fetchData();
});

// updating status details..

async function updateStatus(){
//    const value=document.getElementById('update').value;
//    console.log(value);
//    let response=await fetch("http://127.0.0.1:5000/auditor/auditor_details")
//        let data=await response.json()
//
//        console.log(data)
//        auditorName=data['username']
//        auditorId=data['id']
//        console.log(auditorName ,auditorId);
   const btn=document.getElementById('btnStatus');

   btn.addEventListener('click' ,async ()=>{
    const value=document.getElementById('update').value;

    let response1=await fetch("https://finalavengers.onrender.com/auditor/auditor_details")
        let data=await response1.json()

        auditorName=data['username']
        auditorId=data['id']

       const response=await fetch("https://finalavengers.onrender.com/auditor/status_update " ,{
                       method:'POST',
                       headers: {
                        "Content-Type": "application/json"
                             },
                        body :JSON.stringify({ "status": value ,"id":auditorId})
        })
            // checking if response is okay or not
        if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
        }
        //getting response
        data= await response.json()
        alert(data['message'])
        showSuccessMessage(data['message'])
        function showSuccessMessage(message) {
            let msgDiv = document.getElementById("successMessage");
            msgDiv.innerText = message;
            msgDiv.style.display = "block";  // Show message
            msgDiv.style.opacity = "1";  // Reset opacity

            // Fade out effect after 3 seconds
            setTimeout(() => {
                let fadeEffect = setInterval(() => {
                    if (!msgDiv.style.opacity || msgDiv.style.opacity === "0") {
                        clearInterval(fadeEffect);
                        msgDiv.style.display = "none";  // Hide after fade out
                    } else {
                        msgDiv.style.opacity -= "0.1";  // Reduce opacity
                    }
                }, 100);
        }, 3000);
}


   })
}
updateStatus();