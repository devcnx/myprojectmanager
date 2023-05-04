$(document).ready(function () {
    $('#add_new_contact_link').click(function (event) {
        event.preventDefault();
        let url = $(this).data('url');
        $.get(url, function (data) {
            if (data.success) {
                $('#new_contact_form_container').html(data.form_html);
                $('#new_contact_form_container').show();
                // Change the style of the link to indicate that the form is open
                $('#add_new_contact_link').addClass('link_active');
                $('#id_customer').val(1);
            } else {
                alert(`Error Loading the Form: ${data.error_message}`);
            }

        });
    });

    $('#new_site_form_container').on('click', '#cancel_new_site_button', function (event) {
        event.preventDefault();
        $('#new_site_form_container').empty();
        $('#new_site_form_container').hide();
        $('#add_new_site_link').removeClass('link_active');
    });

    $('#new_contact_form_container').on('click', '#cancel_customer_contact_button', function (event) {
        event.preventDefault();
        $('#new_contact_form_container').empty();
        $('#new_contact_form_container').hide();
        $('#add_new_contact_link').removeClass('link_active');
    });

    $('#add_new_site_link').click(function (event) {
        event.preventDefault();
        let url = $(this).data('url');
        console.log(url);
        $.get(url, function (data) {
            console.log(data);
            if (data.success) {
                $('#new_site_form_container').html(data.form_html);
                $('#new_site_form_container').show();
                // Change the style of the link to indicate that the form is open
                $('#add_new_site_link').addClass('link_active');
            } else {
                alert(`Error Loading the Form: ${data.error_message}`);
            }
        });
    });

    // Submit the new contact form and update the project_contacts selection. 
    $('#new_contact_form_container').on('submit', '#customer_contact_form', function (event) {
        event.preventDefault();
        let url = $('#add_new_contact_link').data('url');
        $.post(url, $(this).serialize(), function (data) {
            if (data.success) {
                let newCheckboxHTML = `<input type="checkbox" name="project_contacts" value="${data.customer_contact_id}" class="multiple_select" id="id_project_contacts_${data.customer_contact_id}">`;
                let newLabelHTML = `<label for="id_project_contacts_${data.customer_contact_id}">${newCheckboxHTML} ${data.first_name} ${data.last_name}</label>`;
                let newContactDiv = $('<div>').html(newLabelHTML);
                $('#id_project_contacts').prepend(newContactDiv);
                // Clear the form and hide it 
                $('#new_contact_form_container').empty();
                $('#new_contact_form_container').hide();

                // Change the style of the link to indicate that the form is closed
                $('#add_new_contact_link').removeClass('link_active');

                // Show the new contact in the project_contacts selection
                $('#id_project_contacts').show();

                // Select the new contact
                $(`#id_project_contacts_${data.customer_contact_id}`).prop('checked', true);

            } else {
                $('#new_contact_form_container').html(data.form_html);
            }
        });

    });

    $('#new_site_form_container').on('submit', '#new_site_form', function (event) {
        event.preventDefault();
        let url = $('#add_new_site_link').data('url');
        $.post(url, $(this).serialize(), function (data) {
            if (data.success) {
                let newCheckboxHTML = `<input type="checkbox" name="project_sites" value="${data.site_id}" class="multiple_select" id="id_project_sites_${data.site_id}">`;
                let newLabelHTML = `<label for="id_project_sites_${data.site_id}">${newCheckboxHTML} ${data.site_id} ${data.site_name}</label>`;
                let newSiteDiv = $('<div>').html(newLabelHTML);
                $('#id_project_sites').prepend(newSiteDiv);
                // Clear the form and hide it 
                $('#new_site_form_container').empty();
                $('#new_site_form_container').hide();

                // Change the style of the link to indicate that the form is closed
                $('#add_new_site_link').removeClass('link_active');

                // Show the new site in the project_sites selection
                $('#id_project_sites').show();

                // Select the new site
                $(`#id_project_sites_${data.site_id}`).prop('checked', true);

            } else {
                $('#new_site_form_container').html(data.form_html);
            }

        });

    });
});
