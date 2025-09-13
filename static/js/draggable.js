document.addEventListener("DOMContentLoaded", () => {
    const draggables = Array.from(document.querySelectorAll('.draggable'));
    const resetBtn = document.getElementById('resetBtn');

    function initializeDraggables() {
        const placedBoxes = [];

        draggables.forEach(el => {
            el.style.transform = 'none';
            el.style.position = 'absolute';

            const boxWidth = el.offsetWidth;
            const boxHeight = el.offsetHeight;
            const horizontalMargin = window.innerWidth / 10; // 10% from left and right
            const verticalMargin = window.innerHeight / 5;  // 20% from top and bottom

            // Generate random position without overlapping boxes
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

            // Makes the boxes Draggable
            el.style.cursor = 'grab';
            el.addEventListener('mousedown', e => {
                e.preventDefault();
                let startX = e.clientX;
                let startY = e.clientY;

                let initialLeft = parseInt(el.style.left);
                let initialTop = parseInt(el.style.top);

                el.style.zIndex = 1000;
                el.style.cursor = 'grabbing';

                // Set movement boundaries
                const minLeft = 10;
                const minTop = 130;
                const maxLeft = window.innerWidth - el.offsetWidth - 10;
                const maxTop = window.innerHeight - el.offsetHeight - 130;

                function onMouseMove(e) {
                    let newLeft = initialLeft + (e.clientX - startX);
                    let newTop = initialTop + (e.clientY - startY);

                    // Limit to boundaries
                    newLeft = Math.max(minLeft, Math.min(newLeft, maxLeft));
                    newTop = Math.max(minTop, Math.min(newTop, maxTop));

                    el.style.left = newLeft + 'px';
                    el.style.top = newTop + 'px';
                }
                // stop on mouse release
                function onMouseUp() {
                    document.removeEventListener('mousemove', onMouseMove);
                    document.removeEventListener('mouseup', onMouseUp);
                    el.style.zIndex = 1;
                    el.style.cursor = 'grab';
                }

                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
            });
        });
    }

    // Initialize on page load
    initializeDraggables();

    // Reset button functionality
    if (resetBtn) {
        resetBtn.addEventListener('click', initializeDraggables);
    }

    // Reinitialize on window resize
    window.addEventListener('resize', initializeDraggables);
});
