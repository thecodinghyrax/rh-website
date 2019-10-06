const newsList = document.querySelector('.news__list');
const items = Array.from(newsList.children);
const dotsNav = document.querySelector('.news__nav');
const dots = Array.from(dotsNav.children);
const itemWidth = items[0].getBoundingClientRect().width;

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
    const targetDot = e.target.closest('button');

    if (!targetDot) return;

    const currentItem = newsList.querySelector('.current-item');
    const currentDot = dotsNav.querySelector('.current-item');
    const targetIndex = dots.findIndex(dot => dot === targetDot);
    const targetItem = items[targetIndex];
    currentDot.classList.remove('current-item');
    targetDot.classList.add('current-item');

    moveToItem(newsList, currentItem, targetItem);
});
