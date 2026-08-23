function copyText(elementId, labelName) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let textToCopy = element.value || element.innerText || element.textContent;
    navigator.clipboard.writeText(textToCopy).then(() => {
        showToast(`Copied ${labelName || 'text'} to clipboard!`);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

function showToast(message) {
    let toast = document.getElementById('toast-notification');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast-notification';
        toast.style.position = 'fixed';
        toast.style.bottom = '20px';
        toast.style.right = '20px';
        toast.style.backgroundColor = '#10b981';
        toast.style.color = '#ffffff';
        toast.style.padding = '12px 24px';
        toast.style.borderRadius = '8px';
        toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        toast.style.zIndex = '9999';
        toast.style.fontWeight = '600';
        toast.style.transition = 'opacity 0.3s ease';
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.style.opacity = '1';
    
    setTimeout(() => {
        toast.style.opacity = '0';
    }, 3000);
}
