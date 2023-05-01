const $ = selector => document.querySelector(selector);

const addForm = (button, prefix, className) => {
    const formIndex = parseInt($(`#${prefix}-TOTAL_FORMS`).value);
    const initialForm = $(`.initial-${prefix}-form`);
    const form = initialForm.cloneNode(true);

    form.innerHTML = form.innerHTML.replaceAll(`-0-`, `-${formIndex}-`);
    form.innerHTML = form.innerHTML.replaceAll(`__prefix__`, `${formIndex}`);

    form.querySelectorAll('input, select, textarea').forEach(field => {
        field.name = field.name.replaceAll(`-0-`, `-${formIndex}-`);
        field.name = field.name.replaceAll(`__prefix__`, `${formIndex}`);
        field.id = field.id.replaceAll(`-0-`, `-${formIndex}-`);
        field.id = field.id.replaceAll(`__prefix__`, `${formIndex}`);
        field.style.background = '#fcfcdc';
        if (field.type !== 'number') {
            field.value = '';
        }
        if (field.type === 'number') {
            field.style.border = '1px solid #ccc';
        }
        if (field.type === 'checkbox') {
            field.type = 'hidden';
            /* Hide the label */
            const label = field.previousElementSibling;
            label.style.display = 'none';
        }
    });
    form.classList.remove(`initial-${prefix}-form`); // Remove the initial class
    form.classList.add(className);
    form.style.display = ''; // Make the form visible
    button.before(form);
    $(`#${prefix}-TOTAL_FORMS`).value = formIndex + 1;
};


const removeLastForm = (prefix, className) => {
    const formIndex = parseInt($(`#${prefix}-TOTAL_FORMS`).value);
    if (formIndex === 0) {
        return;
    }
    if (formIndex > 0) {
        /* Get the count of forms */
        const forms = document.querySelectorAll(`.${prefix}-form.${className}`);
        const formCount = forms.length;
        if (formCount > 0) {
            /* Remove the last form */
            const formToRemove = forms[formCount - 1];
            formToRemove.remove();
            $(`#${prefix}-TOTAL_FORMS`).value = formIndex - 1;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const init = () => {
        const addLaborHoursButton = $("#add_labor_hours");
        const addTravelHoursButton = $("#add_travel_hours");
        const addTravelExpenseButton = $("#add_travel_expense");

        const removeLaborHoursButton = $("#remove_labor_hours");
        const removeTravelHoursButton = $("#remove_travel_hours");
        const removeTravelExpenseButton = $("#remove_travel_expense");

        const addEquipmentButton = $("#add_equipment");
        const removeEquipmentButton = $("#remove_equipment");

        if (addLaborHoursButton) {
            addLaborHoursButton.addEventListener('click', (event) => {
                event.preventDefault();
                addForm(event.target, 'labor_hours', 'dynamic_labor_form');
            });
        }

        if (removeLaborHoursButton) {
            removeLaborHoursButton.addEventListener('click', (event) => {
                event.preventDefault();
                removeLastForm('labor_hours', 'dynamic_labor_form');
            });
        }

        if (addTravelHoursButton) {
            addTravelHoursButton.addEventListener('click', (event) => {
                event.preventDefault();
                addForm(event.target, 'travel_hours', 'dynamic_travel_form');
            });
        }

        if (removeTravelHoursButton) {
            removeTravelHoursButton.addEventListener('click', (event) => {
                event.preventDefault();
                removeLastForm('travel_hours', 'dynamic_travel_form');
            });
        }

        if (addTravelExpenseButton) {
            addTravelExpenseButton.addEventListener('click', (event) => {
                event.preventDefault();
                addForm(event.target, 'travel_expense', 'dynamic_travel_expense_form');
            });
        }

        if (removeTravelExpenseButton) {
            removeTravelExpenseButton.addEventListener('click', (event) => {
                event.preventDefault();
                removeLastForm('travel_expense', 'dynamic_travel_expense_form');
            });
        }

        if (addEquipmentButton) {
            addEquipmentButton.addEventListener('click', (event) => {
                console.log('add equipment');
                event.preventDefault();
                addForm(event.target, 'bid_equipment', 'dynamic_bid_equipment_form');
            });
        }

        if (removeEquipmentButton) {
            removeEquipmentButton.addEventListener('click', (event) => {
                event.preventDefault();
                removeLastForm('bid_equipment', 'dynamic_bid_equipment_form');
            });
        }

    };
    init();
});
