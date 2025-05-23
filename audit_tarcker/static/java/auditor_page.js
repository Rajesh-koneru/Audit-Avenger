document.addEventListener("DOMContentLoaded"  ,async function(){
        let name=document.getElementById('name');
        let tableBody=document.querySelector('.tbody');



        let response=await fetch("/auditor/auditor_details")
        let data=await response.json()


        auditorName=data['username']
        auditorId=data['id']
        alert(auditorId)
     // showing name -->
        name.innerText=auditorName;
        //getting auditor details from db
        async function fetchData(){
            try{
                response=await fetch("/auditor/data" ,{
                       method:'POST',
                       headers: {
                        "Content-Type": "application/json"
                    },
                    body :JSON.stringify({ "Id":auditorId ,'username':auditorName})
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

                        // If in Update Mode, make 'audit_status' editable
                        row.innerHTML = `
                        <td class="bg-gray-800 text-white p-2 text-center">${item.Audit_id}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.auditor_id}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.auditor_name}</td>
                        <td class="bg-gray-800 text-white p-2 text-center ">${item.audit_type}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.planned_date}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.contact}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.email}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.client_id}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.state}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.location}</td>
                        <td class="bg-gray-800 text-white p-2 text-center">${item.payment_amount}</td>
                        <td class="paymentColor" >${item.payment_status}</td>
                        <td class="StatusColor"  >${item.audit_status}</td>
                    `;
                        tableBody.append(row);
                   })
            }catch(error){
                console.error("Error fetching audit data:", error);
            }
        }
        fetchData();
});

////securing updating status...
// async function checking(){
//    const submit=document.getElementById('submit');
//    const audit_id=document.getElementById('Id').value.trim();
//    const client_id=document.getElementById('clId').value.trim();
//    const select=document.getElementById('select');
//
//    let response=await fetch('https://finalavengers.onrender.com/auditor/check');
//    if(!response.ok){
//        console.log('the client was not matched ');
//    }
//    let data=await response.json();
//    console.log(data['message']);
//    if(response.ok){
//
//
//    }
//
//}
//
//
//
//// updating status details..

async function updateStatus(){

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