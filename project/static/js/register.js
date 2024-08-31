window.onload = function () {
  const revealElements = document.querySelectorAll(".reveal");

  revealElements.forEach((element) => {
    element.classList.add("revealed");
  });
};

document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    var isValid = true;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      isValid = false;
    }

    var passwordRegex = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}/;
    if (!passwordRegex.test(password)) {
      alert(
        "Password must contain at least one number, one uppercase letter, one lowercase letter, one special character, and at least 8 or more characters."
      );
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault(); 
    }
  });
