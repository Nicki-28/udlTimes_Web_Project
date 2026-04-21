    // VARIABLES GLOBALES
    let filaActual = 0;
    let colActual = 0;
    let intentoActual = "";
    let juegoTerminado = false;
    let animando = false;
    let tiempoInicio = Date.now();

    function formatearTiempo(segundosTotales) {
        const minutos = Math.floor(segundosTotales / 60);
        const segundos = segundosTotales % 60;
        return `${minutos}:${segundos < 10 ? '0' : ''}${segundos}`;
    }
    // FUNCIONES MODALES
    function abrirAyuda() {
        document.getElementById('modal-ayuda').classList.remove('hidden');
    }

    function cerrarAyuda() {
        document.getElementById('modal-ayuda').classList.add('hidden');
    }

    function mostrarModalFinal(titulo, htmlContenido) {
        const contenedor = document.createElement('div');
        contenedor.className = "fixed inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm";
        contenedor.innerHTML = `
            <div class="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-sm w-full mx-4 text-center font-sans">
                <h2 class="text-3xl font-extrabold mb-4 text-primary font-display">${titulo}</h2>
                ${htmlContenido}
                <button onclick="this.closest('.fixed').remove()" class="mt-4 px-8 py-3 bg-primary text-white rounded-xl font-bold hover:opacity-90 transition-colors w-full">
                    Cerrar
                </button>
            </div>
        `;
        document.body.appendChild(contenedor);
    }
    window.addEventListener('load', () => {
        if (!localStorage.getItem('ayudaWordleVista')) {
            abrirAyuda();
            localStorage.setItem('ayudaWordleVista', 'true');
        }
    });
    // CSRF TOKEN
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const claveLocal = `wordleEstado_{{ request.user.username }}`;

    function guardarJugadaLocal(palabra, colores) {
        const hoy = new Date().toDateString();
        let estado = JSON.parse(localStorage.getItem(claveLocal)) || {
            fecha: hoy,
            jugadas: []
        };
        if (estado.fecha !== hoy) {
            estado = {
                fecha: hoy,
                jugadas: []
            };
        }
        estado.jugadas.push({
            palabra: palabra,
            colores: colores
        });
        localStorage.setItem(claveLocal, JSON.stringify(estado));
    }

    function cargarTableroLocal() {
        const hoy = new Date().toDateString();
        // Lee de la clave única del usuario
        const estado = JSON.parse(localStorage.getItem(claveLocal));
        if (estado && estado.fecha === hoy && estado.jugadas.length > 0) {
            const coloresTailwind = {
                'correct': 'bg-key-correct text-white border-key-correct',
                'present': 'bg-key-present text-white border-key-present',
                'absent': 'bg-key-absent text-white border-key-absent'
            };
            estado.jugadas.forEach((jugada, indexFila) => {
                for (let i = 0; i < 5; i++) {
                    const casilla = document.getElementById(`box-${indexFila}${i}`);
                    const letra = jugada.palabra[i];
                    const colorEstado = jugada.colores[i];
                    casilla.innerText = letra;
                    casilla.className = `w-14 h-14 flex items-center justify-center text-2xl font-bold uppercase transition-all duration-500 ${coloresTailwind[colorEstado]}`;
                    actualizarTeclado(letra, colorEstado);
                }
            });
            filaActual = estado.jugadas.length;
        }
    }
    // 1. GENERACIÓN DEL TABLERO
    const tablero = document.getElementById("tablero");
    for (let fila = 0; fila < 6; fila++) {
        for (let col = 0; col < 5; col++) {
            const casilla = document.createElement("div");
            casilla.id = `box-${fila}${col}`;
            casilla.className = "w-14 h-14 border-2 border-slate-300 dark:border-slate-600 bg-transparent dark:text-slate-100 flex items-center justify-center text-2xl font-bold uppercase transition-all";
            tablero.appendChild(casilla);
        }
    }
    // 2. GENERACIÓN DEL TECLADO VIRTUAL
    const filasTeclado = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"],
        ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "DEL"]
    ];
    const keyboard = document.getElementById("keyboard");
    filasTeclado.forEach((fila) => {
        const filaDiv = document.createElement("div");
        filaDiv.className = "flex gap-1.5 w-full justify-center";
        fila.forEach(letra => {
            const tecla = document.createElement("button");
            tecla.id = `key-${letra}`;
            let clases = "h-14 flex items-center justify-center text-sm font-bold rounded-lg cursor-pointer transition-colors uppercase focus:outline-none ";
            clases += "bg-key-default hover:bg-key-hover text-[#1A1A1A] ";
            if (letra === "ENTER" || letra === "DEL") {
                clases += "px-4 min-w-[70px] bg-[#E3E8EC] border-[#BFC3C7] ";
                if (letra === "ENTER") clases += "text-[10px] ";
            } else {
                clases += "w-11";
            }
            tecla.className = clases;
            tecla.innerText = letra === "DEL" ? "⌫" : letra;
            tecla.onclick = () => manejarEntrada(letra);
            filaDiv.appendChild(tecla);
        });
        keyboard.appendChild(filaDiv);
    });
    const prioridadColor = {
        correct: 3,
        present: 2,
        absent: 1
    };
    const estadoTeclado = {};

    function actualizarTeclado(letra, estado) {
        const prioridadActual = prioridadColor[estadoTeclado[letra]] || 0;
        const prioridadNueva = prioridadColor[estado] || 0;
        if (prioridadNueva <= prioridadActual) return;
        estadoTeclado[letra] = estado;
        const tecla = document.getElementById(`key-${letra}`);
        if (!tecla) return;
        tecla.classList.remove('bg-key-default', 'hover:bg-key-hover', 'text-[#1A1A1A]', 'bg-key-correct', 'hover:bg-key-correct', 'bg-key-present', 'hover:bg-key-present', 'bg-key-absent', 'hover:bg-key-absent', 'text-white');
        if (estado === 'correct') {
            tecla.classList.add('bg-key-correct', 'hover:bg-key-correct', 'text-white');
        } else if (estado === 'present') {
            tecla.classList.add('bg-key-present', 'hover:bg-key-present', 'text-white');
        } else if (estado === 'absent') {
            tecla.classList.add('bg-key-absent', 'hover:bg-key-absent', 'text-white');
        }
    }
    // EASTER EGG
    const videoSecreto = document.getElementById('video-david');

    function activarEasterEgg() {
        videoSecreto.style.display = 'block';
        const playPromise = videoSecreto.play();
        if (playPromise !== undefined) {
            playPromise.catch((err) => {
                console.warn('Reproducción automática bloqueada:', err);
                showPlayOverlay();
            });
        }
    }

    function showPlayOverlay() {
        if (document.getElementById('video-play-overlay')) return;
        const overlay = document.createElement('div');
        overlay.id = 'video-play-overlay';
        overlay.style = 'position: fixed; inset: 0; display:flex; align-items:center; justify-content:center; z-index:10000; background: rgba(0,0,0,0.4);';
        overlay.innerHTML = `<button id="video-play-btn" style="padding:12px 20px; font-size:16px; border-radius:10px; background:#700040; color:#fff; border:none; cursor:pointer;">Reproducir vídeo</button>`;
        overlay.addEventListener('click', (e) => {
            if (e.target.id !== 'video-play-btn') return;
            const btn = document.getElementById('video-play-btn');
            btn.disabled = true;
            videoSecreto.play().then(() => {
                overlay.remove();
            }).catch(err => {
                console.error('No se pudo reproducir el vídeo después de interacción:', err);
                btn.disabled = false;
            });
        });
        document.body.appendChild(overlay);
    }
    videoSecreto.onended = () => {
        videoSecreto.style.display = 'none';
    };
    // 3. LÓGICA CENTRAL DEL JUEGO
    function manejarEntrada(letra) {
        if (juegoTerminado || animando) return;
        if (letra === "DEL") {
            if (colActual > 0) {
                colActual--;
                intentoActual = intentoActual.slice(0, -1);
                document.getElementById(`box-${filaActual}${colActual}`).innerText = "";
            }
        } else if (letra === "ENTER") {
            if (intentoActual.length === 5) {
                // EASTER EGG
                if (intentoActual === "DAVID") {
                    activarEasterEgg();
                    for (let i = 0; i < 5; i++) {
                        document.getElementById(`box-${filaActual}${i}`).innerText = "";
                    }
                    intentoActual = "";
                    colActual = 0;
                    return;
                }
                animando = true;
                const tiempoFinal = Date.now();
                const segundosTranscurridos = Math.floor((tiempoFinal - tiempoInicio) / 1000);
                fetch('/wordle/check-guess/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        guess: intentoActual,
                        attempt: filaActual + 1,
                        time: segundosTranscurridos
                    })
                }).then(response => response.json()).then(data => {
                    if (data.status === "401") {
                        alert(data.mssg);
                        animando = false;
                        return;
                    }
                    if (data.status === "invalid_word") {
                        for (let i = 0; i < 5; i++) {
                            const casilla = document.getElementById(`box-${filaActual}${i}`);
                            casilla.classList.add('shake');
                            setTimeout(() => {
                                casilla.classList.remove('shake');
                                casilla.innerText = "";
                            }, 500);
                        }
                        setTimeout(() => {
                            intentoActual = "";
                            colActual = 0;
                            animando = false;
                        }, 500);
                        return;
                    }
                    const coloresTailwind = {
                        'correct': 'bg-key-correct text-white border-key-correct',
                        'present': 'bg-key-present text-white border-key-present',
                        'absent': 'bg-key-absent text-white border-key-absent'
                    };
                    guardarJugadaLocal(intentoActual, data.colors);
                    const tiempoTotalAnimacion = 5 * 600 + 600;
                    for (let i = 0; i < 5; i++) {
                        const casilla = document.getElementById(`box-${filaActual}${i}`);
                        const colorEstado = data.colors[i];
                        const letraActual = intentoActual[i];
                        setTimeout(() => {
                            casilla.classList.add('anim-flip');
                            setTimeout(() => {
                                casilla.className = `w-14 h-14 flex items-center justify-center text-2xl font-bold uppercase transition-all duration-500 ${coloresTailwind[colorEstado]}`;
                                actualizarTeclado(letraActual, colorEstado);
                            }, 600);
                        }, i * 600);
                    }
                    setTimeout(() => {
                        if (data.win) {
                            juegoTerminado = true;
                            animando = false;
                            for (let i = 0; i < 5; i++) {
                                setTimeout(() => {
                                    const box = document.getElementById(`box-${filaActual}${i}`);
                                    box.classList.add('-translate-y-3');
                                    setTimeout(() => box.classList.remove('-translate-y-3'), 150);
                                }, i * 150);
                            }
                            const intentosUsados = filaActual + 1;
                            const puntuacionFinal = 100 - ((intentosUsados - 1) * 10);
                            const tiempoFormateado = formatearTiempo(segundosTranscurridos);
                            setTimeout(() => {
                                mostrarModalFinal("¡HAS GANADO!", `
                                    <div class="flex justify-around mb-6 text-slate-600 dark:text-slate-300 text-sm mt-4">
                                        <div class="flex flex-col items-center">
                                            <span class="font-bold text-primary text-xl">${intentosUsados}/6</span>
                                            <span>Intentos</span>
                                        </div>
                                        <div class="flex flex-col items-center">
                                            <span class="font-bold text-primary text-xl">${tiempoFormateado}</span>
                                            <span>Tiempo</span>
                                        </div>
                                    </div>
                                    <div class="bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 p-4 rounded-xl mb-4">
                                        <p class="text-xs text-slate-400 dark:text-slate-400 uppercase tracking-widest font-bold mb-1">Puntuación Total</p>
                                        <p class="text-6xl font-extrabold text-[#C9B458] font-display">${puntuacionFinal}</p>
                                    </div>
                                `);
                            }, 1500);
                            setTimeout(() => {
                                var duration = 3 * 1000;
                                var end = Date.now() + duration;
                                (function frame() {
                                    confetti({
                                        particleCount: 3,
                                        angle: 60,
                                        spread: 55,
                                        origin: {
                                            x: 0,
                                            y: 0.8
                                        }
                                    });
                                    confetti({
                                        particleCount: 3,
                                        angle: 120,
                                        spread: 55,
                                        origin: {
                                            x: 1,
                                            y: 0.8
                                        }
                                    });
                                    if (Date.now() < end) requestAnimationFrame(frame);
                                }());
                            }, 900);
                        } else if (filaActual === 5) {
                            juegoTerminado = true;
                            animando = false;
                            const tiempoFormateado = formatearTiempo(segundosTranscurridos);
                            const palabraCorrecta = data.word ? data.word.toUpperCase() : "";
                            mostrarModalFinal("¡OH NO!", `
                                <p class="text-slate-600 dark:text-slate-300 mb-4">Te has quedado sin intentos.</p>
                                ${palabraCorrecta ? `
                                <div class="bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 p-3 rounded-xl mb-4">
                                    <p class="text-xs text-slate-400 dark:text-slate-400 uppercase tracking-widest font-bold mb-1">La palabra era</p>
                                    <p class="text-3xl font-extrabold text-primary font-display">${palabraCorrecta}</p>
                                </div>` : ""}
                                <div class="flex justify-around mb-6 text-slate-600 dark:text-slate-300 text-sm">
                                    <div class="flex flex-col items-center">
                                        <span class="font-bold text-slate-400 text-xl">0</span>
                                        <span>Puntos</span>
                                    </div>
                                    <div class="flex flex-col items-center">
                                        <span class="font-bold text-slate-400 text-xl">${tiempoFormateado}</span>
                                        <span>Tiempo</span>
                                    </div>
                                </div>
                            `);
                        }
                        if (!data.win && filaActual < 5) {
                            filaActual++;
                            colActual = 0;
                            intentoActual = "";
                            animando = false;
                        }
                    }, tiempoTotalAnimacion);
                }).catch(error => {
                    console.error("Error de conexión:", error);
                    animando = false;
                });
            }
        } else if (intentoActual.length < 5 && letra.length === 1) {
            const casilla = document.getElementById(`box-${filaActual}${colActual}`);
            casilla.innerText = letra;
            casilla.classList.add("scale-110", "border-slate-500");
            setTimeout(() => casilla.classList.remove("scale-110", "border-slate-500"), 100);
            intentoActual += letra;
            colActual++;
        }
    }
    // 4. LISTENER TECLADO FÍSICO
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') manejarEntrada('ENTER');
        else if (e.key === 'Backspace') manejarEntrada('DEL');
        else if (e.key.length === 1 && e.key.match(/[a-zñ]/i)) manejarEntrada(e.key.toUpperCase());
    });
    // 5. INICIALIZADOR AL CARGAR LA PÁGINA
    fetch('/wordle/daily/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    }).then(response => response.json()).then(data => {
        if (data.status === "401") {
            console.log("El usuario debe iniciar sesión.");
        } else if (data.status === "200") {
            console.log("Palabra del día lista para jugar.");
            // Cargamos el tablero si recarga a mitad de partida
            cargarTableroLocal();
        } else if (data.status === "409") {
            juegoTerminado = true;
            animando = true;
            cargarTableroLocal();
            const stats = data.stats || {
                attempts: 0,
                score: 0,
                time: 0
            };
            const tiempoFormateado = formatearTiempo(stats.time);
            mostrarModalFinal("YA HAS JUGADO HOY", `
                <div class="flex justify-around mb-6 text-slate-600 dark:text-slate-300 text-sm mt-4">
                    <div class="flex flex-col items-center">
                        <span class="font-bold text-primary text-xl">${stats.attempts}/6</span>
                        <span>Intentos</span>
                    </div>
                    <div class="flex flex-col items-center">
                        <span class="font-bold text-primary text-xl">${tiempoFormateado}</span>
                        <span>Tiempo</span>
                    </div>
                </div>
                <div class="bg-slate-50 dark:bg-slate-700 border-2 border-slate-200 dark:border-slate-600 p-4 rounded-xl mb-4">
                    <p class="text-xs text-slate-400 dark:text-slate-400 uppercase tracking-widest font-bold mb-1">Tu Puntuación</p>
                    <p class="text-6xl font-extrabold text-[#C9B458] font-display">${stats.score}</p>
                </div>
                <p class="text-sm text-slate-400 font-bold uppercase tracking-widest mt-2">Vuelve mañana para un nuevo reto</p>
            `);
        }
    }).catch(error => console.error("Error de conexión:", error));