document.addEventListener("DOMContentLoaded", function () {
    let isUpdateMode = false; // Track mode state
    const toggleButton = document.getElementById("editBtn");
    const tableBody = document.querySelector(".table_body");
    const successMsg =document.getElementById('successMsg');

    // Fetch and load data based on mode
    async function loadTableData() {
        try {
            let response = await fetch("https://finalavengers.onrender.com/admin/report");
            let data = await response.json();
            tableBody.innerHTML = ""; // Clear table before loading new data

            data.forEach((item) => {
                let row = document.createElement("tr");
                console.log(item.planned_data)
                row.setAttribute('class', 'rowData');                // If in Update Mode, make 'audit_status' editable
                row.innerHTML = `
                    <td class="bg-gray-800 text-white p-2">${item.Audit_id}</td>
                    <td class="bg-gray-800 text-white p-2">${item.auditor_name}</td>
                    <td class="bg-gray-800 text-white p-2">${item.planned_date}</td>
                    <td class="bg-gray-800 text-white p-2">${item.state}</td>
                    <td class="bg-gray-800 text-white p-2">${item.city}</td>
                    <td class="bg-gray-800 text-white p-2">${item.client_name}</td>
                    <td class="bg-gray-800 text-white p-2">${item.auditor_contact}</td>
                    <td class="StatusColor" data-field="status" ${isUpdateMode ? 'contenteditable="true" data-id="' + item.Audit_id + '"' : ''}>${item.audit_status}</td>
                    <td class="bg-gray-800 text-white p-2" >${item.payment_amount}</td>
                    <td class="paymentColor" data-field="payment_status" ${isUpdateMode ? 'contenteditable="true" data-id="' + item.Audit_id + '"' : ''} >${item.payment_status}</td>
                `;

                tableBody.appendChild(row);
            });

            // Add event listeners for updating only in update mode
            if (isUpdateMode) {
                enableEditing();
            }
        } catch (error) {
            console.error("Error fetching audit data:", error);
        }
    }

    // Function to enable content editing
    function enableEditing() {
        tableBody.addEventListener("focusout", async function (event) {
            if (event.target.hasAttribute("contenteditable")) {
                let auditId = event.target.getAttribute("data-id");
                let fieldType = event.target.getAttribute("data-field");
                let newStatus = event.target.innerText.trim();


                if (auditId && newStatus) {
                    if(fieldType==='status'){
                        await updateStatus(auditId, newStatus);
                    }
                    else if(fieldType==='payment_status'){
                        await  paymentUpdate(auditId,newStatus);
                    }
                }
            }

        });

        tableBody.addEventListener("keydown", function (event) {
            if (event.target.hasAttribute("contenteditable") && event.key === "Enter") {
                event.preventDefault();
                event.target.blur(); // Trigger update
            }
        });
    }

    // Function to send update request
    async function updateStatus(auditId, newStatus) {
        try {
            const response = await fetch("https://finalavengers.onrender.com/admin/update_status", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "Id": auditId, "value": newStatus })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
            }

            const data = await response.json();
             // Show success message

            if(response.ok){
                  successMsg.style.display='block';
                  successMsg.innerText=data;
            }
             else{
                  successMsg.style.display='none';
            };

            setTimeout(()=>{
                successMsg.style.display='none';
            },1000);

        } catch (error) {
            console.error("Error updating status:", error);
        }

    }



     // Function to send payment  update request
    async function paymentUpdate(auditId, paymentStatus) {
        try {
            const response = await fetch("https://finalavengers.onrender.com/admin/update_payment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "Id": auditId, "value": paymentStatus })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
            }

            const data = await response.json();

             // Show success message
             if(response.ok){
              successMsg.style.display='block';
              successMsg.innerText=data;
              }
              else{
                 successMsg.style.display='none';
              };
               setTimeout(()=>{
                successMsg.style.display='none';
            },1000);


        } catch (error) {
            console.error("Error updating status:", error);
        }
    }

    // Toggle Mode on Button Click
    toggleButton.addEventListener("click", function () {

        isUpdateMode = !isUpdateMode; // Toggle mode
        toggleButton.innerText = isUpdateMode ? "Save" : "Edit";
        loadTableData(); // Reload table with correct mode
    });

    // Initial Data Load
    loadTableData();

    //function to change the text color of audit status  based on there values..
    function ColorUpdate(){
           const color=document.querySelectorAll('.StatusColor');

           console.log('all values Are elements are selected',color);
           console.log(color.textContent)
           color.forEach((ele)=>{
                 let val=ele.textContent;
                 console.log(val)
                 if(val=='Completed'){
                       ele.style.color='#28a745';
                 }
                 else if( val=='In Progress'){
                        ele.style.color="#F97316";
                 }
                 else{
                        ele.style.color="#B91C1C";
                 }
           })

    }
    setTimeout(() => {
         ColorUpdate();
    }, 2000);

    //function for changing payments status color
     function PaymentColor(){
           const payColor=document.querySelectorAll('.paymentColor');

           console.log('all values Are elements are selected',payColor);
           console.log(payColor.innerText)

           payColor.forEach((ele)=>{
                 let val=ele.innerText;

                 if(val=='Paid'){
                       ele.style.color='#28a745';
                       console.log('color added')
                 }
                 else if( val=='Pending'){
                        ele.style.color="#F97316";
                 }
                 else{
                        ele.style.color="#B91C1C";
                 }
           })

    }
                setTimeout(() => {
                    PaymentColor();

                }, 2000);


            function hover() {
                const elements = document.querySelectorAll('.StatusColor'); // Get all elements
                const element1=document.querySelectorAll('.paymentColor');
                console.log(elements); // Debugging
                elements.forEach((ele) => {
                    var col='';
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        const color=ele.style.color;
                        console.log(color);
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in" ; // Apply transition

                        if (value === 'Completed') {
                            ele.style.backgroundColor = '#28a745';
                            ele.style.borderRadius='15px';

                            ele.style.color='black';
                            col='#28a745';


                        } else if (value === 'In Progress') {
                            ele.style.backgroundColor = '#F97316';
                             ele.style.borderRadius='15px';

                              ele.style.color='black';
                              col='#F97316';


                        } else {
                            ele.style.backgroundColor = '#B91C1C';
                            ele.style.borderRadius='15px';

                             ele.style.color='black';
                             col='#B91C1C';


                        }

                    });

                    ele.addEventListener('mouseout', () => {

                        ele.style.backgroundColor = '';
                        ele.style.borderRadius='';// Reset to default
                         ele.style.opacity='';
                         ele.style.color=col;// Reset to default
                    });
                });


                //payment values bg change on hover

                element1.forEach((ele) => {
                    var col='';
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        const color=ele.style.color;
                        console.log(color);
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in" ; // Apply transition

                        if (value === 'Paid') {
                            ele.style.backgroundColor = '#28a745';
                            ele.style.borderRadius='15px';

                            ele.style.color='black';
                            col='#28a745';


                        } else if (value === 'Pending') {
                            ele.style.backgroundColor = '#F97316';
                             ele.style.borderRadius='15px';

                              ele.style.color='black';
                              col='#F97316';


                        } else {
                            ele.style.backgroundColor = '#B91C1C';
                            ele.style.borderRadius='15px';

                             ele.style.color='black';
                             col='#B91C1C';


                        }

                    });

                    ele.addEventListener('mouseout', () => {

                        ele.style.backgroundColor = '';
                        ele.style.borderRadius='';// Reset to default
                         ele.style.opacity='';
                         ele.style.color=col;// Reset to default
                    });
                });
            }

            function rowHover() {
                const elements = document.querySelectorAll('.rowData'); // Get all elements
                console.log(elements); // Debugging
                elements.forEach((ele) => {
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in-out,opacity 0.5s ease-in-out ,transform 0.5s ease-in-out"; // Apply transition
                        ele.style.backgroundColor = 'grey';
                        ele.style.opacity=0.8;
                        ele.style.transform=scale(1.01);
                    });
                    ele.addEventListener('mouseout', () => {
                        ele.style.backgroundColor = ''; // Reset to default
                         ele.style.opacity='';// Reset to default
                    });
                });
            }
            setTimeout(()=>{
                hover();
                rowHover()
            },2000)



});


   // Filtering data based on admin choice
