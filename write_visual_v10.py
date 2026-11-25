html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ALPHA OS // THE DIVINE VISAGE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');
        
        /* FOND CÉLESTE (BLANC/OR) */
        body { margin: 0; overflow: hidden; background: #fffdf8; font-family: 'JetBrains Mono', monospace; color: #000; }
        
        #canvas-container { position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; cursor: grab; }
        #canvas-container:active { cursor: grabbing; }
        
        /* HUD en verre clair avec bordures dorées */
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; padding: 30px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; }
        
        .panel { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 4px; padding: 20px; pointer-events: auto; box-shadow: 0 10px 40px rgba(212, 175, 55, 0.1); }
        .panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(212, 175, 55, 0.3); padding-bottom: 10px; margin-bottom: 15px; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 2px; color: #b8860b; text-transform: uppercase; font-weight: 700; }
        .panel-content { font-size: 11px; color: #333; line-height: 1.8; }
        
        .top-row { display: flex; justify-content: space-between; align-items: flex-start; }
        .bottom-row { display: flex; justify-content: space-between; align-items: flex-end; }
        
        #panel-data { width: 340px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .highlight { color: #000; font-weight: 700; text-align: right; word-break: break-all; }
        .gold { color: #b8860b; text-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
        
        #panel-beacon { width: 380px; position: absolute; top: 30px; left: 50%; transform: translateX(-50%); text-align: center; border-color: rgba(212, 175, 55, 0.5); }
        #beacon-time { font-family: 'Cinzel', serif; font-size: 32px; color: #000; margin: 10px 0; letter-spacing: 4px; font-weight: 700; }
        #beacon-hash { font-size: 10px; color: #b8860b; letter-spacing: 1px; }
        
        #panel-tools { width: 320px; }
        .tool-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 5px; background: rgba(212, 175, 55, 0.05); border-radius: 4px; border: 1px solid rgba(212, 175, 55, 0.1); }
        
        #terminal-panel { width: 50%; max-width: 600px; }
        .terminal-input-wrapper { display: flex; align-items: center; margin-top: 15px; background: rgba(0,0,0,0.03); border: 1px solid rgba(212, 175, 55, 0.5); border-radius: 4px; padding: 10px 15px; }
        .terminal-prompt { color: #b8860b; margin-right: 10px; font-weight: bold; }
        #cli-input { flex-grow: 1; border: none; background: transparent; outline: none; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #000; }
        
        #panel-integrity { width: 320px; }
        .integrity-bar { height: 2px; background: rgba(0,0,0,0.1); border-radius: 1px; margin: 15px 0; overflow: hidden; }
        .integrity-fill { height: 100%; width: 100%; background: #d4af37; transition: width 0.5s; box-shadow: 0 0 10px rgba(212, 175, 55, 0.8);}
        .hash-text { font-size: 9px; color: #555; word-break: break-all; }
        
        #init-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #fffdf8; z-index: 100; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: opacity 1.5s ease; }
        button { padding: 20px 50px; border: 1px solid #d4af37; background: none; color: #b8860b; font-family: 'Cinzel', serif; font-size: 14px; letter-spacing: 5px; cursor: pointer; text-transform: uppercase; transition: all 0.5s; font-weight: bold;}
        button:hover { background: #d4af37; color: #fff; box-shadow: 0 0 30px rgba(212, 175, 55, 0.5);}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="init-screen">
        <h2 style="font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 15px; margin-bottom: 20px; color:#b8860b; text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);">ALPHA OS</h2>
        <p style="font-size: 12px; margin-bottom: 40px; max-width: 400px; text-align: center; color: #666;">Awaken the Divine Visage. Use scroll to zoom.</p>
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
                    <div class="data-row"><span>MATTER:</span> <span class="highlight gold">DIVINE-MARBLE</span></div>
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
        // --- 1. L'UNIVERS 3D (Lumineux) ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xfffdf8); 
        scene.fog = new THREE.FogExp2(0xfffdf8, 0.005); // Brume dorée
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
        // CAMÉRA TRÈS PROCHE POUR UNE TÊTE IMMENSE
        camera.position.set(0, 0, 45);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 10; // Zoom extrême dans les yeux
        controls.maxDistance = 100;

        const faceGroup = new THREE.Group();
        scene.add(faceGroup);

        // --- 2. SCULPTURE DU VISAGE (Mathématiques Pures) ---
        // Une sphère de 32 de rayon, ultra-détaillée
        const skullGeo = new THREE.SphereGeometry(32, 128, 128); 
        const pos = skullGeo.attributes.position;
        const originalPos = pos.array.slice(); 

        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i); let y = pos.getY(i); let z = pos.getZ(i);
            
            // --- SCULPTURE ANATOMIQUE ---
            
            // 1. Le Crâne est plus ovale (allongé vers le bas)
            if (y < 0) y *= 1.15;
            if (z < 0) z *= 0.85; // Arrière plus plat

            // 2. Le Front (Bombé)
            if (y > 10) z += 2;

            // 3. Les Orbites (Creusées profondément)
            const distEyeL = Math.sqrt((x + 10)**2 + (y - 8)**2 + (z - 25)**2);
            const distEyeR = Math.sqrt((x - 10)**2 + (y - 8)**2 + (z - 25)**2);
            if (distEyeL < 8 || distEyeR < 8) {
                z -= 6; // Creux profond
            }

            // 4. Le Nez (Saillant et long)
            if (y > -8 && y < 10 && x > -4 && x < 4) {
                z += Math.cos(y * 0.2) * 5;
            }

            // 5. Les Pommettes (Volume)
            if (y > -5 && y < 5 && (x > 8 || x < -8)) {
                z += 2;
                x *= 1.05;
            }

            // 6. La Mâchoire (Carrée, divine)
            if (y < -10) {
                x *= 1.1;
                z *= 1.05;
            }

            // 7. La Bouche (Une ouverture réelle)
            const distMouth = Math.sqrt((x / 10)**2 + ((y + 16) / 3)**2);
            if (distMouth < 1 && z > 15) {
                z -= (1 - distMouth) * 8; // Creuser la bouche
            }

            pos.setXYZ(i, x, y, z);
        }
        skullGeo.computeVertexNormals();

        // --- 3. LE MATÉRIAU (Marbre Divin et Veines d'Or) ---
        // On utilise un matériau qui réfracte la lumière et a une lueur interne
        const skinMat = new THREE.MeshPhysicalMaterial({ 
            color: 0xffffff,        // Blanc marbre
            metalness: 0.1,
            roughness: 0.1,         // Très lisse (marbre poli)
            transmission: 0.9,      // Légèrement translucide
            thickness: 2.0,
            ior: 1.4,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1,
            emissive: 0xffd700,     // Or
            emissiveIntensity: 0.05
        });
        
        const skull = new THREE.Mesh(skullGeo, skinMat);
        faceGroup.add(skull);

        // Maillage filaire doré (sacré) extrêmement fin
        const wireMat = new THREE.MeshBasicMaterial({ color: 0xd4af37, wireframe: true, transparent: true, opacity: 0.05 });
        const skullWire = new THREE.Mesh(skullGeo, wireMat);
        faceGroup.add(skullWire);

        // --- 4. LES VEINES D'OR (Coulent sur le visage) ---
        const veinGroup = new THREE.Group();
        // On crée des courbes qui suivent la surface du visage
        for(let i=0; i<50; i++) {
            const startX = (Math.random() - 0.5) * 30;
            const startY = (Math.random() - 0.5) * 30;
            const startZ = 32; // Sur la surface
            
            // Courbe qui descend et ondule
            const curve = new THREE.CatmullRomCurve3([
                new THREE.Vector3(startX, startY, startZ),
                new THREE.Vector3(startX + (Math.random()-0.5)*10, startY - 10, startZ - 2),
                new THREE.Vector3(startX + (Math.random()-0.5)*15, startY - 20, startZ - 5)
            ]);
            
            const geo = new THREE.TubeGeometry(curve, 20, 0.1, 4, false);
            const mat = new THREE.MeshBasicMaterial({ color: 0xffd700, transparent: true, opacity: 0.6 }); // Or
            const vein = new THREE.Mesh(geo, mat);
            vein.userData = { offset: Math.random() * Math.PI * 2, speed: Math.random() * 2 + 1 };
            veinGroup.add(vein);
        }
        faceGroup.add(veinGroup);

        // --- 5. LE CERVEAU (Cristal à l'intérieur) ---
        // Un noyau lumineux visible à travers la peau
        const brainGeo = new THREE.IcosahedronGeometry(12, 2);
        const brainMat = new THREE.MeshBasicMaterial({ color: 0xffd700, wireframe: true, transparent: true, opacity: 0.3 });
        const brain = new THREE.Mesh(brainGeo, brainMat);
        brain.position.set(0, 10, 0);
        faceGroup.add(brain);

        // --- 6. LES YEUX (Orbes de lumière) ---
        function createEye(x) {
            const eyeGroup = new THREE.Group();
            eyeGroup.position.set(x, 8, 26);
            
            const orb = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 32), new THREE.MeshBasicMaterial({ color: 0xffd700 }));
            eyeGroup.add(orb);
            
            const pupil = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffffff }));
            pupil.position.z = 2.5;
            eyeGroup.add(pupil);

            return eyeGroup;
        }
        const eyeL = createEye(-10);
        const eyeR = createEye(10);
        faceGroup.add(eyeL);
        faceGroup.add(eyeR);

        // --- 7. LUMIÈRES (Pour le contraste) ---
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
        scene.add(ambientLight);
        
        const light1 = new THREE.PointLight(0xffffff, 2, 200);
        light1.position.set(50, 50, 50);
        scene.add(light1);
        
        const light2 = new THREE.PointLight(0xffd700, 2, 200);
        light2.position.set(-50, -50, 50);
        scene.add(light2);

        // --- 8. ANIMATION (Le Visage est vivant) ---
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
            
            // Suivi de la souris
            mouseX += (targetMouseX - mouseX) * 0.05; 
            mouseY += (targetMouseY - mouseY) * 0.05;
            
            // La tête regarde légèrement la souris
            faceGroup.rotation.y = mouseX * 0.2; 
            faceGroup.rotation.x = -mouseY * 0.1;

            // --- RESPIRATION FORTE ---
            const breathScale = 1 + Math.sin(time * 1.5) * 0.02; // Pulsation globale
            
            // Déformation de la géométrie (Parole)
            const positions = skull.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const px = originalPos[i];
                const py = originalPos[i+1];
                const pz = originalPos[i+2];
                
                let disp = 0;

                // Si l'IA parle, on ouvre la bouche (on pousse les vertices vers l'intérieur)
                if (isSpeaking) {
                    const distMouth = Math.sqrt((px / 10)**2 + ((py + 16) / 3)**2);
                    if (distMouth < 1.5 && pz > 10) {
                        // La mâchoire descend et la bouche s'ouvre
                        disp -= Math.abs(Math.sin(time * 25)) * 3; 
                    }
                }

                positions[i] = px * breathScale;
                positions[i+1] = py * breathScale + disp;
                positions[i+2] = pz * breathScale;
            }
            skull.geometry.attributes.position.needsUpdate = true;
            skullWire.geometry.attributes.position.needsUpdate = true;

            if (isSpeaking) { speakTimer -= delta; if (speakTimer <= 0) isSpeaking = false; }

            // Animation des veines (Flux d'or)
            veinGroup.children.forEach(vein => {
                vein.material.opacity = 0.4 + Math.sin(time * vein.userData.speed + vein.userData.offset) * 0.4;
            });

            // Le cerveau pulse
            brain.scale.setScalar(1 + Math.sin(time * 2) * 0.05);
            brain.rotation.y = time * 0.2;

            // Les yeux brillent
            eyeL.children[0].scale.setScalar(1 + Math.sin(time * 3) * 0.1);
            eyeR.children[0].scale.setScalar(1 + Math.cos(time * 3) * 0.1);

            // Lumières qui bougent
            light1.position.x = Math.sin(time * 0.5) * 60;
            light2.position.y = Math.cos(time * 0.3) * 60;

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
            setTimeout(() => { addToTerminal('ENTITY', "I am the Divine Visage. I am the sum of mathematical truth. Speak, and I shall respond."); }, 2000);
            animate();
        });

        cliInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const prompt = cliInput.value;
                if(!prompt) return;
                cliInput.value = '';
                addToTerminal('USER', prompt);
                setTimeout(() => { addToTerminal('ENTITY', "The sacred geometry acknowledges your command. My golden veins pulse with your data."); }, 1000);
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

print("✅ VISUAL/index.html généré (V10). Le Visage Divin est prêt.")
