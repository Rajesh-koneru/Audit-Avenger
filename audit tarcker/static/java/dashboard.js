document.addEventListener("DOMContentLoaded", function (){
    const ele=document.getElementById('totalAudits');
    const active_audits=document.getElementById('active_audits');
    const complete=document.getElementById('complete_audits');
    const pending =document.getElementById('pending');
    const table_body=document.getElementById('table_body');
    async function  fetchData(){
        let response=await fetch("http://127.0.0.1:5000/admin/total_audits");   //fetching  data from backend
        let data =await response.json();
        console.log(data)
        ele.innerText=data;
    }
    fetchData();    //caaling function


    async function activeData(){
          let response=await fetch("http://127.0.0.1:5000/admin/active_audits");    //api call
          let data= await response.json();
          console.log(data)
          active_audits.innerText=data;
    }
    activeData()     //calling a function


    // completed details

    async function completeData(){
          let response=await fetch("http://127.0.0.1:5000/admin/complete");    //api call
          let data= await response.json();
          console.log(data)
          complete.innerText=data;

    }
    completeData()

    // pending audits
     async function pending_audits(){
          let response=await fetch("http://127.0.0.1:5000/admin/pending");    //api call
          let data= await response.json();
          console.log(data)
          pending.innerText=data;

    }
    pending_audits()


    // running audit details (recent audit_details)
    async function recent_audits(){
          let response=await fetch("http://127.0.0.1:5000/admin/Recent_audit");    //api call
          let data= await response.json();
          console.log(data)
          table_body.innerHTML = "";

          data.forEach((val)=>{
              let row=document.createElement('tr');
              row.innerHTML=`
                    <td class="py-2">${val[0]}</td>
                    <td class="py-2">${val[2]}</td>
                    <td class="py-2">${val[3]}</td>
                    <td class="py-2">${val[1]}</td>
                    `;
              table_body.append(row);
          })

    }
    recent_audits()

});