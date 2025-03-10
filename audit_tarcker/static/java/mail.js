async function sendMail(){

     const name=document.getElementById('name').value.trim();
     const email=document.getElementById('mail').value.trim();
     const message=document.getElementById('msg').value.trim();

     let response=await('https://finalavengers.onrender.com/admin/report',{
            method: "POST",
            headers: {
               "Content-Type": "application/json"
            },
            body: JSON.stringify({ 'SenderName': name, "Email": email,"Message":message })
     });

     if(!response.ok){
            return json('some error occured at server') ,400
     }
     let msg=await response.json();
     console.log(msg)
     alert(msg);
}
document.getElementById('mailBtn').addEventListener('click',sendMail)