document.getElementById('submit').addEventListener("click", () => {
    // Select all elements with the class "input"
    const elements = document.querySelectorAll('.input');

    console.log('All inputs are selected:', elements); // ✅ Fixed syntax error (missing comma)

    let data = {}; // Initialize an empty object

    // Iterate over NodeList using forEach
    elements.forEach((ele) => { // ✅ `forEach` should be used on `elements`, not separately
        let name = ele.name;  // Get the input name attribute
        let value = ele.value; // Get the input value
        data[name] = value; // Store in the data object
    });

    console.log(data); // ✅ Log the collected data

    // Function to send data asynchronously
    async function sendData() {
        try {
            let response = await fetch("https://finalavengers.onrender.com/admin/manual_update", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },  // ✅ Correct content type
                body: JSON.stringify({ "data": data }) // ✅ Ensure proper JSON structure
            });

            if (!response.ok) {
                console.warn('Data not sent');
                return 'Data not sent';
            }

            let msg = await response.json(); // ✅ Corrected variable name (`meg` → `msg`)
            console.log(msg);
            alert(msg.message || "Data sent successfully!"); // ✅ Show a proper message

        } catch (error) {
            console.error("Error sending data:", error); // ✅ Handle network errors
            alert("An error occurred while sending data.");
        }
    }

    sendData(); // ✅ Call function to send data
});
