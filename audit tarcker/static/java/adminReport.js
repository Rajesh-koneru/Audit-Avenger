document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector(".table_body");

    async function fetchAuditData() {
        try {
            let response = await fetch("http://127.0.0.1:5000/admin/report"); // Fetch from Flask API
            let data = await response.json();
            console.log(data);
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
                    <td class="py-2 px-4">${item.contact}</td>
                    <td class="py-2 px-4">${item.audit_status}</td>
                    <td class="py-2 px-4">${item.payment_amount}</td>
                    <td class="py-2 px-4">${item.payment_status}</td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error("Error fetching audit data:", error);
        }
    }

    fetchAuditData(); // Call function to load data
});

async function filteredData(){
    let filter=document.getElementById('filter').value;
    console.log(filter)
     const tableBody = document.querySelector(".table_body");
    try{
        const response= await fetch("http://127.0.0.1:5000/admin/filter",{
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
                    <td class="py-2 px-4">${item[0]}</td>
                    <td class="py-2 px-4">${item[1]}</td>
                    <td class="py-2 px-4">${item[2]}</td>
                    <td class="py-2 px-4">${item[3]}</td>
                    <td class="py-2 px-4">${item[4]}</td>
                    <td class="py-2 px-4">${item[5]}</td>
                    <td class="py-2 px-4">${item[6]}</td>
                    <td class="py-2 px-4">${item[7]}</td>
                    <td class="py-2 px-4">${item[8]}</td>
                    <td class="py-2 px-4">${item[9]}</td>
                `;
                tableBody.appendChild(row);
            })

    } catch (error) {
        console.error("Error:", error);
    }

}
document.getElementById("filterBtn").addEventListener("click", filteredData);
