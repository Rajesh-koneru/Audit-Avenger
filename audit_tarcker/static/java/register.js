
// function for registration

async function register(){
     let name =document.getElementById('name').value;
     let mail=document.getElementById('email').value;
     let phone =document.getElementById('phone').value;
     let qualification=document.getElementById('qualification').value;
     let experience = document.getElementById('experience').value;
     let  password = document.getElementById('password').value;
     console.log(password)

    let response=await fetch('/registration',{
            method:'POST',
            headers: {
             'Content-Type': 'application/json'
             },
            body :JSON.stringify({ "name":name,'email':mail,'phone':phone,'qualification':qualification,'experience':experience,'password':password})
    })
    if (!response.ok) {

         throw new Error(`HTTP error! Status: ${response.status} not okay`);
    }
     data= await response.json()
      console.log(data)
      alert(data['message']);
}


//calling function

document.getElementById('button').addEventListener('click',register);