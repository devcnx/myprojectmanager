
document.addEventListener('DOMContentLoaded', () => {

    const addMaterialToSelected = (material) => {
        const selectedMaterials = $("#selected_materials");
        const option = document.createElement('option');
        option.value = material.material_id;
        option.text = material.description;
        selectedMaterials.add(option);
    };



    const init = () => {
        const materialForm = $("#add_material_form");
        const descriptionInput = $("#id_description");
        const manufacturerInput = $("#id_manufacturer");
        const manufacturerNumber = $("#id_manufacturer_number");
        const messageContainer = $("#messages");

        materialForm.addEventListener('submit', (event) => {
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