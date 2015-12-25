$(document).ready(function(){
    $('#id_leads').html('');
    $('#id_location').change(function(){
        l_id =$(this).val();
        request_url = '/region/lead/get_leads/' + l_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                data = $.parseJSON(data);
                $('#id_leads').html('');
		for(var i=0; i<data.length; i++) {
			$('#id_leads').append('<option value="' + data[i][0] + '">' + data[i][1] +'</option>');
		}
            }
        })
    })
})
