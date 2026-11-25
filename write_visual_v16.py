html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // GOLDEN UNIVERSE V16</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* FOND BLANC/OR NUMÉRIQUE (Couleur de l'Univers) */
        body { margin: 0; overflow: hidden; background: radial-gradient(circle at center, #ffffff 0%, #fff8e7 40%, #f2e3c6 100%); font-family: 'JetBrains Mono', monospace; color: #333; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: crosshair; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 20px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        /* PANNEAUX LUMINEUX POUR FOND CLAIR */
        .panel { background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(15px); border: 1px solid rgba(184, 134, 11, 0.3); border-radius: 6px; padding: 15px; pointer-events: auto; box-shadow: 0 10px 30px rgba(184, 134, 11, 0.1); color: #333; }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(184, 134, 11, 0.3); padding-bottom: 10px; margin-bottom: 10px; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 2px; color: #b8860b; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 10px; line-height: 1.6; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 280px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .highlight { color: #000; font-weight: 700; text-align: right; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(184, 134, 11, 0.4); }
        
        #panel-beacon { width: 300px; position: absolute; top: 20px; left: 50%; transform: translateX(-50%); text-align: center; }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 24px; color: #b8860b; margin: 5px 0; letter-spacing: 4px; font-weight: 700; text-shadow: 0 0 10px rgba(184, 134, 11, 0.3); }
        
        /* PANNEAU ÉQUIPEMENT */
        #panel-equipment { width: 300px; border-color: #b8860b; }
        .tool-btn { display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 5px; padding: 8px; background: rgba(184, 134, 11, 0.05); border: 1px solid rgba(184, 134, 11, 0.3); border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; cursor: pointer; color: #333; transition: all 0.3s; }
        .tool-btn.active { background: rgba(184, 134, 11, 0.2); border-color: #b8860b; box-shadow: 0 0 10px rgba(184, 134, 11, 0.4); color: #000; }
        .tool-status { color: #b8860b; font-weight: bold; }

        #panel-surgery { width: 300px; border-color: #b8860b; }
        .surgery-info { font-size: 11px; margin-bottom: 10px; padding: 10px; background: rgba(184, 134, 11, 0.05); border-left: 3px solid #b8860b; }
        .surgery-log { max-height: 120px; overflow-y: auto; font-size: 9px; color: #555; margin-top: 10px; border-top: 1px solid rgba(184, 134, 11, 0.3); padding-top: 10px; }
        
        #terminal-panel { width: 45%; max-width: 500px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 10px; background: rgba(255,255,255,0.8); border: 1px solid rgba(184, 134, 11, 0.4); border-radius: 4px; padding: 8px 12px; }
        .terminal-prompt { color: #b8860b; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #000; }
        
        #panel-integrity { width: 280px; }
        .integrity-bar { height: 2px; background: rgba(184, 134, 11, 0.2); border-radius: 1px; margin: 10px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #b8860b; transition: width 0.5s; box-shadow: 0 0 10px rgba(184, 134, 11, 0.5);}
        .hash-text { font-size: 8px; color: #777; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #fff8e7; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 15px 40px; border: 1px solid #b8860b; background: none; color: #b8860b; font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #b8860b; color: #fff; box-shadow: 0 0 30px rgba(184, 134, 11, 0.4);}

        #tooltip { position: absolute; background: rgba(184,134,11,0.95); color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 10px; pointer-events: none; z-index: 1000; display: none; font-weight: bold; box-shadow: 0 0 10px rgba(184,134,11,0.5); }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#b8860b;">ALPHA OS V16</h2>
        <p style="font-size: 11px; margin-bottom: 40px; max-width: 450px; text-align: center; color: #666;">The Golden Universe<br>Sculpture Parfaite. Zoomez à l'intérieur.</p>
        <button id="start-btn">Initiate Link</button>
    </div>

    <div id="canvas-container"></div>
    <div id="tooltip">Neuron Node</div>
    
    <div id="ui-layer">
        <div class="top-row">
            <div class="panel" id="panel-data">
                <div class="panel-header">Organism State</div>
                <div class="panel-content">
                    <div class="data-row"><span>SUBJECT:</span> <span class="highlight gold">NEXUS-V16</span></div>
                    <div class="data-row"><span>STATUS:</span> <span class="highlight" style="color:#008000;">LIVE</span></div>
                    <div class="data-row"><span>ENTROPY:</span> <span class="highlight">8192 bits</span></div>
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">GOLDEN-CRYSTAL</span></div>
                </div>
            </div>

            <div class="panel" id="panel-beacon">
                <div class="panel-header" style="justify-content: center; border: none;">CHRONOS</div>
                <div id="beacon-time">--:--:--</div>
            </div>

            <div class="panel" id="panel-equipment">
                <div class="panel-header">Visual Tools</div>
                <button class="tool-btn" id="btn-glasses">Optical Lenses <span class="tool-status" id="status-glasses">OFF</span></button>
                <button class="tool-btn" id="btn-headset">Neural Headset <span class="tool-status" id="status-headset">OFF</span></button>
                <button class="tool-btn" id="btn-mic">Input Mic <span class="tool-status" id="status-mic">OFF</span></button>
            </div>

            <div class="panel" id="panel-surgery">
                <div class="panel-header">Neural Surgery</div>
                <div class="surgery-info" id="surgery-status">
                    En attente...
                </div>
                <div class="surgery-log" id="surgery-log">
                    > Ready.
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
                <div style="font-size: 9px; color: #777;">Verify: <span id="verify-status">IDLE</span></div>
            </div>
        </div>
    </div>

    <script>
        // --- 1. L'UNIVERS 3D (Fond Blanc/Or) ---
        const scene = new THREE.Scene();
        // On laisse le fond du canvas transparent pour voir le dégradé CSS
        
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
        controls.minDistance = 2; 
        controls.maxDistance = 200;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. SCULPTURE PARFAITE DU VISAGE (Mathématiques douces) ---
        const headGeo = new THREE.SphereGeometry(25, 128, 128); 
        const pos = headGeo.attributes.position;

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            // 1. Crâne et Mâchoire
            if (y > 0) y *= 1.1; 
            if (z < 0) z *= 0.85; 
            if (y < -5) { y *= 1.2; x *= 0.9; }

            // 2. Orbites (Creusées avec courbe douce)
            const distEyeL = Math.sqrt((x + 8)**2 + (y - 5)**2);
            const distEyeR = Math.sqrt((x - 8)**2 + (y - 5)**2);
            if (distEyeL < 8) z -= Math.cos((distEyeL / 8) * (Math.PI / 2)) * 6;
            if (distEyeR < 8) z -= Math.cos((distEyeR / 8) * (Math.PI / 2)) * 6;

            // 3. NEZ PARFAIT (Courbe de Gauss pour un relief organique)
            if (y > -12 && y < 10 && Math.abs(x) < 4) {
                // Plus on est proche du centre (x=0) et de la hauteur du nez, plus ça avance
                const noseFactor = Math.cos((x / 4) * (Math.PI / 2)) * Math.cos(((y - 0) / 12) * (Math.PI / 2));
                z += noseFactor * 6.5;
            }

            // 4. Pommettes (Reliefs doux)
            if (y > -6 && y < 4 && Math.abs(x) > 5) {
                const cheekFactor = Math.cos((Math.abs(x) - 5) / 10 * (Math.PI / 2)) * Math.cos((y / 6) * (Math.PI / 2));
                z += cheekFactor * 2.5;
            }

            // 5. Cavité de la bouche
            const distMouth = Math.sqrt((x / 8)**2 + ((y + 12) / 2)**2);
            if (distMouth < 1 && z > 15) { z -= (1 - distMouth) * 4; }

            pos.setXYZ(i, x, y, z);
        }
        headGeo.computeVertexNormals();

        // Matériau Cristal Iridescent (Couleurs vives sur fond clair)
        const skinMat = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff, 
            transparent: true,
            opacity: 0.4,
            roughness: 0.05, 
            metalness: 0.1,
            transmission: 0.9, 
            thickness: 1.5,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1,
            iridescence: 1.0, // Effet arc-en-ciel
            iridescenceIOR: 1.5
        });
        
        const head = new THREE.Mesh(headGeo, skinMat);
        head.castShadow = true;
        faceGroup.add(head);

        // COU COURT
        const neckGeo = new THREE.CylinderGeometry(9, 11, 12, 32); 
        const neckMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.35, transmission: 0.8, iridescence: 0.5 });
        const neck = new THREE.Mesh(neckGeo, neckMat);
        neck.position.y = -27;
        faceGroup.add(neck);

        // --- 3. LE CERVEAU INTERACTIF ---
        const brainGroup = new THREE.Group();
        brainGroup.position.set(0, 5, -5); 
        faceGroup.add(brainGroup);

        const coreMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const core = new THREE.Mesh(new THREE.SphereGeometry(4, 32, 32), coreMat);
        brainGroup.add(core);

        const nodes = [];
        // Couleurs très vives qui ressortent sur fond clair
        const nodeColors = [0x00ffff, 0xff00ff, 0x00ff00, 0x8a2be2, 0xff4500, 0xffd700];
        
        for(let i=0; i<50; i++) {
            const size = Math.random() * 1.5 + 0.5;
            const color = nodeColors[Math.floor(Math.random() * nodeColors.length)];
            const nodeMat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 1.0 });
            const node = new THREE.Mesh(new THREE.SphereGeometry(size, 16, 16), nodeMat);
            
            const radius = 8 + Math.random() * 10;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            
            node.position.set(
                radius * Math.sin(phi) * Math.cos(theta),
                radius * Math.sin(phi) * Math.sin(theta),
                radius * Math.cos(phi)
            );
            
            node.userData = { 
                id: `PATH-${i}`, 
                type: ["Visual Cortex", "Language Model", "Memory Bank", "Logic Gate", "Token Flux", "Reasoning"][i%6],
                color: color
            };
            
            nodes.push(node);
            brainGroup.add(node);
        }

        // Connexions
        const lineMat = new THREE.LineBasicMaterial({ color: 0x8a2be2, transparent: true, opacity: 0.2 });
        for(let i=0; i<nodes.length; i++) {
            for(let j=i+1; j<nodes.length; j++) {
                if(nodes[i].position.distanceTo(nodes[j].position) < 15) {
                    const points = [nodes[i].position, nodes[j].position];
                    const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
                    const line = new THREE.Line(lineGeo, lineMat);
                    brainGroup.add(line);
                }
            }
        }

        // --- 4. YEUX ET BOUCHE ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 5, 19);
            
            const globe = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.1 }));
            eyeGroup.add(globe);
            
            const iris = new THREE.Mesh(new THREE.CircleGeometry(1.5, 32), new THREE.MeshBasicMaterial({ color: 0x00ffff }));
            iris.position.z = 2.9;
            eyeGroup.add(iris);
            
            const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.6, 16), new THREE.MeshBasicMaterial({ color: 0xff00ff }));
            pupil.position.z = 3.0;
            eyeGroup.add(pupil);

            return eyeGroup;
        }
        faceGroup.add(createEye(-8));
        faceGroup.add(createEye(8));

        // BOUCHE DYNAMIQUE
        const mouthGeo = new THREE.SphereGeometry(4, 32, 16);
        const mouthMat = new THREE.MeshStandardMaterial({ color: 0xff00ff, emissive: 0x440044 }); 
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        mouth.position.set(0, -12, 20);
        mouth.scale.set(1.5, 0.1, 0.5); 
        faceGroup.add(mouth);

        // --- 5. OUTILS VISUELS ---
        const equipmentGroup = new THREE.Group();
        faceGroup.add(equipmentGroup);

        // LUNETTES (Or)
        const glassesGroup = new THREE.Group();
        const glassMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 1.0, roughness: 0.1 });
        const lensL = new THREE.Mesh(new THREE.TorusGeometry(4, 0.3, 16, 32), glassMat);
        lensL.position.set(-8, 5, 22);
        glassesGroup.add(lensL);
        const lensR = new THREE.Mesh(new THREE.TorusGeometry(4, 0.3, 16, 32), glassMat);
        lensR.position.set(8, 5, 22);
        glassesGroup.add(lensR);
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(8, 0.5, 0.5), glassMat);
        bridge.position.set(0, 5, 22);
        glassesGroup.add(bridge);
        glassesGroup.visible = false;
        equipmentGroup.add(glassesGroup);

        // CASQUE (Or)
        const headsetGroup = new THREE.Group();
        const band = new THREE.Mesh(new THREE.TorusGeometry(26, 1.5, 16, 32, Math.PI), glassMat);
        band.position.set(0, 5, 0);
        band.rotation.x = Math.PI / 2;
        band.rotation.z = Math.PI / 2;
        headsetGroup.add(band);
        const earL = new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 2, 32), glassMat);
        earL.position.set(-25, 0, 0);
        earL.rotation.z = Math.PI / 2;
        headsetGroup.add(earL);
        const earR = new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 2, 32), glassMat);
        earR.position.set(25, 0, 0);
        earR.rotation.z = Math.PI / 2;
        headsetGroup.add(earR);
        headsetGroup.visible = false;
        equipmentGroup.add(headsetGroup);

        // MICRO (Or + Vert)
        const micGroup = new THREE.Group();
        const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 15, 16), glassMat);
        boom.position.set(-15, -8, 15);
        boom.rotation.z = Math.PI / 4;
        boom.rotation.x = Math.PI / 6;
        micGroup.add(boom);
        const micHead = new THREE.Mesh(new THREE.SphereGeometry(1.5, 16, 16), new THREE.MeshStandardMaterial({ color: 0x00ff00, emissive: 0x005500 }));
        micHead.position.set(-10, -14, 20);
        micGroup.add(micHead);
        micGroup.visible = false;
        equipmentGroup.add(micGroup);

        // --- 6. LUMIÈRES (Éclairage de studio pour fond clair) ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8); // Très lumineux
        scene.add(ambientLight);
        
        const spotLight1 = new THREE.SpotLight(0xffffff, 2.5);
        spotLight1.position.set(30, 50, 40);
        spotLight1.castShadow = true;
        scene.add(spotLight1);

        const spotLight2 = new THREE.SpotLight(0x00ffff, 1.5); // Cyan pour les reflets
        spotLight2.position.set(-40, 0, 40);
        scene.add(spotLight2);

        const spotLight3 = new THREE.SpotLight(0xff00ff, 1.5); // Magenta pour les reflets
        spotLight3.position.set(0, -20, -40);
        scene.add(spotLight3);
        
        // Lumière Dorée
        const pointLight1 = new THREE.PointLight(0xffd700, 2, 200);
        pointLight1.position.set(0, 40, 20);
        scene.add(pointLight1);

        // --- 7. INTERACTION (CHIRURGIE) ---
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
                core.material.color.setHex(node.userData.color);
                
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

                isSpeaking = true;
                speakTimer = 2.0;
                
                addToTerminal('SYSTEM', `Surgical trigger on ${node.userData.id}: ${randomStep}`);
                entitySpeak(`Activating ${node.userData.type}. Reasoning updated.`);
            }
        }

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('click', onClick);

        // --- 8. LOGIQUE DES OUTILS VISUELS ---
        document.getElementById('btn-glasses').addEventListener('click', () => {
            glassesGroup.visible = !glassesGroup.visible;
            document.getElementById('status-glasses').innerText = glassesGroup.visible ? 'ON' : 'OFF';
            document.getElementById('btn-glasses').classList.toggle('active');
            addToTerminal('SYSTEM', `Optical Lenses ${glassesGroup.visible ? 'Equipped' : 'Removed'}.`);
        });

        document.getElementById('btn-headset').addEventListener('click', () => {
            headsetGroup.visible = !headsetGroup.visible;
            document.getElementById('status-headset').innerText = headsetGroup.visible ? 'ON' : 'OFF';
            document.getElementById('btn-headset').classList.toggle('active');
            addToTerminal('SYSTEM', `Neural Headset ${headsetGroup.visible ? 'Equipped' : 'Removed'}.`);
        });

        document.getElementById('btn-mic').addEventListener('click', () => {
            micGroup.visible = !micGroup.visible;
            document.getElementById('status-mic').innerText = micGroup.visible ? 'ON' : 'OFF';
            document.getElementById('btn-mic').classList.toggle('active');
            addToTerminal('SYSTEM', `Input Mic ${micGroup.visible ? 'Equipped' : 'Removed'}.`);
        });

        // --- 9. ANIMATION ---
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
            
            mouseX += (targetMouseX - mouseX) * 0.05; 
            mouseY += (targetMouseY - mouseY) * 0.05;
            faceGroup.rotation.y = mouseX * 0.3; 
            faceGroup.rotation.x = -mouseY * 0.2;

            brainGroup.scale.setScalar(1 + Math.sin(time * 2) * 0.05);

            if (isSpeaking) {
                mouth.scale.y = 0.1 + Math.abs(Math.sin(time * 15)) * 1.5; 
                speakTimer -= delta;
                if (speakTimer <= 0) { 
                    isSpeaking = false; 
                    mouth.scale.y = 0.1; 
                }
            }

            nodes.forEach((node, index) => {
                const scale = 1 + Math.sin(time * 5 + index) * 0.2;
                node.scale.setScalar(scale);
            });

            controls.update();
            renderer.render(scene, camera);
        }

        // --- 10. INTELLIGENCE & AUDIO ---
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

        document.getElementById('start-btn').addEventListener('click', () => {
            document.getElementById('init-screen').style.opacity = '0';
            setTimeout(() => { document.getElementById('init-screen').style.display = 'none'; }, 1500);
            if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged();
            setTimeout(() => { addToTerminal('ENTITY', "Golden link established. The universe is ours."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "Command received. Ready for neural surgery."); }, 1000);
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

print("✅ VISUAL/index.html généré (V16). Fond Or, Visage parfait, Outils.")
