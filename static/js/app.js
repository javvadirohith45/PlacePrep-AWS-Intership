(function(){
  const root=document.documentElement;
  const saved=localStorage.getItem('placeprep-theme');
  if(saved==='light' || saved==='dark') root.dataset.theme=saved;

  const iconMap=[
    {keys:['percentage','percent'],icon:'percent'},
    {keys:['profit','loss'],icon:'trending-up'},
    {keys:['simple interest'],icon:'badge-dollar-sign'},
    {keys:['compound interest'],icon:'landmark'},
    {keys:['ratio','proportion'],icon:'scale'},
    {keys:['average'],icon:'chart-column'},
    {keys:['time & work','time and work'],icon:'timer'},
    {keys:['pipe','cistern'],icon:'funnel'},
    {keys:['time, speed','speed','distance'],icon:'gauge'},
    {keys:['train'],icon:'train-front'},
    {keys:['boat','stream'],icon:'ship'},
    {keys:['mixture','alligation'],icon:'flask-conical'},
    {keys:['partnership'],icon:'handshake'},
    {keys:['number system','number & letter','number and letter'],icon:'binary'},
    {keys:['hcf','lcm','factor'],icon:'sigma'},
    {keys:['probability'],icon:'dice-5'},
    {keys:['permutation','combination'],icon:'shuffle'},
    {keys:['ages'],icon:'users-round'},
    {keys:['algebra'],icon:'sigma'},
    {keys:['calendar'],icon:'calendar-days'},
    {keys:['clock'],icon:'clock-3'},
    {keys:['data interpretation'],icon:'chart-no-axes-combined'},
    {keys:['blood relation'],icon:'git-branch'},
    {keys:['direction sense'],icon:'compass'},
    {keys:['coding-decoding','coding decoding'],icon:'binary'},
    {keys:['series'],icon:'list-ordered'},
    {keys:['syllogism'],icon:'git-fork'},
    {keys:['seating arrangement'],icon:'armchair'},
    {keys:['floor','box puzzle'],icon:'building-2'},
    {keys:['order','ranking'],icon:'medal'},
    {keys:['puzzle'],icon:'puzzle'},
    {keys:['analogy'],icon:'scale-3d'},
    {keys:['odd one'],icon:'scan-search'},
    {keys:['statement','conclusion'],icon:'message-square-warning'},
    {keys:['coding'],icon:'code-2'},
    {keys:['dsa'],icon:'network'},
    {keys:['company'],icon:'building-2'},
    {keys:['mock'],icon:'clipboard-check'},
    {keys:['interview'],icon:'messages-square'},
    {keys:['resume'],icon:'file-user'},
    {keys:['hr'],icon:'users'},
    {keys:['technical'],icon:'terminal-square'}
  ];

  const companyIcons={
    tcs:'building-2', infosys:'landmark', wipro:'wind', accenture:'sparkles',
    cognizant:'brain-circuit', capgemini:'hexagon', hcl:'layers-3',
    deloitte:'briefcase-business', 'tech mahindra':'network', zoho:'boxes',
    ibm:'server', amazon:'shopping-bag', microsoft:'monitor-smartphone', ey:'eye'
  };

  function textOf(el){ return (el?.textContent || '').replace(/\s+/g,' ').trim().toLowerCase(); }
  function findIcon(name){
    const hit=iconMap.find(x=>x.keys.some(k=>name.includes(k)));
    return hit?.icon || 'sparkles';
  }
  function toneFor(name){
    let sum=0; for(let i=0;i<name.length;i++) sum=(sum+name.charCodeAt(i)*(i+1))%8;
    return `icon-tone-${sum+1}`;
  }

  function semanticIcons(){
    document.querySelectorAll('.topic-card').forEach(card=>{
      const title=card.querySelector('h3,h2,strong');
      const tile=card.querySelector('.topic-icon');
      if(!tile || !title) return;
      const name=textOf(title); tile.innerHTML=`<i data-lucide="${findIcon(name)}"></i>`;
      tile.classList.remove(...Array.from({length:8},(_,i)=>`icon-tone-${i+1}`));
      tile.classList.add(toneFor(name));
    });

    document.querySelectorAll('.company-card,.company-hero').forEach(card=>{
      const title=card.querySelector('h3,h1,strong');
      const tile=card.querySelector('.company-logo');
      if(!tile || !title) return;
      const name=textOf(title);
      const icon=Object.entries(companyIcons).find(([key])=>name.includes(key))?.[1] || 'building-2';
      tile.innerHTML=`<i data-lucide="${icon}"></i>`;
      tile.classList.remove(...Array.from({length:8},(_,i)=>`icon-tone-${i+1}`));
      tile.classList.add(toneFor(name));
    });

    document.querySelectorAll('.feature-card').forEach(card=>{
      const heading=card.querySelector('h2,h3,strong');
      const svg=card.querySelector('svg');
      if(!heading || svg) return;
      const icon=findIcon(textOf(heading));
      heading.insertAdjacentHTML('beforebegin',`<i class="feature-semantic-icon icon-tone-${(Array.from(textOf(heading)).reduce((a,c)=>a+c.charCodeAt(0),0)%8)+1}" data-lucide="${icon}"></i>`);
    });

    document.querySelectorAll('.cl-feature').forEach(card=>{
      const heading=card.querySelector('strong');
      if(!heading || card.querySelector('.feature-semantic-icon')) return;
      const name=textOf(heading);
      const icon=name.includes('real run')?'play-circle':name.includes('hidden')?'shield-check':name.includes('custom')?'flask-conical':'chart-no-axes-combined';
      heading.insertAdjacentHTML('beforebegin',`<i class="feature-semantic-icon ${toneFor(name)}" data-lucide="${icon}"></i>`);
    });

    document.querySelectorAll('.cl-lang').forEach(card=>{
      const title=card.querySelector('h3'); const tile=card.querySelector('.cl-lang-icon');
      if(!title || !tile) return;
      const name=textOf(title);
      tile.classList.add(toneFor(name));
    });
  }

  function refreshIcons(){
    semanticIcons();
    if(window.lucide) lucide.createIcons();
  }

  const toggle=document.getElementById('themeToggle');
  function updateThemeIcon(){
    if(!toggle) return;
    const isLight=root.dataset.theme==='light';
    toggle.innerHTML=`<i data-lucide="${isLight?'sun':'moon'}"></i>`;
    toggle.title=isLight?'Switch to dark theme':'Switch to light theme';
    if(window.lucide) lucide.createIcons();
  }
  if(toggle){
    updateThemeIcon();
    toggle.onclick=()=>{
      root.dataset.theme=root.dataset.theme==='light'?'dark':'light';
      localStorage.setItem('placeprep-theme',root.dataset.theme);
      updateThemeIcon();
    };
  }

  const menu=document.getElementById('mobileMenu');
  if(menu) menu.onclick=()=>document.querySelector('.nav-links')?.classList.toggle('mobile-open');
  document.querySelectorAll('.toast').forEach(t=>setTimeout(()=>t.remove(),4200));

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',refreshIcons,{once:true});
  else refreshIcons();
})();
