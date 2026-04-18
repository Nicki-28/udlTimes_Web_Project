const EE_USERNAME = window.APP_CONFIG.eeUser;

function onUsernameInput(val) {
    const row = document.getElementById('captcha-row');

    if (val === EE_USERNAME) {
        row.classList.remove('hidden');
        row.classList.add('flex');
    } else {
        row.classList.add('hidden');
        row.classList.remove('flex');
        document.getElementById('captcha_ok').value = '1';
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const usernameVal = document.getElementById('id_username').value;
    if (usernameVal) onUsernameInput(usernameVal);

    if (window.APP_CONFIG.showLoginModal) {
        document.getElementById('login-modal').classList.remove('hidden');
    }
});

/* CAPTCHA CLICK */
function handleCaptchaClick() {
    const chk = document.getElementById('captcha-chk');
    if (chk.dataset.checked === 'true') return;

    tttReset();
    document.getElementById('ttt-modal').classList.remove('hidden');
}

function markCaptchaDone() {
    const chk = document.getElementById('captcha-chk');

    chk.dataset.checked = 'true';
    chk.classList.remove('border-slate-400');
    chk.classList.add('bg-blue-500', 'border-blue-500');

    chk.innerHTML = `
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 7l4 4 6-7" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    `;

    document.getElementById('captcha_ok').value = '1';
}

/* TIC TAC TOE */
const WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
];

let tttBoard = Array(9).fill(null);
let tttOver = false;

function tttCheckWinner(b) {
    for (const [a,x,c] of WINS) {
        if (b[a] && b[a] === b[x] && b[a] === b[c]) {
            return { winner: b[a], line: [a,x,c] };
        }
    }
    if (b.every(v => v)) return { winner: 'draw', line: [] };
    return null;
}

function tttMinimax(b, isMax) {
    const r = tttCheckWinner(b);
    if (r) {
        if (r.winner === 'O') return 10;
        if (r.winner === 'X') return -10;
        return 0;
    }

    let scores = [];

    for (let i = 0; i < 9; i++) {
        if (!b[i]) {
            b[i] = isMax ? 'O' : 'X';
            scores.push(tttMinimax(b, !isMax));
            b[i] = null;
        }
    }

    return isMax ? Math.max(...scores) : Math.min(...scores);
}

function tttRender(winLine = []) {
    const el = document.getElementById('ttt-board');
    el.innerHTML = '';

    tttBoard.forEach((v, i) => {
        const cell = document.createElement('div');

        cell.className = [
            'aspect-square flex items-center justify-center rounded-lg text-3xl font-bold transition-colors',
            'border border-slate-200 dark:border-slate-600',
            winLine.includes(i)
                ? 'bg-primary/10 dark:bg-primary/20'
                : 'bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700',
            v === 'X' ? 'text-primary' : 'text-red-500',
            (!v && !tttOver) ? 'cursor-pointer' : ''
        ].join(' ');

        cell.textContent = v || '';

        if (!v && !tttOver) {
            cell.onclick = () => tttHumanMove(i);
        }

        el.appendChild(cell);
    });
}

function tttHumanMove(i) {
    if (tttBoard[i] || tttOver) return;

    tttBoard[i] = 'X';

    const res = tttCheckWinner(tttBoard);
    if (res) return tttEndGame(res);

    tttRender();
    document.getElementById('ttt-status').textContent = 'Thinking...';

    setTimeout(tttAiMove, 450);
}

function tttAiMove() {
    let moves = [];

    for (let i = 0; i < 9; i++) {
        if (!tttBoard[i]) {
            tttBoard[i] = 'O';
            const score = tttMinimax(tttBoard, false);
            tttBoard[i] = null;

            moves.push({ i, score });
        }
    }

    const makeMistake = Math.random() < 0.1;

    let chosenMove;

    if (makeMistake) {
        const shuffled = moves.sort(() => Math.random() - 0.5);
        chosenMove = shuffled[0].i;
    } else {
        moves.sort((a, b) => b.score - a.score);
        chosenMove = moves[0].i;
    }

    tttBoard[chosenMove] = 'O';

    const res = tttCheckWinner(tttBoard);
    if (res) return tttEndGame(res);

    tttRender();
    document.getElementById('ttt-status').textContent = 'Your turn — you play X';
}

function tttEndGame(res) {
    tttOver = true;
    tttRender(res.line);

    const status = document.getElementById('ttt-status');
    const btn = document.getElementById('ttt-verify-btn');

    if (res.winner === 'X') {
        status.textContent = "You won! Click Verify to continue.";
        btn.disabled = false;
    } else if (res.winner === 'draw') {
        status.textContent = "Draw! Click Verify to continue.";
        btn.disabled = false;
    } else {
        status.textContent = "You lost. Try again.";
        btn.disabled = true;
    }
}

function tttReset() {
    tttBoard = Array(9).fill(null);
    tttOver = false;

    document.getElementById('ttt-verify-btn').disabled = true;
    document.getElementById('ttt-status').textContent = 'Your turn — you play X';

    tttRender();
}

function tttVerify() {
    document.getElementById('ttt-modal').classList.add('hidden');
    markCaptchaDone();
}