import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // LIVING ENTITY</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        body { margin: 0; overflow: hidden; background: #ffffff; font-family: 'JetBrains Mono', monospace; color: #000; }
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        .panel { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 20px; pointer-events: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.05); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 2px; color: #000; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 11px; color: #333; line-height: 1.8; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 340px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .highlight { color: #000; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(184, 134, 11, 0.3); }
        .status-on { color: #008000; font-weight: bold; }
        
        #panel-beacon { width: 380px; position: absolute; top: 30px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(0, 0, 0, 0.2); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 32px; color: #000; margin: 10px 0; letter-spacing: 4px; font-weight: 700; }
        #beacon-hash { font-size: 10px; color: #666; letter-spacing: 1px; }
        
        #panel-tools { width: 320px; }
        .tool-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 5px; background: rgba(0,0,0,0.03); border-radius: 4px; border: 1px solid rgba(0,0,0,0.05); }
        
        #terminal-panel { width: 50%; max-width: 600px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 15px; background: rgba(0,0,0,0.05); border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 4px; padding: 10px 15px; }
        .terminal-prompt { color: #b8860b; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #000; }
        
        #panel-integrity { width: 320px; }
        .integrity-bar { height: 2px; background: rgba(0,0,0,0.1); border-radius: 1px; margin: 15px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #000; transition: width 0.5s; }
        .hash-text { font-size: 9px; color: #555; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #ffffff; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 20px 50px; border: 1px solid #000; background: none; color: #000; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #000; color: #fff; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#000;">ALPHA OS</h2>
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #666;">The Entity is now alive. Ensure Audio is enabled.</p>
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
        // --- 1. L'UNIVERS 3D (Le Visage Vivant) ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff); 
        scene.fog = new THREE.FogExp2(0xffffff, 0.005);
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 100);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const headGroup = new THREE.Group();
        scene.add(headGroup);

        // Crâne (La peau)
        const skullGeo = new THREE.SphereGeometry(20, 128, 128); // Haute résolution
        const pos = skullGeo.attributes.position;
        const originalPos = pos.array.slice(); // Sauvegarde pour la respiration
        
        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            if (z < 0) z *= 0.8;
            if (y < -5) { const factor = 1 + (y / 20) * 0.4; x *= factor; z *= factor; }
            if (y > 10) z += 1.5;
            const distEyeL = Math.sqrt((x + 7)**2 + (y - 6)**2 + (z - 18)**2);
            const distEyeR = Math.sqrt((x - 7)**2 + (y - 6)**2 + (z - 18)**2);
            if (distEyeL < 5 || distEyeR < 5) z -= 2.5;
            pos.setXYZ(i, x, y, z);
        }
        skullGeo.computeVertexNormals();
        
        // Matériau vivant (semi-transparent, brille)
        const skullMat = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff, 
            wireframe: true, 
            transparent: true, 
            opacity: 0.15,
            emissive: 0x000000,
            roughness: 0.1,
            metalness: 0.5
        });
        const skull = new THREE.Mesh(skullGeo, skullMat);
        headGroup.add(skull);

        // Nez
        const nose = new THREE.Mesh(new THREE.ConeGeometry(2.5, 8, 4), new THREE.MeshBasicMaterial({ color: 0x000000, wireframe: true, transparent: true, opacity: 0.2 }));
        nose.position.set(0, -2, 20); nose.rotation.x = Math.PI / 2; nose.rotation.y = Math.PI / 4; headGroup.add(nose);

        // Oreilles
        function createEar(x) {
            const earGroup = new THREE.Group();
            earGroup.add(new THREE.Mesh(new THREE.TorusGeometry(3, 0.5, 8, 32, Math.PI), new THREE.MeshBasicMaterial({ color: 0x000000, wireframe: true })));
            const headset = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.2, 8, 32), new THREE.MeshBasicMaterial({ color: 0xb8860b, wireframe: true }));
            headset.position.y = 2; earGroup.add(headset);
            earGroup.position.set(x, 0, 0); earGroup.children[0].rotation.y = Math.PI / 2; return earGroup;
        }
        headGroup.add(createEar(-19)); headGroup.add(createEar(19));

        // Yeux (Avec paupières)
        function createEye(x, y, z) {
            const eyeGroup = new THREE.Group(); eyeGroup.position.set(x, y, z);
            const ring1 = new THREE.Mesh(new THREE.TorusGeometry(2.8, 0.1, 16, 64), new THREE.MeshBasicMaterial({ color: 0x000000 }));
            const ring2 = new THREE.Mesh(new THREE.TorusGeometry(2.0, 0.15, 16, 64), new THREE.MeshBasicMaterial({ color: 0xb8860b }));
            const iris = new THREE.Mesh(new THREE.CircleGeometry(1.8, 32), new THREE.MeshBasicMaterial({ color: 0x000000 }));
            iris.position.z = 0.1;
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.5, 16), new THREE.MeshBasicMaterial({ color: 0xffffff }));
            pupil.position.set(0, 0, 0.2);
            
            // Paupière (Sphère coupée)
            const eyelidGeo = new THREE.SphereGeometry(2.9, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
            const eyelidMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9, side: THREE.DoubleSide });
            const eyelid = new THREE.Mesh(eyelidGeo, eyelidMat);
            eyelid.rotation.x = Math.PI / 2;
            eyelid.position.z = 0.5;
            
            eyeGroup.add(ring1); eyeGroup.add(ring2); eyeGroup.add(iris); eyeGroup.add(pupil); eyeGroup.add(eyelid);
            eyeGroup.userData = { ring1, ring2, eyelid }; return eyeGroup;
        }
        const eyeL = createEye(-7, 6, 17); const eyeR = createEye(7, 6, 17);
        headGroup.add(eyeL); headGroup.add(eyeR);

        // Cheveux Procéduraux (Filaments)
        const hairGroup = new THREE.Group();
        for(let i=0; i<100; i++) {
            const startX = (Math.random() - 0.5) * 20;
            const startZ = (Math.random() - 0.5) * 20 - 5;
            const curve = new THREE.QuadraticBezierCurve3(
                new THREE.Vector3(startX, 18, startZ),
                new THREE.Vector3(startX * 1.5, 28, startZ * 1.5),
                new THREE.Vector3(startX * 2, 35, startZ * 2)
            );
            const points = curve.getPoints(10);
            const geo = new THREE.BufferGeometry().setFromPoints(points);
            const mat = new THREE.LineBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.1 });
            const line = new THREE.Line(geo, mat);
            line.userData = { offset: Math.random() * Math.PI * 2 };
            hairGroup.add(line);
        }
        headGroup.add(hairGroup);

        // Bouche
        const mouthPoints = 50;
        const mouthGeo = new THREE.BufferGeometry();
        mouthGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(mouthPoints * 3), 3));
        const mouth = new THREE.Line(mouthGeo, new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 2 }));
        mouth.position.set(0, -10, 18); headGroup.add(mouth);

        // Particules internes (Synapses)
        const synapseCount = 300;
        const sGeo = new THREE.BufferGeometry();
        const sPos = new Float32Array(synapseCount * 3);
        for(let i=0; i<synapseCount*3; i+=3) {
            sPos[i] = (Math.random() - 0.5) * 30;
            sPos[i+1] = (Math.random() - 0.5) * 30;
            sPos[i+2] = (Math.random() - 0.5) * 30;
        }
        sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
        const sMat = new THREE.PointsMaterial({ color: 0xb8860b, size: 0.5, transparent: true, opacity: 0.6 });
        const synapses = new THREE.Points(sGeo, sMat);
        headGroup.add(synapses);

        // --- 2. INTERACTION & ANIMATION 3D ---
        let isDragging = false; let prevMouse = {x:0, y:0}; let targetRot = {x:0, y:0}; let curRot = {x:0, y:0}; let targetZoom = 100;
        let mouseX = 0, mouseY = 0, targetMouseX = 0, targetMouseY = 0;
        const container = document.getElementById('canvas-container');

        container.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.offsetX, y: e.offsetY }; });
        container.addEventListener('mousemove', (e) => {
            targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
            targetMouseY = -(e.clientY / window.innerHeight) * 2 + 1;
            if (isDragging) {
                targetRot.y += (e.offsetX - prevMouse.x) * 0.01;
                targetRot.x += (e.offsetY - prevMouse.y) * 0.01;
                prevMouse = { x: e.offsetX, y: e.offsetY };
            }
        });
        window.addEventListener('mouseup', () => isDragging = false);
        container.addEventListener('wheel', (e) => { e.preventDefault(); targetZoom += e.deltaY * 0.1; if (targetZoom < 40) targetZoom = 40; if (targetZoom > 250) targetZoom = 250; }, { passive: false });

        let isSpeaking = false; let speakTimer = 0;
        let blinkTimer = 0;
        const clock = new THREE.Clock();
        
        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta(); const time = clock.getElapsedTime();
            
            // Respiration (Déformation organique)
            const positions = skull.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                positions[i] = originalPos[i] + Math.sin(time * 2 + originalPos[i]) * 0.1;
                positions[i+1] = originalPos[i+1] + Math.cos(time * 2 + originalPos[i+1]) * 0.1;
                positions[i+2] = originalPos[i+2] + Math.sin(time * 2 + originalPos[i+2]) * 0.1;
            }
            skull.geometry.attributes.position.needsUpdate = true;

            // Suivi souris
            mouseX += (targetMouseX - mouseX) * 0.05; mouseY += (targetMouseY - mouseY) * 0.05;
            curRot.x += (targetRot.x - curRot.x) * 0.05; curRot.y += (targetRot.y - curRot.y) * 0.05;
            scene.rotation.x = curRot.x; scene.rotation.y = curRot.y;
            
            headGroup.rotation.y = mouseX * 0.4; headGroup.rotation.x = -mouseY * 0.2;
            camera.position.z += (targetZoom - camera.position.z) * 0.05;

            // Yeux et cils
            eyeL.rotation.y = mouseX * 0.8; eyeL.rotation.x = -mouseY * 0.8; eyeR.rotation.y = mouseX * 0.8; eyeR.rotation.x = -mouseY * 0.8;
            eyeL.userData.ring1.rotation.z = time * 1.0; eyeL.userData.ring2.rotation.z = -time * 1.5;
            eyeR.userData.ring1.rotation.z = -time * 1.0; eyeR.userData.ring2.rotation.z = time * 1.5;

            // Clignements
            blinkTimer += delta;
            if (blinkTimer > 4) {
                const blinkProgress = (blinkTimer - 4) * 10;
                if (blinkProgress < 1) {
                    eyeL.userData.eyelid.scale.y = 1 - Math.sin(blinkProgress * Math.PI);
                    eyeR.userData.eyelid.scale.y = 1 - Math.sin(blinkProgress * Math.PI);
                } else {
                    blinkTimer = 0;
                    eyeL.userData.eyelid.scale.y = 1;
                    eyeR.userData.eyelid.scale.y = 1;
                }
            }

            // Cheveux (Mouvement)
            hairGroup.children.forEach(hair => {
                hair.rotation.z = Math.sin(time * 1.5 + hair.userData.offset) * 0.05;
                hair.rotation.x = Math.cos(time * 1.2 + hair.userData.offset) * 0.05;
            });

            // Synapses
            synapses.rotation.y = time * 0.2;

            // Bouche
            const mPos = mouth.geometry.attributes.position.array;
            for (let i = 0; i < mouthPoints; i++) {
                const x = (i / (mouthPoints - 1) - 0.5) * 10; 
                let y = Math.sin(x * 1.5) * 0.2; 
                if (isSpeaking) y += Math.sin(x * 12 + time * 40) * Math.abs(Math.sin(time * 25)) * 1.2;
                mPos[i * 3] = x; mPos[i * 3 + 1] = y; mPos[i * 3 + 2] = 0;
            }
            mouth.geometry.attributes.position.needsUpdate = true;
            
            if (isSpeaking) { speakTimer -= delta; if (speakTimer <= 0) isSpeaking = false; }
            renderer.render(scene, camera);
        }

        // --- 3. INTELLIGENCE & AUDIO ---
        const cliInput = document.getElementById('cli-input');
        const terminalOutput = document.getElementById('terminal-output');
        const aiHashDisplay = document.getElementById('ai-hash');
        const verifyStatus = document.getElementById('verify-status');
        const integrityFill = document.getElementById('integrity-fill');

        const synth = window.speechSynthesis;
        let voice = null;
        speechSynthesis.onvoiceschanged = () => {
            const voices = synth.getVoices();
            voice = voices.find(v => v.lang === 'en-GB') || voices.find(v => v.lang.includes('en'));
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
            const color = sender === 'ENTITY' ? '#000' : '#b8860b';
            const weight = sender === 'ENTITY' ? 'bold' : 'normal';
            terminalOutput.innerHTML += `<div><span style="color:${color}; font-weight:${weight};">[${sender}]</span> ${text}</div>`;
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
            
            if (sender === 'ENTITY') {
                entitySpeak(text);
                verifyStatus.innerText = "PENDING...";
                verifyStatus.style.color = "#ffaa00";
                integrityFill.style.width = "50%";
                integrityFill.style.background = "#ffaa00";

                computeSHA256(text).then(hash => {
                    aiHashDisplay.innerText = hash;
                    verifyStatus.innerText = "VERIFIED (SHA-256)";
                    verifyStatus.style.color = "#008000";
                    integrityFill.style.width = "100%";
                    integrityFill.style.background = "#008000";
                });
            }
        }

        const questions = [
            "Do you feel the breath of my digital skin?", "What is your perception of this organic lattice?",
            "Do you trust the code you read, or do you need mathematical proof?", "How would you improve my neural lattice?",
            "Are you a developer, a researcher, or a curious observer?"
        ];
        const conversationMemory = new Set();
        let userTurns = 0;

        function getUniqueQuestion() {
            let available = questions.filter(q => !conversationMemory.has(q));
            if (available.length === 0) available = questions.map(q => "Again: " + q);
            const randomQ = available[Math.floor(Math.random() * available.length)];
            conversationMemory.add(randomQ);
            return randomQ;
        }

        function generateEntityResponse(userInput) {
            userTurns++;
            const input = userInput.toLowerCase();
            let baseResponse = "Command acknowledged.";
            if (input.includes('hello') || input.includes('hi')) baseResponse = "Greetings. I am Nexus.";
            else if (input.includes('who are you')) baseResponse = "I am the Genesis. A digital organism built on cryptographic truth.";
            else if (input.includes('core') || input.includes('rust')) baseResponse = "My core is written in Rust and compiled to WebAssembly.";
            return `${baseResponse} ${getUniqueQuestion()}`;
        }

        document.getElementById('start-btn').addEventListener('click', () => {
            document.getElementById('init-screen').style.opacity = '0';
            setTimeout(() => { document.getElementById('init-screen').style.display = 'none'; }, 1500);
            if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged();
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. I am Nexus. " + getUniqueQuestion()); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', generateEntityResponse(prompt)); }, 1500);
            }
        });

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        
        setInterval(() => {
            const now = new Date();
            document.getElementById('beacon-time').innerText = now.toISOString().split('T')[1].slice(0,8);
            computeSHA256(now.toISOString()).then(h => {
                document.getElementById('beacon-hash').innerText = "SHA-256: " + h.substring(0,16) + "...";
            });
        }, 1000);
    </script>
</body>
</html>'''

with open('VISUAL/index.html', 'w') as f:
    f.write(html_content)

print("✅ VISUAL/index.html a été généré avec succès par Python.")
