html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // LIQUID NEURAL MATTER</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        body { margin: 0; overflow: hidden; background: #fcfcfc; font-family: 'JetBrains Mono', monospace; color: #000; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        .panel { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(15px); border: 1px solid rgba(184, 134, 11, 0.2); border-radius: 4px; padding: 20px; pointer-events: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.03); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(184, 134, 11, 0.2); padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 2px; color: #000; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 11px; color: #333; line-height: 1.8; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 340px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .highlight { color: #000; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(184, 134, 11, 0.2); }
        
        #panel-beacon { width: 380px; position: absolute; top: 30px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(184, 134, 11, 0.3); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 32px; color: #000; margin: 10px 0; letter-spacing: 4px; font-weight: 700; }
        #beacon-hash { font-size: 10px; color: #666; letter-spacing: 1px; }
        
        #panel-tools { width: 320px; }
        .tool-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 5px; background: rgba(184, 134, 11, 0.03); border-radius: 4px; border: 1px solid rgba(184, 134, 11, 0.1); }
        
        #terminal-panel { width: 50%; max-width: 600px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 15px; background: rgba(0,0,0,0.02); border: 1px solid rgba(184, 134, 11, 0.3); border-radius: 4px; padding: 10px 15px; }
        .terminal-prompt { color: #b8860b; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #000; }
        
        #panel-integrity { width: 320px; }
        .integrity-bar { height: 2px; background: rgba(0,0,0,0.05); border-radius: 1px; margin: 15px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #b8860b; transition: width 0.5s; box-shadow: 0 0 10px rgba(184, 134, 11, 0.5);}
        .hash-text { font-size: 9px; color: #555; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #fcfcfc; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 20px 50px; border: 1px solid #b8860b; background: none; color: #b8860b; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #b8860b; color: #fff; box-shadow: 0 0 30px rgba(184, 134, 11, 0.3);}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#b8860b; text-shadow: 0 0 20px rgba(184, 134, 11, 0.5);">ALPHA OS</h2>
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #666;">Synthesizing Liquid Neural Matter...</p>
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
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">LIQUID-GLASS</span></div>
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
                    <div class="tool-item"><span>LLM:</span> <span style="color:#008000;">OLLAMA</span></div>
                    <div class="tool-item"><span>Formal Verif.:</span> <span style="color:#008000;">ACTIVE</span></div>
                    <div class="tool-item"><span>Symbolic Regr.:</span> <span style="color:#008000;">READY</span></div>
                </div>
            </div>
        </div>

        <div class="bottom-row">
            <div class="panel" id="terminal-panel">
                <div class="panel-header">Language Core</div>
                <div id="terminal-output" style="height: 100px; overflow-y: auto; margin-bottom: 5px; font-size: 11px; color: #333;">
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
        // --- 1. L'UNIVERS 3D (Fond Blanc & Or) ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xfcfcfc); 
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 80);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 30;
        controls.maxDistance = 200;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. LA SCULPTURE DU VISAGE (Un seul maillage dense) ---
        // Icosaèdre haute résolution pour sculpter la matière
        const skullGeo = new THREE.IcosahedronGeometry(22, 6); 
        const pos = skullGeo.attributes.position;
        const originalPos = pos.array.slice(); 

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            // 1. Étirer la mâchoire vers le bas (Menton)
            if (y < 0) {
                y *= 1.25;
                // Affiner la mâchoire
                if (y < -10) { x *= 0.8; z *= 0.9; }
            }
            
            // 2. Créer le front
            if (y > 8) z += 1.5;

            // 3. Creuser les orbites (Yeux)
            const distEyeL = Math.sqrt((x + 7)**2 + (y - 6)**2 + (z - 18)**2);
            const distEyeR = Math.sqrt((x - 7)**2 + (y - 6)**2 + (z - 18)**2);
            if (distEyeL < 6 || distEyeR < 6) {
                z -= 3.5; // Creux profond
            }

            // 4. Sculpter le nez (Saillie)
            if (y > -5 && y < 8 && x > -3 && x < 3) {
                z += Math.cos(y * 0.15) * 3;
            }

            // 5. SCULPTER LA BOUCHE (Le creux)
            // On définit une zone ovale pour la bouche
            const distMouth = Math.sqrt((x / 8)**2 + ((y + 12) / 2)**2);
            if (distMouth < 1 && z > 10) {
                // On enfonce la matière pour créer la fente
                z -= (1 - distMouth) * 4; 
            }

            pos.setXYZ(i, x, y, z);
        }
        skullGeo.computeVertexNormals();

        // --- 3. LE MATÉRIAU "GLUANT / FUSION / VERRE LIQUIDE" ---
        const skinMat = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff,        // Blanc
            metalness: 0.2,         
            roughness: 0.05,        // Très lisse (gluant)
            transmission: 0.95,     // Transparence (verre)
            thickness: 3.0,         // Épaisseur pour la réfraction
            ior: 1.5,               // Indice de réfraction
            clearcoat: 1.0,         // Effet mouillé/glu
            clearcoatRoughness: 0.1,
            emissive: 0xb8860b,     // Lueur dorée interne
            emissiveIntensity: 0.1,
            wireframe: false
        });
        
        const skull = new THREE.Mesh(skullGeo, skinMat);
        faceGroup.add(skull);

        // Ajout d'un maillage filaire doré extrêmement fin par-dessus pour l'effet "digital"
        const wireMat = new THREE.MeshBasicMaterial({ color: 0xb8860b, wireframe: true, transparent: true, opacity: 0.05 });
        const skullWire = new THREE.Mesh(skullGeo, wireMat);
        faceGroup.add(skullWire);

        // --- 4. LES YEUX (Flottants dans les orbites) ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 6, 16);
            
            // Globe oculaire (Blanc laiteux)
            const globe = new THREE.Mesh(new THREE.SphereGeometry(3.5, 32, 32), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.1, transmission: 0.5 }));
            eyeGroup.add(globe);
            
            // Iris (Or pur lumineux)
            const iris = new THREE.Mesh(new THREE.CircleGeometry(1.8, 32), new THREE.MeshBasicMaterial({ color: 0xffd700 }));
            iris.position.z = 3.4;
            eyeGroup.add(iris);
            
            // Pupille (Noir profond)
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.7, 16), new THREE.MeshBasicMaterial({ color: 0x000000 }));
            pupil.position.z = 3.5;
            eyeGroup.add(pupil);
            
            eyeGroup.userData = { iris, pupil };
            return eyeGroup;
        }
        const eyeL = createEye(-7);
        const eyeR = createEye(7);
        faceGroup.add(eyeL);
        faceGroup.add(eyeR);

        // --- 5. LES CHEVEUX (Filaments Organiques) ---
        const hairGroup = new THREE.Group();
        for(let i=0; i<150; i++) {
            // Point de départ sur le crâne
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI * 0.4; // Seulement le haut de la tête
            
            const startX = Math.sin(phi) * Math.cos(theta) * 20;
            const startY = Math.cos(phi) * 20 + 5;
            const startZ = Math.sin(phi) * Math.sin(theta) * 20;

            // Courbe de Bézier pour un mouvement organique
            const curve = new THREE.CubicBezierCurve3(
                new THREE.Vector3(startX, startY, startZ),
                new THREE.Vector3(startX * 1.5, startY + 10, startZ * 1.5),
                new THREE.Vector3(startX * 2.5, startY + 5, startZ * 2.5),
                new THREE.Vector3(startX * 3, startY - 10, startZ * 3)
            );
            
            const geo = new THREE.TubeGeometry(curve, 20, 0.08, 4, false);
            const mat = new THREE.MeshBasicMaterial({ color: 0xb8860b, transparent: true, opacity: 0.4 });
            const line = new THREE.Mesh(geo, mat);
            line.userData = { offset: Math.random() * Math.PI * 2, speed: Math.random() * 0.5 + 0.5 };
            hairGroup.add(line);
        }
        faceGroup.add(hairGroup);

        // --- 6. L'INTÉRIEUR (Cerveau / Synapses) ---
        const pCount = 800;
        const pGeo = new THREE.BufferGeometry();
        const pPos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i+=3) {
            pPos[i] = (Math.random() - 0.5) * 25;
            pPos[i+1] = (Math.random() - 0.5) * 25;
            pPos[i+2] = (Math.random() - 0.5) * 25;
        }
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
        const pMat = new THREE.PointsMaterial({ color: 0xffd700, size: 0.5, transparent: true, opacity: 0.8 });
        const particles = new THREE.Points(pGeo, pMat);
        faceGroup.add(particles);

        // --- 7. LUMIÈRES (Pour la réfraction) ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
        scene.add(ambientLight);
        
        const light1 = new THREE.PointLight(0xffffff, 2, 200);
        light1.position.set(40, 40, 40);
        scene.add(light1);
        
        const light2 = new THREE.PointLight(0xb8860b, 2, 200);
        light2.position.set(-40, -20, 40);
        scene.add(light2);

        // --- 8. ANIMATION (La Matière Vit) ---
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
            
            mouseX += (targetMouseX - mouseX) * 0.05; mouseY += (targetMouseY - mouseY) * 0.05;
            faceGroup.rotation.y = mouseX * 0.4; faceGroup.rotation.x = -mouseY * 0.2;

            // Yeux
            eyeL.rotation.y = mouseX * 0.8; eyeL.rotation.x = -mouseY * 0.8;
            eyeR.rotation.y = mouseX * 0.8; eyeR.rotation.x = -mouseY * 0.8;

            // --- DÉFORMATION DE LA MATIÈRE (Respiration & Parole) ---
            const positions = skull.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const px = originalPos[i];
                const py = originalPos[i+1];
                const pz = originalPos[i+2];
                
                // Bruit organique
                const noise = Math.sin(px * 0.2 + time) * Math.cos(py * 0.2 + time) * Math.sin(pz * 0.2 + time);
                let displacement = noise * 0.3;

                // Animation de la bouche (si l'IA parle)
                if (isSpeaking) {
                    const distMouth = Math.sqrt((px / 8)**2 + ((py + 12) / 2)**2);
                    if (distMouth < 1.2 && pz > 10) {
                        // On ouvre la bouche en repoussant la matière vers l'avant
                        displacement += Math.abs(Math.sin(time * 30)) * 2;
                    }
                }

                positions[i] = px + px * displacement * 0.05;
                positions[i+1] = py + py * displacement * 0.05;
                positions[i+2] = pz + pz * displacement * 0.05;
            }
            skull.geometry.attributes.position.needsUpdate = true;
            skullWire.geometry.attributes.position.needsUpdate = true;

            if (isSpeaking) { speakTimer -= delta; if (speakTimer <= 0) isSpeaking = false; }

            // Cheveux (vent)
            hairGroup.children.forEach(hair => {
                hair.rotation.z = Math.sin(time * hair.userData.speed + hair.userData.offset) * 0.1;
                hair.rotation.x = Math.cos(time * hair.userData.speed * 0.8 + hair.userData.offset) * 0.1;
            });

            // Particules cerveau
            particles.rotation.y = time * 0.2;

            // Lumières orbitent
            light1.position.x = Math.sin(time * 0.5) * 50;
            light1.position.z = Math.cos(time * 0.5) * 50;
            light2.position.x = Math.sin(time * 0.3 + 2) * 50;
            light2.position.z = Math.cos(time * 0.3 + 2) * 50;

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
            const color = sender === 'ENTITY' ? '#b8860b' : '#333';
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
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. Touch the liquid glass."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. The matter responds."); }, 1000);
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

print("✅ VISUAL/index.html généré (V8). Matière liquide et visage sculpté.")
