html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // THE GOLDEN ENTITY</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* FOND BLANC CASSÉ AVEC ACCENTS DORÉS */
        body { margin: 0; overflow: hidden; background: #fcfcfc; font-family: 'JetBrains Mono', monospace; color: #000; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        /* Panneaux Blancs avec bordures dorées */
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
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #666;">Synthesizing Golden Entity...</p>
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
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">GOLDEN-WIRE</span></div>
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
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 30;
        controls.maxDistance = 200;

        // --- 2. ASSEMBLAGE DU VISAGE (Formes Géométriques) ---
        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // Couleurs
        const skinColor = 0xffffff;
        const goldColor = 0xb8860b;
        const blackColor = 0x000000;

        // A. Le Crâne (Ovale)
        const skullGeo = new THREE.SphereGeometry(20, 64, 64);
        skullGeo.scale(1, 1.2, 0.9); // Étirer vers le haut
        const skullMat = new THREE.MeshPhongMaterial({ color: skinColor, shininess: 30, transparent: true, opacity: 0.3, wireframe: false });
        const skull = new THREE.Mesh(skullGeo, skullMat);
        faceGroup.add(skull);

        // Filaire du crâne
        const skullWire = new THREE.Mesh(skullGeo, new THREE.MeshBasicMaterial({ color: 0xcccccc, wireframe: true, transparent: true, opacity: 0.1 }));
        faceGroup.add(skullWire);

        // B. La Mâchoire (Cône pour le menton pointu)
        const jawGeo = new THREE.ConeGeometry(18, 25, 32);
        const jawMat = new THREE.MeshPhongMaterial({ color: skinColor, shininess: 30, transparent: true, opacity: 0.3 });
        const jaw = new THREE.Mesh(jawGeo, jawMat);
        jaw.position.set(0, -25, 0);
        jaw.rotation.x = Math.PI;
        faceGroup.add(jaw);
        
        const jawWire = new THREE.Mesh(jawGeo, new THREE.MeshBasicMaterial({ color: 0xcccccc, wireframe: true, transparent: true, opacity: 0.1 }));
        jawWire.position.set(0, -25, 0);
        jawWire.rotation.x = Math.PI;
        faceGroup.add(jawWire);

        // C. Le Nez (Prisme)
        const noseGeo = new THREE.ConeGeometry(3, 10, 4);
        const noseMat = new THREE.MeshPhongMaterial({ color: skinColor, shininess: 30, transparent: true, opacity: 0.5 });
        const nose = new THREE.Mesh(noseGeo, noseMat);
        nose.position.set(0, 0, 22);
        nose.rotation.x = Math.PI / 2;
        nose.rotation.y = Math.PI / 4;
        faceGroup.add(nose);

        // D. Les Yeux (Sphères + Anneaux)
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 5, 18);
            
            // Globe oculaire
            const globe = new THREE.Mesh(new THREE.SphereGeometry(4, 32, 32), new THREE.MeshPhongMaterial({ color: 0xffffff, shininess: 100 }));
            eyeGroup.add(globe);
            
            // Iris (Or)
            const iris = new THREE.Mesh(new THREE.CircleGeometry(2, 32), new THREE.MeshBasicMaterial({ color: goldColor }));
            iris.position.z = 3.9;
            eyeGroup.add(iris);
            
            // Pupille (Noir)
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.8, 16), new THREE.MeshBasicMaterial({ color: blackColor }));
            pupil.position.z = 4;
            eyeGroup.add(pupil);
            
            // Paupière (Demi-sphère)
            const eyelid = new THREE.Mesh(new THREE.SphereGeometry(4.1, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshPhongMaterial({ color: skinColor, shininess: 30, transparent: true, opacity: 0.8, side: THREE.DoubleSide }));
            eyelid.rotation.x = Math.PI / 2;
            eyelid.position.z = 0.5;
            eyeGroup.add(eyelid);

            eyeGroup.userData = { iris, pupil, eyelid };
            return eyeGroup;
        }
        const eyeL = createEye(-7);
        const eyeR = createEye(7);
        faceGroup.add(eyeL);
        faceGroup.add(eyeR);

        // E. La Bouche (Courbe de Bézier)
        const mouthPoints = 20;
        const mouthCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(-6, -15, 20),
            new THREE.Vector3(-3, -17, 21),
            new THREE.Vector3(0, -18, 21.5),
            new THREE.Vector3(3, -17, 21),
            new THREE.Vector3(6, -15, 20)
        ]);
        const mouthGeo = new THREE.TubeGeometry(mouthCurve, 64, 0.5, 8, false);
        const mouthMat = new THREE.MeshBasicMaterial({ color: blackColor });
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        faceGroup.add(mouth);

        // F. Les Oreilles (Demi-cercles)
        function createEar(x) {
            const earGroup = new THREE.Group();
            earGroup.position.set(x, 0, 0);
            
            const earGeo = new THREE.TorusGeometry(5, 1, 8, 32, Math.PI);
            const earMat = new THREE.MeshPhongMaterial({ color: skinColor, shininess: 30, transparent: true, opacity: 0.5 });
            const ear = new THREE.Mesh(earGeo, earMat);
            ear.rotation.y = Math.PI / 2;
            earGroup.add(ear);
            
            return earGroup;
        }
        faceGroup.add(createEar(-20));
        faceGroup.add(createEar(20));

        // G. Les Cheveux (Lignes Dorées)
        const hairGroup = new THREE.Group();
        for(let i=0; i<80; i++) {
            const startX = (Math.random() - 0.5) * 20;
            const startZ = (Math.random() - 0.5) * 20 - 10;
            const curve = new THREE.CatmullRomCurve3([
                new THREE.Vector3(startX, 20, startZ),
                new THREE.Vector3(startX * 1.2, 30, startZ * 1.2),
                new THREE.Vector3(startX * 1.5, 40, startZ * 1.5)
            ]);
            const geo = new THREE.TubeGeometry(curve, 8, 0.1, 4, false);
            const mat = new THREE.MeshBasicMaterial({ color: goldColor, transparent: true, opacity: 0.3 });
            const line = new THREE.Mesh(geo, mat);
            line.userData = { offset: Math.random() * Math.PI * 2 };
            hairGroup.add(line);
        }
        faceGroup.add(hairGroup);

        // --- 3. LUMIÈRES ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);
        
        const light1 = new THREE.PointLight(0xffffff, 1, 200);
        light1.position.set(30, 20, 50);
        scene.add(light1);
        
        const light2 = new THREE.PointLight(0xb8860b, 1, 200);
        light2.position.set(-30, -20, 50);
        scene.add(light2);

        // --- 4. ANIMATION & INTERACTION ---
        let isSpeaking = false; let speakTimer = 0;
        let blinkTimer = 0;
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
            
            // La tête suit la souris
            faceGroup.rotation.y = mouseX * 0.3; faceGroup.rotation.x = -mouseY * 0.2;

            // Les yeux suivent
            eyeL.rotation.y = mouseX * 0.8; eyeL.rotation.x = -mouseY * 0.8;
            eyeR.rotation.y = mouseX * 0.8; eyeR.rotation.x = -mouseY * 0.8;

            // Clignements
            blinkTimer += delta;
            if (blinkTimer > 3) {
                const blinkProgress = (blinkTimer - 3) * 5;
                if (blinkProgress < 1) {
                    eyeL.userData.eyelid.scale.y = 1 - Math.sin(blinkProgress * Math.PI);
                    eyeR.userData.eyelid.scale.y = 1 - Math.sin(blinkProgress * Math.PI);
                } else {
                    blinkTimer = 0;
                    eyeL.userData.eyelid.scale.y = 1;
                    eyeR.userData.eyelid.scale.y = 1;
                }
            }

            // Parole (Bouche)
            if (isSpeaking) {
                mouth.scale.y = 1 + Math.abs(Math.sin(time * 20)) * 0.5;
                speakTimer -= delta;
                if (speakTimer <= 0) { isSpeaking = false; mouth.scale.y = 1; }
            }

            // Cheveux
            hairGroup.children.forEach(hair => {
                hair.rotation.z = Math.sin(time * 1.5 + hair.userData.offset) * 0.05;
            });

            controls.update();
            renderer.render(scene, camera);
        }

        // --- 5. INTELLIGENCE & AUDIO ---
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
            setTimeout(() => { addToTerminal('ENTITY', "Neural link established. I am Nexus. My skin is gold, my eyes see you."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. The golden wire vibrates."); }, 1000);
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

print("✅ VISUAL/index.html généré (V7). Visage géométrique blanc et or.")
