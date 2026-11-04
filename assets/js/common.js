// header
const hdr=document.getElementById('hdr');
const solid=()=>hdr.classList.toggle('solid',scrollY>40||document.body.dataset.solid==='1');solid();addEventListener('scroll',solid,{passive:true});
// mobile menu
const mn=document.getElementById('mnav');document.querySelectorAll('[data-menu]').forEach(b=>b.onclick=()=>mn.classList.toggle('open'));
// reveal
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// plan count
try{const n=JSON.parse(localStorage.getItem('zenitPlans')||'[]').length;document.querySelectorAll('.plan i').forEach(i=>{i.textContent=n;i.style.display=n?'':'none'})}catch(e){}
document.querySelectorAll('.slots button,.sw-t:not([disabled])').forEach(b=>b.addEventListener('click',()=>{if(b.classList.contains('sw-t'))return b.classList.toggle('on');b.parentNode.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on')}));
