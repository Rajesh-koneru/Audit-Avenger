document.addEventListener("DOMContentLoaded", function () {
    let isUpdateMode = false; // Track mode state
    const toggleButton = document.getElementById("toggleMode");
    const tableBody = document.querySelector(".table_body");

    // Fetch and load data based on mode
    async function loadTableData() {
        try {
            let response = await fetch("https://finalavengers.onrender.com/admin/report");
            let data = await response.json();
            tableBody.innerHTML = ""; // Clear table before loading new data

            data.forEach((item) => {
                let row = document.createElement("tr");
                console.log(item.planned_data)
                // If in Update Mode, make 'audit_status' editable
                row.innerHTML = `
                    <td class="py-2 px-4">${item.Audit_id}</td>
                    <td class="py-2 px-4">${item.auditor_name}</td>
                    <td class="py-2 px-4">${item.planned_date}</td>
                    <td class="py-2 px-4">${item.state}</td>
                    <td class="py-2 px-4">${item.city}</td>
                    <td class="py-2 px-4">${item.client_name}</td>
                    <td class="py-2 px-4">${item.auditor_contact}</td>
                    <td class="py-2 px-4" ${isUpdateMode ? 'contenteditable="true" data-id="' + item.Audit_id + '"' : ''}>${item.audit_status}</td>
                    <td class="py-2 px-4">${item.payment_amount}</td>
                    <td class="py-2 px-4">${item.payment_status}</td>
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
                let newStatus = event.target.innerText.trim();

                if (auditId && newStatus) {
                    await updateStatus(auditId, newStatus);
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

        } catch (error) {
            console.error("Error updating status:", error);
        }
    }

    // Toggle Mode on Button Click
    toggleButton.addEventListener("click", function () {
        isUpdateMode = !isUpdateMode; // Toggle mode
        toggleButton.innerText = isUpdateMode ? "Switch to Report Mode" : "Switch to Update Mode";
        loadTableData(); // Reload table with correct mode
    });

    // Initial Data Load
    loadTableData();
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
                row.innerHTML = `
                    <td class="py-2 px-4">${item.Audit_id}</td>
                    <td class="py-2 px-4">${item.auditor_name}</td>
                    <td class="py-2 px-4">${item.planned_date}</td>
                    <td class="py-2 px-4">${item.state}</td>
                    <td class="py-2 px-4">${item.city}</td>
                    <td class="py-2 px-4">${item.client_name}</td>
                    <td class="py-2 px-4">${item.auditor_contact}</td>
                    <td class="py-2 px-4" id='status' style="background-color='green'">${item.audit_status}</td>
                    <td class="py-2 px-4">${item.payment_amount}</td>
                    <td class="py-2 px-4">${item.payment_status}</td>
                `;

                tableBody.appendChild(row);
            })

    } catch (error) {
        console.error("Error:", error);
    }

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
                fetch('https://finalavengers.onrender.com/upload-excel', {
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