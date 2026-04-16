let images = [];
let currentIndex = 0;
let conceptName = '';
let visited = [];

// --- INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
    loadGame();

    // Asignar eventos a los botones (Elimina la necesidad de onclick en el HTML)
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitAnswer);
    }

    const skipBtn = document.getElementById('skip-end-btn');
    if (skipBtn) {
        skipBtn.addEventListener('click', handleSkipOrEnd);
    }
});

async function loadGame() {
    try {
        const res = await fetch('/api/framed/');
        if (!res.ok) {
            document.getElementById('img-container').innerHTML = 
                '<p class="text-slate-400 p-4">No game for today :p</p>';
            return;
        }
        const data = await res.json();
        images = data.images;
        conceptName = data.concept;
        
        // Inicializar visitados basándonos en el número de imágenes recibidas
        visited = new Array(images.length).fill(false);
        
        showImage(0); 
    } catch (e) {
        console.error('Error loading the game:', e);
    }
}

// --- LÓGICA DE JUEGO ---

function showImage(index) {
    const img = document.getElementById('framed-img');
    const counter = document.getElementById('img-counter');
    
    if (!img || !images[index]) return;

    currentIndex = index;
    img.src = images[index];
    
    if (counter) {
        counter.textContent = `FRAME ${index + 1} / ${images.length}`;
    }

    visited[index] = true;
    updateProgressBar();
    updateSkipButton();
}

function submitAnswer() {
    const input = document.getElementById('response-input');
    const userAnswer = input.value.trim();
    if (!userAnswer) return;

    const isCorrect = userAnswer.toLowerCase() === conceptName.toLowerCase();
    
    if (isCorrect) {
        showSuccessState();
    } else {
        input.value = ''; // Limpiar input si falla
        const next = getNextUnvisited();
        if (next !== -1) {
            showImage(next);
        } else {
            showLossState();
        }
    }
}

function handleSkipOrEnd() {
    const next = getNextUnvisited();
    if (next !== -1) {
        showImage(next);
    } else {
        showLossState();
    }
}

function getNextUnvisited() {
    for (let i = 0; i < images.length; i++) {
        if (!visited[i]) return i;
    }
    return -1;
}

// --- INTERFAZ ---

function updateProgressBar() {
    const container = document.getElementById('progress-bar');
    if (!container) return;
    container.innerHTML = '';

    images.forEach((_, i) => {
        const segment = document.createElement('div');
        segment.className = `flex-1 h-6 flex items-center justify-center rounded-full text-[10px] font-bold font-display transition-all duration-300`;
        segment.innerText = i + 1;
        
        if (i === currentIndex) {
            segment.classList.add('bg-primary', 'text-white', 'scale-105', 'ring-2', 'ring-primary/30');
        } else if (visited[i]) {
            segment.classList.add('bg-primary/40', 'text-white', 'cursor-pointer', 'hover:bg-primary/60');
            segment.onclick = () => showImage(i);
        } else {
            segment.classList.add('bg-slate-200', 'dark:bg-slate-700', 'text-slate-400');
        }
        container.appendChild(segment);
    });
}

function updateSkipButton() {
    const btn = document.getElementById('skip-end-btn');
    if (!btn) return;
    
    const isLast = getNextUnvisited() === -1;
    
    if (isLast) {
        btn.textContent = 'END';
        btn.className = 'px-8 py-4 border-2 border-red-600 text-red-600 font-display text-xl rounded-xl hover:bg-red-50 dark:hover:bg-red-950 transition-colors';
    } else {
        btn.textContent = 'SKIP';
        btn.className = 'px-8 py-4 border-2 border-slate-900 dark:border-slate-100 font-display text-xl rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors';
    }
}

function showSuccessState() {
    document.getElementById('input-section').classList.add('hidden');
    document.getElementById('success-section').classList.remove('hidden');
}

function showLossState() {
    document.getElementById('input-section').classList.add('hidden');
    document.getElementById('loss-section').classList.remove('hidden');
    document.getElementById('loss-concept').textContent = conceptName;
}



function updateProgressBar() {
    const container = document.getElementById('progress-bar');
    container.innerHTML = '';

    for (let i = 0; i < images.length; i++) {
        const segment = document.createElement('div');
        
        segment.className = `
            flex-1 h-6
            flex items-center justify-center
            rounded-full
            text-[10px] font-bold font-display
            transition-all duration-300
        `;

        segment.innerText = i + 1;
        
        if (i === currentIndex) {
            segment.classList.add('bg-primary', 'text-white', 'scale-105');
        }else if(visited[i]){
            segment.classList.add('bg-primary/50', 'text-white', 'cursor-pointer', 'hover:bg-primary');
            segment.onclick = () => showImage(i);
        } else {
            segment.classList.add('bg-slate-200', 'dark:bg-slate-700', 'text-slate-400');
        }

        container.appendChild(segment);
    }
}



document.addEventListener('DOMContentLoaded', loadGame);