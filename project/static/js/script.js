const header = document.querySelector("header");

let lastScrollTop = 0;

window.addEventListener("scroll", () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollTop > lastScrollTop && scrollTop > header.clientHeight) {
    header.style.top = `-${header.clientHeight}px`;
  } else {
    header.style.top = "0";
  }

  lastScrollTop = scrollTop;
});

document.addEventListener("DOMContentLoaded", function () {
  const revealElements = document.querySelectorAll(".reveal");

  function revealOnScroll() {
    const windowHeight = window.innerHeight;
    const scrollTop = window.scrollY;

    for (let i = 0; i < revealElements.length; i++) {
      const revealTop = revealElements[i].getBoundingClientRect().top;
      const revealPoint = 50;

      if (
        revealTop < windowHeight - revealPoint ||
        revealTop > windowHeight + revealPoint
      ) {
        revealElements[i].classList.add("revealed");
      } else {
        revealElements[i].classList.remove("revealed");
      }
    }
  }

  window.addEventListener("scroll", revealOnScroll);
});

var ageInput = document.getElementById("bmi-age");
var heightInput = document.getElementById("bmi-height");
var weightInput = document.getElementById("bmi-weight");
var bmiResultArea = document.querySelector("#bmi-result");
var bmiCommentArea = document.querySelector(".bmi-comment");

var modal = document.getElementById("bmi-modal");
var modalText = document.querySelector("#bmi-modalText");
var modalCloseButton = document.querySelector(".bmi-close");

function calculate() {
  var age = ageInput.value.trim();
  var height = heightInput.value.trim();
  var weight = weightInput.value.trim();

  if (age === "" || height === "" || weight === "") {
    showModal("All fields are required!");
  } else {
    countBmi(age, height, weight);
  }
}

function countBmi(age, height, weight) {
  var bmi = (weight / (((height / 100) * height) / 100)).toFixed(2);
  var result = "";

  bmiResultArea.textContent = bmi;
  bmiCommentArea.innerHTML = `You are <span id="comment">${result}</span>`;
}

function showModal(message) {
  modalText.textContent = message;
  modal.style.display = "block";
}

function closeModal() {
  modal.style.display = "none";
}

modalCloseButton.onclick = closeModal;

window.onclick = function (event) {
  if (event.target == modal) {
    closeModal();
  }
};

function checkInputAndCalculate() {
  var age = ageInput.value.trim();
  var height = heightInput.value.trim();
  var weight = weightInput.value.trim();

  if (age <= 0 || height <= 0 || weight <= 0) {
    alert("Please ensure all fields are filled and contain positive values.");
    return;
  }

  countBmi(age, height, weight);
}

function setColor(result) {
  var color = "";

  switch (result) {
    case "Underweight":
      color = "red";
      break;
    case "Obese":
      color = "red";
      break;
    case "Extremely Obese":
      color = "#8B0000";
      break;
    case "Healthy":
      color = "green";
      break;
    case "Overweight":
      color = "#FFBF00";
      break;
    default:
      color = "black";
  }

  document.getElementById("comment").style.color = color;
}

function countBmi(age, height, weight) {
  var bmi = (weight / (((height / 100) * height) / 100)).toFixed(2);
  var result = "";

  if (bmi < 18.5) {
    result = "Underweight";
  } else if (bmi >= 18.5 && bmi <= 24.99) {
    result = "Healthy";
  } else if (bmi >= 25 && bmi <= 29.99) {
    result = "Overweight";
  } else if (bmi >= 30 && bmi <= 34.99) {
    result = "Obese";
  } else {
    result = "Extremely Obese";
  }

  bmiResultArea.textContent = bmi;
  bmiCommentArea.innerHTML = `You are <span id="comment">${result}</span>`;
  setColor(result);
}
