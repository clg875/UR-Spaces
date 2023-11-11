function reveal() {
    var x = document.getElementById("reveal");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function revealComment(id) {
    var x = document.getElementById(id);
    var y = document.getElementById("editCommentForm");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }

    y.action = "{% url 'comment_update' post.slug id %}"
  }

  function deleteComment(id) {
    var y = document.getElementById("deleteCommentForm");
    y.action = "{% url 'comment_update' post.slug id %}";

  }

  function confirmPost() {
    confirm("Are you sure you want to create this post?");
  }