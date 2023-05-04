$(document).ready(function () {
    const init = () => {

        const filterMaterials = (event) => {
            event.preventDefault();
            var searchValue = $("#search_input").val().toLowerCase();

            $(".material_item").each(function () {
                var materialDescription = "";
                $(this).find("td").each(function () {
                    materialDescription += $(this).text();
                });
                materialDescription = materialDescription.toLowerCase();

                if (materialDescription.includes(searchValue)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }

            });
        }


        $('#search_input').on('change input', filterMaterials);
        // Toggle the quantity input visibility
        $(document).on("change", ".material_checkbox", function () {
            var quantityInput = $(this).closest('.material_item').find("input[name^='item_quantity']");
            if ($(this).is(":checked")) {
                quantityInput.show();
                // Set the default quantity to 1
                quantityInput.val(1);
                // Set the minimum allowed value to 1
                quantityInput.attr('min', 1);
            } else {
                quantityInput.hide();
            }
        });

        const getUOM = (uom) => {
            uom = uom.replace(/(ea|ft)/gi, '').trim();
            return uom === '' ? 1 : parseInt(uom);
        };

        const getPricesAndUOM = (vendorPrices) => {
            const priceRegex = /(\d+(\.\d{1,2})?)/;
            const uomRegex = /\(([^)]+)\)/;

            const price1 = parseFloat(priceRegex.exec($(vendorPrices[0]).text())[0]);
            const price2 = parseFloat(priceRegex.exec($(vendorPrices[1]).text())[0]);
            const uom1 = getUOM(uomRegex.exec($(vendorPrices[0]).text())[1]);
            const uom2 = getUOM(uomRegex.exec($(vendorPrices[1]).text())[1]);

            return {
                price1,
                price2,
                uom1,
                uom2,
            };
        };

        const addMaterialToBidList = (material, quantity, selectedRow) => {
            for (let index = 0; index < quantity; index++) {
                const vendorPrices = selectedRow.find('td.vendor_price');
                let lowestPrice = 0;
                let selectedUOM = '';
                let selectedUOMText = '';
                let lowestVendor;
                const uomRegex = /\(([^)]+)\)/;


                if (vendorPrices.length >= 2) {
                    const { price1: graybarPrice, price2: anixterPrice, uom1: graybarUOM, uom2: anixterUOM } = getPricesAndUOM(vendorPrices);

                    const graybarPerUnitPrice = parseFloat((graybarPrice / graybarUOM));
                    const anixterPerUnitPrice = parseFloat((anixterPrice / anixterUOM));

                    if (graybarPerUnitPrice === 0 && anixterPerUnitPrice > 0) {
                        lowestPrice = anixterPerUnitPrice;
                    } else if (anixterPerUnitPrice === 0 && graybarPerUnitPrice > 0) {
                        lowestPrice = graybarPerUnitPrice;
                    } else {
                        lowestPrice = Math.min(graybarPerUnitPrice, anixterPerUnitPrice);
                    }
                    lowestPrice = parseFloat(lowestPrice);

                    // Determine the selected UOM
                    if (graybarPerUnitPrice === lowestPrice) {
                        selectedUOMText = uomRegex.exec($(vendorPrices[0]).text())[1];
                        selectedUOM = { value: graybarUOM, text: selectedUOMText };
                    } else if (anixterPerUnitPrice === lowestPrice) {
                        selectedUOMText = uomRegex.exec($(vendorPrices[1]).text())[1];
                        selectedUOM = { value: anixterUOM, text: uomRegex.exec($(vendorPrices[1]).text())[1] };
                    } else {
                        selectedUOMText = uomRegex.exec($(vendorPrices[0]).text())[1];
                        selectedUOM = { value: graybarUOM, text: uomRegex.exec($(vendorPrices[0]).text())[1] };
                    }

                    const isGraybarLowest = graybarPrice === lowestPrice;

                    selectedUOM = isGraybarLowest ? graybarUOM : anixterUOM;
                    lowestVendor = isGraybarLowest ? 'Graybar' : 'Anixter';
                } else if (vendorPrices.length === 1) {
                    const priceRegex = /(\d+(\.\d{1,2})?)/;
                    const uomRegex = /\(([^)]+)\)/;
                    selectedUOM = uomRegex.exec($(vendorPrices[0]).text())[1];
                }

                // The rest of the code remains the same.
                const bidMaterialList = $("#bid_materials_list");
                const materialItem = $('<div>').addClass('bid_material_item').attr('data-material-id', material.material_id);

                const firstLine = $('<div>').addClass('bid_material_item_first_line');
                const materialLabel = $('<label>').text(`${material.description} | ${material.manufacturer} | ${material.manufacturer_number}`);
                const blankSpace = $('<span>').text(' | ');
                lowestVendor = $('<span>').text(`${lowestVendor}`)
                const removeButton = $('<button>').addClass('remove_bid_material_button').text('Remove');
                firstLine.append(materialLabel, blankSpace, lowestVendor, removeButton);

                const secondLine = $('<div>').addClass('bid_material_item_second_line');
                const quantityLabel = $('<label>').text(`QTY `);
                const unitOfMeasureLabel = $('<label>').text(`Unit of Measure`);
                const unitPriceLabel = $('<label>').text(`Unit Price`);
                secondLine.append(quantityLabel, unitOfMeasureLabel, unitPriceLabel);

                const thirdLine = $('<div>').addClass('bid_material_item_third_line');
                const quantityInput = $('<input>').attr({
                    type: 'number',
                    class: 'bid_quantity_input',
                    name: `quantity_${material.material_id}`,
                    min: 1,
                });

                const unitOfMeasureSelect = $('<select>').attr({
                    name: `existing_bid_material_uom_${material.material_id}`,
                    class: 'bid_material_uom_select',
                });
                const unitOfMeasureOptions = [
                    { value: 1, text: 'EA' },
                    { value: 1, text: 'FT' },
                    { value: 100, text: '100EA' },
                    { value: 100, text: '100FT' },
                    { value: 1000, text: '1000EA' },
                    { value: 1000, text: '1000FT' },
                ];
                unitOfMeasureOptions.forEach((option) => {
                    const optionElement = $('<option>').attr('value', option.value).text(option.text);
                    if (selectedUOM && option.value === selectedUOM && option.text === selectedUOMText.toUpperCase()) {
                        console.log('selectedUOM', selectedUOM);
                        optionElement.attr('selected', true);
                        // Disable the ability to change the UOM
                        optionElement.attr('readonly', true);

                    }

                    unitOfMeasureSelect.append(optionElement);

                });

                const unitPriceInput = $('<input>').attr({
                    type: 'number',
                    class: 'bid_unit_price_input',
                    name: `unit_price_${material.material_id}`,
                });

                // Unit price value is either the graybar price or anixter price, as long as it's not 0.
                const value = Math.round(lowestPrice, 4) * Math.round(selectedUOM, 4).toFixed(2);
                console.log(value);
                unitPriceInput.val(value);


                thirdLine.append(quantityInput, unitOfMeasureSelect, unitPriceInput);
                materialItem.append(firstLine, secondLine, thirdLine);
                bidMaterialList.append(materialItem);
            }
        };


        // const addMaterialToBidList = (material, quantity) => {
        // const addMaterialToBidList = (material, quantity, selectedRow) => {
        //     for (let index = 0; index < quantity; index++) {
        //         // Find the lowest price from the two vendor_price elements. 
        //         // If the lowest is 0, then use the other one.
        //         // If both are 0, then use 0.
        //         const vendorPrices = selectedRow.find('td.vendor_price');
        //         let lowestPrice = 0;
        //         let selectedUOM = '';
        //         let lowestVendor;
        //         if (vendorPrices.length >= 2) {
        //             const priceRegex = /(\d+(\.\d{1,2})?)/;
        //             const uomRegex = /\(([^)]+)\)/;
        //             let graybarPrice = parseFloat(priceRegex.exec($(vendorPrices[0]).text())[0]);
        //             let anixterPrice = parseFloat(priceRegex.exec($(vendorPrices[1]).text())[0]);

        //             // Determine the selected UOM
        //             let graybarUOM = uomRegex.exec($(vendorPrices[0]).text())[1];
        //             let anixterUOM = uomRegex.exec($(vendorPrices[1]).text())[1];

        //             // Remove the UOM and then determine if there is a value left. 
        //             // If 'ea', 'ft' in the UOM, remove the 'ea' and 'ft' and then parse the number.
        //             if (graybarUOM.toLowerCase().includes('ea')) {
        //                 graybarUOM = graybarUOM.replace('ea', '').trim();
        //             } else if (graybarUOM.toLowerCase().includes('EA')) {
        //                 graybarUOM = graybarUOM.replace('EA', '').trim();
        //             } else if (graybarUOM.toLowerCase().includes('ft')) {
        //                 graybarUOM = graybarUOM.replace('ft', '').trim();
        //             } else if (graybarUOM.toLowerCase().includes('FT')) {
        //                 graybarUOM = graybarUOM.replace('FT', '').trim();
        //             }

        //             if (anixterUOM.toLowerCase().includes('ea')) {
        //                 anixterUOM = anixterUOM.replace('ea', '').trim();
        //             } else if (anixterUOM.toLowerCase().includes('EA')) {
        //                 anixterUOM = anixterUOM.replace('EA', '').trim();
        //             } else if (anixterUOM.toLowerCase().includes('ft')) {
        //                 anixterUOM = anixterUOM.replace('ft', '').trim();
        //             } else if (anixterUOM.toLowerCase().includes('FT')) {
        //                 anixterUOM = anixterUOM.replace('FT', '').trim();
        //             }

        //             // If not, the UOM would be 1 for EA.
        //             if (graybarUOM === '') {
        //                 graybarUOM = 1;
        //             } else {
        //                 graybarUOM = parseInt(graybarUOM);
        //             }

        //             if (anixterUOM === '') {
        //                 anixterUOM = 1;
        //             } else {
        //                 anixterUOM = parseInt(anixterUOM);
        //             }


        //             graybarPerUnitPrice = parseFloat((graybarPrice / parseFloat(graybarUOM)).toFixed(2));
        //             anixterPerUnitPrice = parseFloat((anixterPrice / parseFloat(anixterUOM)).toFixed(2));

        //             lowestPrice = Math.min(graybarPerUnitPrice, anixterPerUnitPrice);
        //             lowestPrice = parseFloat(lowestPrice.toFixed(2));


        //             if (graybarPerUnitPrice === lowestPrice) {
        //                 selectedUOM = uomRegex.exec($(vendorPrices[0]).text())[1];
        //             } else if (anixterPerUnitPrice === lowestPrice) {
        //                 selectedUOM = uomRegex.exec($(vendorPrices[1]).text())[1];
        //             } else {
        //                 selectedUOM = uomRegex.exec($(vendorPrices[0]).text())[1];
        //             }

        //             console.log(`Material ID : ${material.material_id}`);
        //             console.log(`Material Description : ${material.description}`);
        //             console.log(`Material Manufacturer : ${material.manufacturer}`);
        //             console.log(`Material Manufacturer Number : ${material.manufacturer_number}`);
        //             console.log(`Line Item Quantity : ${quantity}`);
        //             console.log(`Material Unit of Measure : ${selectedUOM}`);
        //             console.log(`Material Unit Price : ${lowestPrice}`);

        //             if (graybarPerUnitPrice === lowestPrice) {
        //                 lowestVendor = 'Graybar';
        //             } else if (anixterPerUnitPrice === lowestPrice) {
        //                 lowestVendor = 'Anixter';
        //             } else {
        //                 lowestVendor = '';
        //             }

        //         } else if (vendorPrices.length === 1) {
        //             const priceRegex = /(\d+(\.\d{1,2})?)/;
        //             const uomRegex = /\(([^)]+)\)/;
        //             lowestPrice = parseFloat(priceRegex.exec($(vendorPrices[0]).text())[0]);
        //             selectedUOM = uomRegex.exec($(vendorPrices[0]).text())[1];
        //         }


        //         const bidMaterialList = $("#bid_materials_list");
        //         const materialItem = $('<div>').addClass('bid_material_item').attr('data-material-id', material.material_id);

        //         const firstLine = $('<div>').addClass('bid_material_item_first_line');
        //         const materialLabel = $('<label>').text(`${material.description} | ${material.manufacturer} | ${material.manufacturer_number}`);
        //         const blankSpace = $('<span>').text(' | ');
        //         lowestVendor = $('<span>').text(`${lowestVendor}`)
        //         const removeButton = $('<button>').addClass('remove_bid_material_button').text('Remove');
        //         firstLine.append(materialLabel, blankSpace, lowestVendor, removeButton);

        //         const secondLine = $('<div>').addClass('bid_material_item_second_line');
        //         const quantityLabel = $('<label>').text(`QTY `);
        //         const unitOfMeasureLabel = $('<label>').text(`Unit of Measure`);
        //         const unitPriceLabel = $('<label>').text(`Unit Price`);
        //         secondLine.append(quantityLabel, unitOfMeasureLabel, unitPriceLabel);

        //         const thirdLine = $('<div>').addClass('bid_material_item_third_line');
        //         const quantityInput = $('<input>').attr({
        //             type: 'number',
        //             class: 'bid_quantity_input',
        //             name: `quantity_${material.material_id}`,
        //             min: 1,
        //         });

        //         const unitOfMeasureSelect = $('<select>').attr({
        //             name: `existing_bid_material_uom_${material.material_id}`,
        //             class: 'bid_material_uom_select',
        //         });
        //         const unitOfMeasureOptions = [
        //             { value: 1, text: 'EA' },
        //             { value: 1, text: 'FT' },
        //             { value: 100, text: '100EA' },
        //             { value: 100, text: '100FT' },
        //             { value: 1000, text: '1000EA' },
        //             { value: 1000, text: '1000FT' },
        //         ];
        //         unitOfMeasureOptions.forEach((option) => {
        //             const optionElement = $('<option>').attr('value', option.value).text(option.text);
        //             // if (option.value === unitOfMeasure) {
        //             if (selectedUOM && option.text === selectedUOM.toUpperCase()) {
        //                 optionElement.attr('selected', true);
        //             }
        //             unitOfMeasureSelect.append(optionElement);
        //         });

        //         const unitPriceInput = $('<input>').attr({
        //             type: 'number',
        //             class: 'bid_unit_price_input',
        //             name: `unit_price_${material.material_id}`,
        //         });

        //         // Divide the lowest price by the UOM to get the unit price.
        //         unitPriceInput.val(lowestPrice);

        //         thirdLine.append(quantityInput, unitOfMeasureSelect, unitPriceInput);
        //         materialItem.append(firstLine, secondLine, thirdLine);
        //         bidMaterialList.append(materialItem);
        //     }

        // };


        $("#add_selected_materials").on("click", function () {
            $('.material_checkbox:checked').each(function () {
                const materialId = $(this).val();
                const materialRow = $(this).closest('tr');
                const materialData = {
                    material_id: materialId,
                    description: materialRow.find('td:nth-child(1)').text(),
                    manufacturer: materialRow.find('td:nth-child(2)').text(),
                    manufacturer_number: materialRow.find('td:nth-child(3)').text(),
                };

                const quantity = materialRow.find('input[name^="item_quantity"]').val();
                if (quantity === '' || quantity === '0') {
                    alert('Enter the # of Line Items to Add to Bid List');
                    return;
                }
                // const unitOfMeasure = materialRow.find('td:nth-child(6) select').val();

                // addMaterialToBidList(materialData, quantity, unitOfMeasure, materialRow);
                addMaterialToBidList(materialData, quantity, materialRow);

                // Uncheck the checkbox after adding to the bid list
                $(this).prop('checked', false);
                // Hide the quantity input
                materialRow.find('input[name^="item_quantity"]').hide();
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
            let url = $('#add_material_form').attr('data-url');

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
                }
            });

        });


        // const materialForm = $("#add_material_form");

        // materialForm.on('submit', (event) => {
        //     event.preventDefault();

        //     const formData = new FormData(materialForm[0]);
        //     console.log(formData.get('description'));
        //     const url = materialForm.attr('data-url');

        //     fetch(url, {
        //         method: 'POST',
        //         body: formData,

        //     })
        //         .then((response) => {
        //             if (response.ok) {
        //                 alert(`Material ${formData.get('description')} Added Successfully.`)
        //                 return response.json();
        //             } else {
        //                 throw new Error("Item Already Exists")
        //             }
        //         })
        //         .catch((error) => {
        //             alert(`Item with MFR# ${formData.get('manufacturer_number')} Already Exists.`);

        //         })
        //         .then((data) => {
        //             if (data) {
        //                 addMaterialToSelected(data, data.material);
        //             } else {
        //                 console.log('no data');
        //             }
        //         });

        // });


    };

    init();
});