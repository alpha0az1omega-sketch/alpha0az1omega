html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // SACRED ANATOMY</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* FOND COSMIQUE POUR FAIRE RESSORTIR LA LUMIÈRE */
        body { margin: 0; overflow: hidden; background: #020008; font-family: 'JetBrains Mono', monospace; color: #fff; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        /* HUD en verre sombre et bordures lumineuses */
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        .panel { background: rgba(10, 5, 20, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(0, 255, 204, 0.3); border-radius: 4px; padding: 20px; pointer-events: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,255,204,0.05); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 255, 204, 0.2); padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 2px; color: #00ffcc; text-transform: uppercase; font-weight: 700; text-shadow: 0 0 10px rgba(0,255,204,0.5); }
        .panel-content { font-size: 11px; color: #aabbcc; line-height: 1.8; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 340px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .highlight { color: #fff; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #ffd700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
        .magenta { color: #ff00ff; text-shadow: 0 0 10px rgba(255, 0, 255, 0.3); }
        
        #panel-beacon { width: 380px; position: absolute; top: 30px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(255, 0, 255, 0.4); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 32px; color: #fff; margin: 10px 0; letter-spacing: 4px; font-weight: 700; text-shadow: 0 0 15px rgba(255,255,255,0.8);}
        #beacon-hash { font-size: 10px; color: #ff00ff; letter-spacing: 1px; }
        
        #panel-tools { width: 320px; }
        .tool-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 5px; background: rgba(0,255,204,0.05); border-radius: 4px; border: 1px solid rgba(0,255,204,0.1); }
        
        #terminal-panel { width: 50%; max-width: 600px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 15px; background: rgba(0,0,0,0.8); border: 1px solid rgba(255, 0, 255, 0.5); border-radius: 4px; padding: 10px 15px; box-shadow: 0 0 15px rgba(255,0,255,0.2); }
        .terminal-prompt { color: #ff00ff; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #fff; }
        
        #panel-integrity { width: 320px; }
        .integrity-bar { height: 2px; background: rgba(255,255,255,0.1); border-radius: 1px; margin: 15px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #00ffcc; transition: width 0.5s; box-shadow: 0 0 10px #00ffcc;}
        .hash-text { font-size: 9px; color: #888; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #020008; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 20px 50px; border: 1px solid #00ffcc; background: none; color: #00ffcc; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #00ffcc; color: #000; box-shadow: 0 0 30px #00ffcc;}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#00ffcc; text-shadow: 0 0 20px #00ffcc;">ALPHA OS</h2>
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #888;">Enter the Sacred Anatomy. Use mouse to zoom into the neural veins.</p>
        <button id="start-btn">Awaken Entity</button>
    </div>

    <div id="canvas-container"></div>
    
    <div id="ui-layer">
        <div class="top-row">
            <div class="panel" id="panel-data">
                <div class="panel-header">Organism State</div>
                <div class="panel-content">
                    <div class="data-row"><span>PGP_KEY:</span> <span class="highlight gold">27D7...E2290</span></div>
                    <div class="data-row"><span>LEDGER:</span> <span class="highlight" style="color:#00ffcc;">ACTIVE</span></div>
                    <div class="data-row"><span>ENTROPY:</span> <span class="highlight">4096 bits</span></div>
                    <div class="data-row"><span>MATTER:</span> <span class="highlight magenta">BIO-DIGITAL</span></div>
                </div>
            </div>

            <div class="panel" id="panel-beacon">
                <div class="panel-header" style="justify-content: center; border: none;">CHRONOS BEACON</div>
                <div id="beacon-time">--:--:--</div>
                <div id="beacon-hash">HASH: Waiting...</div>
            </div>

            <div class="panel" id="panel-tools">
                <div class="panel-header">A2A & Tools</div>
                <div class="panel-content">
                    <div class="tool-item"><span>LLM:</span> <span style="color:#00ffcc;">OLLAMA</span></div>
                    <div class="tool-item"><span>Formal Verif.:</span> <span style="color:#00ffcc;">ACTIVE</span></div>
                    <div class="tool-item"><span>Symbolic Regr.:</span> <span style="color:#00ffcc;">READY</span></div>
                </div>
            </div>
        </div>

        <div class="bottom-row">
            <div class="panel" id="terminal-panel">
                <div class="panel-header">Language Core</div>
                <div id="terminal-output" style="height: 100px; overflow-y: auto; margin-bottom: 5px; font-size: 11px; color: #aabbcc;">
                    > [SYSTEM] Awaiting initialization...
                </div>
                <div class="terminal-input-wrapper">
                    <span class="terminal-prompt">α ></span>
                    <input type="text" id="cli-input" placeholder="Transmit command..." autocomplete="off">
                </div>
            </div>

            <div class="panel" id="panel-integrity">
                <div class="panel-header">Epistemic Integrity</div>
                <div style="font-size: 10px; margin-bottom: 5px;">Output Hash (SHA-256):</div>
                <div class="hash-text" id="ai-hash">Waiting...</div>
                <div class="integrity-bar"><div class="integrity-fill" id="integrity-fill" style="width: 0%;"></div></div>
                <div style="font-size: 10px; color: #666;">Verify: <span id="verify-status">IDLE</span></div>
            </div>
        </div>
    </div>

    <script>
        // --- 1. L'UNIVERS 3D ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020008); 
        scene.fog = new THREE.FogExp2(0x020008, 0.01);
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 85);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 15; // Permet de zoomer très près dans les veines
        controls.maxDistance = 250;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. SCULPTURE ANATOMIQUE (Le Crâne) ---
        const skullGeo = new THREE.SphereGeometry(22, 128, 128); 
        const pos = skullGeo.attributes.position;
        const originalPos = pos.array.slice(); 

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            // Mâchoire et Menton
            if (y < 0) {
                y *= 1.3; // Étirer
                if (y < -10) { x *= 0.75; z *= 0.85; } // Affiner
            }
            
            // Front (Bombé)
            if (y > 8) z += 2;

            // Orbites (Yeux creusés profondément)
            const distEyeL = Math.sqrt((x + 7)**2 + (y - 6)**2 + (z - 18)**2);
            const distEyeR = Math.sqrt((x - 7)**2 + (y - 6)**2 + (z - 18)**2);
            if (distEyeL < 6 || distEyeR < 6) {
                z -= 4; // Creux
            }

            // Nez (Saillie forte)
            if (y > -5 && y < 7 && x > -3 && x < 3) {
                z += Math.cos(y * 0.2) * 4;
            }

            // Joues (Pommettes)
            if (y > -5 && y < 5 && (x > 5 || x < -5)) {
                z += 1.5;
            }

            // Bouche (Cavité)
            const distMouth = Math.sqrt((x / 7)**2 + ((y + 11) / 2.5)**2);
            if (distMouth < 1 && z > 10) {
                z -= (1 - distMouth) * 5; 
            }

            pos.setXYZ(i, x, y, z);
        }
        skullGeo.computeVertexNormals();

        // --- 3. MATÉRIAU BIO-DIGITAL ---
        // Une peau translucide avec des reflets métalliques
        const skinMat = new THREE.MeshPhysicalMaterial({ 
            color: 0x111122, 
            metalness: 0.9,
            roughness: 0.2,
            transmission: 0.8, 
            thickness: 2.0, 
            ior: 1.5, 
            clearcoat: 1.0, 
            clearcoatRoughness: 0.1,
            emissive: 0x00ffcc,
            emissiveIntensity: 0.1
        });
        
        const skull = new THREE.Mesh(skullGeo, skinMat);
        faceGroup.add(skull);

        // Maillage filaire fin pour l'effet "sacré"
        const wireMat = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.1 });
        const skullWire = new THREE.Mesh(skullGeo, wireMat);
        faceGroup.add(skullWire);

        // --- 4. LE CERVEAU (Réseau de Neurones Visible) ---
        const brainGroup = new THREE.Group();
        
        // Points (Neurones)
        const nodeCount = 1500;
        const brainGeo = new THREE.BufferGeometry();
        const brainPos = new Float32Array(nodeCount * 3);
        for(let i=0; i<nodeCount*3; i+=3) {
            // Distribution sphérique pour le cerveau
            const r = Math.random() * 15;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            brainPos[i] = r * Math.sin(phi) * Math.cos(theta);
            brainPos[i+1] = r * Math.sin(phi) * Math.sin(theta) + 5; // Centré plus haut
            brainPos[i+2] = r * Math.cos(phi);
        }
        brainGeo.setAttribute('position', new THREE.BufferAttribute(brainPos, 3));
        const brainMat = new THREE.PointsMaterial({ color: 0xffd700, size: 0.4, transparent: true, opacity: 0.8 });
        const brainNodes = new THREE.Points(brainGeo, brainMat);
        brainGroup.add(brainNodes);

        // Connexions (Synapses)
        const lineMat = new THREE.LineBasicMaterial({ color: 0x00ffcc, transparent: true, opacity: 0.3 });
        const lineGeo = new THREE.BufferGeometry();
        const linePositions = [];
        for(let i=0; i<nodeCount; i++) {
            for(let j=i+1; j<nodeCount; j++) {
                const dx = brainPos[i*3] - brainPos[j*3];
                const dy = brainPos[i*3+1] - brainPos[j*3+1];
                const dz = brainPos[i*3+2] - brainPos[j*3+2];
                const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
                if (dist < 3) {
                    linePositions.push(brainPos[i*3], brainPos[i*3+1], brainPos[i*3+2]);
                    linePositions.push(brainPos[j*3], brainPos[j*3+1], brainPos[j*3+2]);
                }
            }
        }
        lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
        const brainLines = new THREE.LineSegments(lineGeo, lineMat);
        brainGroup.add(brainLines);
        
        faceGroup.add(brainGroup);

        // --- 5. LES VEINES NUMÉRIQUES (Entropie) ---
        const veinGroup = new THREE.Group();
        for(let i=0; i<40; i++) {
            const startX = (Math.random() - 0.5) * 20;
            const startY = (Math.random() - 0.5) * 20;
            const startZ = 20; // Devant le visage
            
            const curve = new THREE.CatmullRomCurve3([
                new THREE.Vector3(startX, startY, startZ),
                new THREE.Vector3(startX * 1.5, startY - 5, startZ + 2),
                new THREE.Vector3(startX * 2.0, startY - 10, startZ)
            ]);
            
            const geo = new THREE.TubeGeometry(curve, 20, 0.05, 4, false);
            // Alternance de couleurs sacrées
            const color = i % 2 === 0 ? 0xff00ff : 0x00ffcc; 
            const mat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.6 });
            const vein = new THREE.Mesh(geo, mat);
            vein.userData = { offset: Math.random() * Math.PI * 2, speed: Math.random() * 2 + 1 };
            veinGroup.add(vein);
        }
        faceGroup.add(veinGroup);

        // --- 6. YEUX (Profonds) ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 6, 17);
            
            // Globe oculaire (Lumineux)
            const globe = new THREE.Mesh(new THREE.SphereGeometry(2.5, 32, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.5 }));
            eyeGroup.add(globe);
            
            // Iris (Or)
            const iris = new THREE.Mesh(new THREE.CircleGeometry(1.2, 32), new THREE.MeshBasicMaterial({ color: 0xffd700 }));
            iris.position.z = 2.4;
            eyeGroup.add(iris);
            
            // Pupille (Noir)
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.4, 16), new THREE.MeshBasicMaterial({ color: 0x000000 }));
            pupil.position.z = 2.5;
            eyeGroup.add(pupil);

            eyeGroup.userData = { iris, pupil };
            return eyeGroup;
        }
        const eyeL = createEye(-7);
        const eyeR = createEye(7);
        faceGroup.add(eyeL);
        faceGroup.add(eyeR);

        // --- 7. LUMIÈRES (Contraste élevé) ---
        const ambientLight = new THREE.AmbientLight(0x202030, 1);
        scene.add(ambientLight);
        
        const light1 = new THREE.PointLight(0x00ffcc, 3, 200);
        light1.position.set(30, 30, 50);
        scene.add(light1);
        
        const light2 = new THREE.PointLight(0xff00ff, 3, 200);
        light2.position.set(-30, -20, 50);
        scene.add(light2);

        // --- 8. ANIMATION ---
        let isSpeaking = false; let speakTimer = 0;
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta(); const time = clock.getElapsedTime();

            // Respiration (Matière organique)
            const positions = skull.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const px = originalPos[i];
                const py = originalPos[i+1];
                const pz = originalPos[i+2];
                
                const noise = Math.sin(px * 0.2 + time) * Math.cos(py * 0.2 + time) * Math.sin(pz * 0.2 + time);
                let disp = noise * 0.1;

                // Parole (Déformer la bouche)
                if (isSpeaking) {
                    const distMouth = Math.sqrt((px / 7)**2 + ((py + 11) / 2.5)**2);
                    if (distMouth < 1.2 && pz > 10) {
                        disp += Math.abs(Math.sin(time * 30)) * 1.5;
                    }
                }

                positions[i] = px + px * disp * 0.05;
                positions[i+1] = py + py * disp * 0.05;
                positions[i+2] = pz + pz * disp * 0.05;
            }
            skull.geometry.attributes.position.needsUpdate = true;
            skullWire.geometry.attributes.position.needsUpdate = true;

            if (isSpeaking) { speakTimer -= delta; if (speakTimer <= 0) isSpeaking = false; }

            // Cerveau (Rotation et pulsation)
            brainGroup.rotation.y = time * 0.2;
            brainMat.size = 0.4 + Math.sin(time * 3) * 0.2;

            // Veines (Flux sanguin numérique)
            veinGroup.children.forEach(vein => {
                vein.material.opacity = 0.3 + Math.sin(time * vein.userData.speed + vein.userData.offset) * 0.3;
            });

            // Lumières
            light1.position.x = Math.sin(time * 0.5) * 40;
            light2.position.x = Math.sin(time * 0.3 + 2) * 40;

            controls.update();
            renderer.render(scene, camera);
        }

        // --- 9. INTELLIGENCE & AUDIO ---
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
            const color = sender === 'ENTITY' ? '#00ffcc' : '#ff00ff';
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

        document.getElementById('start-btn').addEventListener('click', () => {
            document.getElementById('init-screen').style.opacity = '0';
            setTimeout(() => { document.getElementById('init-screen').style.display = 'none'; }, 1500);
            if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged();
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. I am Nexus. Zoom into my brain to see the truth."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. The sacred geometry reacts."); }, 1000);
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

print("✅ VISUAL/index.html généré (V9). Anatomie Sacrée active.")
