document.getElementById('submit').addEventListener("click", () => {
    // Select all elements with the class "input"
    const elements = document.querySelectorAll('.input');


    let data = {}; // Initialize an empty object

    // Iterate over NodeList using forEach
    elements.forEach((ele) => { // ✅ `forEach` should be used on `elements`, not separately
        let name = ele.name.trim();  // Get the input name attribute
        let value = ele.value.trim(); // Get the input value
        data[name] = value; // Store in the data object
    });



    // Function to send data asynchronously
    async function sendData() {
        try {
            let response = await fetch("https://finalavengers.onrender.com/admin/manual_update", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },  // ✅ Correct content type
                body: JSON.stringify({ "data": data }) // ✅ Ensure proper JSON structure
            });

            if (!response.ok) {

                return 'Data not sent';
            }


            let msg = await response.json(); // ✅ Corrected variable name (`meg` → `msg`)


            // redirecting to dashboard after success
            if (response.ok) {
                window.location.href = 'https://finalavengers.onrender.com/admin/dashboard';
            }
        }catch(error) {
           // ✅ Handle network errors
            alert("An error occurred while sending data.");
        }
    }

    sendData(); // ✅ Call function to send data

});

