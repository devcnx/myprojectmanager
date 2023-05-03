$(document).ready(function () {
    $('#project_contacts_search').on('keyup', function () {
        let searchValue = $(this).val().toLowerCase();
        $('#id_project_contacts div').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(searchValue) > -1);
        });
    });

    $('#project_sites_search').on('keyup', function () {
        let searchValue = $(this).val().toLowerCase();
        $('#id_project_sites div').filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(searchValue) > -1);

            // If there are no matches, show the "Add Site" button
            if ($('#id_project_sites div:visible').length === 0) {
                $('#id_project_sites_add').show();
            } else {
                $('#id_project_sites_add').hide();
            }
        });
    });
});