
document.addEventListener('DOMContentLoaded', function() {



  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = "";
  document.querySelector('#compose-subject').value = "";
  document.querySelector('#compose-body').value = "";
  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => {
    console.log(response);
    return response.json();
  })
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      const element = document.createElement('div');
      element.classList.add("inbox-email");
      element.style.border = '1px solid black';
      element.style.padding = '10px';
      element.style.margin = '10px';
      element.style.cursor = 'pointer';
      element.style.borderRadius = '5px';
      if (mailbox !== 'sent') {
      element.innerHTML = `<span class="sender">${email.sender}</span> <span class="subject">${email.subject}</span> <span class="timestamp">${email.timestamp}</span> <button id="archiveBtn">${email.archived ? 'Unarchive' : 'Archive'}</button>`;
      } else {
        element.innerHTML = `<span class="recipient">${email.recipients}</span> <span class="subject">${email.subject}</span> <span class="timestamp">${email.timestamp}</span>`;
      }
      if (email.read) {
        element.style.backgroundColor = 'lightgray';
      }
      document.querySelector('#emails-view').append(element);
      element.addEventListener('mouseover', () => {
        element.style.boxShadow = '0 4px 8px 0 rgba(50, 91, 227, 0.64)';
      });
      element.addEventListener('mouseout', () => {
        element.style.boxShadow = 'none';
      });
      element.addEventListener('click', () => load_email(email.id));
      const archiveBtn = element.querySelector('#archiveBtn');
      archiveBtn.style.float = 'right';
      archiveBtn.style.padding = '5px 10px';
      archiveBtn.style.border = 'none';
      archiveBtn.style.borderRadius = '3px';
      archiveBtn.style.backgroundColor = email.archived ? '#f44336' : '#4CAF50';
      archiveBtn.style.color = 'white';
      archiveBtn.style.cursor = 'pointer';
      archiveBtn.style.boxShadow = email.archived ? '0 2px 4px 0 rgba(203, 61, 42, 0.65)' : '4px 4px 8px 0 rgba(133, 208, 47, 0.61)';
      element.style.height = '50px';
      archiveBtn.addEventListener('mouseover', () => {
        archiveBtn.style.backgroundColor = email.archived ? '#d32f2f' : '#45a049';
        archiveBtn.style.boxShadow = email.archived ? '0 4px 8px 0 rgba(42, 85, 203, 0.24)' : '4px 4px 8px 0 rgba(208, 111, 47, 0.37)';
      });
      archiveBtn.addEventListener('mouseout', () => {
        archiveBtn.style.backgroundColor = email.archived ? '#f44336' : '#4CAF50';
        archiveBtn.style.boxShadow = email.archived ? '0 2px 4px 0 rgba(42, 85, 203, 0.24)' : '4px 4px 8px 0 rgba(208, 111, 47, 0.37)';
      });
      archiveBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived,
          })
        })
        .then(() => {
          load_mailbox('inbox');
        });
      });
    });
  });
}





function send_email(event){
  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');
  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
    recipients: recipients.value,
    subject: subject.value,
    body: body.value
    })
    })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    })
  .then(compose_email)
}



function load_email(id) {
  fetch(`/emails/${id}`,
  {method: 'PUT',
   body: JSON.stringify({
    read: true
  })
}
  );
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const element = document.createElement('div');
    element.innerHTML = `<p><strong>From:</strong> ${email.sender}</p>
                         <p><strong>To:</strong> ${email.recipients}</p>
                         <p><strong>Subject:</strong> ${email.subject}</p>
                         <p><strong>Timestamp:</strong> ${email.timestamp}</p>
                         <hr>
                         <p>${email.body}</p>`;
    document.querySelector('#emails-view').innerHTML = '';
    document.querySelector('#emails-view').append(element);
      const replyBtn = document.createElement('button');
  replyBtn.innerHTML = 'Reply';
  replyBtn.style.padding = '10px 20px';
  replyBtn.style.border = 'none';
  replyBtn.style.borderRadius = '5px';
  replyBtn.style.backgroundColor = '#008CBA';
  replyBtn.style.color = 'white';
  replyBtn.style.cursor = 'pointer';
  replyBtn.style.boxShadow = '0 4px 8px 0 rgba(0, 140, 186, 0.24)';
  document.querySelector('#emails-view').append(replyBtn);
  replyBtn.addEventListener('mouseover', () => {
    replyBtn.style.backgroundColor = '#007B9E';
    replyBtn.style.boxShadow = '0 4px 8px 0 rgba(0, 123, 158, 0.24)';
  });
  replyBtn.addEventListener('mouseout', () => {
    replyBtn.style.backgroundColor = '#008CBA';
    replyBtn.style.boxShadow = '0 4px 8px 0 rgba(0, 140, 186, 0.24)';
  });
  replyBtn.addEventListener('click', (event) => {
    event.preventDefault();
    email_reply(email);
  });
});
}


function email_reply(email) {
  compose_email();
  document.querySelector("h3").innerHTML = "Reply to Email";
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
}