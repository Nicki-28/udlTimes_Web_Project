(function() {
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

	const isEasterEggUser = window.APP_CONFIG?.eeUser &&
		window.APP_CONFIG.eeUser !== '' &&
		window.APP_CONFIG.eeUser === window.APP_CONFIG.currentUser;


	if (isEasterEggUser) {
		document.documentElement.classList.add('ee-transition');
		const audio = new Audio('https://www.myinstants.com/media/sounds/never-gonna-give-you-up.mp3');
		audio.volume = 0.6;
		audio.play().catch(() => {});
		setTimeout(() => {
			audio.pause();
			audio.currentTime = 0;
		}, 3000);
	} else {
		document.documentElement.classList.remove('ee-transition');
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