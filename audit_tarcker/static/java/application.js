document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector(".table_body");
    // Fetch and load data based on mode
    async function loadTableData() {
        try {
            let response = await fetch("/admin/application");
            let data = await response.json();
            tableBody.innerHTML = ""; // Clear table before loading new data
            console.log(data)
            data.forEach((item) => {
                let row = document.createElement("tr");
                row.setAttribute('class', 'rowData');
                 row.setAttribute('class','rowData');
                 row.style.borderBottomWidth = '1px';
                 row.style.borderColor = '#eab308';
                 row.innerHTML = `
                    <td class="bg-gray-800 text-white p-2 text-center">${item.Audit_id}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.Auditor_id}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.Auditor_name}</td>
                    <td class="bg-gray-800 text-white p-2 text-center ">${item.audit_type}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.Date}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.phone}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.email}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.state}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">${item.Client_id}</td>
                    <td class="bg-gray-800 text-white p-2 text-center">
                      <input
                        type="text"
                        placeholder="Enter payment"
                        class="bg-gray-700 text-white px-3 py-1 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </td>
                    <td class="bg-gray-800 text-white p-2 text-center">
                        <button
                          class="toggle-btn ${item.status === 'accepted' ? 'bg-green-500' : 'bg-red-500'} text-white px-2 py-1 rounded"
                          data-auditor-id="${item.Auditor_id}"
                        >
                          ${item.status === 'accepted' ? 'Accepted' : 'Rejected'}
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            // Add event listeners for updating only in update mode
        } catch (error) {
            console.error("Error fetching audit data:",error);
        }
    }
   loadTableData();
});

//update button logic for application
setTimeout(()=>{
        document.querySelectorAll('.toggle-btn').forEach(button => {
          console.log(button)
          button.addEventListener('click', async function () {
            const auditId = this.dataset.auditorId;
            const newStatus = this.textContent === 'Accepted' ? 'rejected' : 'accepted';

            const response = await fetch(`/applications/status`, {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ status: newStatus, Id: auditId })
            });

            if (response.ok) {
              this.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
              this.classList.toggle('bg-green-500');
              this.classList.toggle('bg-red-500');
            } else {
              alert('Failed to update status');
            }
          });
        });
        // submitting the aceptted data to the backend...
        document.getElementById('submitBtn').addEventListener('click', async function sendAcceptedRowData() {
                const table = document.querySelector('.table_body'); // Only one element
                const rows = table.getElementsByTagName("tr");
                let sendData=[]
                for (let i = 0; i < rows.length; i++) {
                    const cells = rows[i].getElementsByTagName("td");
                    const statusButton = cells[10].querySelector('button'); // status is inside a button
                    const paymentInput = cells[9].querySelector('input');

                    const status = statusButton.textContent.trim(); // Get button text

                    if (status === "Accepted") {
                         sendData.push({
                            audit_id: cells[0]?.innerText.trim(),
                            auditor_id: cells[1]?.innerText.trim(),
                            auditor_name: cells[2]?.innerText.trim(),
                            audit_type: cells[3]?.innerText.trim(),
                            Date: cells[4]?.innerText.trim(),
                            phone: cells[5]?.innerText.trim(),
                            email: cells[6]?.innerText.trim(),
                            state: cells[7]?.innerText.trim(),
                            client_id: cells[8]?.innerText.trim(),
                            payment: paymentInput.value.trim(),
                            status: status
                        });
                    }
                }
                 console.log("Sending accepted row:", sendData);

                try {
                        const response = await fetch("/application/audit_report", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify(sendData)
                            });
                            const result = await response.json();
                            console.log("Response:", result);
                            alert(result['message']);
                            setTimeout(()=>{
                                alert(result['delete_message']);
                            },7000)
                        } catch (error) {
                            console.error("Error submitting accepted row:", error);
                        }
            });
        } ,2000);



