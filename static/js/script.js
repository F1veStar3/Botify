

// Map

    document.addEventListener("DOMContentLoaded", function () {
        console.log("DOM fully loaded and parsed");
        ymaps.ready(init);
        function init() {
            console.log("Yandex Maps ready");
            var myMap = new ymaps.Map("map", {
                center: [55.751574, 37.573856],
                zoom: 10
            });

            console.log("Map initialized");

            fetch('/api/points/')
                .then(response => {
                    console.log("Fetched points");
                    return response.json();
                })
                .then(data => {
                    console.log("Data received:", data);
                    data.forEach(point => {
                        var placemark = new ymaps.Placemark([point.latitude, point.longitude], {
                            balloonContent: point.name
                        });
                        myMap.geoObjects.add(placemark);
                    });
                })
                .catch(error => {
                    console.error("Error fetching points:", error);
                });
        }
    });




// change logo

    document.addEventListener('DOMContentLoaded', function () {
        const userLogo = document.getElementById('user-logo');
        const fileInput = document.querySelector('input[name="logo"]');

        userLogo.addEventListener('mouseover', function () {
            userLogo.style.opacity = '0.7'; // Зміна непрозорості для вказівки на наведення
        });

        userLogo.addEventListener('mouseout', function () {
            userLogo.style.opacity = '1'; // Скидання непрозорості
        });

        userLogo.addEventListener('click', function () {
            fileInput.click();
        });

        fileInput.addEventListener('change', function () {
            document.getElementById('profile-form').submit();
        });
    });