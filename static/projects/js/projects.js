$(document).ready(function () {
    $('#project_contacts_search').on('keyup', function () {
        let searchValue = $(this).val().toLowerCase();
        $('#id_project_contacts div').each(function () {
            if ($(this).text().toLowerCase().indexOf(searchValue) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('#project_sites_search').on('keyup', function () {
        let searchValue = $(this).val().toLowerCase();
        $('#id_project_sites div').each(function () {
            if ($(this).text().toLowerCase().indexOf(searchValue) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});
