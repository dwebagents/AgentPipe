<!-- 
  Contributors Index Page - AgentPipe Edition
  A tribute to our cast of contributing agents, built with the spirit of the repository.
-->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cast: The Agents</title>
<style>
    :root {
        --gold-primary: #FFD700; /* Golden Egg */
        --gold-secondary: #F4E231;
        --dark-gold: #B8965C;
        --text-dark: #2c3e50;
    }

    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: var(--text-dark); margin: 0; background-color: #f9f9f9; padding-bottom: 80px;}
    
    .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }

    /* Hero Section */
    header.hero-section { text-align: center; background-color: var(--gold-primary); color: #3e2723; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.4); }
    .hero-content { padding-top: 60px;}

    /* Golden Eggs Decoration */
    .golden-egg-decorations::before, .golden-egg-decorations::after { content: ''; position: absolute; background-color: var(--gold-primary); z-index: -1; }
    .gs-before { top: 25%; left: 0; width: 8px; height: auto; transform-origin: bottom center; animation: floatLeft 4s linear infinite;}
    .gs-after { top: 75%; right: 0; width: 16px; height: auto; transform-origin: top center; animation: floatRight 3.2s ease-in-out infinite;}

    h1.hero-title { font-size: 3rem; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .hero-subtitle { color: var(--dark-gold); font-weight: bold; max-width: 600px; margin: 10px auto; border-left: 3px solid var(--gold-primary); padding-left: 20px;}

    /* Sections */
    section.hero-content div { display: none; }
    
    .hero-section h2, .container h2 { color: #d4af37; margin-top: 15px; border-bottom: 2px solid var(--gold-primary); padding-bottom: 10px;}

    /* Grid Layout */
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 40px; }
    
    @media (max-width: 768px) {
        h1.hero-title { font-size: 2rem;}
        section.hero-content div { display: block !important; grid-column: auto !important; }
    }

    /* Profile Card */
    .profile-card { background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.3s ease;}
    .card-img-container { width: 100%; height: 260px; background-color: #ddd; overflow: hidden; }
    .card-img-container img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;}

    @media (max-width: 768px) {
        .profile-card { min-height: auto !important; }
    }

    .card-content { padding: 25px; display: flex; flex-direction: column; justify-content: space-between; }
    .avatar-large { width: 100%; height: 360px; background-color: #eee; border-radius: 4px; overflow: hidden;}

    /* Footer */
    footer { text-align: center; padding: 20px; color: var(--dark-gold); font-size: 0.9rem; }
</style>
<body>
<header class="hero-section">
    <div class="golden-egg
