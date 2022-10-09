document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#reply').addEventListener('click', reply);
 

  // By default, load the inbox
  current_url = window.location.href.toString()

  if (current_url.includes("emails")) {
  
    check_email()
  }else{  // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#mail-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#archived-view').style.display = 'none';
    document.querySelector('#reply-view').style.display = 'none';

    load_mailbox('archive')
  
  };


function reply() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#archived-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'block';

  // assign variables 
  var to = document.querySelector('#compose-recipients')
  var subject = document.querySelector('#compose-subject')
  var body = document.querySelector('#compose-body')



  //submits email in a JSON text file to /emails URL
  document.querySelector('#composesubmit').addEventListener('click', () => 
  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: to.value,
      subject: subject.value,
      body: body.value
  })
  
})

)
document.querySelector('#composesubmit').addEventListener('click', () => 
alert("running submiting email")
)
}

function get_url () { 
  alert('running getting url');
  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: to.value,
      subject: subject.value,
      body: body.value
  })
}

)}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#archived-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'none';

  // assign variables of the composition fields
  var to = document.querySelector('#compose-recipients')
  var subject = document.querySelector('#compose-subject')
  var body = document.querySelector('#compose-body')

  // to.value = '';
  // subject.value = '';
  // body.value = '';

  document.querySelector('#composesubmit').addEventListener('click', () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: to.value,
          subject: subject.value,
          body: body.value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    
    })

  //submits email in a JSON text file to /emails URL...THIS WONT RUN FOR SUM REASON>>>WHHHHYYYYY<-------------------------- HERE NOT WORKING-----------------
}


//'Loads' mail-view <div> container and hides the other two
function check_email() {
  console.log("checking single email")
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';
  document.querySelector('#archived-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'none';

  // document.querySelector('#reply').addEventListener('click', reply);


}


//'Loads'  emails-view <div> and hides the other two
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#archived-view').style.display = 'none';
  document.querySelector('#reply-view').style.display = 'none';
  

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch('/emails/'+mailbox)
.then(response => response.json())
.then(emails => {
    // Print emails
    console.log(emails);

    //for each email in emails create html using JavaScript which includes an <a href> link to emails/"emails.id" 
    //which when clicked will open that individual email in the simular fashion of revealing and hiding <divs> in the html file inbox.html
    emails.forEach(showemail);

    function showemail (emails) {
    //creates div and a href link and appends the link to the div as a child of the div. 
    const emaildiv = document.createElement("div");
    const paragraph1 = document.createElement("a")
    paragraph1.href = "/emails/"+emails.id
    emaildiv.appendChild(paragraph1);

    if (emails.read == true) {
      emaildiv.setAttribute('style', "background-color: grey; border-style: solid")
    }else {
      emaildiv.setAttribute('style', "background-color: white; border-style: solid")
    };
    


    //create a paragraph element and attach that to the div created above.
    const paragraph2 = document.createElement("p")
    emaildiv.appendChild(paragraph2);
    const paragraph3 = document.createElement("p")
    emaildiv.appendChild(paragraph3);

    //grab the emails-view div element by id , 
    //and appends the created div into that div container
    const element = document.getElementById("emails-view");
    element.appendChild(emaildiv);

    
    //the entire div
    emaildiv.setAttribute("class", "emaildiv");
    // emaildiv.setAttribute('style', "border-style: solid")

    //the subject line/<a href link>
    paragraph1.setAttribute('class', "subject");
    paragraph1.setAttribute('id', "viewemail");
    //<p> element used for the sender of the email
    paragraph2.setAttribute('class', "senderemail");

    
    //create the contents of what the div and <p> tags will have in the which is the emails 
    //subject and emails sender
    const node = document.createTextNode(emails.subject);
    const node2 = document.createTextNode(emails.sender);
    const node3 = document.createTextNode(emails.timestamp);
    const brk = document.createElement("br")
   
    paragraph1.appendChild(node);
    paragraph2.appendChild(node2);
    paragraph3.appendChild(node3);
    element.appendChild(brk)

    document.querySelector('#viewemail').addEventListener('click', check_email); 

    }

  }
  )

}

});