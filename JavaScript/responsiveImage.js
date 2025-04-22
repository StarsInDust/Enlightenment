// JavaScript Document
document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll("article.main img");
    images.forEach(img => {
        if (img.width < 500) {
            if (img.width < 300 && img.height < 300) {
                img.classList.add("imgLeft");
                img.classList.remove("responsiveImage"); // Remove .responsiveImage if .imgLeft is applied
            } else {
                img.classList.add("responsiveImage");
            }
        } else {
            img.classList.add("wideImg");
        }
    });
});