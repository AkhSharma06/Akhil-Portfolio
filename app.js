// document.addEventListener("DOMContentLoaded", () => {
// const hiddenElements = document.querySelectorAll(".hidden");

//     const observer = new IntersectionObserver(
//         (entries) => {
//             entries.forEach((entry) => {
//                 if (entry.isIntersecting) {
//                     entry.target.classList.add("visible");
//                     // entry.target.classList.remove("hidden");
//                     // observer.unobserve(entry.target); // Stop observing once visible
//                 } else {
//                     entry.target.classList.remove("visible");
//                 }
//             });
//         },
//     );

//     // hiddenElements.forEach((el) => observer.observe(el));
// });

// // const hiddenElements = document.querySelectorAll('.hidden');
// hiddenElements.forEach((el) => observer.observer(el));

document.addEventListener("DOMContentLoaded", () => {
    const hiddenElements = document.querySelectorAll(".hidden");

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                entry.target.classList.remove("hidden"); // Optional
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    });

    hiddenElements.forEach((el) => observer.observe(el));
});

