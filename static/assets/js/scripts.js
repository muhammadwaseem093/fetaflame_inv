document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-sidebar");
    const sidebar = document.getElementById("sidebar-container");
  
    // Check if the toggle button and sidebar exist
    if (toggleButton && sidebar) {
      // Initially hide the sidebar on small screens
      sidebar.classList.add("d-none");
  
      // Toggle the sidebar on button click
      toggleButton.addEventListener("click", function () {
        sidebar.classList.toggle("d-none"); // Toggle the visibility of sidebar
        sidebar.classList.toggle("d-block"); // Add the block class for visibility
      });
    }
  });
  