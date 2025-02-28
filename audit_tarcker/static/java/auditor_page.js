document.addEventListener("DOMContentLoaded"  ,async function(){
        let name=document.querySelector('.name');
        let tableBody=document.querySelector('.tbody');



        let response=await fetch("http://127.0.0.1:5000/auditor/auditor_details")
        let data=await response.json()

        console.log(data)
        auditorName=data['username']
        console.log(auditorName);
        name.innerText=auditorName;
        async function fetchData(){
            try{
                response=await fetch("http://127.0.0.1:5000/auditor/data" ,{
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
                   console.log(data)

                   tableBody.innerHTML = ""; // Clear table before loading new data
                   data.forEach((item) => {
                        let row = document.createElement("tr");
                        console.log(item.state)
                        // If in Update Mode, make 'audit_status' editable
                        row.innerHTML = `
                            <td class="py-2 px-4">${item.Audit_id}</td>
                            <td class="py-2 px-4">${item.auditor_name}</td>
                            <td class="py-2 px-4">${item.planned_date}</td>
                            <td class="py-2 px-4">${item.state}</td>
                            <td class="py-2 px-4">${item.city}</td>
                             <td class="py-2 px-4">${item.client_name}</td>
                             <td class="py-2 px-4">${item.contact}</td>
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
    console.log(value);
    let response1=await fetch("http://127.0.0.1:5000/auditor/auditor_details")
        let data=await response1.json()

        console.log(data)
        auditorName=data['username']
        auditorId=data['id']
        console.log(auditorName ,auditorId);
       const response=await fetch("http://127.0.0.1:5000/auditor/status_update " ,{
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
        console.log(data)
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