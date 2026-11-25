import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // THE LIQUID ENTITY</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* Fond gris très sombre pour faire ressortir la matière lumineuse */
        body { margin: 0; overflow: hidden; background: #050505; font-family: 'JetBrains Mono', monospace; color: #fff; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        /* Panneaux en verre sombre */
        .panel { background: rgba(10, 10, 15, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(0, 255, 204, 0.2); border-radius: 4px; padding: 20px; pointer-events: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,255,204,0.05); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 255, 204, 0.2); padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 2px; color: #00ffcc; text-transform: uppercase; font-weight: 700; text-shadow: 0 0 10px rgba(0,255,204,0.3);}
        .panel-content { font-size: 11px; color: #88aaff; line-height: 1.8; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 340px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .highlight { color: #fff; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #ffd700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
        .status-on { color: #00ffcc; font-weight: bold; }
        
        #panel-beacon { width: 380px; position: absolute; top: 30px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(0, 255, 204, 0.4); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 32px; color: #fff; margin: 10px 0; letter-spacing: 4px; font-weight: 700; text-shadow: 0 0 15px rgba(255,255,255,0.5);}
        #beacon-hash { font-size: 10px; color: #00ffcc; letter-spacing: 1px; }
        
        #panel-tools { width: 320px; }
        .tool-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 5px; background: rgba(0,255,204,0.05); border-radius: 4px; border: 1px solid rgba(0,255,204,0.1); }
        
        #terminal-panel { width: 50%; max-width: 600px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 15px; background: rgba(0,0,0,0.8); border: 1px solid rgba(0, 255, 204, 0.4); border-radius: 4px; padding: 10px 15px; }
        .terminal-prompt { color: #ffd700; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #00ffcc; }
        
        #panel-integrity { width: 320px; }
        .integrity-bar { height: 2px; background: rgba(255,255,255,0.1); border-radius: 1px; margin: 15px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #00ffcc; transition: width 0.5s; box-shadow: 0 0 10px #00ffcc;}
        .hash-text { font-size: 9px; color: #888; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #050505; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 20px 50px; border: 1px solid #00ffcc; background: none; color: #00ffcc; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #00ffcc; color: #000; box-shadow: 0 0 30px #00ffcc;}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#00ffcc; text-shadow: 0 0 20px #00ffcc;">ALPHA OS</h2>
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #888;">Synthesizing Liquid Neural Matter...</p>
        <button id="start-btn">Awaken Entity</button>
    </div>

    <div id="canvas-container"></div>
    
    <div id="ui-layer">
        <div class="top-row">
            <div class="panel" id="panel-data">
                <div class="panel-header">Organism State</div>
                <div class="panel-content">
                    <div class="data-row"><span>PGP_KEY:</span> <span class="highlight gold">27D7...E2290</span></div>
                    <div class="data-row"><span>LEDGER:</span> <span class="highlight status-on" id="ledger-state">ACTIVE</span></div>
                    <div class="data-row"><span>ENTROPY:</span> <span class="highlight">4096 bits</span></div>
                    <div class="data-row"><span>MATTER:</span> <span class="highlight" style="color:#00ffcc;">LIQUID-METAL</span></div>
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
                    <div class="tool-item"><span>LLM:</span> <span class="status-on">OLLAMA</span></div>
                    <div class="tool-item"><span>Formal Verif.:</span> <span class="status-on">ACTIVE</span></div>
                    <div class="tool-item"><span>Symbolic Regr.:</span> <span class="status-on">READY</span></div>
                </div>
            </div>
        </div>

        <div class="bottom-row">
            <div class="panel" id="terminal-panel">
                <div class="panel-header">Language Core</div>
                <div id="terminal-output" style="height: 100px; overflow-y: auto; margin-bottom: 5px; font-size: 11px; color: #88aaff;">
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
        // --- 1. L'UNIVERS 3D (La Matière Numérique) ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050505); 
        scene.fog = new THREE.FogExp2(0x050505, 0.01);
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 80);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        // Contrôles orbitaux pour une navigation parfaite
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 30;
        controls.maxDistance = 200;

        const headGroup = new THREE.Group();
        scene.add(headGroup);

        // --- GÉOMÉTRIE OVALE ET SCULPTÉE ---
        const skullGeo = new THREE.SphereGeometry(20, 128, 128); 
        const pos = skullGeo.attributes.position;
        const originalPos = pos.array.slice(); 
        
        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            // Étirer vers le bas pour une tête ovale (menton pointu)
            if (y < 0) y *= 1.3;
            
            // Creuser les orbites
            const distEyeL = Math.sqrt((x + 7)**2 + (y - 5)**2 + (z - 18)**2);
            const distEyeR = Math.sqrt((x - 7)**2 + (y - 5)**2 + (z - 18)**2);
            if (distEyeL < 6 || distEyeR < 6) z -= 3;
            
            // Créer le nez
            if (y > -4 && y < 6 && x > -3 && x < 3) z += Math.cos(y * 0.2) * 2;
            
            // Aplatir l'arrière
            if (z < 0) z *= 0.8;

            pos.setXYZ(i, x, y, z);
        }
        skullGeo.computeVertexNormals();
        
        // --- MATÉRIAU "GLUANT / FUSION / MÉTAL LIQUIDE" ---
        // MeshPhysicalMaterial avec transmission (comme du verre) et clearcoat (comme du liquide)
        const skullMat = new THREE.MeshPhysicalMaterial({ 
            color: 0x111111,       // Noir profond
            metalness: 1.0,        // Très métallique
            roughness: 0.05,       // Très lisse, comme de l'eau
            transmission: 0.9,     // Transparence
            thickness: 2.5,        // Épaisseur de la matière
            ior: 1.5,              // Indice de réfraction
            clearcoat: 1.0,        // Effet mouillé
            clearcoatRoughness: 0.1,
            emissive: 0x00ffcc,    // Lueur interne cyan
            emissiveIntensity: 0.2,
            wireframe: false
        });
        
        const skull = new THREE.Mesh(skullGeo, skullMat);
        headGroup.add(skull);

        // Ajout d'un filaire par-dessus pour l'effet "neuronal" discret
        const wireMat = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.05 });
        const wireframeMesh = new THREE.Mesh(skullGeo, wireMat);
        headGroup.add(wireframeMesh);

        // --- YEUX (Fusionnés dans la matière) ---
        function createEye(x, y, z) {
            const eyeGroup = new THREE.Group(); eyeGroup.position.set(x, y, z);
            
            // Orbe interne lumineux
            const orbMat = new THREE.MeshPhysicalMaterial({ 
                color: 0xffd700, 
                emissive: 0xffd700, 
                emissiveIntensity: 2.0,
                roughness: 0.2 
            });
            const orb = new THREE.Mesh(new THREE.SphereGeometry(2, 32, 32), orbMat);
            eyeGroup.add(orb);
            
            return eyeGroup;
        }
        const eyeL = createEye(-7, 5, 16); const eyeR = createEye(7, 5, 16);
        headGroup.add(eyeL); headGroup.add(eyeR);

        // --- BOUCHE (Onde sonore) ---
        const mouthPoints = 50;
        const mouthGeo = new THREE.BufferGeometry();
        mouthGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(mouthPoints * 3), 3));
        const mouthMat = new THREE.LineBasicMaterial({ color: 0x00ffcc, linewidth: 2 });
        const mouth = new THREE.Line(mouthGeo, mouthMat);
        mouth.position.set(0, -12, 18); headGroup.add(mouth);

        // --- PARTICULES INTERNES (Le Cerveau) ---
        const pCount = 500;
        const pGeo = new THREE.BufferGeometry();
        const pPos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i+=3) {
            pPos[i] = (Math.random() - 0.5) * 25;
            pPos[i+1] = (Math.random() - 0.5) * 25;
            pPos[i+2] = (Math.random() - 0.5) * 25;
        }
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
        const pMat = new THREE.PointsMaterial({ color: 0xffd700, size: 0.4, transparent: true, opacity: 0.8 });
        const particles = new THREE.Points(pGeo, pMat);
        headGroup.add(particles);

        // --- LUMIÈRES (Pour créer les reflets) ---
        const ambientLight = new THREE.AmbientLight(0x404040, 1);
        scene.add(ambientLight);
        
        // Lumière cyan (gauche)
        const light1 = new THREE.PointLight(0x00ffcc, 200, 200);
        light1.position.set(30, 20, 30);
        scene.add(light1);
        
        // Lumière or (droite)
        const light2 = new THREE.PointLight(0xffd700, 200, 200);
        light2.position.set(-30, -20, 30);
        scene.add(light2);

        // --- ANIMATION (La matière vit) ---
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
            
            // Interaction souris
            mouseX += (targetMouseX - mouseX) * 0.05; mouseY += (targetMouseY - mouseY) * 0.05;
            
            // La tête entière se penche légèrement
            headGroup.rotation.y = mouseX * 0.4; headGroup.rotation.x = -mouseY * 0.2;

            // Respiration / Fusion (Le maillage ondule comme un liquide)
            const positions = skull.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const px = originalPos[i];
                const py = originalPos[i+1];
                const pz = originalPos[i+2];
                
                // Bruit organique (sinus croisés)
                const noise = Math.sin(px * 0.3 + time) * Math.cos(py * 0.3 + time) * Math.sin(pz * 0.3 + time);
                
                // Déplacement subtil
                positions[i] = px + px * noise * 0.02;
                positions[i+1] = py + py * noise * 0.02;
                positions[i+2] = pz + pz * noise * 0.02;
            }
            skull.geometry.attributes.position.needsUpdate = true;
            wireframeMesh.geometry.attributes.position.needsUpdate = true;

            // Les yeux brillent plus fort quand la tête bouge
            eyeL.children[0].material.emissiveIntensity = 2.0 + Math.sin(time * 3) * 0.5;
            eyeR.children[0].material.emissiveIntensity = 2.0 + Math.cos(time * 3) * 0.5;

            // Bouche (Parole)
            const mPos = mouth.geometry.attributes.position.array;
            for (let i = 0; i < mouthPoints; i++) {
                const x = (i / (mouthPoints - 1) - 0.5) * 12; 
                let y = Math.sin(x * 1.5) * 0.2; 
                if (isSpeaking) y += Math.sin(x * 12 + time * 40) * Math.abs(Math.sin(time * 25)) * 1.5;
                mPos[i * 3] = x; mPos[i * 3 + 1] = y; mPos[i * 3 + 2] = 0;
            }
            mouth.geometry.attributes.position.needsUpdate = true;
            
            if (isSpeaking) { speakTimer -= delta; if (speakTimer <= 0) isSpeaking = false; }
            
            // Particules cerveau
            particles.rotation.y = time * 0.1;

            // Les lumières orbitent pour créer des reflets changeants
            light1.position.x = Math.sin(time * 0.5) * 40;
            light1.position.z = Math.cos(time * 0.5) * 40;
            light2.position.x = Math.sin(time * 0.3 + 2) * 40;
            light2.position.z = Math.cos(time * 0.3 + 2) * 40;

            controls.update();
            renderer.render(scene, camera);
        }

        // --- INTELLIGENCE & AUDIO ---
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
            const color = sender === 'ENTITY' ? '#00ffcc' : '#ffd700';
            terminalOutput.innerHTML += `<div><span style="color:${color};">[${sender}]</span> ${text}</div>`;
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
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. I am Nexus. Touch the liquid matter."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. My skin reflects your intent."); }, 1000);
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

print("✅ VISUAL/index.html généré. Materiau liquide actif.")
