
document.addEventListener('DOMContentLoaded', function () {
    const countryField = document.querySelector('#id_country');
    const cityField = document.querySelector('#id_city');

    if (countryField) {
        countryField.addEventListener('change', function () {
            const countryId = this.value;

            if (countryId) {
                fetch(`/admin/get_cities/${countryId}/`)
                    .then(response => response.json())
                    .then(data => {
                        cityField.innerHTML = '';
                        data.cities.forEach(city => {
                            const option = document.createElement('option');
                            option.value = city.id;
                            option.textContent = city.name;
                            cityField.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                cityField.innerHTML = '';
            }
        });
    }
});
