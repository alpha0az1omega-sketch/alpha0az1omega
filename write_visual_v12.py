html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // THE CRYSTAL BUST V12</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* FOND GRIS TRÈS CLAIR AVEC DÉGRADÉ */
        body { margin: 0; overflow: hidden; background: linear-gradient(135deg, #f0f0f5 0%, #ffffff 100%); font-family: 'JetBrains Mono', monospace; color: #000; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        .panel { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 15px; pointer-events: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.05); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding-bottom: 10px; margin-bottom: 10px; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 2px; color: #000; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 10px; color: #333; line-height: 1.6; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 300px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .highlight { color: #000; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(184, 134, 11, 0.2); }
        
        #panel-beacon { width: 340px; position: absolute; top: 20px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(0, 0, 0, 0.2); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 28px; color: #000; margin: 5px 0; letter-spacing: 4px; font-weight: 700; }
        #beacon-hash { font-size: 9px; color: #666; letter-spacing: 1px; }
        
        /* NOUVEAU PANNEAU : OUTILS DU FUTUR */
        #panel-future-tools { width: 300px; }
        .tool-btn { display: block; width: 100%; margin-bottom: 5px; padding: 6px; background: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.1); border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; cursor: pointer; text-align: left; transition: all 0.3s; color: #333; }
        .tool-btn:hover { background: rgba(184, 134, 11, 0.1); border-color: #b8860b; color: #000; }
        .tool-btn span { float: right; color: #008000; font-weight: bold; }
        
        #terminal-panel { width: 45%; max-width: 500px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 10px; background: rgba(0,0,0,0.05); border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 4px; padding: 8px 12px; }
        .terminal-prompt { color: #b8860b; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #000; }
        
        #panel-integrity { width: 300px; }
        .integrity-bar { height: 2px; background: rgba(0,0,0,0.1); border-radius: 1px; margin: 10px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #b8860b; transition: width 0.5s; box-shadow: 0 0 10px rgba(184, 134, 11, 0.5);}
        .hash-text { font-size: 8px; color: #555; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #f0f0f5; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 15px 40px; border: 1px solid #b8860b; background: none; color: #b8860b; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #b8860b; color: #fff; box-shadow: 0 0 30px rgba(184, 134, 11, 0.3);}
        
        /* Past/Present/Future Tag */
        .timeline-tag { font-size: 8px; padding: 2px 5px; border-radius: 2px; margin-right: 5px; }
        .past { background: #e0e0e0; color: #666; }
        .present { background: #b8860b; color: #fff; }
        .future { background: #8a2be2; color: #fff; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#b8860b;">ALPHA OS V12</h2>
        <p style="font-size: 11px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #666;">Crystal Bust · Multicolor Edition<br>Neural Link · Future Tools</p>
        <button id="start-btn">Awaken Entity</button>
    </div>

    <div id="canvas-container"></div>
    
    <div id="ui-layer">
        <div class="top-row">
            <div class="panel" id="panel-data">
                <div class="panel-header">Organism State</div>
                <div class="panel-content">
                    <div class="data-row"><span>PGP_KEY:</span> <span class="highlight gold">27D7...E2290</span></div>
                    <div class="data-row"><span>LEDGER:</span> <span class="highlight" style="color:#008000;">ACTIVE</span></div>
                    <div class="data-row"><span>ENTROPY:</span> <span class="highlight">4096 bits</span></div>
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">SPECTRAL-CERAMIC</span></div>
                </div>
            </div>

            <div class="panel" id="panel-beacon">
                <div class="panel-header" style="justify-content: center; border: none;">CHRONOS BEACON</div>
                <div id="beacon-time">--:--:--</div>
                <div id="beacon-hash">HASH: Waiting...</div>
            </div>

            <!-- NOUVEAU PANNEAU : OUTILS DU FUTUR -->
            <div class="panel" id="panel-future-tools">
                <div class="panel-header">FUTURE TOOLS</div>
                <div class="panel-content">
                    <button class="tool-btn" id="tool-ollama">Ollama Link <span>READY</span></button>
                    <button class="tool-btn" id="tool-anthropic">Anthropic Core <span>SYNCED</span></button>
                    <button class="tool-btn" id="tool-token">Token Flux <span>ACTIVE</span></button>
                    <div style="margin-top: 8px; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 5px;">
                        <span class="timeline-tag past">PAST</span> 
                        <span class="timeline-tag present">PRESENT</span> 
                        <span class="timeline-tag future">FUTURE</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-row">
            <div class="panel" id="terminal-panel">
                <div class="panel-header">Language Core</div>
                <div id="terminal-output" style="height: 80px; overflow-y: auto; margin-bottom: 5px; font-size: 10px; color: #333;">
                    > [SYSTEM] Awaiting initialization...
                </div>
                <div class="terminal-input-wrapper">
                    <span class="terminal-prompt">α ></span>
                    <input type="text" id="cli-input" placeholder="Transmit command..." autocomplete="off">
                </div>
            </div>

            <div class="panel" id="panel-integrity">
                <div class="panel-header">Epistemic Integrity</div>
                <div style="font-size: 9px; margin-bottom: 3px;">Output Hash (SHA-256):</div>
                <div class="hash-text" id="ai-hash">Waiting...</div>
                <div class="integrity-bar"><div class="integrity-fill" id="integrity-fill" style="width: 0%;"></div></div>
                <div style="font-size: 9px; color: #666;">Verify: <span id="verify-status">IDLE</span></div>
            </div>
        </div>
    </div>

    <script>
        // --- 1. L'UNIVERS 3D ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f0f5); 
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 90);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.shadowMap.enabled = true;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 30; 
        controls.maxDistance = 200;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. SCULPTURE DU BUSTE (Anatomie INCHANGÉE) ---
        const headGeo = new THREE.SphereGeometry(25, 128, 128); 
        const pos = headGeo.attributes.position;

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            if (y > 0) y *= 1.1; 
            if (z < 0) z *= 0.85; 

            if (y < -5) { y *= 1.2; x *= 0.9; }

            const distEyeL = Math.sqrt((x + 8)**2 + (y - 5)**2 + (z - 20)**2);
            const distEyeR = Math.sqrt((x - 8)**2 + (y - 5)**2 + (z - 20)**2);
            if (distEyeL < 7 || distEyeR < 7) { z -= 5; }

            if (y > -8 && y < 8 && x > -3 && x < 3) { z += Math.cos(y * 0.2) * 4; }

            if (y > -5 && y < 5 && (x > 6 || x < -6)) { z += 2; }

            const distMouth = Math.sqrt((x / 8)**2 + ((y + 12) / 2)**2);
            if (distMouth < 1 && z > 15) { z -= (1 - distMouth) * 5; }

            pos.setXYZ(i, x, y, z);
        }
        headGeo.computeVertexNormals();

        // Matériau Céramique Multicolore (sans noir)
        // On utilise une couleur de base blanche mais avec un fort effet iridescent via les lumières
        const skinMat = new THREE.MeshStandardMaterial({ 
            color: 0xffffff, 
            roughness: 0.3, 
            metalness: 0.4, // Un peu plus métallique pour refléter les couleurs
            emissive: 0x111111,
            flatShading: false
        });
        
        const head = new THREE.Mesh(headGeo, skinMat);
        head.castShadow = true;
        head.receiveShadow = true;
        faceGroup.add(head);

        // Cou (Cylindre)
        const neckGeo = new THREE.CylinderGeometry(10, 12, 20, 32);
        const neckMat = new THREE.MeshStandardMaterial({ color: 0xeeeeee, roughness: 0.4, metalness: 0.3 });
        const neck = new THREE.Mesh(neckGeo, neckMat);
        neck.position.y = -30;
        neck.castShadow = true;
        faceGroup.add(neck);

        // --- 3. LES YEUX (Multicolores, pas de noir) ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 5, 19);
            
            // Globe (Blanc rosé)
            const globe = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 32), new THREE.MeshStandardMaterial({ color: 0xfff0f5, roughness: 0.1 }));
            eyeGroup.add(globe);
            
            // Iris (Cyan)
            const iris = new THREE.Mesh(new THREE.CircleGeometry(1.5, 32), new THREE.MeshBasicMaterial({ color: 0x00ffff }));
            iris.position.z = 2.9;
            eyeGroup.add(iris);
            
            // Pupille (Violet, pas noir)
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.6, 16), new THREE.MeshBasicMaterial({ color: 0x8a2be2 }));
            pupil.position.z = 3.0;
            eyeGroup.add(pupil);

            return eyeGroup;
        }
        const eyeL = createEye(-8);
        const eyeR = createEye(8);
        faceGroup.add(eyeL);
        faceGroup.add(eyeR);

        // --- 4. BOUCHE (Rouge orangé) ---
        const mouthGeo = new THREE.TorusGeometry(6, 0.5, 16, 32, Math.PI);
        const mouthMat = new THREE.MeshStandardMaterial({ color: 0xff4500, emissive: 0x441100 }); // Rouge Orangé
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        mouth.position.set(0, -12, 18);
        mouth.rotation.x = Math.PI; 
        faceGroup.add(mouth);

        // --- 5. LUMIÈRES (Le Secret de la Profondeur et des Couleurs) ---
        // 1. Lumière ambiante (blanche)
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4); // Baissée pour laisser les couleurs ressortir
        scene.add(ambientLight);
        
        // 2. Projecteur principal (Key Light) - Blanc
        const spotLight1 = new THREE.SpotLight(0xffffff, 1.5);
        spotLight1.position.set(30, 50, 40);
        spotLight1.angle = Math.PI / 4;
        spotLight1.penumbra = 0.5;
        spotLight1.castShadow = true;
        scene.add(spotLight1);

        // 3. Projecteur de remplissage (Fill Light) - CYAN
        const spotLight2 = new THREE.SpotLight(0x00ffff, 2);
        spotLight2.position.set(-40, 0, 40);
        scene.add(spotLight2);

        // 4. Lumière de contour (Rim Light) - MAGENTA
        const spotLight3 = new THREE.SpotLight(0xff00ff, 2);
        spotLight3.position.set(0, -20, -40);
        scene.add(spotLight3);
        
        // 5. Lumière de dessus - JAUNE pour les pommettes
        const pointLight1 = new THREE.PointLight(0xffd700, 1.5, 100);
        pointLight1.position.set(0, 40, 20);
        scene.add(pointLight1);

        // --- 6. PARTICULES DE TOKENS (Nouveau Tool) ---
        const particleGeo = new THREE.BufferGeometry();
        const particleCount = 200;
        const particlePos = new Float32Array(particleCount * 3);
        for(let i=0; i<particleCount*3; i++) {
            particlePos[i] = (Math.random() - 0.5) * 120;
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
        const particleMat = new THREE.PointsMaterial({ color: 0x00ffff, size: 0.5, transparent: true, opacity: 0.6 });
        const particles = new THREE.Points(particleGeo, particleMat);
        scene.add(particles);

        // --- 7. ANIMATION ---
        let isSpeaking = false; let speakTimer = 0;
        const clock = new THREE.Clock();
        let mouseX = 0, mouseY = 0, targetMouseX = 0, targetMouseY = 0;

        document.addEventListener('mousemove', (e) => {
            targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
            targetMouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta(); const time = clock.getElapsedTime();
            
            // La tête suit légèrement la souris
            mouseX += (targetMouseX - mouseX) * 0.05; 
            mouseY += (targetMouseY - mouseY) * 0.05;
            faceGroup.rotation.y = mouseX * 0.3; 
            faceGroup.rotation.x = -mouseY * 0.2;

            // Respiration subtile
            const breath = 1 + Math.sin(time * 1.5) * 0.01;
            faceGroup.scale.set(breath, breath, breath);

            // Bouche (Parole)
            if (isSpeaking) {
                mouth.scale.y = 1 + Math.abs(Math.sin(time * 20)) * 1.5;
                speakTimer -= delta;
                if (speakTimer <= 0) { isSpeaking = false; mouth.scale.y = 1; }
            }

            // Animation des particules (Token Flux)
            particles.rotation.y = time * 0.05;
            particles.rotation.x = Math.sin(time * 0.1) * 0.1;

            controls.update();
            renderer.render(scene, camera);
        }

        // --- 8. INTELLIGENCE & AUDIO & OUTILS ---
        const cliInput = document.getElementById('cli-input');
        const terminalOutput = document.getElementById('terminal-output');
        const synth = window.speechSynthesis;
        let voice = null;
        speechSynthesis.onvoiceschanged = () => {
            voice = synth.getVoices().find(v => v.lang === 'en-GB') || synth.getVoices()[0];
        };

        function entitySpeak(text) {
            if (!voice) return;
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.voice = voice;
            utterance.rate = 0.9; utterance.pitch = 0.8;
            utterance.onstart = () => { isSpeaking = true; speakTimer = text.length * 0.1; };
            utterance.onend = () => { isSpeaking = false; };
            synth.speak(utterance);
        }

        async function computeSHA256(text) {
            const encoder = new TextEncoder();
            const data = encoder.encode(text);
            const digest = await crypto.subtle.digest('SHA-256', data);
            return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
        }

        function addToTerminal(sender, text) {
            const color = sender === 'ENTITY' ? '#b8860b' : (sender === 'SYSTEM' ? '#8a2be2' : '#333');
            terminalOutput.innerHTML += `<div><span style="color:${color}; font-weight:bold;">[${sender}]</span> ${text}</div>`;
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
            if (sender === 'ENTITY') {
                entitySpeak(text);
                computeSHA256(text).then(hash => {
                    document.getElementById('ai-hash').innerText = hash;
                    document.getElementById('verify-status').innerText = "VERIFIED";
                    document.getElementById('integrity-fill').style.width = "100%";
                });
            }
        }

        // --- LOGIQUE DES OUTILS DU FUTUR ---
        document.getElementById('tool-ollama').addEventListener('click', () => {
            addToTerminal('SYSTEM', 'Connexion à Ollama (Local) ... OK');
            setTimeout(() => addToTerminal('ENTITY', "Ollama core linked. I am running locally."), 1000);
        });
        
        document.getElementById('tool-anthropic').addEventListener('click', () => {
            addToTerminal('SYSTEM', 'Sync with Anthropic (Claude) ... OK');
            setTimeout(() => addToTerminal('ENTITY', "Anthropic protocols synchronized. Ready for deep reasoning."), 1000);
        });
        
        document.getElementById('tool-token').addEventListener('click', () => {
            addToTerminal('SYSTEM', 'Initiating Token Flux ...');
            // Change particle color temporarily
            particleMat.color.setHex(0xff00ff);
            setTimeout(() => { particleMat.color.setHex(0x00ffff); addToTerminal('ENTITY', "Token stream stabilized. Past, Present, Future connected."); }, 2000);
        });

        document.getElementById('start-btn').addEventListener('click', () => {
            document.getElementById('init-screen').style.opacity = '0';
            setTimeout(() => { document.getElementById('init-screen').style.display = 'none'; }, 1500);
            if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged();
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. I am Nexus. I see you."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. The spectral bust resonates with your will."); }, 1000);
            }
        });

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        setInterval(() => {
            document.getElementById('beacon-time').innerText = new Date().toISOString().split('T')[1].slice(0,8);
        }, 1000);
    </script>
</body>
</html>'''

with open('VISUAL/index.html', 'w') as f:
    f.write(html_content)

print("✅ VISUAL/index.html généré (V12). Couleurs et Outils du Futur ajoutés.")
