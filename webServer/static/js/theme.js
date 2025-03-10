document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("themeToggle");

    if (!themeToggle) {
        console.error("Theme toggle button not found!");
        return;
    }

    // Load saved theme from localStorage or default to 'dark'
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    themeToggle.innerText = savedTheme === "dark" ? "Switch to Light Theme" : "Switch to Dark Theme";

    // Add event listener to toggle button
    themeToggle.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        // Update theme and button text
        document.documentElement.setAttribute("data-theme", newTheme);
        themeToggle.innerText = newTheme === "dark" ? "Switch to Light Theme" : "Switch to Dark Theme";

        // Save preference in localStorage
        localStorage.setItem("theme", newTheme);
    });
});
