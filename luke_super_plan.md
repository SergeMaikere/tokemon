# LUKE SUPER PLAN !

## Step 1 -> Install the installer

Je te conseille d'installer brew ([lien ici](https://brew.sh/)).  
Tu devras pour ce faire entrer la commande suivante dans ton terminal
>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

## Step 2 -> Install Git

Comme d'hab ça va être une commande à rentrer ([lien ici](https://git-scm.com/install/mac))
>brew install git

## Step 3 -> Install Rust and Cargo

Rust est le language de programation et cargo c'est l'app qui fait tourner les trucs codé en Rust.
L'installation est assé suimple ([lien ici](https://rustup.rs/))  
Tu dois juste rentrer la commande suivante et suivre toutes les instructions
>curl https://sh.rustup.rs -sSf | sh  

Si tour va bien tu devrais voir le message suivant  

>Rust is installed now. Great!


## Step 4 -> Let's get Photocraft !

1. Place toi dans le bon dossier
	> cd ~/Applications
2. Clone le repo
	>git clone https://github.com/storytold/photocraft
3. Va dans le repo que tu viens de creer
	>cd photocraf
4. Launch the desktop app
	>cargo run --release -p photocraft -- image.psd
5. Test pour voir que tout va bien
	>cargo test --workspace 

## Step 5 -> Lets's get Effectcraft

1. Place toi dans le bon dossier
	> cd ~/Applications
2. Clone le repo
	>git clone https://github.com/storytold/effectcraft
3. Rentres les commandes suivantes les unes à la suite de l'autre. Je t'avoue que je ne sais pas du tout ce qu'elles font, mais ça à l'air d'être du lourd  

	>cargo run --release -p effectcraft   
	>cargo run --release -p effectcraft-cli -- render --out intro.mp4  
	>cargo xtask web --serve 8765  