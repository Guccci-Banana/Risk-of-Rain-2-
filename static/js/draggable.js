document.addEventListener("DOMContentLoaded", () => {
    const draggables = Array.from(document.querySelectorAll('.draggable'));
    const resetBtn = document.getElementById('resetBtn');
    const lineUpBtn = document.getElementById('lineUpBtn');

    if (draggables.length > 0 && controls) {
        controls.style.display = 'flex';
    }

    // Attach dragging once
    function makeDraggable(el) {
        el.style.position = 'absolute';
        el.style.cursor = 'grab';

        el.addEventListener('mousedown', e => {
            e.preventDefault();
            let startX = e.clientX;
            let startY = e.clientY;

            let initialLeft = parseInt(el.style.left) || 0;
            let initialTop = parseInt(el.style.top) || 0;

            el.style.zIndex = 1000;
            el.style.cursor = 'grabbing';

            const minLeft = 10;
            const minTop = 160;
            const maxLeft = window.innerWidth - el.offsetWidth - 10;
            const maxTop = window.innerHeight - el.offsetHeight - 50;

            function onMouseMove(e) {
                let newLeft = initialLeft + (e.clientX - startX);
                let newTop = initialTop + (e.clientY - startY);

                newLeft = Math.max(minLeft, Math.min(newLeft, maxLeft));
                newTop = Math.max(minTop, Math.min(newTop, maxTop));

                el.style.left = newLeft + 'px';
                el.style.top = newTop + 'px';
            }

            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                el.style.zIndex = 1;
                el.style.cursor = 'grab';
            }

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }

    // Shuffle positions
    function initializeDraggables() {
        const placedBoxes = [];

        draggables.forEach(el => {
            const boxWidth = el.offsetWidth;
            const boxHeight = el.offsetHeight;
            const horizontalMargin = window.innerWidth / 10;
            const verticalMargin = window.innerHeight / 5;

            let left, top, tries = 0;
            const maxTries = 100;
            let overlapping = true;

            do {
                left = Math.random() * (window.innerWidth - boxWidth - 2 * horizontalMargin) + horizontalMargin;
                top = Math.random() * (window.innerHeight - boxHeight - 2 * verticalMargin) + verticalMargin;
                tries++;

                overlapping = placedBoxes.some(box => (
                    left < box.right &&
                    left + boxWidth > box.left &&
                    top < box.bottom &&
                    top + boxHeight > box.top
                ));

                if (tries >= maxTries) overlapping = false;
            } while (overlapping);

            el.style.left = left + 'px';
            el.style.top = top + 'px';

            placedBoxes.push({
                left: left,
                top: top,
                right: left + boxWidth,
                bottom: top + boxHeight
            });
        });
    }

    // Line up vertically
    function lineUpDraggables() {
        const spacing = 20;
        const totalHeight = draggables.reduce((acc, el) => acc + el.offsetHeight, 0) + (draggables.length - 1) * spacing;
        let currentTop = (window.innerHeight - totalHeight) / 1.5;

        draggables.forEach(el => {
            const left = (window.innerWidth - el.offsetWidth) / 2;
            el.style.left = left + 'px';
            el.style.top = currentTop + 'px';
            currentTop += el.offsetHeight + spacing;
        });
    }

    // Add drag functionality to all boxes once
    draggables.forEach(makeDraggable);

    // Start with lined-up boxes
    lineUpDraggables();

    // Buttons
    if (lineUpBtn) lineUpBtn.addEventListener('click', lineUpDraggables);
    if (resetBtn) resetBtn.addEventListener('click', initializeDraggables);

    // On resize → re-line up (not shuffle, unless you want both)
    window.addEventListener('resize', lineUpDraggables);
});