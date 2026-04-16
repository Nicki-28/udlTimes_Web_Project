
let images = [];
let currentIndex = 0;
let conceptName = '';
let visited = [];
let guesses = [];

function initVisited() {
    visited = new Array(images.length).fill(false);
    visited[0] = true; 
}

async function loadGame() {
    try {
        const res = await fetch('/api/framed/');
        if (!res.ok) {
            document.getElementById('img-container').innerHTML = 
                '<p class="text-slate-400">No game for today :p</p>';
            return;
        }
        const data = await res.json();
        images = data.images;
        conceptName = data.concept;
        initVisited();
        showImage(0);
    } catch (e) {
        console.error('Error loading the game:', e);
    }
}

//autocomplete (pendent fix)
const responseInput = document.getElementById('response-input');
const responseOptions = document.getElementById('response-options');

let autocompleteTimeout = null;
let suppressAutocomplete = false;

responseInput.addEventListener('input', function () {
    if (suppressAutocomplete) return;
    clearTimeout(autocompleteTimeout);

    const query = this.value.trim();

    if (query.length < 2) {
        responseOptions.innerHTML = '';
        return;
    }

    autocompleteTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`/framed/movie-autocomplete/?term=${encodeURIComponent(query)}`);
            if (!res.ok) return;

            const concepts = await res.json();

            responseOptions.innerHTML = '';

            concepts.forEach(concept => {
                const option = document.createElement('option');
                option.value = concept;
                responseOptions.appendChild(option);
            });

        } catch (e) {
            console.error('Autocomplete error:', e);
        }
    },);
});

function submitAnswer() {
    const input = document.getElementById('response-input');
    const userAnswer = input.value.trim();
    if (!userAnswer) return;

    const isCorrect = userAnswer.toLowerCase() === conceptName.toLowerCase();
    input.value = '';

    if (isCorrect) {
        showSuccessState();
    } else {
        const next = getNextUnvisited();
        if (next !== -1) {
            showImage(next);
        }
    }
}


function showSuccessState() {
    document.getElementById('input-section').classList.add('hidden');
    document.getElementById('success-section').classList.remove('hidden');
}

function canAccess(index) {
    if (index === 0) return true;
    if (visited[index]) return true;
    return index === getNextUnvisited();
}

function showImage(index) {
    if (!canAccess(index)) return;

    const img = document.getElementById('framed-img');
    const counter = document.getElementById('img-counter');
    currentIndex = index;

    if (img && images[index]) {
        img.src = images[index];
    }
    if (counter) {
        counter.textContent = `FRAME ${index + 1} / ${images.length}`;
    }

    visited[index] = true;

    updateProgressBar();
    updateSkipButton();
}

function getNextUnvisited(){
    for (let i = currentIndex + 1; i < images.length; i++){
        if(!visited[i]) return i;
    }
    return -1; 
}

function skipImage() {
    const next = getNextUnvisited();
    if (next !== -1) {
        showImage(next);
    }
}

function handleSkipOrEnd(){
    const next = getNextUnvisited();
    if (next !== -1) {
        showImage(next);
    } else {
        showLossState();
    }
}
function isLastFrame() {
    return getNextUnvisited() === -1;
}

function updateSkipButton() {
    const btn = document.getElementById('skip-end-btn');
    if (!btn) return;
    if (isLastFrame()) {
        btn.textContent = 'END';
        btn.className = 'px-8 py-4 border-2 border-red-600 text-red-600 font-display text-xl rounded-xl hover:bg-red-50 dark:hover:bg-red-950 transition-colors';
    } else {
        btn.textContent = 'SKIP';
        btn.className = 'px-8 py-4 border-2 border-slate-900 dark:border-slate-100 font-display text-xl rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors';
    }
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
            segment.classList.add('bg-slate-400', 'dark:bg-slate-500', 'text-white', 'cursor-pointer', 'hover:bg-primary', 'transition-colors');
            segment.onclick = () => showImage(i);
        } else {
            segment.classList.add('bg-slate-200', 'dark:bg-slate-700', 'text-slate-400');
        }

        container.appendChild(segment);
    }
}



document.addEventListener('DOMContentLoaded', loadGame);

