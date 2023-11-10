function reveal() {
    var x = document.getElementById("reveal");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function revealComment() {
    var x = document.getElementById("revealComment");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  function confirmPost() {
    confirm("Are you sure you want to create this post?");
  }