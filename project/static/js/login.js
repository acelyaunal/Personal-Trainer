window.onload = function () {
  const revealElements = document.querySelectorAll(".reveal");

  revealElements.forEach((element) => {
    element.classList.add("revealed");
  });
};
