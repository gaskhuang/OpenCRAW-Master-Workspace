function updateTime() {
    const now = new Date();
    const timeString = now.getFullYear() + '/' + 
        String(now.getMonth() + 1).padStart(2, '0') + '/' + 
        String(now.getDate()).padStart(2, '0') + ' ' + 
        String(now.getHours()).padStart(2, '0') + ':' + 
        String(now.getMinutes()).padStart(2, '0') + ':' + 
        String(now.getSeconds()).padStart(2, '0');
    document.getElementById('current-time').textContent = timeString;
}

setInterval(updateTime, 1000);
updateTime();

// 未來數據對接邏輯可在此擴充
console.log("SLIDER Dashboard initialized.");
