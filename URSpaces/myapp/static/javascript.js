function reveal() {
    var x = document.getElementById("reveal");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function revealComment(id, firstId) {
    var x = document.getElementById(id);
    var y = document.getElementById("editCommentForm");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }

    if( id == firstId)
    {
      y.action =".";
    }
    else{
      y.action = "{% url 'comment_update' post.slug id %}";
    }
  }

function validatePost() {
    var header = document.forms[0]["newHeader"].value;
    var contents = document.forms[0]["newContents"].value;

    if (header.trim() === "" || contents.trim() === "") {
        alert("Header and content must be filled out.");
        return false;
    }

    return true;
}

function validateComment() {
  var contents = document.getElementsByName("newCommentContents")[0].value;

    if (contents.trim() === "") {
          alert("Comment cannot be blank.");
          return false; 
      }

        return true; 
}

class ConfirmationSimpleFactory{


  createConfirmationMessage(action) {
    var confirmationMessage;
  
    if (action.startsWith("banUser")) 
    {
      confirmationMessage = new BanMessage;
    } else if (action.startsWith("ignore"))
     {
      confirmationMessage = new ignoreMessage;
    } else if (action.startsWith("report")) 
    {
      confirmationMessage = new reportMessage;
    } else if (action.startsWith("delete"))
    {
      confirmationMessage = new deleteMessage;
    }
  
    return confirmationMessage;
  };
  

};

class BanMessage extends createConfirmationMessage
{
  confirmationMessage = "Are you sure you want to ban this user?";
}

class reportMessage extends createConfirmationMessage
{
  confirmationMessage = "Are you sure you want to report this user?";
}

class deleteMessage extends createConfirmationMessage
{
  confirmationMessage = "Are you sure you want to delete this item?";
}

class ignoreMessage extends createConfirmationMessage
{
  confirmationMessage = "Are you sure you want to ignore this report?";
}

function confirmAction(event) {
  var action = event.submitter.name;
  var confirmationCreation = new ConfirmationSimpleFactory();
  var confirmationMessage = confirmationCreation.createConfirmationMessage(action);

  return confirm(confirmationMessage);
}