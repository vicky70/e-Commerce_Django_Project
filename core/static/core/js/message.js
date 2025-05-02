document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.notification-card');
    console.log('checking if this script is getting called or not')
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('notification-hide');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 2000);  
    });

    const closeButtons = document.querySelectorAll('.btn-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.classList.add('notification-hide');
            setTimeout(() => {
                this.parentElement.remove();
            }, 500);
        });
    });
});