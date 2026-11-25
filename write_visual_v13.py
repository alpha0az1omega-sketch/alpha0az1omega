html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // NEURAL SURGERY V13</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        body { margin: 0; overflow: hidden; background: #f8f8fc; font-family: 'JetBrains Mono', monospace; color: #000; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: crosshair; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        .panel { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 15px; pointer-events: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding-bottom: 10px; margin-bottom: 10px; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 2px; color: #000; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 10px; color: #333; line-height: 1.6; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 280px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .highlight { color: #000; font-weight: 700; text-align: right; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(184, 134, 11, 0.2); }
        
        #panel-beacon { width: 300px; position: absolute; top: 20px; left: 50%; transform: translateX(-50%); text-align: center; }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 24px; color: #000; margin: 5px 0; letter-spacing: 4px; font-weight: 700; }
        
        /* PANNEAU CHIRURGIE */
        #panel-surgery { width: 300px; border-color: #8a2be2; }
        .surgery-info { font-size: 11px; margin-bottom: 10px; padding: 10px; background: rgba(138, 43, 226, 0.05); border-left: 3px solid #8a2be2; }
        .surgery-log { max-height: 150px; overflow-y: auto; font-size: 9px; color: #555; margin-top: 10px; border-top: 1px solid #ddd; padding-top: 10px; }
        
        #terminal-panel { width: 45%; max-width: 500px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 10px; background: rgba(0,0,0,0.05); border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 4px; padding: 8px 12px; }
        .terminal-prompt { color: #8a2be2; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #000; }
        
        #panel-integrity { width: 280px; }
        .integrity-bar { height: 2px; background: rgba(0,0,0,0.1); border-radius: 1px; margin: 10px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #8a2be2; transition: width 0.5s; box-shadow: 0 0 10px rgba(138, 43, 226, 0.5);}
        .hash-text { font-size: 8px; color: #555; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #f8f8fc; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 15px 40px; border: 1px solid #8a2be2; background: none; color: #8a2be2; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #8a2be2; color: #fff; box-shadow: 0 0 30px rgba(138, 43, 226, 0.3);}

        /* TAGS */
        .timeline-tag { font-size: 8px; padding: 2px 5px; border-radius: 2px; margin-right: 5px; }
        .past { background: #e0e0e0; color: #666; }
        .present { background: #8a2be2; color: #fff; }
        .future { background: #00ffff; color: #000; }
        
        /* CUSTOM TOOLTIP */
        #tooltip { position: absolute; background: rgba(0,0,0,0.8); color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 10px; pointer-events: none; z-index: 1000; display: none; border: 1px solid #00ffff; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#8a2be2;">ALPHA OS V13</h2>
        <p style="font-size: 11px; margin-bottom: 40px; max-width: 450px; text-align: center; color: #666;">Neural Surgery Interface<br>Zoomez à l'intérieur du crâne. Cliquez sur les neurones pour interagir.</p>
        <button id="start-btn">Begin Surgery</button>
    </div>

    <div id="canvas-container"></div>
    <div id="tooltip">Neuron Node</div>
    
    <div id="ui-layer">
        <div class="top-row">
            <div class="panel" id="panel-data">
                <div class="panel-header">Organism State</div>
                <div class="panel-content">
                    <div class="data-row"><span>SUBJECT:</span> <span class="highlight gold">NEXUS-V13</span></div>
                    <div class="data-row"><span>STATUS:</span> <span class="highlight" style="color:#008000;">LIVE SURGERY</span></div>
                    <div class="data-row"><span>ENTROPY:</span> <span class="highlight">8192 bits</span></div>
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">CRYSTAL-GLASS</span></div>
                </div>
            </div>

            <div class="panel" id="panel-beacon">
                <div class="panel-header" style="justify-content: center; border: none;">CHRONOS BEACON</div>
                <div id="beacon-time">--:--:--</div>
            </div>

            <!-- PANNEAU CHIRURGIE -->
            <div class="panel" id="panel-surgery">
                <div class="panel-header">Neural Surgery</div>
                <div class="surgery-info" id="surgery-status">
                    En attente d'interaction...
                </div>
                <div style="font-size: 10px; margin-bottom: 5px;">Active Pathways:</div>
                <div class="surgery-log" id="surgery-log">
                    > System ready.
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
        scene.background = new THREE.Color(0xf8f8fc); 
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(0, 0, 80);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.shadowMap.enabled = true;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 5; // Zoom très proche pour entrer dans la tête
        controls.maxDistance = 250;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. SCULPTURE DU BUSTE (Tête Agrandie, Matériau Verre) ---
        const headGeo = new THREE.SphereGeometry(35, 128, 128); // Tête plus grosse
        const pos = headGeo.attributes.position;

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            if (y > 0) y *= 1.1; 
            if (z < 0) z *= 0.85; 

            if (y < -7) { y *= 1.2; x *= 0.9; }

            const distEyeL = Math.sqrt((x + 11)**2 + (y - 7)**2 + (z - 28)**2);
            const distEyeR = Math.sqrt((x - 11)**2 + (y - 7)**2 + (z - 28)**2);
            if (distEyeL < 9 || distEyeR < 9) { z -= 7; }

            if (y > -11 && y < 11 && x > -4 && x < 4) { z += Math.cos(y * 0.2) * 5; }

            if (y > -7 && y < 7 && (x > 8 || x < -8)) { z += 3; }

            const distMouth = Math.sqrt((x / 11)**2 + ((y + 17) / 3)**2);
            if (distMouth < 1 && z > 20) { z -= (1 - distMouth) * 6; }

            pos.setXYZ(i, x, y, z);
        }
        headGeo.computeVertexNormals();

        // Matériau Verre/Cristal Transparent
        const skinMat = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff, 
            transparent: true,
            opacity: 0.25,
            roughness: 0.1, 
            metalness: 0.1,
            transmission: 0.9, // Effet verre
            thickness: 2.0,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1
        });
        
        const head = new THREE.Mesh(headGeo, skinMat);
        head.castShadow = false; // Désactivé pour voir l'intérieur
        head.receiveShadow = false;
        faceGroup.add(head);

        // Cou
        const neckGeo = new THREE.CylinderGeometry(14, 16, 25, 32);
        const neckMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.2, transmission: 0.9 });
        const neck = new THREE.Mesh(neckGeo, neckMat);
        neck.position.y = -40;
        faceGroup.add(neck);

        // --- 3. LE CERVEAU ET LE RAISONNEMENT (INTERACTIF) ---
        const brainGroup = new THREE.Group();
        brainGroup.position.set(0, 5, -5); // Centré à l'intérieur du crâne
        faceGroup.add(brainGroup);

        // Cerveau central (Noyau)
        const coreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const core = new THREE.Mesh(new THREE.SphereGeometry(5, 32, 32), coreMat);
        brainGroup.add(core);

        // Nœuds de raisonnement (Neurones)
        const nodes = [];
        const nodeColors = [0x00ffff, 0xff00ff, 0x00ff00, 0x8a2be2, 0xff4500]; // Cyan, Magenta, Vert, Violet, Orange
        
        for(let i=0; i<40; i++) {
            const size = Math.random() * 1.5 + 0.5;
            const color = nodeColors[Math.floor(Math.random() * nodeColors.length)];
            const nodeMat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.9 });
            const node = new THREE.Mesh(new THREE.SphereGeometry(size, 16, 16), nodeMat);
            
            // Position aléatoire dans le cerveau
            const radius = 12 + Math.random() * 8;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            
            node.position.set(
                radius * Math.sin(phi) * Math.cos(theta),
                radius * Math.sin(phi) * Math.sin(theta),
                radius * Math.cos(phi)
            );
            
            node.userData = { 
                id: `PATH-${i}`, 
                type: ["Visual Cortex", "Language Model", "Memory Bank", "Logic Gate", "Token Flux"][i%5],
                color: color
            };
            
            nodes.push(node);
            brainGroup.add(node);
        }

        // Connexions (Synapses)
        const lineMat = new THREE.LineBasicMaterial({ color: 0x4444ff, transparent: true, opacity: 0.2 });
        for(let i=0; i<nodes.length; i++) {
            for(let j=i+1; j<nodes.length; j++) {
                if(nodes[i].position.distanceTo(nodes[j].position) < 18) {
                    const points = [nodes[i].position, nodes[j].position];
                    const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
                    const line = new THREE.Line(lineGeo, lineMat);
                    brainGroup.add(line);
                }
            }
        }

        // --- 4. YEUX ET BOUCHE (Corrigés) ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 7, 27);
            
            const globe = new THREE.Mesh(new THREE.SphereGeometry(4, 32, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.1 }));
            eyeGroup.add(globe);
            
            const iris = new THREE.Mesh(new THREE.CircleGeometry(2, 32), new THREE.MeshBasicMaterial({ color: 0x00ffff })); // Cyan vif
            iris.position.z = 3.9;
            eyeGroup.add(iris);
            
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.8, 16), new THREE.MeshBasicMaterial({ color: 0xff00ff })); // Magenta
            pupil.position.z = 4.0;
            eyeGroup.add(pupil);

            return eyeGroup;
        }
        faceGroup.add(createEye(-11));
        faceGroup.add(createEye(11));

        // BOUCHE (Fixée : plus de langue, une simple ouverture dynamique)
        const mouthGeo = new THREE.TorusGeometry(7, 0.8, 16, 32, Math.PI);
        const mouthMat = new THREE.MeshStandardMaterial({ color: 0xff4500, emissive: 0x441100 }); // Rouge Orangé vif
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        mouth.position.set(0, -17, 24);
        mouth.rotation.x = Math.PI; 
        faceGroup.add(mouth);

        // --- 5. LUMIÈRES ULTRA-VIVES ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6); // Plus lumineux
        scene.add(ambientLight);
        
        // Lumière principale
        const spotLight1 = new THREE.SpotLight(0xffffff, 2);
        spotLight1.position.set(40, 60, 50);
        spotLight1.castShadow = true;
        scene.add(spotLight1);

        // Lumière Cyan
        const spotLight2 = new THREE.SpotLight(0x00ffff, 3);
        spotLight2.position.set(-50, 0, 50);
        scene.add(spotLight2);

        // Lumière Magenta
        const spotLight3 = new THREE.SpotLight(0xff00ff, 3);
        spotLight3.position.set(0, -30, -50);
        scene.add(spotLight3);
        
        // Lumière Verte
        const pointLight1 = new THREE.PointLight(0x00ff00, 2, 150);
        pointLight1.position.set(0, 40, 30);
        scene.add(pointLight1);

        // --- 6. INTERACTION (CHIRURGIE) ---
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        const surgeryLog = document.getElementById('surgery-log');
        const surgeryStatus = document.getElementById('surgery-status');

        function onMouseMove(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(nodes);

            if (intersects.length > 0) {
                const node = intersects[0].object;
                tooltip.style.display = 'block';
                tooltip.style.left = event.clientX + 15 + 'px';
                tooltip.style.top = event.clientY + 15 + 'px';
                tooltip.innerHTML = `<b>${node.userData.type}</b><br>${node.userData.id}`;
                document.body.style.cursor = 'pointer';
            } else {
                tooltip.style.display = 'none';
                document.body.style.cursor = 'crosshair';
            }
        }

        function onClick(event) {
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(nodes);

            if (intersects.length > 0) {
                const node = intersects[0].object;
                
                // Change la couleur du noyau
                core.material.color.setHex(node.userData.color);
                
                // Logique de raisonnement
                const reasoningSteps = [
                    "Analyse des tokens d'entrée...",
                    "Recherche dans la mémoire sémantique...",
                    "Application des poids synaptiques...",
                    "Génération de la réponse...",
                    "Vérification épistémique..."
                ];
                const randomStep = reasoningSteps[Math.floor(Math.random() * reasoningSteps.length)];
                
                surgeryStatus.innerHTML = `Activation : <span style="color:${new THREE.Color(node.userData.color).getStyle()}">${node.userData.type}</span>`;
                surgeryLog.innerHTML += `<div>> [${node.userData.id}] ${randomStep}</div>`;
                surgeryLog.scrollTop = surgeryLog.scrollHeight;

                // Animation de l'IA
                isSpeaking = true;
                speakTimer = 2.0;
                
                addToTerminal('SYSTEM', `Surgical trigger on ${node.userData.id}: ${randomStep}`);
                entitySpeak(`Activating ${node.userData.type}. Reasoning process updated.`);
            }
        }

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('click', onClick);

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

            // Respiration du cerveau
            brainGroup.scale.setScalar(1 + Math.sin(time * 2) * 0.05);

            // Bouche (Parole - fixée, pas de langue)
            if (isSpeaking) {
                mouth.scale.y = 1 + Math.abs(Math.sin(time * 20)) * 2.0; // S'ouvre plus grand
                speakTimer -= delta;
                if (speakTimer <= 0) { isSpeaking = false; mouth.scale.y = 1; }
            }

            // Animation des nœuds (Pulsation)
            nodes.forEach((node, index) => {
                const scale = 1 + Math.sin(time * 5 + index) * 0.2;
                node.scale.setScalar(scale);
            });

            controls.update();
            renderer.render(scene, camera);
        }

        // --- 8. INTELLIGENCE & AUDIO ---
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
            const color = sender === 'ENTITY' ? '#8a2be2' : (sender === 'SYSTEM' ? '#00ffff' : '#333');
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
            setTimeout(() => { addToTerminal('ENTITY', "Surgical link established. I am open. Explore my neural pathways."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. Neural surgery interface is ready."); }, 1000);
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

print("✅ VISUAL/index.html généré (V13). Chirurgie IA et Cerveau interactif.")
