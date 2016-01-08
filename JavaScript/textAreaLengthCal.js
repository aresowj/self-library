(function() {
    $(document).ready(function () {
        // when user changes the content with keyboard
        $('#primary_product_description').keyup(function(e) {
            $('#CharCount').text($(this).val().length);
        });

        // when user paste something
        $('#primary_product_description').change(function () {
            $(this).keyup();
        });
        
        // when the page is ready, calculate the length of existing content
        $('#primary_product_description').keyup();
