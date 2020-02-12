const newsList = document.querySelector('.news__list');
const items = Array.from(newsList.children);
const dotsNav = document.querySelector('.news__nav');
const dots = Array.from(dotsNav.children);
const itemWidth = items[0].getBoundingClientRect().width;
var slideOn = true;

const setItmePosition = (item, index) => {
    item.style.left = itemWidth * index + 'px';
};

items.forEach(setItmePosition);

const moveToItem = (newsList, currentItem, targetItem) => {
    newsList.style.transform = 'translateX(-' + targetItem.style.left + ')';
    currentItem.classList.remove('current-item');
    targetItem.classList.add('current-item');
};

dotsNav.addEventListener('click', e => {
    slideOn = false;
    console.log('The slideOn var is now: ' + slideOn);
    
    const targetDot = e.target.closest('button');

    if (!targetDot) return;

    const currentItem = newsList.querySelector('.current-item');
    const currentDot = dotsNav.querySelector('.current-item');
    const targetIndex = dots.findIndex(dot => dot === targetDot);
    const targetItem = items[targetIndex];
    currentDot.classList.remove('current-item');
    targetDot.classList.add('current-item');

    moveToItem(newsList, currentItem, targetItem);
}
);

function stopSlide() {
    clearInterval(changeSlide);
}

function changeSlide() {
    if (slideOn === true){
        
        const currentItem = newsList.querySelector('.current-item');
        const currentDot = dotsNav.querySelector('.current-item');
        var targetIndex = dots.findIndex(dot => dot === currentDot);
        if (targetIndex === (dots.length - 1)) {
            targetIndex = -1;
        };
        const targetDot = dots[targetIndex + 1];
        const targetItem = items[targetIndex + 1];
        currentDot.classList.remove('current-item');
        targetDot.classList.add('current-item');

        moveToItem(newsList, currentItem, targetItem);
    } 
        
};

var startSlide = setInterval(changeSlide, 5000)

if (slideOn === false){
    stopSlide();
};
