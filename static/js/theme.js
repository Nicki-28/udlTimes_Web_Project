(function () {
   const saved = localStorage.getItem('theme');
   if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
   }
})();

function switchTheme() {
   const isDark = document.documentElement.classList.toggle('dark');
   localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

function toggleTheme() {
   if (!document.startViewTransition) {
      switchTheme();
      return;
   }
   document.startViewTransition(switchTheme);
}


tailwind.config = {
   darkMode: "class",
   theme: {
      extend: {
         colors: {
            primary: "var(--color-primary, #700040)",
            "background-light": "#f8fafc",
            "background-dark": "#0d1117",
            secondary: "#f59e0b",
         },
         fontFamily: {
            display: ["Bungee", "cursive"],
            sans: ["Inter", "sans-serif"],
         },
         borderRadius: {
            DEFAULT: "0.75rem",
         },
      },
   },
};