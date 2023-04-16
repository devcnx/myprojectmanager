const $ = selector => document.querySelector(selector);

const addForm = (button, prefix, className) => {
    const formIndex = parseInt($(`#${prefix}-TOTAL_FORMS`).value);
    const forms = document.querySelectorAll(`.${prefix}-form`);
    const formCount = forms.length;
    const form = forms[formCount - 1].cloneNode(true);

    // const form = $(`.${prefix}-form`).cloneNode(true);
    form.innerHTML = form.innerHTML.replaceAll(`-${formIndex - 1}-`, `-${formIndex}-`);

    form.querySelectorAll('input, select, textarea').forEach(field => {
        field.name = field.name.replaceAll(`-${formIndex - 1}-`, `-${formIndex}-`);
        field.id = field.id.replaceAll(`-${formIndex - 1}-`, `-${formIndex}-`);
        // field.value = ''; // clear the field value if needed
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
    form.classList.add(className);
    button.before(form);
    $(`#${prefix}-TOTAL_FORMS`).value = formIndex + 1;
};

// const removeLastForm = (prefix, className) => {
//     const formIndex = parseInt($(`#${prefix}-TOTAL_FORMS`).value);
//     if (formIndex === 1) {
//         return;
//     }
//     if (formIndex > 1) {
//         /* Get the count of .dynamic_form */
//         const forms = document.querySelectorAll(`.${prefix}-form ${className}`);
//         const formCount = forms.length;
//         if (formCount > 1) {
//             const formToRemove = forms[formCount - 1];
//             formToRemove.remove();
//             $(`#${prefix}-TOTAL_FORMS`).value = formIndex - 1;
//         }
//     }
// }
const removeLastForm = (prefix, className) => {
    const formIndex = parseInt($(`#${prefix}-TOTAL_FORMS`).value);
    if (formIndex === 0) {
        return;
    }
    if (formIndex > 1) {
        /* Get the count of .dynamic_form */
        const forms = document.querySelectorAll(`.${prefix}-form.${className}`);
        const formCount = forms.length;
        if (formCount > 0) {
            const formToRemove = forms[formCount - 1];
            formToRemove.remove();
            $(`#${prefix}-TOTAL_FORMS`).value = formIndex - 1;
        }
    }
};


document.addEventListener('DOMContentLoaded', () => {
    const init = () => {
        const addLaborHoursButton = $("#add_labor_hours");
        const removeLaborHoursButton = $("#remove_labor_hours");
        const addTravelExpenseButton = $("#add_travel_expense");

        const addTravelHoursButton = $("#add_travel_hours");
        const removeTravelHoursButton = $("#remove_travel_hours");
        const removeTravelExpenseButton = $("#remove_travel_expense");

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


    };
    init();
});
