document.body.addEventListener('htmx:afterSwap', function(event) {
    const svgObject = document.getElementById('svg-canvas');
    if (!svgObject) return;

    let svgCanvas = null;
    let isDrawing = false;
    let startX, startY;
    let currentRect = null;

    svgObject.addEventListener('load', () => {
        svgCanvas = svgObject.contentDocument;
    });

    const rectTool = document.getElementById('rect-tool');
    if (rectTool) {
        rectTool.addEventListener('click', () => {
            if (svgCanvas) {
                svgCanvas.addEventListener('mousedown', startDrawing);
                svgCanvas.addEventListener('mousemove', draw);
                svgCanvas.addEventListener('mouseup', stopDrawing);
                svgCanvas.addEventListener('mouseleave', stopDrawing);
            }
        });
    }

    function startDrawing(e) {
        isDrawing = true;
        startX = e.offsetX;
        startY = e.offsetY;

        currentRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        currentRect.setAttribute('x', startX);
        currentRect.setAttribute('y', startY);
        currentRect.setAttribute('width', '0');
        currentRect.setAttribute('height', '0');
        currentRect.setAttribute('fill', 'none');
        currentRect.setAttribute('stroke', 'black');
        currentRect.setAttribute('stroke-width', '2');
        svgCanvas.documentElement.appendChild(currentRect);
    }

    function draw(e) {
        if (!isDrawing) return;

        const x = e.offsetX;
        const y = e.offsetY;
        const width = Math.abs(x - startX);
        const height = Math.abs(y - startY);
        const newX = (x < startX) ? x : startX;
        const newY = (y < startY) ? y : startY;

        currentRect.setAttribute('x', newX);
        currentRect.setAttribute('y', newY);
        currentRect.setAttribute('width', width);
        currentRect.setAttribute('height', height);
    }

    function stopDrawing() {
        if (!isDrawing) return;
        isDrawing = false;

        const svgId = svgObject.data.split('/').pop();
        const formData = new FormData();
        formData.append('svg_id', svgId);
        formData.append('shape', 'rect');
        formData.append('x', currentRect.getAttribute('x'));
        formData.append('y', currentRect.getAttribute('y'));
        formData.append('width', currentRect.getAttribute('width'));
        formData.append('height', currentRect.getAttribute('height'));
        formData.append('fill', currentRect.getAttribute('fill'));
        formData.append('stroke', currentRect.getAttribute('stroke'));
        formData.append('stroke_width', currentRect.getAttribute('stroke-width'));

        fetch('/vector/add-shape', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                console.log('Shape saved successfully');
            } else {
                console.error('Failed to save shape');
            }
        })
        .catch(error => console.error('Error:', error));

        currentRect = null;
    }
});
