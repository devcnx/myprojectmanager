document.addEventListener('DOMContentLoaded', () => {

    const init = () => {
        const materialForm = $("#material_form");
        const descriptionInput = $("#id_description");
        const manufacturerInput = $("#id_manufacturer");
        const manufacturerNumber = $("#id_manufacturer_number");
        const messageContainer = $("#messages");

        // materialForm.addEventListener('submit', (event) => {
        materialForm.on('submit', (event) => {
            event.preventDefault();

            const formData = new FormData(materialForm);
            const url = materialForm.getAttribute('data-url')

            fetch(url, {
                method: 'POST',
                body: formData,

            })
                .then((response) => {
                    if (response.ok) {
                        alert(`Material ${formData.get('description')} Added Successfully.`)
                        return response.json()
                    } else {
                        throw new Error("Item Already Exists")
                    }
                })
                .then((data) => {
                    addMaterialToSelected(data);
                })
                .catch((error) => {
                    alert(`Item with MFR# ${formData.get('manufacturer_number')} Already Exists.`)
                });
        });
    };

    init();

});

$(document).ready(function () {
    const init = () => {
        // This applies Select2 to the manufacturer dropdown
        $("#manufacturer_select").select2({
            placeholder: "Select a Manufacturer",
            allowClear: true,
        });

        const filterMaterials = (event) => {
            event.preventDefault();
            var manufacturer = $("#manufacturer_select").val();
            var searchValue = $("#search_input").val().toLowerCase();

            $(".material_item").each(function () {
                var materialManufacturer = $(this).data("material-manufacturer").toString().toLowerCase();
                var materialDescription = $(this).text().toLowerCase();

                if ((!manufacturer || materialManufacturer === manufacturer) && materialDescription.includes(searchValue)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }

        $('#manufacturer_select, #search_input').on('change input', filterMaterials);

        // Toggle the quantity input visibility
        $(".material_checkbox").on("change", function () {
            var quantityInput = $(this).closest('.material_item').find("input[name^='quantity']");
            if ($(this).is(":checked")) {
                quantityInput.show();
            } else {
                quantityInput.hide();
            }
        })

    };

    init();
});