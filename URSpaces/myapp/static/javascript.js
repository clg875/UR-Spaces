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


function confirmDelete() {
  return confirm("Are you sure you want to delete?");
}

function confirmBanUser(event){
  var action = event.submitter.name;

  if (action === "banUserComment_btn" || action === "banUser_btn" || action === "banUserPost_btn") {
    confirmationMessage = "Are you sure you want to ban this user?";
    } else if (action === "ignoreComment_btn" || action === "ignoreUser_btn" || action === "ignorePost_btn" ) {
    confirmationMessage = "Are you sure you want to ignore this report?";
    }

    return confirm(confirmationMessage);

}


function confirmReport() {
  return confirm("Are you sure you want to report this user?");
}