// document.addEventListener('DOMContentLoaded', () => {

//     const init = () => {
//         const materialForm = $("#material_form");

//         materialForm.on('submit', (event) => {
//             event.preventDefault();

//             const formData = new FormData(materialForm[0]);
//             // const url = materialForm.getAttribute('data-url')
//             const url = materialForm.attr('data-url');

//             fetch(url, {
//                 method: 'POST',
//                 body: formData,
//             })
//                 .then((response) => {
//                     if (response.ok) {
//                         alert(`Material ${formData.get('description')} Added Successfully.`)
//                         return response.json()
//                     } else {
//                         throw new Error("Item Already Exists")
//                     }
//                 })
//                 .then((data) => {
//                     addMaterialToSelected(data);
//                 })
//                 .catch((error) => {
//                     alert(`Item with MFR# ${formData.get('manufacturer_number')} Already Exists.`)
//                 });
//         });
//     };

//     init();

// });

$(document).ready(function () {
    const init = () => {
        // This applies Select2 to the manufacturer dropdown
        $("#manufacturer_select").select2({
            placeholder: "Select a Manufacturer",
            allowClear: true,
        });

        // const filterMaterials = (event) => {
        //     event.preventDefault();
        //     var manufacturer = $("#manufacturer_select").val();
        //     var searchValue = $("#search_input").val().toLowerCase();

        //     $(".material_item").each(function () {
        //         var materialManufacturer = $(this).data("material-manufacturer").toString().toLowerCase();
        //         // var materialDescription = $(this).text().toLowerCase();
        //         var materialDescription = $(this).find('label').text().toLowerCase();

        //         if (manufacturer === 'All') {
        //             if (materialDescription.includes(searchValue)) {
        //                 $(this).show();
        //             } else {
        //                 $(this).hide();
        //             }
        //         } else {
        //             if ((!manufacturer || materialManufacturer.toLowerCase() === manufacturer.toLowerCase()) && materialDescription.includes(searchValue)) {
        //                 $(this).show();
        //             } else {
        //                 $(this).hide();
        //             }
        //         }

        //     });
        // }

        const filterMaterials = (event) => {
            event.preventDefault();
            var manufacturer = $("#manufacturer_select").val();
            var searchValue = $("#search_input").val().toLowerCase();

            $(".material_item").each(function () {
                var materialManufacturer = $(this).data("material-manufacturer").toString().toLowerCase();
                var materialDescription = "";
                $(this).find("td").each(function () {
                    materialDescription += $(this).text();
                });
                materialDescription = materialDescription.toLowerCase();

                if (manufacturer === 'All') {
                    if (materialDescription.includes(searchValue)) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                } else {
                    if ((!manufacturer || materialManufacturer.toLowerCase() === manufacturer.toLowerCase()) && materialDescription.includes(searchValue)) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                }
            });
        }


        $('#manufacturer_select, #search_input').on('change input', filterMaterials);

        // Toggle the quantity input visibility
        $(document).on("change", ".material_checkbox", function () {
            var quantityInput = $(this).closest('.material_item').find("input[name^='item_quantity']");
            var quantityInputLabel = $(this).closest('.material_item').find("label[for^='item_quantity']");
            if ($(this).is(":checked")) {
                quantityInput.show();
                quantityInputLabel.show();
            } else {
                quantityInput.hide();
                quantityInputLabel.hide();
            }
        });

        // const addMaterialToBidList = (material, quantity) => {
        const addMaterialToBidList = (material, quantity, unitOfMeasure, unitPrice) => {
            for (let index = 0; index < quantity; index++) {
                const bidMaterialList = $("#bid_materials_list");
                const materialItem = $('<div>').addClass('bid_material_item').attr('data-material-id', material.material_id);
                const materialLabel = $('<label>').text(`${material.description}`);
                const quantityLabel = $('<label>').text(`QTY: `);
                const quantityInput = $('<input>').attr({
                    type: 'number',
                    class: 'bid_quantity_input',
                    name: `quantity_${material.material_id}`,
                });
                const removeButton = $('<button>').addClass('remove_bid_material_button').text('Remove');
                const unitOfMeasureSelect = $('<select>').attr({
                    name: `existing_bid_material_uom_${material.material_id}`,
                    class: 'bid_material_uom_select',
                });
                const unitOfMeasureOptions = [
                    { value: 1, text: 'EA' },
                    { value: 100, text: '100EA' },
                    { value: 1000, text: '1000EA' },
                ];
                unitOfMeasureOptions.forEach((option) => {
                    const optionElement = $('<option>').attr('value', option.value).text(option.text);
                    if (option.value === unitOfMeasure) {
                        optionElement.attr('selected', true);
                    }
                    unitOfMeasureSelect.append(optionElement);
                });

                const unitPriceInput = $('<input>').attr({
                    type: 'number',
                    class: 'bid_unit_price_input',
                    name: `unit_price_${material.material_id}`,
                });
                if (unitPrice) {
                    unitPriceInput.val(unitPrice);
                }

                materialItem.append(quantityLabel, quantityInput, unitOfMeasureSelect, unitPriceInput, materialLabel, removeButton);
                bidMaterialList.append(materialItem);
            }

        };


        $("#add_selected_materials").on("click", function () {
            $('.material_checkbox:checked').each(function () {
                const materialId = $(this).val();
                const materialItem = $(this).closest('.material_item');
                const materialData = {
                    material_id: materialId,
                    description: materialItem.find('label').text(),
                    manufacturer: materialItem.data('material-manufacturer'),
                };
                const quantity = materialItem.find('input[name^="item_quantity"]').val();
                if (quantity === '' || quantity === '0') {
                    alert('Enter the # of Line Items to Add to Bid List');
                    return;
                }
                const unitOfMeasure = materialItem.find('select[name^="item_uom"]').val();
                const unitPrice = materialItem.find('input[name^="item_unit_price"]').val();


                addMaterialToBidList(materialData, quantity, unitOfMeasure, unitPrice);

                // Uncheck the checkbox after adding to the bid list
                $(this).prop('checked', false);
                // Hide the quantity input
                materialItem.find('input[name^="item_quantity"]').hide();
            });

        });

        $(document).on("click", ".remove_bid_material_button", function () {
            $(this).closest('.bid_material_item').remove();
        }
        );

        const isValidQuantity = (quantity) => {
            return quantity > 0;
        };


        $('#save_bid_materials').on('click', function (event) {
            event.preventDefault();

            let bidMaterialsData = [];

            $('#bid_materials_list .bid_material_item').each(function () {
                const materialId = $(this).data("material-id");
                const quantity = $(this).find("input[name^='quantity_']").val();
                const unitOfMeasure = $(this).find("select[name^='existing_bid_material_uom_']").val();
                const unitPrice = $(this).find("input[name^='unit_price_']").val();

                if (!isValidQuantity(quantity)) {
                    alert("Invalid Quantity");
                    return;
                } else {
                    bidMaterialsData.push({
                        material_id: materialId,
                        quantity: parseInt(quantity),
                        unit_of_measure: parseInt(unitOfMeasure),
                        unit_price: parseFloat(unitPrice),
                    });
                }
            });

            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();
            let url = $('material_form').attr('data-url');

            $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify(bidMaterialsData),
                contentType: "application/json",
                dataType: "json",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                success: function (response) {
                    if (response.status === 'success') {
                        alert("Bid Materials Saved Successfully");
                        window.location.href = response.redirect_url;
                    } else {
                        alert("Error Saving Bid Materials");
                    }
                },
                error: function (response) {
                    alert("Error Saving Bid Materials");
                    // Log as much information about the error as possible
                    console.log(response);
                    console.log(response.status);
                    console.log(response.statusText);
                    console.log(response.responseText);

                }
            });

        });


    };

    init();
});