async function filteredData(){
    let filter=document.getElementById('filter').value;
    console.log(filter)
    const tableBody = document.querySelector(".table_body");
    try{
        const response= await fetch("https://finalavengers.onrender.com/admin/filter",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "data": filter })

        });
        console.log("Response object:", response);
        if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
    }

        const data = await response.json();
        console.log(data)
        tableBody.innerHTML = ""; // Clear existing rows

            data.forEach((item) => {
                console.log(`${item.planned_data}`)
                let row = document.createElement("tr");
                row.setAttribute('class','rowData');
                row.innerHTML = `
                    <td class="bg-gray-800 text-white p-2">${item.Audit_id}</td>
                    <td class="bg-gray-800 text-white p-2">${item.auditor_name}</td>
                    <td class="bg-gray-800 text-white p-2">${item.planned_date}</td>
                    <td class="bg-gray-800 text-white p-2">${item.state}</td>
                    <td class="bg-gray-800 text-white p-2">${item.city}</td>
                    <td class="bg-gray-800 text-white p-2">${item.client_name}</td>
                    <td class="bg-gray-800 text-white p-2">${item.auditor_contact}</td>
                    <td class="StatusColor" >${item.audit_status}</td>
                    <td class="bg-gray-800 text-white p-2">${item.payment_amount}</td>
                    <td class="paymentColor">${item.payment_status}</td>
                `;

                tableBody.appendChild(row);
            })

    } catch (error) {
        console.error("Error:", error);
    }


    //audit status text  color update
    function ColorUpdate(){
           const color=document.querySelectorAll('.StatusColor');

           console.log('all values Are elements are selected',color);
            console.log(color.textContent)
           color.forEach((ele)=>{
                 let val=ele.textContent;
                 console.log(val)
                 if(val=='Completed'){
                       ele.style.color='#28a745';
                 }
                 else if( val=='In Progress'){
                        ele.style.color="#F97316";
                 }
                 else{
                        ele.style.color="#B91C1C";
                 }
           })

    }
    //function for changing payments status color
     function PaymentColor(){
           const payColor=document.querySelectorAll('.paymentColor');

           console.log('all values Are elements are selected',payColor);
           console.log(payColor.innerText)

           payColor.forEach((ele)=>{
                 let val=ele.innerText;

                 if(val=='Paid'){
                       ele.style.color='#28a745';
                       console.log('color added')
                 }
                 else if( val=='Pending'){
                        ele.style.color="#F97316";
                 }
                 else{
                        ele.style.color="#B91C1C";
                 }
           })

    }

            function hover() {
                const elements = document.querySelectorAll('.StatusColor'); // Get all elements
                const payEle= document.querySelectorAll('.paymentColor');
                console.log(elements); // Debugging
                elements.forEach((ele) => {
                    var col='';
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        const color=ele.style.color;
                        console.log(color);
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in" ; // Apply transition

                        if (value === 'Completed') {
                            ele.style.backgroundColor = '#28a745';
                            ele.style.borderRadius='15px';

                            ele.style.color='black';
                            col='#28a745';


                        } else if (value === 'In Progress') {
                            ele.style.backgroundColor = '#F97316';
                             ele.style.borderRadius='15px';

                              ele.style.color='black';
                              col='#F97316';


                        } else {
                            ele.style.backgroundColor = '#B91C1C';
                            ele.style.borderRadius='15px';

                             ele.style.color='black';
                             col='#B91C1C';


                        }

                    });

                    ele.addEventListener('mouseout', () => {

                        ele.style.backgroundColor = '';
                        ele.style.borderRadius='';// Reset to default
                         ele.style.opacity='';
                         ele.style.color=col;// Reset to default
                    });
                });

                payEle.forEach((ele) => {
                    var col='';
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        const color=ele.style.color;
                        console.log(color);
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in" ; // Apply transition

                        if (value === 'Paid') {
                            ele.style.backgroundColor = '#28a745';
                            ele.style.borderRadius='15px';

                            ele.style.color='black';
                            col='#28a745';


                        } else if (value === 'Pending') {
                            ele.style.backgroundColor = '#F97316';
                             ele.style.borderRadius='15px';

                              ele.style.color='black';
                              col='#F97316';


                        } else {
                            ele.style.backgroundColor = '#B91C1C';
                            ele.style.borderRadius='15px';
                             ele.style.color='black';
                             col='#B91C1C';
                        }
                    });

                    ele.addEventListener('mouseout', () => {

                        ele.style.backgroundColor = '';
                        ele.style.borderRadius='';// Reset to default
                         ele.style.opacity='';
                         ele.style.color=col;// Reset to default
                    });
                });
            }

            function rowHover() {
                const elements = document.querySelectorAll('.rowData'); // Get all elements
                console.log(elements); // Debugging
                elements.forEach((ele) => {
                    ele.addEventListener('mouseover', () => {
                        const value = ele.innerText.trim(); // Get text inside td
                        console.log(value); // Debugging

                        ele.style.transition = "background-color 0.5s ease-in-out,opacity 0.5s ease-in-out ,transform 0.5s ease-in-out"; // Apply transition
                        ele.style.backgroundColor = 'grey';
                        ele.style.opacity=0.8;
                        ele.style.transform=scale(1.01);
                    });
                    ele.addEventListener('mouseout', () => {
                        ele.style.backgroundColor = ''; // Reset to default
                         ele.style.opacity='';// Reset to default
                    });
                });
            }


   setTimeout(() => {
     PaymentColor();
     ColorUpdate();
     hover();
     rowHover()
   }, 1000);

}
document.getElementById("filterBtn").addEventListener("click", filteredData);



// file upload script
document.getElementById('uploadButton').addEventListener('click', function(event) {
            event.preventDefault();  // Prevent default form submission behavior

            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            console.log(file)
            if (!file) {
                alert("Please select an Excel file first!");
                return;
            }

            const reader = new FileReader();
            reader.onload = function(event) {
                const data = new Uint8Array(event.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                const jsonData = XLSX.utils.sheet_to_json(sheet,{
                raw: false,  // Keeps the data as strings, but dates need conversion
                dateNF: "dd-mm-yyyy" // Ensures proper date format
                });
                console.log("this is data",jsonData)
                 if (jsonData.length === 0) {
                        console.warn("File was read, but it returned an empty array.");
                }

                // ✅ Sending JSON data to Flask backend
                fetch('/upload-excel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },  // 👈 Ensure correct JSON content type
                    body: JSON.stringify({ "data": jsonData })  // 👈 Convert object to JSON
                })
                .then(response => response.json())  // Handle response properly
                .then(data => {
                    console.log(data);
                    alert(data.message);
                })
                .catch(error => console.error('Error:', error));
            };

            reader.readAsArrayBuffer(file);
});




